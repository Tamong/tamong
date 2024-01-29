import numpy as np


class Optimizer:
    """
    Base class for implementing optimization algorithms that can be used to
    optimize the parameters of Classifer instances.

    This base class should not be used directly; instead subclasses should
    override the step method.

    An Optimizer object is expected to be used like this:

    model = LinearClassifier()  # Or another Classifier subclass
    optimizer = Optimizer(model.parameters(), [other arguments])
    while not_done:
      # Run a forward and backward pass of the model to get a grads dict
      grads = model.backward() # Compute gradient of loss w/respect to params
      optimizer.step(grads)    # Update the parameters of the model in-place
    """
    def __init__(self, params):
        """
        Create a new Optimizer object. Subclasses should implement their own
        initializer that takes any required hyperparameters.
        """
        raise NotImplementedError

    def step(self, grads):
        """
        Update the parameters of the model. Subclasses should override this.

        IMPORTANT: The step method must update the parameters of the model
        in-place -- it should not replace any numpy arrays in params.

        For example, this is an in-place operation and is ok:
        params[k] -= learning_rate * grads[k]

        This is NOT an in-place operation, and is NOT OK:
        params[k] = params[k] - learning_rate * grads[k]
        """
        raise NotImplementedError


class SGD(Optimizer):
    """
    Implements stochastic gradient descent, which updates parameters according
    to the learning rule

    p -= learning_rate * g

    where p is a parameter and g is the gradient of the loss with respect to
    the parameter.
    """
    def __init__(self, params, learning_rate):
        self.params = params
        self.learning_rate = learning_rate

    def step(self, grads):
        for k, g in grads.items():
            self.params[k] -= self.learning_rate * g


