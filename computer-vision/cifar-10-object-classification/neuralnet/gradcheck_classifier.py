import numpy as np
from linear_classifier import LinearClassifier
from two_layer_net import TwoLayerNet
from utils import numeric_backward


def classifier_numeric_backward(model, X, grad_scores):
    numeric_grads = {}
    for k, param in model.parameters().items():
        def f(_):
            old_val = param.copy()
            param[:] = _
            scores, _ = model.forward(X)
            param[:] = old_val
            return scores
        numeric_grads[k] = numeric_backward(f, param, grad_scores)
    return numeric_grads


def gradcheck_classifier(model, X, grad_scores):
    scores, cache = model.forward(X)
    grads = model.backward(grad_scores, cache)
    numeric_grads = classifier_numeric_backward(model, X, grad_scores)
    assert grads.keys() == numeric_grads.keys()
    for k, grad in grads.items():
        numeric_grad = numeric_grads[k]
        max_diff = np.abs(grad - numeric_grad).max()
        print(f'  Max diff for grad_{k}: ', max_diff)


def gradcheck_linear_classifier():
    print('Running numeric gradient check for LinearClassifier')
    N, D, C = 3, 4, 5
    model = LinearClassifier(D, C)

    X = np.random.randn(N, D)
    grad_scores = np.random.randn(N, C)

    gradcheck_classifier(model, X, grad_scores)


def gradcheck_two_layer_net():
    print('Running numeric gradient check for TwoLayerNet')
    N, D, C, H = 3, 4, 5, 6
    model = TwoLayerNet(D, C, H)

    X = np.random.randn(N, D)
    grad_scores = np.random.randn(N, C)

    gradcheck_classifier(model, X, grad_scores)


def main():
    gradcheck_linear_classifier()
    gradcheck_two_layer_net()


if __name__ == '__main__':
    main()
