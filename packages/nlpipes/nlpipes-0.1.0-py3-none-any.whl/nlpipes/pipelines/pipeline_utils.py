from typing import (
    List,
    Optional,
)

from dataclasses import dataclass

import tensorflow as tf
import transformers

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizerFast,
    TFPreTrainedModel,
)

from tokenizers.pre_tokenizers import Whitespace

from nlpipes.losses.losses import softmax_cross_entropy

from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_processors import DataProcessorForSequenceClassification
from nlpipes.data.data_cleaners import clean
from nlpipes.data.data_utils import chunk

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

def select_corpus(
    corpus: Corpus,
    tokenizer: PreTrainedTokenizerFast,
    target_corpus_size: int,
    similarity_metrics: List[str],
    diversity_metrics: List[str],
) -> Corpus :
    """ """

    data_selector = DataSelector(
        name='DataSelection',
        tokenizer=tokenizer,
        target_corpus_size=target_corpus_size,
        similarity_metrics=similarity_metrics,
        diversity_metrics=diversity_metrics,
    )

    clean_corpus = [clean(text) for text in corpus]
    sub_corpus= data_selector(clean_corpus)

    return sub_corpus

def augment_vocabulary(
    corpus: Corpus,
    tokenizer: PreTrainedTokenizerFast, 
    target_vocab_size: int,
) -> List[Token]:
    """ """

    vocab_augmentor = VocabAugmentor(
        name='VocabAugmentation',
        tokenizer=tokenizer,
        target_vocab_size=target_vocab_size,
        cased=False, 
    )

    new_tokens = vocab_augmentor.get_new_tokens(corpus)

    return new_tokens

def preprocess(texts: Corpus,
               labels: Optional[str] = None,
               chunk_text: Optional[bool] = False,
              ) -> List[InputExample]:
    """ Serialize each raw text into examples. Raw texts can 
    eventually be chunked into spans. E.g., at inference time,
    each span need to be chunked into sentences if the model 
    has been trained at the sentence level. """

    if labels is not None:
        input_examples = [
            InputExample(text=text, label=label)
            for text, label in zip(texts, labels)
        ]
    else:
        spans = chunk(text) if chunk_text == True else texts
        input_examples = [
            InputExample(span) for span in spans
        ]

    return input_examples

def tokenize(examples: List[InputExample],
             tokenizer: PreTrainedTokenizerFast,
            ) -> InputTokens:
    """ Convert examples into tokens. Tokens encapsulate both 
    words, wordpieces and enriched wordpieces with the special
    [CLS] and [SEP] tokens. """

    texts = [example.text for example in examples]

    words = [Whitespace().pre_tokenize_str(text) for text in texts]

    wordpieces = [
        encoding.tokens for encoding 
        in tokenizer.backend_tokenizer.encode_batch(
           texts, add_special_tokens=False
        )
    ]

    tokens = [
        encoding.tokens for encoding 
        in tokenizer.backend_tokenizer.encode_batch(
           texts, add_special_tokens=True
        )
    ]

    input_tokens = InputTokens(
        words=words,
        wordpieces=wordpieces,
        tokens=tokens,
    )

    return input_tokens

def encode(tokens: InputTokens,
           tokenizer: PreTrainedTokenizerFast,
          ) -> InputFeatures: 
    """ Encode human-readable wordpieces into encoded features
    that can be use as input by the model. """

    inputs = tokenizer(
       tokens.wordpieces,
       add_special_tokens=False,
       padding=True,
       truncation=True,
       max_length=512,
       is_split_into_words = True,
       return_tensors='tf',
    )

    input_features = InputFeatures(
       input_ids=inputs['input_ids'],
       attention_mask=inputs['attention_mask'],
       token_type_ids=inputs['token_type_ids'],
    )

    return input_features

def estimate(features: InputFeatures,
             model: TFPreTrainedModel,
             config: PretrainedConfig,
            ) -> Predictions:
    """ Predict the label index matching the maximum prediction
    score and compute the loss value associated with each
    prediction."""

    outputs = model.call(
        input_ids=features.input_ids,
        attention_mask=features.attention_mask,
        token_type_ids=features.token_type_ids,
    )

    logits = outputs.logits
    label = tf.argmax(logits, axis=-1)
    label_onehot = tf.one_hot(label, config.num_labels)
    scores = tf.nn.softmax(logits, axis=1)
    losses = softmax_cross_entropy(label_onehot, logits)

    predictions = Predictions(
        label=label,
        scores=scores,
        losses=losses,
    )

    return predictions

def postprocess(predictions: Predictions, 
                config: PretrainedConfig,
               ) -> Outcomes:
    """ Convert outputs tensors into more handy numpy lists. """

    indice = [label.numpy() for label in predictions.label]
    scores = [
        score.numpy().tolist() 
        for score in predictions.scores
    ] 
    losses = [loss.numpy() for loss in predictions.losses]

    label = [config.id2label[idx] for idx in indice]

    outcomes = Outcomes(
        indice=indice,
        label=label,
        scores=scores,
        losses=losses,
    )

    return outcomes


