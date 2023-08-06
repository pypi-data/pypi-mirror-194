<!-- PROJECT NAME -->
<div align="center">
  <h1>NLPIPES</h1>
  <h2>Text Classification with Transformers</h2>
</div>

<div align="center">
    <a href="https://opensource.org/licenses/Apache-2.0">
       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">
    </a>
</div>

<br>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#overview">Overview</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li> 
        <li>
           <a href="#how-to-use">How to Use</a>
        </li>
      <ul>
        <li><a href="#Train a model">Train a model</a></li>
        <li><a href="#Evaluate a model">Evaluate a model</a></li>
        <li><a href="#Predict with model">Predict with a model</a></li>
      </ul>
      <li><a href="#References">References</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## Overview

`NLPipes` provides an easy way to use Transformers-based models for training, evaluation and inference on a diversity of text classification tasks, including:

* **Single-label classification**: Assign one label to each text. A typical use case is sentiment analysis where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.
* **Multi-label classification** [Not yet implemented]: Assign one or more label to each text from a list of possible labels. A typical use case is tag detection where one want to detect the multiple aspects mentionned in a review (e.g., #product_quality, #delivery_time, #price, ...).
* **Aspect-based classification** [Not yet implemented]: Assign one label from a list of possible labels for each of a list of aspects. A typical use case is aspect based sentiment analysis where one want to detect each aspect mentionned in a review along his assocated sentiment polarity (e.g., #product_quality: neutral, #delivery_time: negative, #price: positive, ...).
* **Zero-shot classification** [Not yet implemented]: Assign one or more label to each text from a list of possible labels without the requirement of an annotated training dataset.


#### Built with
`NLPipes` is built with TensorFlow and HuggingFace Transformers:
* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework
* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures

#### Pre-required
We recommend using a machine with at least 1 GPU accelerator and XX Go of memory to use `NLPipes`.

<!-- USAGE EXAMPLES -->
## How To Use

`NLPipes` expose a simple `Model` API that offers an high-level abstraction to run several text classification tasks. The `Model` encapsulate most of the complex code from the library and save having to deal with the diversity and complexity of transformers based algorithms to build an end-to-end solution for text classification.


### Train a model
Give `NLPipes` a single label for each text as a target to train a single-label classifier.

 ```python
 from nlpipes import Model
 
 reviews = ["text", "text", "text", ...]
 sentiments = ["positive", "negative", "neutral", ...]
 all_labels = ["negative", "neutral", "positive"]
 
 model = Model(task='single-label-classification',
               name_or_path='bert-base-uncased',
               all_labels=all_labels)
 
 model.train(reviews, sentiments)
  
 model.save('./sentiment_detection_model')
 
 ```

### Evaluate a model
Give `NLPipes` an evaluation metric and the label(s) for each text to evaluate the model.

 ```python
 from nlpipes import Model, Confusion_matrix
 
 eval_reviews   = ["text", "text", "text", ...]
 eval_sentiments = ["positive", "negative", "neutral", ...]
 eval_metric = Confusion_matrix(num_labels=3)
 
 model = Model('./sentiment_detection_model')
 
 evaluation = model.evaluate(eval_reviews, eval_sentiments,
                             metric=eval_metric)
  
 print('Model performance: ', evaluation)
 
 ```
 
 ### Predict with a model
 Give `NLPipes` new texts to predict the most relevant label(s).
 
 ```python
 from nlpipes import Model
 
 new_reviews = ["text", "text", "text", ...]
 
 model = Model('./sentiment_detection_model')
 
 predictions = model.predict(new_reviews)
 
 print("Reviews: ", new_reviews)
 print('Predicted labels: ', predictions.label)
 print('Confidence Score: ', predictions.scores)
 
 ```
 
 <!-- References -->
## References