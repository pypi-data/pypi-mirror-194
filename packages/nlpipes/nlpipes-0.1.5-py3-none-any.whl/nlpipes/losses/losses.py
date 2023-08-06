import tensorflow as tf

def softmax_cross_entropy(labels, logits) -> tf.Tensor:
    """  """
    softmax = tf.nn.softmax_cross_entropy_with_logits
    loss_value = softmax(labels, logits, axis=-1, name='Loss')
    return loss_value
