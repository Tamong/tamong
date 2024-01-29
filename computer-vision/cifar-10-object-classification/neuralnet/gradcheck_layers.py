import numpy as np
from utils import numeric_backward, numeric_gradient
from layers import fc_forward, fc_backward
from layers import relu_forward, relu_backward
from layers import softmax_loss, l2_regularization


def gradcheck_fc():
    print('Running numeric gradient check for fc')
    N, Din, Dout = 3, 4, 5
    x = np.random.randn(N, Din)
    w = np.random.randn(Din, Dout)
    b = np.random.randn(Dout)

    y, cache = fc_forward(x, w, b)
    if y is None:
        print('  Forward pass is not implemented!')
        return

    grad_y = np.random.randn(*y.shape)
    grad_x, grad_w, grad_b = fc_backward(grad_y, cache)
    if grad_x is None or grad_w is None or grad_b is None:
        print('  Backward pass is not implemented!')
        return

    fx = lambda _: fc_forward(_, w, b)[0]
    grad_x_numeric = numeric_backward(fx, x, grad_y)
    max_diff = np.abs(grad_x - grad_x_numeric).max()
    print('  grad_x difference: ', max_diff)

    fw = lambda _: fc_forward(x, _, b)[0]
    grad_w_numeric = numeric_backward(fw, w, grad_y)
    max_diff = np.abs(grad_w - grad_w_numeric).max()
    print('  grad_w difference: ', max_diff)

    fb = lambda _: fc_forward(x, w, _)[0]
    grad_b_numeric = numeric_backward(fb, b, grad_y)
    max_diff = np.abs(grad_b - grad_b_numeric).max()
    print('  grad_b difference: ', max_diff)


def gradcheck_relu():
    print('Running numeric gradient check for relu')
    N, Din = 4, 5
    x = np.random.randn(N, Din)

    y, cache = relu_forward(x)
    if y is None:
        print('  Forward pass is not implemented!')
        return

    grad_y = np.random.randn(*y.shape)
    grad_x = relu_backward(grad_y, cache)
    if grad_x is None:
        print('  Backward pass is not implemented!')
        return

    f = lambda _: relu_forward(_)[0]
    grad_x_numeric = numeric_backward(f, x, grad_y)
    max_diff = np.abs(grad_x - grad_x_numeric).max()
    print('  grad_x difference: ', max_diff)


def gradcheck_softmax():
    print('Running numeric gradient check for softmax loss')
    N, C = 4, 5
    x = np.random.randn(N, C)
    y = np.random.randint(C, size=(N,))
    loss, grad_x = softmax_loss(x, y)
    if loss is None or grad_x is None:
        print('  Softmax not implemented!')
        return

    f = lambda _: softmax_loss(_, y)[0]
    grad_x_numeric = numeric_gradient(f, x)
    max_diff = np.abs(grad_x - grad_x_numeric).max()
    print('  grad_x difference: ', max_diff)


def gradcheck_l2_regularization():
    print('Running numeric gradient check for L2 regularization')
    Din, Dout = 3, 4
    reg = 0.1
    w = np.random.randn(Din, Dout)
    loss, grad_w = l2_regularization(w, reg)
    if loss is None or grad_w is None:
        print('  L2 regularization not implemented!')
        return

    f = lambda _: l2_regularization(_, reg)[0]
    grad_w_numeric = numeric_gradient(f, w)
    max_diff = np.abs(grad_w - grad_w_numeric).max()
    print('  grad_w difference: ', max_diff)


def main():
    gradcheck_fc()
    gradcheck_relu()
    gradcheck_softmax()
    gradcheck_l2_regularization()


if __name__ == '__main__':
    main()
