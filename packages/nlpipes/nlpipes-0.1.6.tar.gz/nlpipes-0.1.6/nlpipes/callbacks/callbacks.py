import os
import sys
import logging
import time
import datetime

from abc import ABC, abstractmethod
from collections import defaultdict

from dataclasses import astuple
from dataclasses import dataclass
from dataclasses import field

import numpy as np
import tensorflow as tf
from transformers import TFPreTrainedModel

from tqdm.auto import tqdm

from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)

from nlpipes.data.data_types import (
    InputFeatures,
    TFSequenceClassifierBatchOutput,
)

logger = logging.getLogger('__name__')


"""
obj:`Callbacks` encapsulate a set of functions to be applied at given
stages of the training procedure to customize the trainer behavior. 
The relevant callbacks functions will then be called at the 
various stages of the model training lifecycle, such as when:
 - the training starts.
 - the training ends.
 - the testing starts.
 - the testing ends.
 - an epoch starts
 - an epoch ends.
 - a batch starts.
 - a batch ends.
"""

class Callback(ABC):
    
    """ Abstract base class for callback objects. """
    
    def on_train_begin(self):
        """ Called at the beginning of the training. """
     
    def on_train_end(self):
        """ Called at the end of the training. """
      
    def on_test_begin(self):
        """ Called at the beginning of the evaluation. """
     
    def on_test_end(self):
        """ Called at the end of the evaluation. """
    
    def on_epoch_begin(self, *args):
        """ Called at the beginning of an epoch. """

    def on_epoch_end(self, *args):
        """ Called at the end of an epoch. """
    
    def on_train_batch_begin(self, *args):
        """ Called at the beginning of a training batch. """
    
    def on_train_batch_end(self, *args):
        """ Called at the end of a training batch. """
    
    def on_test_batch_begin(self, *args):
        """ Called at the beginning of a test batch. """

    def on_test_batch_end(self, *args):
        """ Called at the end of a testing batch. """


@dataclass
class CallbackList(Callback):
        
    """ Internal class that just calls the list of callbacks.
    The CallbackList serves two main purposes:
        1. It stores all the callbacks.
        2. It allows to call all of the individual callbacks 
           easily. For example, if we have three callbacks 
           that do something at the end of an epoch, then 
           callbacks.on_epoch_end() will call the three
           callback objects in order. 
    """

    callbacks: List[Callback]
   
    def on_train_begin(self, *args):
        for callback in self.callbacks:
            callback.on_train_begin(*args)
        
    def on_train_end(self, *args):
        for callback in self.callbacks:
            callback.on_train_end(*args)
        
    def on_test_begin(self, *args):
        for callback in self.callbacks:
            callback.on_test_begin(*args)
        
    def on_test_end(self, *args):
        for callback in self.callbacks:
            callback.on_test_end(*args)

    def on_epoch_begin(self, *args):
        for callback in self.callbacks:
            callback.on_epoch_begin(*args)

    def on_epoch_end(self, *args):
        for callback in self.callbacks:
            callback.on_epoch_end(*args)
            
    def on_train_batch_begin(self, *args):
        for callback in self.callbacks:
            callback.on_train_batch_begin(*args)

    def on_train_batch_end(self, *args):
        for callback in self.callbacks:
            callback.on_train_batch_end(*args)

    def on_test_batch_begin(self, *args):
        for callback in self.callbacks:
            callback.on_test_batch_begin(*args)

    def on_test_batch_end(self, *args):
        for callback in self.callbacks:
            callback.on_test_batch_end(*args) 


