import argparse
from data import load_cifar10, DataSampler
from two_layer_net import TwoLayerNet
from utils import check_accuracy

"""
Runs a trained model on the CIFAR-10 test set
"""


parser = argparse.ArgumentParser()
parser.add_argument(
    '--checkpoint-file',
    default='checkpoint.pkl',
    help='File where trained model has been saved')
parser.add_argument(
    '--batch-size',
    type=int,
    default=128,
    help='Batch size to use for evaluation')


def main(args):
    data = load_cifar10()
    sampler = DataSampler(data['X_test'], data['y_test'], args.batch_size)
    print(f'Loading model from {args.checkpoint_file}')
    model = TwoLayerNet.load(args.checkpoint_file)
    acc = check_accuracy(model, sampler)
    print(f'Test-set accuracy: {acc:.2f}')


if __name__ == '__main__':
    main(parser.parse_args())
