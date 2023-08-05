import os
import logging

from typing import List
from typing import Optional
from typing import Union

from pathlib import Path

from dataclasses import dataclass

import tensorflow as tf
import transformers

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizer,
    TFPreTrainedModel,
)

from nlpipes.trainers.trainers import Trainer

from nlpipes.losses.losses import softmax_cross_entropy

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_processors import DataProcessorForLanguageModeling

from nlpipes.pipelines.pipeline_utils import (
     select_corpus,
     augment_vocabulary,
)

from nlpipes.data.data_utils import (
     create_examples,
     split_examples,
)

from nlpipes.data.data_types import (
     Corpus,
     Token,
     InputExample,
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
class TFPipelineForMaskedLM():
    """ The pipeline for masked language modeling task """
    
    model: TFPreTrainedModel
    tokenizer: PreTrainedTokenizer
    config: PretrainedConfig
    
    def __post_init__(self):
        self.sub_corpus: Corpus
    
    def train(
        self,
        texts: Corpus,
        train_frac: float=0.75,
        test_frac: float=0.25,
        num_epochs: int=2,
        batch_size: int=4,
        lr: float=2e-5,
        min_delta: float = 0.01,
        patience: int = 5,
        time_limit: int = 86400,
        rand_seed: int = 69,
        target_corpus_size: Union[int, float]=0.5,
        target_vocab_size: int=31000,
        similarity_metrics: Optional[List[str]]=['euclidean'],
        diversity_metrics: Optional[List[str]]=['entropy'],
        keep_checkpoints: bool = False,
        save_corpus_dir: str = './selected_corpus',
        checkpoints_dir: str = './checkpoints',
        logs_dir: str = './logs',
    ) -> TFPreTrainedModel:
        """ Train the model on a masked modeling task. """
        
        sub_corpus = select_corpus(
            corpus=texts,
            tokenizer=self.tokenizer,
            target_corpus_size=target_corpus_size,
            similarity_metrics=similarity_metrics,
            diversity_metrics=diversity_metrics,
        )
        
        new_tokens = augment_vocabulary(
            corpus=sub_corpus,
            tokenizer=self.tokenizer,
            target_vocab_size=target_vocab_size,
        )
        
        self.sub_corpus = sub_corpus
        self.tokenizer.add_tokens(new_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))
        
        examples = create_examples(
            texts=sub_corpus, 
            labels=None,
            config=self.config,
        )
        
        train_examples, test_examples = split_examples(
            examples=examples,
            train_frac=train_frac,
            test_frac=test_frac, 
            shufffle=True, 
        )

        data_processor = DataProcessorForLanguageModeling(
            name='DataProcessor',
            tokenizer=self.tokenizer,
            config=self.config,
            mlm_proba=0.15
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
            name='BatchTraining',
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
    
    def evaluate(self):
        raise NotImplementedError
        
    def predict(self):
        raise NotImplementedError
    
    def save(self, save_dir: str):
        """ Save the model and the tokenizer on disk """
        
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            
        corpus_path = os.path.join(save_dir, 'selected_corpus.txt')         
        Path(corpus_path).write_text('\n'.join(self.sub_corpus))
        self.tokenizer.save_pretrained(save_dir)
        self.model.save_pretrained(save_dir)
        