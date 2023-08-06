# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlpipes',
 'nlpipes.callbacks',
 'nlpipes.configurations',
 'nlpipes.data',
 'nlpipes.layers',
 'nlpipes.losses',
 'nlpipes.metrics',
 'nlpipes.models',
 'nlpipes.optimization',
 'nlpipes.pipelines',
 'nlpipes.trainers']

package_data = \
{'': ['*']}

install_requires = \
['ftfy>=6.1.1,<7.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'tensorflow>=2.11.0,<3.0.0',
 'tokenizers>=0.13.0,<0.14.0',
 'tqdm>=4.64.0,<5.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'nlpipes',
    'version': '0.1.3',
    'description': 'Text Classification with TensorFlow',
    'long_description': '<!-- PROJECT NAME -->\n<div align="center">\n  <h1>NLPIPES</h1>\n  <h2>Text Classification with Transformers</h2>\n</div>\n\n<div align="center">\n    <a href="https://opensource.org/licenses/Apache-2.0">\n       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">\n    </a>\n</div>\n\n<br>\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary>Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#overview">Overview</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n      </ul>\n    </li> \n        <li>\n           <a href="#how-to-use">How to Use</a>\n        </li>\n      <ul>\n        <li><a href="#Train a model">Train a model</a></li>\n        <li><a href="#Evaluate a model">Evaluate a model</a></li>\n        <li><a href="#Predict with model">Predict with a model</a></li>\n      </ul>\n      <li><a href="#References">References</a></li>\n  </ol>\n</details>\n\n\n<!-- ABOUT THE PROJECT -->\n## Overview\n\n`NLPipes` provides an easy way to use Transformers-based models for training, evaluation and inference on a diversity of text classification tasks, including:\n\n* **Single-label classification**: Assign one label to each text. A typical use case is sentiment analysis where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.\n* **Multi-label classification** [Not yet implemented]: Assign one or more label to each text from a list of possible labels. A typical use case is tag detection where one want to detect the multiple aspects mentionned in a review (e.g., #product_quality, #delivery_time, #price, ...).\n* **Aspect-based classification** [Not yet implemented]: Assign one label from a list of possible labels for each of a list of aspects. A typical use case is aspect based sentiment analysis where one want to detect each aspect mentionned in a review along his assocated sentiment polarity (e.g., #product_quality: neutral, #delivery_time: negative, #price: positive, ...).\n* **Zero-shot classification** [Not yet implemented]: Assign one or more label to each text from a list of possible labels without the requirement of an annotated training dataset.\n\n\n#### Built with\n`NLPipes` is built with TensorFlow and HuggingFace Transformers:\n* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework\n* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures\n\n#### Pre-required\nWe recommend using a machine with at least 1 GPU accelerator and XX Go of memory to use `NLPipes`.\n\n<!-- USAGE EXAMPLES -->\n## How To Use\n\n`NLPipes` expose a simple `Model` API that offers an high-level abstraction to run several text classification tasks. The `Model` encapsulate most of the complex code from the library and save having to deal with the diversity and complexity of transformers based algorithms to build an end-to-end solution for text classification.\n\n\n### Train a model\nGive `NLPipes` a single label for each text as a target to train a single-label classifier.\n\n ```python\n from nlpipes import Model\n \n reviews = ["text", "text", "text", ...]\n sentiments = ["positive", "negative", "neutral", ...]\n all_labels = ["negative", "neutral", "positive"]\n \n model = Model(task=\'single-label-classification\',\n               name_or_path=\'bert-base-uncased\',\n               all_labels=all_labels)\n \n model.train(reviews, sentiments)\n  \n model.save(\'./sentiment_detection_model\')\n \n ```\n\n### Evaluate a model\nGive `NLPipes` an evaluation metric and the label(s) for each text to evaluate the model.\n\n ```python\n from nlpipes import Model, Confusion_matrix\n \n eval_reviews   = ["text", "text", "text", ...]\n eval_sentiments = ["positive", "negative", "neutral", ...]\n eval_metric = Confusion_matrix(num_labels=3)\n \n model = Model(\'./sentiment_detection_model\')\n \n evaluation = model.evaluate(eval_reviews, eval_sentiments,\n                             metric=eval_metric)\n  \n print(\'Model performance: \', evaluation)\n \n ```\n \n ### Predict with a model\n Give `NLPipes` new texts to predict the most relevant label(s).\n \n ```python\n from nlpipes import Model\n \n new_reviews = ["text", "text", "text", ...]\n \n model = Model(\'./sentiment_detection_model\')\n \n predictions = model.predict(new_reviews)\n \n print("Reviews: ", new_reviews)\n print(\'Predicted labels: \', predictions.label)\n print(\'Confidence Score: \', predictions.scores)\n \n ```\n \n <!-- References -->\n## References',
    'author': 'Ayhan UYANIK',
    'author_email': 'ayhan.uyanik@renault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
