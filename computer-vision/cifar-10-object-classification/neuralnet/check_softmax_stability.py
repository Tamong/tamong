import numpy as np
from layers import softmax_loss


""" A simple test-case to check the numeric stability of softmax_loss """


def main():
    big = 1e3
    x = np.array([
          [big, 0, -big],  # noqa: E126
          [-big, big, 0],  # noqa: E126
          [0, -big, big],  # noqa: E126
        ])                 # noqa: E126
    y = np.array([0, 1, 2])
    loss, _ = softmax_loss(x, y)
    if loss is None:
        print('You have not yet implemented softmax_loss')
        return
    print('Input scores:')
    print(x)
    print(f'Input labels: {y}')
    print(f'Output loss: {loss}')
    if np.isnan(loss):
        print('Your softmax_loss gave a NaN with big input values.')
        print('Did you forget to implement the max-subtraction trick?')
    else:
        print('It seems like your softmax_loss is numerically stable!')


if __name__ == '__main__':
    main()
