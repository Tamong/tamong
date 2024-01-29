import pickle


class Classifier:
    """
    A base class for an image classification model.

    Subclasses should override the following methods:
    - parameters
    - forward
    - backward
    """
    def parameters(self):
        """
        Returns a dictionary of all learnable parameters for this model.

        The keys of the dictionary should be strings giving a human-readable
        name for each parameter, and the values should be numpy arrays of the
        parameters.

        Subclasses should override this.
        """
        raise NotImplementedError

    def forward(self, X):
        """
        Computes the forward pass of the model to compute classification scores
        over C categories giving a minibatch of N inputs.

        Subclasses should override this.

        Inputs:
        - X: A numpy array of shape (N, D) giving input images to classify

        Returns a tuple of:
        - scores: A numpy array of shape (N, C) giving classification scores
        - cache: An object containing data that will be needed during backward
        """
        raise NotImplementedError

    def backward(self, grad_scores, cache):
        """
        Computes the backward pass of the model to compute the gradient of the
        loss with respect to all parameters of the model.

        Subclasses should override this.

        Inputs:
        - grad_scores: A numpy array of shape (N, C) giving upstream gradients
          of the loss with respect to the classification scores predicted by
          the forward pass of this model
        - cache: A cache object created by the forward pass of this model

        Returns:
        - grads: A dictionary of gradients for all learnable parameters of this
          model. The grads dict should have the same keys as the dict returned
          by self.parameters(), and grads[k] should be a numpy array of the
          same shape as self.parameters()[k] giving the gradient of the loss
          with respect to that parameter.
        """
        raise NotImplementedError

    def predict(self, X):
        """
        Make predictions for a batch of images.

        Inputs:
        - X: A numpy array of shape (N, D) giving input images to classify

        Returns:
        - y_pred: A numpy array of shape (N,) where each element is an integer
          in the range 0 <= y_pred[i] < C giving the predicted category for
          the input X[i].
        """
        scores, _ = self.forward(X)
        y_pred = scores.argmax(axis=1)
        return y_pred

    def save(self, filename):
        """
        Save the parameters of this model to disk.

        Inputs:
        - filename: Path to the file where this model should be saved
        """
        params = self.parameters()
        with open(filename, 'wb') as f:
            pickle.dump(params, f)

    @classmethod
    def load(cls, filename):
        """
        Load the parameters of this model from disk.

        This copies data in-place into the ndarrays returned by the parameters
        method, so this will only work properly for subclasses if:
        (1) The subclass __init__ method can be called without arguments
        (2) The ndarrays returned by the parameters method are sufficient for
            capturing the state of the model.

        Example usage:
        model = TwoLayerNet(...)
        model.save('checkpoint.pkl')
        model2 = TwoLayerNet.load('checkpoint.pkl')

        Inputs:
        - filename: Path to the file from which parameters should be read

        Returns:
        - A Classifier subclass loaded from the file
        """
        model = cls()
        params = model.parameters()
        with open(filename, 'rb') as f:
            saved_params = pickle.load(f)
        for k, param in params.items():
            saved_param = saved_params[k]
            param.resize(saved_param.shape, refcheck=False)
            param[:] = saved_param
        return model
