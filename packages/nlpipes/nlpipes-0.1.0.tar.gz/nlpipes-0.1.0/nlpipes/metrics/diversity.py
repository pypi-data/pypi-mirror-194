"""Diversity metrics for for in-domain subcorpus selection.
Code from: 
reference: https://github.com/georgian-io/Transformers-Domain-Adaptation.
reference: https://github.com/sebastianruder/learn-to-select-data.
"""

from functools import partial
from typing import Callable, Dict, Sequence
from typing_extensions import Literal

import numpy as np
import scipy.stats

from nlpipes.data.data_types import Token


def entropy(example: Sequence[Token], 
            vocab2id: Dict[Token, int],
           ) -> float:
    """Calculate Entropy 
    ref: https://en.wikipedia.org/wiki/Entropy_(information_theory%29#Definition).
    """
    example = {term for term in example if term in vocab2id}
    term_ids = [vocab2id[term] for term in example]
    return scipy.stats.entropy(term_ids)

def simpsons_index(
    example: Sequence[Token], 
    train_term_dist: np.ndarray, 
    vocab2id: Dict[Token, int],
) -> float:
    """ Calculate Simpson's Index 
    ref: https://en.wikipedia.org/wiki/Diversity_index#Simpson_index
    """
    if not len(example):
        return 0
    example = {term for term in example if term in vocab2id}
    term_ids = [vocab2id[term] for term in example]
    score = (train_term_dist[term_ids] ** 2).sum()
    return score

def renyi_entropy(
    example: Sequence[Token], 
    domain_tokens_distribution: np.ndarray, 
    vocab2id: Dict[Token, int],
) -> float:
    """ Calculate Rényi Entropy
    ref: https://en.wikipedia.org/wiki/R%C3%A9nyi_entropy
    """
    example = {term for term in example if term in vocab2id}
    term_ids = [vocab2id[term] for term in example]

    alpha = 0.99
    summed = (domain_tokens_distribution[term_ids] ** alpha).sum()
    if summed == 0:
        # 0 if none of the terms appear in the dictionary;
        # set to a small constant == low prob instead
        summed = 0.0001
    score = 1 / (1 - alpha) * np.log(summed)
    return score

def number_of_term_types(example: Sequence[Token]) -> int:
    """Calculate the number of term types of the example."""
    return len(set(example))

def type_token_diversity(example: Sequence[Token]) -> float:
    """Calculate diversity based on the type-token ratio of the example."""
    if not len(example):
        return 1
    type_token_ratio = number_of_term_types(example) / len(example)
    return -type_token_ratio


DiversityMetric = Literal[
    "num_token_types",
    "type_token_ratio",
    "entropy",
    "simpsons_index",
    "renyi_entropy",
]
DiversityFunction = Callable[
    [Sequence[Token]], float
]
DIVERSITY_FEATURES = {
    "num_token_types",
    "type_token_ratio",
    "entropy",
    "simpsons_index",
    "renyi_entropy",
}


def diversity_metrics_factory(
    metric: DiversityMetric, 
    tokens_distribution: np.ndarray, 
    vocab2id: Dict[Token, int]
) -> DiversityFunction:
    """Return the corresponding diversity function based on the provided metric.
    Args:
        metric (str): Diversity metric
        train_term_dist: Term distribution of the training data
        vocab2id: Vocabulary-to-id mapping
    Raises:
        ValueError: If `metric` does not exist in DIVERSITY_FEATURES
    """
    if metric not in DIVERSITY_FEATURES:
        raise ValueError(f'"{metric}" is not a valid diversity metric.')

    mapping: Dict[DiversityMetric, DiversityFunction] = {
        "num_token_types": number_of_term_types,
        "type_token_ratio": type_token_diversity,
        "entropy": partial(entropy, vocab2id=vocab2id),
        "simpsons_index": partial(
            simpsons_index, 
            tokens_distribution=tokens_distribution,
            vocab2id=vocab2id,
        ),
        "renyi_entropy": partial(
            renyi_entropy,
            domain_tokens_distribution=tokens_distribution,
            vocab2id=vocab2id,
        ),
    }
    
    diversity_function = mapping[metric]
    return diversity_function
