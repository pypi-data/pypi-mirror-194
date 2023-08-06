import numpy as np
import tensorflow as tf

from typeguard import typechecked


class ConfusionMatrix(tf.metrics.Metric):
    """ Computes confusion matrix for mono-label classification. """
    
    @typechecked
    def __init__(self, 
                 num_classes: int,
                 name: str = "Confusion_matrix",
                 dtype = tf.dtypes.int32,
                ):
        super().__init__(name=name, dtype=dtype)
        self.num_classes = num_classes
        self.confusion_matrix = self.add_weight(
            'total',
            shape=[num_classes, num_classes],
            initializer='zeros',
            dtype=self.dtype,
        )

    def update_state(self, y_true, y_pred):
        batch = tf.math.confusion_matrix(
            y_true, y_pred,
            num_classes=self.num_classes,
            dtype=self.dtype,
        )
        self.confusion_matrix.assign_add(batch)

    def result(self):
        return self.confusion_matrix


class MultiLabelConfusionMatrix(tf.metrics.Metric):
    """ Computes confusion matrix for multi-label classification.
    Every class has a dedicated matrix of shape `(2, 2)` 
    that contains:
    - true negatives in cell `(0,0)`
    - false positives in cell `(0,1)`
    - false negatives in cell `(1,0)`
    - true positives in cell `(1,1)`
    Args:
        num_classes: `int`, the number of labels the 
                     prediction task can have.
        name: (Optional) string name of the metric 
              instance.
        dtype: (Optional) data type of the metric 
               result.
    """

    @typechecked
    def __init__(self,
                 num_classes: int,
                 name: str = "Multilabel_confusion_matrix",
                 dtype = tf.dtypes.int32,
        **kwargs,
    ):
        super().__init__(name=name, dtype=dtype)
        self.num_classes = num_classes
        self.true_positives = self.add_weight(
            "true_positives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )
        self.false_positives = self.add_weight(
            "false_positives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )
        self.false_negatives = self.add_weight(
            "false_negatives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )
        self.true_negatives = self.add_weight(
            "true_negatives",
            shape=[self.num_classes],
            initializer="zeros",
            dtype=self.dtype,
        )

    def update_state(self, y_true, y_pred):
        
        y_true = tf.cast(y_true, tf.int32)
        y_pred = tf.cast(y_pred, tf.int32)
        
        true_positive = tf.math.count_nonzero(y_true * y_pred, 0)
        pred_sum = tf.math.count_nonzero(y_pred, 0)
        true_sum = tf.math.count_nonzero(y_true, 0)
        false_positive = pred_sum - true_positive
        false_negative = true_sum - true_positive
        y_true_negative = tf.math.not_equal(y_true, 1)
        y_pred_negative = tf.math.not_equal(y_pred, 1)
        true_negative = tf.math.count_nonzero(
            tf.math.logical_and(y_true_negative, y_pred_negative), axis=0
        )

        self.true_positives.assign_add(tf.cast(true_positive, self.dtype))
        self.false_positives.assign_add(tf.cast(false_positive, self.dtype))
        self.false_negatives.assign_add(tf.cast(false_negative, self.dtype))
        self.true_negatives.assign_add(tf.cast(true_negative, self.dtype))

    def result(self):
        flat_confusion_matrix = tf.convert_to_tensor(
            [
                self.true_negatives,
                self.false_positives,
                self.false_negatives,
                self.true_positives,
            ]
        )
        
        confusion_matrix = tf.reshape(
            tf.transpose(flat_confusion_matrix), [-1, 2, 2]
        )

        return confusion_matrix
    
    def reset_state(self):
        reset_value = np.zeros(self.num_classes, dtype=np.int32)
        tf.keras.backend.batch_set_value([(v, reset_value) for v in self.variables])
    