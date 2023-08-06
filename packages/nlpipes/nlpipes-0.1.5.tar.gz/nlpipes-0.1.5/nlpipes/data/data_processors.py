from typing import Callable
from typing import List

from dataclasses import dataclass

import copy

import numpy as np
import tensorflow as tf

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizer,
    AutoTokenizer,
)

from nlpipes.data.data_types import InputExample
from nlpipes.data.data_types import InputFeatures


""" The data processor classes.

The data processor encapsulates all the transformations
needed to encode input examples into input features 
expected by the model. """


@dataclass
class DataProcessorForLanguageModeling:
    
    """ 
    Data processor for Masked Language Modeling:
    80% MASK, 10% random, 10% original.
    Inputs are dynamically padded to the maximum 
    length of a batch if they are not all of the 
    same length.
    
    Args
    ----------

    tokenizer (transformers.PreTrainedTokenizer):
        The tokenizer used for encoding the data.

    config (transformers.PreTrainedCOnfig):
        The configuration of the model.

    """
    name: str = 'LanguageModelingProcessor'
    tokenizer: PreTrainedTokenizer = None
    config: PretrainedConfig = None
    mlm_proba: float = None
    
    def __call__(self, 
                 examples: List[InputExample],
                ) -> InputFeatures:
        
        texts = [example.text for example in examples]
        
        inputs = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding=True,
            truncation=True,
            max_length=512,
            is_split_into_words=False,
            return_tensors='tf',
        )
        
        input_ids = tf.identity(inputs.input_ids)
        
        mask = self.create_mask(
            inputs=inputs.input_ids,
            mask_frac=self.mlm_proba,
            excluded=self.tokenizer.all_special_ids,
        )
        
        inputs['input_ids'] = self.apply_mask(
            inputs=inputs.input_ids,
            mask=mask,
            mask_token_id=self.tokenizer.mask_token_id,
        )
        
        labels = self.apply_mask(
            inputs=input_ids,
            mask=~mask,
            mask_token_id=-100,
        )
        
        inputs['label'] = tf.one_hot(
            [label for label in labels],
            depth=len(self.tokenizer)
        )
        
        input_features = InputFeatures(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            label=inputs['label'],
        )
        
        return input_features
    
    def create_mask(
        self,
        inputs: tf.Tensor,
        mask_frac: float,
        excluded: tf.Tensor,  
    ) -> tf.Tensor:
        """ Create the mask used for the masked 
        language modeling """
        
        random = tf.random.uniform(inputs.shape)
        
        mask = tf.math.logical_and(
            random < mask_frac, 
            ~np.isin(inputs, excluded),
        )
        
        return mask
    
    def apply_mask(
        self,
        inputs: tf.Tensor,
        mask: tf.Tensor,
        mask_token_id: int,
    ) -> tf.Tensor:
        """ Apply the mask to the given inputs """
        
        masked_inputs = tf.where(
            condition=mask,
            x=mask_token_id,
            y=inputs,
        )
        
        return masked_inputs


@dataclass
class DataProcessorForSequenceClassification:
    
    """
    Data Processor for Sequence Classification.
    Inputs are dynamically padded to the maximum 
    length of a batch if they are not all of the 
    same length.
    
    Args
    ----------

    tokenizer (transformers.PreTrainedTokenizer):
        The tokenizer used for encoding the data.

    config (transformers.PreTrainedCOnfig):
        The configuration of the model.

    """
    name: str = 'SequenceClassificationProcessor'
    tokenizer: PreTrainedTokenizer = None
    config: PretrainedConfig = None
    
    def __call__(self, 
                 examples: List[InputExample],
                ) -> InputFeatures:
        
        texts = [example.text for example in examples]
        
        inputs = self.tokenizer(
            texts,
            add_special_tokens=True,
            padding=True,
            truncation = True,
            max_length=512,
            is_split_into_words = False,
            return_tensors='tf',
        )
        
        inputs['label'] = tf.one_hot(
            [example.label for example in examples],
            depth=self.config.num_labels
        )
        
        input_features = InputFeatures(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            token_type_ids=inputs['token_type_ids'],
            label=inputs['label'],
        )
        
        return input_features
    