@dataclass
class TrainingStep(Callback):
    """ Callback that define the training step. The training step is
    a single iteration of the training process. It consists of a 
    forward pass (where the obj:`model` makes predictions based on
    the input data) and a backward pass (where the obj:`optimizer`
    updates the obj:`model` weights and biases based on the difference
    between the predicted output and the expected output as expressed
    by the obj:`loss_finction`).
    """
    
    name: str = 'TrainingStep'
    model: TFPreTrainedModel = None
    optimizer: tf.optimizers.Optimizer = None
    loss_function: tf.losses = None
    
    def _train_step(self, features: InputFeatures):
        """ Train the obj:`model` on a single batch of examples. """
        
        with tf.GradientTape() as tape:
            model_outputs = self.model.call(
                input_ids=features.input_ids,
                attention_mask=features.attention_mask,
                token_type_ids=features.token_type_ids,
                training=True,
            )
            
            loss_values = self.loss_function(
                features.label, model_outputs.logits
            )
            
        trainable_variables = self.model.trainable_variables
        gradients = tape.gradient(loss_values, trainable_variables)
        
        self.optimizer.apply_gradients(
            zip(gradients, trainable_variables)
        )
        
        output_batch = TFSequenceClassifierBatchOutput(
            loss=loss_values,
            logits=model_outputs.logits,
            hidden_states=model_outputs.hidden_states,
            attentions=model_outputs.attentions,
        )
        
        return output_batch
    
    def _test_step(self, features: InputFeatures):
        """ Test the obj:`model` on a single batch of examples. """
        
        model_outputs = self.model.call(
                  input_ids=features.input_ids,
                  attention_mask=features.attention_mask,
                  token_type_ids=features.token_type_ids,
                  training=False,
        )
        
        loss_values = self.loss_function(
            features.label, model_outputs.logits
        )
        
        return TFSequenceClassifierBatchOutput(
            loss=loss_values,
            logits=model_outputs.logits,
            hidden_states=model_outputs.hidden_states,
            attentions=model_outputs.attentions,
        )
    
    def on_train_begin(self):
        message = self.model.summary()
        logger.info(message)           
     
    def on_train_batch_begin(self, step: int, features: InputFeatures):
        self.train_step_output = self._train_step(features)
             
    def on_test_batch_begin(self, step: int, features: InputFeatures):
        self.test_step_output = self._test_step(features)


@dataclass
class History(Callback):
    """ Callback that records the performance of the model 
    during training. It stores all the evaluation metrics 
    such as loss and accuracy at each training and testing
    steps. This allows to track the progress of the model
    over time, and can be used by other callbacks, e.g. to
    detect when the model has reached its optimal performance.
    """
    
    name: str = 'History'
    epoch: int = field(default_factory=int)
    metric: Callable[[], tf.metrics.Metric] = None
    training_step: Callback = None
    train: Dict = field(default_factory=lambda: defaultdict(dict))
    test: Dict = field(default_factory=lambda: defaultdict(dict))
    train_details: Dict = field(default_factory=lambda: defaultdict(dict))
    test_details: Dict = field(default_factory=lambda: defaultdict(dict))

    
    def __post_init__(self):
        self.train_metric = self.metric()
        self.test_metric = self.metric()
    
    def on_epoch_begin(self, epoch: int):
        """ Resets all of the metric state variables """
        self.epoch = epoch
        self.train_metric.reset_states()
        self.test_metric.reset_states()
        
        self.train['loss'] = {}
        self.train_details['loss'] = {}
        self.test_details['loss'] = {}
        self.train['loss'][epoch] = []
        self.train_details['loss'][epoch] = []
        self.test_details['loss'][epoch] = []
        
        self.test['accuracy'] = {}
        self.train_details['accuracy'] = {}
        self.test_details['accuracy'] = {}
        self.test['accuracy'][epoch] = []
        self.train_details['accuracy'][epoch] = []
        self.test_details['accuracy'][epoch] = []
    
    def on_epoch_end(self, epoch: int):
        """ Display the performance metrics after each epoch """
        self.train['loss'][self.epoch] = self.train_metric.result()
        self.test['loss'][self.epoch] = self.test_metric.result()
        
        message = f'Epoch {self.epoch+1:4d} {self.name:10} ' \
                  f'Train {self.train_metric.result():1.3f} ' \
                  f'Test {self.test_metric.result():1.3f}'
        
        logger.info(message)

    def on_train_batch_end(self, step: int):
        """ Compute the performance metrics after each training batch """
        loss = self.training_step.train_step_output.loss
        self.train_metric(loss)
        self.train_details['loss'][self.epoch].extend(loss)
        self.train['loss'][self.epoch] = self.train_metric.result()
        
    def on_test_batch_end(self, step: int):
        """ Compute the performance metrics after each testing batch """
        loss = self.training_step.test_step_output.loss
        self.test_metric(loss)
        self.test_details['loss'][self.epoch].extend(loss)
        self.test['loss'][self.epoch] = self.test_metric.result()
        
    @property
    def best_result(self) -> float:
        return min(self.test['loss'].values())
    

