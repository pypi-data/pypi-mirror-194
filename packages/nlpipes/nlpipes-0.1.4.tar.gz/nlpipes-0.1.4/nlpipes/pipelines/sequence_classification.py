import os
import logging
import shutil

from typing import (
    List,
    Optional,
    Union,
)

from dataclasses import dataclass

from pathlib import Path

import tensorflow as tf
import transformers

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizerFast,
    TFPreTrainedModel,
    TFAutoModelForMaskedLM,
    AutoConfig,
    AutoTokenizer,
)

from tokenizers.pre_tokenizers import Whitespace

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_processors import DataProcessorForSequenceClassification
from nlpipes.data.data_cleaners import clean

from nlpipes.trainers.trainers import Trainer

from nlpipes.losses.losses import softmax_cross_entropy

from nlpipes.data.data_utils import (
     create_examples,
     split_examples,
     generate_batches,
     chunk,
)

from nlpipes.pipelines.pipeline_utils import (
     preprocess,
     tokenize,
     encode,
     estimate,
     postprocess,
)

from nlpipes.data.data_types import (
     Corpus,
     Document,
     Token,
     InputExample,
     InputTokens,
     InputFeatures,
     Predictions,
     Outcomes,
)

from nlpipes.callbacks.callbacks import (
     Callback,
     TrainingStep,
     History,
     ModelCheckpoint,
     CSVLogger,
     ProgbarLogger,
     EarlyStopping,
     TimedStopping,
)

transformers.logging.set_verbosity_error()

logger = logging.getLogger('__name__')

#uncomment row below for debugging rust tokenizer
#os.environ["RUST_BACKTRACE"]="full" 


@dataclass
class TFPipelineForSequenceClassification():
    """ The pipeline for mono-label sequence classification """
    
    model: TFPreTrainedModel
    tokenizer: PreTrainedTokenizerFast
    config: PretrainedConfig
    
    def train(self, 
              X: List[str], 
              Y: List[str],
              train_frac: float = 0.75,
              test_frac: float = 0.25,
              num_epochs: int = 3,
              batch_size: int = 4,
              lr: float = 2e-5,
              patience: int = 5,
              min_delta: float = 0.01,
              time_limit: int = 86400,
              rand_seed: int = 69,
              keep_checkpoints: bool = False,
              checkpoints_dir: str = './checkpoints',
              logs_dir: str = './logs',
             ) -> List[History]:
        """ Train a model for mono-label classification.
        
        Most of the behavior of the training process is implemented
        in callbacks objects. Even the actual training step 
        (calculating the gradient and updating the weights using 
        an optimizer) is implemented as callbacks and is not part of
        the Trainer itself. 
        This modular architecture allows new ideas to be implemented 
        without having to change and increase the complexity of the
        trainer. This keeps the overall system clean, even if many 
        different training improvements are implemented """
        
        examples = create_examples(
            texts=X, 
            labels=Y,
            config=self.config,
        )
        
        train_examples, test_examples = split_examples(
            examples,
            train_frac=train_frac,
            test_frac=test_frac,
            shufffle=True,
        )
        
        data_processor = DataProcessorForSequenceClassification(
            name='DataProcessing',
            tokenizer=self.tokenizer,
            config=self.config,
        )
        
        train_stream = DataLoader(
            name='TrainDataLoader',
            examples=train_examples,
            batch_size=batch_size,
            data_processor=data_processor,
        )
        
        test_stream = DataLoader(
            name='TestDataLoader',
            examples=test_examples,
            batch_size=batch_size,
            data_processor=data_processor,
        )
        
        training_step = TrainingStep(
            name='TrainingStep',
            model=self.model,
            loss_function=softmax_cross_entropy,
            optimizer=tf.optimizers.Adam(lr),
        )
        
        history = History(
            name='History', 
            training_step=training_step,
            metric=tf.metrics.Mean,
        )
        
        model_checkpoint = ModelCheckpoint(
            name='ModelCheckpoint',
            model=self.model, 
            history=history,
            checkpoints_dir=checkpoints_dir,
        )
        
        early_stopping = EarlyStopping(
            name='EarlyStopping', 
            history=history,
            direction='minimize',
            min_delta=min_delta,
            patience=patience,
        )
        
        timed_stopping = TimedStopping(
            name='TimedStopping',
            time_limit=time_limit,
        )
       
        csv_logger = CSVLogger(
            name='CSVLogging',
            logs_dir=logs_dir,
        )
        
        progbar_logger = ProgbarLogger(
            name='ProgbarLogger',
            batch_size=batch_size,
            num_epochs=num_epochs,
            history=history,
            num_samples=sum([
                train_stream.num_examples(),
                test_stream.num_examples(),
            ])
        )
        
        callbacks = [
            training_step,
            history,
            model_checkpoint,
            csv_logger,
            progbar_logger,
            early_stopping,
            timed_stopping,
        ]
        
        trainer = Trainer(
            train_stream=train_stream,
            test_stream=test_stream,
            callbacks=callbacks,
            num_epochs=num_epochs,
        )
        
        trainer.train()
        
        if keep_checkpoints == False:
            shutil.rmtree(checkpoints_dir)
         
        return history
    
    def evaluate(self,
                 X: List[str],
                 Y: List[str],
                 metric: tf.metrics.Metric,
                 batch_size: int = 32,
                ) -> tf.metrics.Metric:
        """ Evaluate the model performance on a new unseen 
        labeled data according to the user-defined evaluation
        metric """
        
        for texts, labels in generate_batches(X, Y, batch_size):
            examples = preprocess(texts, labels)
            tokens = tokenize(examples, self.tokenizer)
            features = encode(tokens, self.tokenizer)
            predictions = estimate(features, self.model, self.config)
            
            y_pred = predictions.label
            y_true = [example.label for example in examples]
            y_true = [self.config.label2id[y] for y in y_true]
            
            metric.update_state(y_true, y_pred)
        
        return metric.result()
    
    def predict(self, 
                texts: Corpus, 
                chunk_text: bool = False,
               ) -> Outcomes:
        """ Get predictions a new unseen unlabeled data """
        
        examples = preprocess(texts)
        tokens = tokenize(examples, self.tokenizer)
        features = encode(tokens, self.tokenizer)
        predictions = estimate(features, self.model, self.config)
        outcomes = postprocess(predictions, self.config)
        
        return outcomes
    
    def save(self, save_dir: str):
        """ Save the trained model on disk """
        
        os.makedirs(save_dir, exist_ok=True)
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)
        self.config.save_pretrained(save_dir)
    