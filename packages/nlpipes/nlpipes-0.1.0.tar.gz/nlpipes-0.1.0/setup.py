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
['ftfy>=6.1.0,<7.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=2.1.2,<3.0.0',
 'scipy>=1.9.0,<2.0.0',
 'tensorflow>=2.11.0,<3.0.0',
 'tokenizers>=0.13.0,<0.14.0',
 'tqdm>=4.64.0,<5.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'nlpipes',
    'version': '0.1.0',
    'description': 'Text Classification with TensorFlow',
    'long_description': '<!-- PROJECT NAME -->\n<div align="center">\n  <center><h1>NLPipes</h1></center>\n  <center><h2>A Tensorflow Library for Text Classification</h2></center>\n</div>\n\n<div align="center">\n    <a href="https://opensource.org/licenses/Apache-2.0">\n        <center>\n            <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">\n        </center>\n    </a>\n</div>\n\n</div>\n\n<br>\n\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary>Table of Contents</summary>\n  <ol>\n    <li>\n      <a href="#overview">Overview</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n      </ul>\n    </li> \n        <li>\n           <a href="#how-to-use">How to Use</a>\n        </li>\n      <ul>\n    <li><a href="#mono-label classification">Mono Label task</a></li>\n      </ul>\n  </ol>\n</details>\n\n\n<!-- ABOUT THE PROJECT -->\n## Overview\n\n`NLPipes` is a Tensorflow library that provides an easy way \nto train and use deep-learning based models for a diversity of text classification tasks.\n\n`NLPipes` supports the following tasks:\n* Mono-label classification: Assign one label to each text (e.g. positive, neutral, negative).\n* Multi-label classification: Assign one or more label to each text from a list of possible classes (e.g., Product Category, Product Quality, Delivery Time, and Price)\n* Class-label classification: Assign one label from a list of possible labels for each of a list of classes. A typical use case is aspect based sentiment analysis where one want to detect each aspect mentionned in a review along his assocated sentiment polarity.\n\n#### Built with\n`NLPipes` is built with TensorFlow and HuggingFace Transformers:\n* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework\n* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures\n\n\n<!-- USAGE EXAMPLES -->\n## How To Use\n\n`NLPipes` provides high level abstractions to save having to deal with the complexity of \ndeep-learning based [Natural Language Understanding](https://en.wikipedia.org/wiki/Natural-language_understanding) algorithms.\n\n\n### Mono-label classification\nGive `NLPipes` a single label for each text as a target.\n\n ```python\n from nlpipes import Model\n \n model = Model(task = \'mono-label-classification\',\n               name_or_path = \'bert-base-uncased\')\n \n reviews   = ["text", "text", "text", ...]\n sentiments = ["positive", "negative", "neutral", ...]\n \n test_reviews = ["text", "text", "text", ...]\n test_sentiments = ["positive", "negative", "neutral", ...]\n \n new_reviews = ["text", "text", "text", ...]\n \n model.train(reviews, sentiments)\n \n evaluation = model.evaluate(test_reviews, test_sentiments)\n \n predictions = model.predict(new_reviews)\n  \n model.save(\'./sentiment_detection_model\')\n \n ```\n',
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