@dataclass
class ModelCheckpoint(Callback):
    """ Callback that save the model weights and configuration 
    after each epoch and to keep track of the best model """
    
    name: str = 'ModelCheckpointing'
    model: TFPreTrainedModel = None
    history: History = None
    direction: str = 'minimize'
    best_result: float = np.inf
    best_model_dir: str = ''
    checkpoints_dir: str = 'checkpoints'

    def __post_init__(self):
        """ Create the directory for saving checkpoints. """
        if self.direction not in ['minimize', 'maximize']:
            raise ValueError
        if self.direction == 'maximize':
            self.best_result = 0

        if not os.path.isdir(self.checkpoints_dir):
            abs_path = os.path.abspath(self.checkpoints_dir)
            text = f'Make a checkpoint directory: {abs_path}'
            logger.info(text)
            os.makedirs(self.checkpoints_dir)

    def on_epoch_end(self, epoch: int):
        """ Pass the obj:`ModelCheckpoint` callback after the obj:`History`. """
        result = self.history.test['loss'][epoch]
        diff = self.best_result - result
        is_better = diff > 0 if self.direction == 'minimize' else diff < 0
        if is_better:
            name = f'epoch-{epoch:02d}-{result:.2f}'
            model_dir = os.path.join(self.checkpoints_dir, name)
            os.mkdir(model_dir)
            self.model.config.architectures = self.model.__class__.__name__
            self.model.save_pretrained(model_dir)
            self.best_result = result
            self.best_model_dir = model_dir
            message = f'New model checkpoint saved'
            logger.info(message)


@dataclass
class CSVLogger(Callback):
    """ Callback that save the logs of the performance metrics
    into a csv file. """
    
    name: str = 'CSVLogging'
    logs_dir: str = None
    level: int = 20
    msg_format: str = '%(asctime)s [%(levelname)-5s] %(message)s'

    def __post_init__(self):
        root_logger = logging.getLogger('__name__')
        root_logger.setLevel(self.level)
        root_logger.propagate = False
        formatter = logging.Formatter(self.msg_format, 
                                      datefmt='%Y-%m-%d %H:%M:%S')
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        
        root_logger.addHandler(console)
        if self.logs_dir:
            logs_dir = os.path.abspath(self.logs_dir)
            os.makedirs(logs_dir, exist_ok=True)
            file_path = os.path.join(logs_dir, 'experiment.log')
            file_handler = logging.FileHandler(file_path, mode='w')
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)


@dataclass
class EarlyStopping(Callback):
    """ Callback that stop training the model once a certain metric
    is no longer improving. The metric used is typically the 
    validation loss, but it can also be a metric such as accuracy
    or precision """
    
    name: str = 'EarlyStopping'
    history: History = None
    patience: int = 3
    min_delta: float = 0.01
    best_result: float = np.inf
    current_patience: int = 0
    direction: str = 'maximize'

    def __post_init__(self):
        """ """
        if self.direction not in ['minimize', 'maximize']:
            raise ValueError
        if self.direction == 'maximize':
            self.best_result = 0

    def on_epoch_end(self, epoch: int):
        """ """
        result = self.history.test['loss'][epoch]
        diff = self.best_result - result
        is_better = diff > self.min_delta if self.direction == 'minimize' \
            else diff < self.min_delta * -1
        if is_better:
            self.best_result = result
            self.current_patience = 0
            return
        self.current_patience += 1
        if self.current_patience >= self.patience:
            raise Exception('Early stopping of the training')


@dataclass
class TimedStopping(Callback):
    """ Callbacks that stop training the model when a specified
    amount of time has passed.
    Args:
        time_limit: maximum amount of time in seconds before stopping.
        stopped_epoch: the epoch number where the training loop stopped.
    """

    name: str = 'TimedStopping'
    time_limit: int = 86000
    stopped_epoch: int = None

    def get_config(self):
        config = {"seconds": self.time_limit}
        base_config = super().get_config()
        return {**base_config, **config}
    
    def on_train_begin(self):
        self.stopping_time = time.time() + self.time_limit
        
    def on_epoch_end(self, epoch: int):
        if time.time() >= self.stopping_time:
            self.stopped_epoch = epoch
            formatted_time = datetime.timedelta(seconds=self.time_limit)
            message = "Timed stopping at epoch {} after training for {}".format(
                self.stopped_epoch + 1, formatted_time
            )
            raise Exception(message)

    def on_train_end(self):
        if self.stopped_epoch is not None:
            formatted_time = datetime.timedelta(seconds=self.time_limit)
            message = "Timed stopping at epoch {} after training for {}".format(
                self.stopped_epoch + 1, formatted_time
            )
            logger.info(message)


