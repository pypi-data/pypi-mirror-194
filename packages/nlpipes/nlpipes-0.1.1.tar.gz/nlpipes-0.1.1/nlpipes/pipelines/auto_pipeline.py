import os
import importlib
import logging
import re
import sys

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
)

from transformers import (
    TFPreTrainedModel,
    TFAutoModelForMaskedLM,
    TFAutoModelForSequenceClassification,
    BertTokenizerFast,
    AutoModel,
    AutoTokenizer,
    AutoConfig, 
)

from nlpipes import (
    Task,
    TFPipeline,
    TFPipelineForMaskedLM,
    TFPipelineForSequenceClassification,
    TFAdaptedBertForSequenceClassification,
    AdaptedBertForSequenceClassification,
    AdaptedBertConfig,
    LabelsMapping,
)


logger = logging.getLogger('__name__')

TASKS = {
  "domain-adaptation": {
      "pipeline": TFPipelineForMaskedLM,
      "models": {
          "default": TFAutoModelForMaskedLM,
          "bottleneck-adapters": TFAutoModelForMaskedLM, #to be updated
      },
      "tokenizers": {
          "default": AutoTokenizer,
          "bottleneck-adapters": AutoTokenizer,
      },
      "configs": {
          "default": AutoConfig,
          "bottleneck-adapters": AdaptedBertConfig,
      },
  },
  "single-label-classification": {
      "pipeline": TFPipelineForSequenceClassification,
      "models": {
          "default": TFAutoModelForSequenceClassification,
          "bottleneck-adapters": TFAdaptedBertForSequenceClassification,
      },
      "tokenizers": {
          "default": AutoTokenizer,
          "bottleneck-adapters": AutoTokenizer,
      },
      "configs": {
          "default": AutoConfig,
          "bottleneck-adapters": AdaptedBertConfig,
      },
  },
}

MODELS_MODULE = 'nlpipes.models.sequence_classification'

def Model(
    name_or_path: TFPreTrainedModel = None,
    task: str = None,
    all_labels: Optional[List] = None,
    **model_kwargs
) -> TFPipeline:

    """ The `Model` is an abstraction that return a pipeline.
    Which pipeline the model shall call is determined
    automatically from the target task supplied to train the
    model. For more information, see the task argument.

    Args
    ----------
    task(str):
          Determines which task the model should learn. Setting
          the task manually will be not needed in the future as it
          will be determined automatically from the input data. But
          it has been implemented for more flexibility in future 
          developments. Available tasks currently are :
            - `mono_label` classification`
            - `class_label` classification`
            - `multi_label` classification`
            
    model(str):
          A path or name of the model that should be used.
          It can be:
            - The path of a model available in a local repo.
            - The name of a model available in the Huggingface
              model repo.
    
    all_labels (List[str]): 
          A list of all labels. Only used for classification task.
    """
    
    try:
        
        pipeline = create_pipeline_from_task(
            task=task, 
            name_or_path=name_or_path, 
            all_labels=all_labels,
            customization_tag='#',
        )
        
        return pipeline

    except EnvironmentError as error:
        message = "The pipeline, model, tokenizer or config file could not be found."
        logger.error(message)
        raise error
        

def create_pipeline_from_task(
    task:str, 
    name_or_path:str,
    all_labels:List[str],
    customization_tag=str,
) -> TFPipeline:
    """ Create the pipeline given a target task. """
        
    if os.path.exists(name_or_path):
        config = AutoConfig.from_pretrained(name_or_path)
        PIPELINE = TASKS[config.finetuning_task]['pipeline']
        
        MODEL = get_model_class_from_name(
            module_name=MODELS_MODULE, 
            model_name=config.architectures[0]
        )
        model = MODEL.from_pretrained(name_or_path)
        tokenizer = AutoTokenizer.from_pretrained(name_or_path)
        
        pipeline = PIPELINE(
            model=model,
            tokenizer=tokenizer,
            config=config,
        )

    else: 
        TASK = TASKS[task]
        PIPELINE = TASK["pipeline"]
    
        if customization_tag in name_or_path:
            customization = name_or_path.split(customization_tag, 1)[1]
            MODEL = TASK["models"][customization]
            TOKENIZER = TASK["tokenizers"][customization]
            CONFIG = TASK["configs"][customization]
            name_or_path = name_or_path.replace(
                customization_tag+customization,""
            )
        else:
            MODEL = TASK["models"]["default"]
            TOKENIZER = TASK["tokenizers"]["default"]
            CONFIG = TASK["configs"]["default"]

        config = CONFIG.from_pretrained(name_or_path)
        
        if all_labels:
            config.id2label=LabelsMapping(all_labels).id2label()
            config.label2id=LabelsMapping(all_labels).label2id()
            config.num_labels=LabelsMapping(all_labels).num_labels()
            
        if not config.finetuning_task:
            config.finetuning_task=task

        tokenizer = TOKENIZER.from_pretrained(name_or_path)
        model = MODEL.from_pretrained(name_or_path, config=config)
        
        pipeline = PIPELINE(
            model=model,
            tokenizer=tokenizer,
            config=config,
        )
    
    return pipeline


def get_model_class_from_name(module_name, model_name):
    """ Get the model class given his name and the module directory. """
    module = importlib.import_module(module_name)
    return getattr(module, model_name)


def get_available_tasks() -> List[str]:
    """ Get a list of all available tasks."""
    return list(TASKS.keys())
