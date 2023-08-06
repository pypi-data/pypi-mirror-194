<!-- PROJECT NAME -->
<div align="center">
  <h2>NLPIPES</h2>
  <h3>Text Classification with Transformers</h3>
</div>

<div align="center">
    <a href="https://opensource.org/licenses/Apache-2.0">
       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">
    </a>
     <a href="https://opensource.org/licenses/Apache-2.0">
       <img alt="PyPi Version" src="https://img.shields.io/pypi/pyversions/nlpipes">
    </a> 
    <a href="https://pypi.org/project/nlpipes/">
        <img alt="PyPi Package Version" src="https://img.shields.io/pypi/v/nlpipes">
    </a>
    <a href="https://pepy.tech/project/nlpipes/">
        <img alt="PyPi Downloads" src="https://static.pepy.tech/badge/nlpipes/month">
    </a>
</div>

<div align="center">
   <center>
          <a href="https://git.irt-systemx.fr/ec3-fa16/nlpipes/-/tree/main/notebooks"><strong>Examples</strong></a>
        • <a href="https://git.irt-systemx.fr/ec3-fa16/nlpipes/-/tree/main/docs"><strong>Documentation</strong></a>
        • <a href="https://git.irt-systemx.fr/ec3-fa16/nlpipes"><strong>References</strong></a>
    </center>
</div>

<div align="center">
  <img src="img/nlpipes_screenshot.png" alt="nlpipes_screenshot" title="nlpipes screenshot">
</div>


## Overview

`NLPipes` provides an easy way to use Transformers-based models for training, evaluation and inference on a diversity of text classification tasks, including:

* **Single-label classification**: Assign one label to each text. A typical use case is sentiment analysis where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.
* **Multi-labels classification** [Not yet implemented]: Assign one or more label to each text from a list of possible labels. A typical use case is tag detection where one want to detect the multiple aspects mentionned in a review (e.g., #product_quality, #delivery_time, #price, ...).
* **Aspect-based classification** [Not yet implemented]: Assign one label from a list of possible labels for each of a list of aspects. A typical use case is aspect based sentiment analysis where one want to detect each aspect mentionned in a review along his assocated sentiment polarity (e.g., #product_quality: neutral, #delivery_time: negative, #price: positive, ...).
* **Zero-shot classification** [Not yet implemented]: Assign one or more label to each text from a list of possible labels without the requirement of an annotated training dataset.


#### Built with
`NLPipes` is built with TensorFlow and HuggingFace Transformers:
* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework
* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures

## Getting Started

#### Installation
1. Create a virtual environment

 ```console
 python3 -m venv nlpipesenv
 source nlpipesenv/bin/activate
 ```

2. Install the package

 ```console
 pip install nlpipes
 ```

#### Examples

`NLPipes` expose a simple `Model` API that offers a common abstraction to run several text classification tasks. The `Model` encapsulate most of the complex code from the library and save having to deal with the complexity of transformers based algorithms to build a text classifier. Here are some examples of `NLPipes` applications on real open datasets:

Name|Notebook|Description|Task|Size|Memory| 
----|-----------|-----|---------|---------|---------|
GooglePlay Sentiment Detection|[Link](https://git.irt-systemx.fr/ec3-fa16/nlpipes/-/blob/dev/notebooks/googleplay_sentiment_labeling.ipynb)|Train a model to label reviews from the GooglePlay store reviews|Single-label classification|  |  
StackOverflow tags Detection|Coming soon|Train a model to detect tags from the StackOverFlow questions |Multiple-labels classification|  | 
GooglePlay Aspect and Sentiment Detection|Coming soon|Train a model for aspect based sentiment detection to detect the aspects mentionned in GooglePlay reviews along his assocated sentiment polarity |Aspect-based classification|  | 

 
 
## Notice
`NLPipes` is still in its early stage and is not yet suitable for production usage. Proceed with caution and use it at your own risk. The library comes with no warranty and future releases could bring substantial API and behavior changes.