@dataclass
class ProgbarLogger(Callback):
    """ Callbacks to monitor the progress of a model's training, 
    and display the progress bar and performance metrics in the
    console. """ 
    
    name: str = 'ProgbarLogger'
    history: List[History] = None
    metric: Callable = tf.metrics.Mean
    epoch: int = field(default_factory=int)
    num_samples: int = None
    num_epochs: int = None
    batch_size: int = None
    show_overall_progress: bool = False
    show_epoch_progress: bool = True
    update_per_second: int = 10
    is_training = False

    def __post_init__(self):
        self.tqdm = tqdm
        self.num_steps: int = int(self.num_samples/self.batch_size)
        self.update_interval = 1/self.update_per_second
        self.last_update_time = time.time()
        self.overall_bar_format: str = "{l_bar}{bar} {n_fmt}/{total_fmt} " \
                                       "ETA: {remaining}s, {rate_fmt}{postfix}"
        self.epoch_bar_format: str = "Batch {n_fmt}/{total_fmt}{bar} " \
                                     "ETA: {remaining}s - {desc}"
        self.metrics_format: str = "{name}: {value:0.4f}" 
        self.metrics_separator: str = " - "
        
    def _initialize_progbar(self, hook, epoch):
        self.num_samples_seen = 0
        self.steps_to_update = 0
        self.steps_so_far = 0
        self.train_logs = defaultdict(float)
        self.test_logs = defaultdict(float)
        
        if hook == "train":
            current_epoch_description = "Epoch {epoch}/{num_epochs}".format(
                epoch=epoch+1, num_epochs=self.num_epochs
            )
            if self.show_epoch_progress:
                print(current_epoch_description)
                self.epoch_progress_tqdm=self.tqdm(
                    total=self.num_steps,
                    position=0,
                    bar_format=self.epoch_bar_format,
                    leave=False,
                    dynamic_ncols=True,
                    unit="steps",
                )
        elif hook == "test":
            if self.show_epoch_progress:
                self.epoch_progress_tqdm=self.tqdm(
                    desc="Testing progress",
                    total=self.num_steps,
                    position=0,
                    bar_format=self.epoch_bar_format,
                    leave=False,
                    dynamic_ncols=True,
                    unit="steps",
                )

    def _update_progbar(self):
        self.num_samples_seen += self.batch_size
        self.steps_to_update += 1
        self.steps_so_far += 1

        if self.steps_so_far <= self.num_steps:  
            now = time.time()
            time_diff = now - self.last_update_time
            if self.show_epoch_progress and time_diff >= self.update_interval:
                
                self.epoch_progress_tqdm.desc = \
                     f'loss: {self.train_logs["loss"]:04F} - ' \
                     f'val_loss: {self.test_logs["loss"]:04F}'
                     #f'acc: {self.logs["accuracy"]:04F} - ' \
                     #f'val_acc: {self.logs["test_accuracy"]:04F}'

                self.epoch_progress_tqdm.update(self.steps_to_update)
                self.steps_to_update = 0
                self.last_update_time = now
                
    def _clean_up_progbar(self, hook):
        if self.show_epoch_progress:
            self.epoch_progress_tqdm.miniters = 0
            self.epoch_progress_tqdm.mininterval = 0
            self.epoch_progress_tqdm.update(
               self.num_steps - self.epoch_progress_tqdm.n
           )
            self.epoch_progress_tqdm.close()
                 
    def on_train_begin(self):
        self.is_training = True
        
    def on_train_end(self):
        self.is_training = False
        self._clean_up_progbar("train")
        
    def on_test_begin(self):
        if not self.is_training:
            self._initialize_progbar("test", epoch=None)
            
    def on_test_end(self):
        if not self.is_training:
            self._clean_up_progbar("test")
     
    def on_epoch_begin(self, epoch: int):
        self.epoch = epoch
        self._initialize_progbar("train", epoch)
    
    def on_epoch_end(self, epoch: int):
        self._clean_up_progbar("train")
        if self.show_overall_progress:
            self.overall_progress_tqdm.update(1)
        self.epoch_progress_tqdm.close()

    def on_train_batch_end(self, step: int):
        train_logs = defaultdict(float)
        train_logs["loss"] = self.history.train['loss'][self.epoch]
        self.train_logs = train_logs
        self._update_progbar()
        
    def on_test_batch_end(self, step: int):
        test_logs = defaultdict(float)
        test_logs["loss"] = self.history.test['loss'][self.epoch]
        self.test_logs = test_logs 
        self._update_progbar()
