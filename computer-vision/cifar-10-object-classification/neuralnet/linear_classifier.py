import numpy as np
from classifier import Classifier
from layers import fc_forward, fc_backward


class LinearClassifier(Classifier):
    def __init__(self, input_dim=3072, num_classes=10, weight_scale=1e-3):
        """
        Initialize a new linear classifier.

        Inputs:
        - input_dim: The number of dimensions in the input.
        - num_classes: The number of classes over which to classify
        - weight_scale: The weights of the model will be initialized from a
          Gaussian distribution with standard deviation equal to weight_scale.
          The bias of the model will always be initialized to zero.
        """
        self.W = weight_scale * np.random.randn(input_dim, num_classes)
        self.b = np.zeros(num_classes)

    def parameters(self):
        params = {
            'W': self.W,
            'b': self.b,
        }
        return params

    def forward(self, X):
        scores, cache = fc_forward(X, self.W, self.b)
        return scores, cache

    def backward(self, grad_scores, cache):
        grad_X, grad_W, grad_b = fc_backward(grad_scores, cache)
        grads = {
            'W': grad_W,
            'b': grad_b,
        }
        return grads
