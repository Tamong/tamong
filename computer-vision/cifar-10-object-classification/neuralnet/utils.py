import numpy as np


def numeric_gradient(f, x, h=1e-6):
    """
    Computes a numeric gradient of a function that takes an array argument.

    Inputs:
    - f: A function of the form y = f(x) where x is a numpy array and y is
      a Python float
    - x: The point at which to compute a numeric gradient
    - h: The step size to use for computing the numeric gradient

    Returns:
    - grad_x: Numpy array of the same shape as x giving a numeric approximation
      to the gradient of f at the point x.
    """
    grad = np.zeros_like(x)
    grad_flat = grad.reshape(-1)
    x_flat = x.reshape(-1)
    for i in range(grad_flat.shape[0]):
        old_val = x_flat[i]
        x_flat[i] = old_val + h
        pos = f(x)
        x_flat[i] = old_val - h
        neg = f(x)
        grad_flat[i] = (pos - neg) / (2.0 * h)
        x_flat[i] = old_val
    return grad


def numeric_backward(f, x, grad_y, h=1e-6):
    """
    Computes a numeric backward pass for a function that inputs and outputs a
    numpy array.

    Inputs:
    - f: A function of the form y = f(x) where x and y are both numpy arrays
      of any shape.
    - x: A numpy array giving the point at which to compute the numeric
      backward pass.
    - grad_y: A numpy array of the same shape as f(x) giving upstream gradients
    - h: The step size to use for the numeric derivative

    Returns:
    - grad_x: A numpy array with the same shape as x giving a numeric
      approximation to a backward pass through f.
    """
    grad_x = np.zeros_like(x)
    grad_x_flat = grad_x.reshape(-1)
    x_flat = x.reshape(-1)
    for i in range(x_flat.shape[0]):
        old_val = x_flat[i]
        x_flat[i] = old_val + h
        pos = f(x)
        x_flat[i] = old_val - h
        neg = f(x)
        local_grad = (pos - neg) / (2.0 * h)
        grad_x_flat[i] = np.sum(local_grad * grad_y)
        x_flat[i] = old_val
    return grad_x


def check_accuracy(model, sampler):
    num_correct, num_samples = 0, 0
    for X_batch, y_batch in sampler:
        y_pred = model.predict(X_batch)
        num_correct += (y_pred == y_batch).sum()
        num_samples += y_pred.shape[0]
    acc = 100 * num_correct / num_samples
    return acc
