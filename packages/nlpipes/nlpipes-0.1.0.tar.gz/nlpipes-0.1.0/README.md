<!-- PROJECT NAME -->
<div align="center">
  <center><h1>NLPipes</h1></center>
  <center><h2>A Tensorflow Library for Text Classification</h2></center>
</div>

<div align="center">
    <a href="https://opensource.org/licenses/Apache-2.0">
        <center>
            <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">
        </center>
    </a>
</div>

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
    <li><a href="#mono-label classification">Mono Label task</a></li>
      </ul>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## Overview

`NLPipes` is a Tensorflow library that provides an easy way 
to train and use deep-learning based models for a diversity of text classification tasks.

`NLPipes` supports the following tasks:
* Mono-label classification: Assign one label to each text (e.g. positive, neutral, negative).
* Multi-label classification: Assign one or more label to each text from a list of possible classes (e.g., Product Category, Product Quality, Delivery Time, and Price)
* Class-label classification: Assign one label from a list of possible labels for each of a list of classes. A typical use case is aspect based sentiment analysis where one want to detect each aspect mentionned in a review along his assocated sentiment polarity.

#### Built with
`NLPipes` is built with TensorFlow and HuggingFace Transformers:
* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework
* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures


<!-- USAGE EXAMPLES -->
## How To Use

`NLPipes` provides high level abstractions to save having to deal with the complexity of 
deep-learning based [Natural Language Understanding](https://en.wikipedia.org/wiki/Natural-language_understanding) algorithms.


### Mono-label classification
Give `NLPipes` a single label for each text as a target.

 ```python
 from nlpipes import Model
 
 model = Model(task = 'mono-label-classification',
               name_or_path = 'bert-base-uncased')
 
 reviews   = ["text", "text", "text", ...]
 sentiments = ["positive", "negative", "neutral", ...]
 
 test_reviews = ["text", "text", "text", ...]
 test_sentiments = ["positive", "negative", "neutral", ...]
 
 new_reviews = ["text", "text", "text", ...]
 
 model.train(reviews, sentiments)
 
 evaluation = model.evaluate(test_reviews, test_sentiments)
 
 predictions = model.predict(new_reviews)
  
 model.save('./sentiment_detection_model')
 
 ```
