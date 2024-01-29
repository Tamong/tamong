import os
import pickle
import numpy as np


class DataSampler:
    """
    A helper class to iterate through data and labels in minibatches.

    Example usage:

    X = torch.randn(N, D)
    y = torch.randn(N)
    sampler = DataSampler(X, y, batch_size=64)
    for X_batch, y_batch in sampler:
        print(X_batch.shape)  # (64, D)
        print(y_batch.shape)  # (64,)

    The loop will run for exactly one epoch over X and y -- that is, each entry
    will appear in exactly one minibatch. If the batch size does not evenly
    divide the number of elements in X and y then the last batch will be have
    fewer than batch_size elements.

    You can use a DataSampler object to iterate through the data as many times
    as you want. Each epoch will iterate through the data in a random order.
    """
    def __init__(self, X, y, batch_size):
        """
        Create a new DataSampler.

        Inputs:
        - X: Numpy array of shape (N, D)
        - y: Numpy array of shape (N,)
        - batch_size: Integer giving the number of elements for each minibatch
        """
        self.X = X
        self.y = y
        self.batch_size = batch_size

    def __iter__(self):
        """
        Iterate through the data. This returns a generator which yields tuples:
        - X_batch: Numpy array of shape (batch_size, D)
        - y_batch: Numpy array of shape (batch_size,)

        Note that when the batch size does not divide the number of elements N,
        then the last minibatch will have fewer than batch_size elements.
        """
        N = self.X.shape[0]
        perm = np.random.permutation(N)
        start, stop = 0, self.batch_size
        while start < N:
            idx = perm[start:stop]
            X_batch = self.X[idx]
            y_batch = self.y[idx]
            start += self.batch_size
            stop += self.batch_size
            yield X_batch, y_batch

    def __len__(self):
        """ Get the number of minibatches in an epoch. """
        return self.X.shape[0] // self.batch_size


_CIFAR_DIR = 'cifar-10-batches-py'


def load_cifar10(data_dir=_CIFAR_DIR, num_train=10000, num_val=5000,
                 num_test=10000, seed=442):
    """
    Load and preprocess CIFAR-10 data. More specifically:

    (1) Load the raw data from disk
    (2) Shuffle the train and test sets
    (3) Subsample the training set to create train and val sets
    (4) Subsample the test set
    (5) Preprocess all images to be float32 in the range [0, 1]

    Inputs:
    - data_dir: Path to the cifar-10-batches-py directory where the CIFAR-10
      dataset has been downloaded
    - num_train: Size of training set after subsampling
    - num_val: Size of validation set after subsampling
    - num_test: Size of test set after subsampling
    - seed: Random seed to use when shuffling data

    Returns a dictionary with keys and values:
    - X_train: float32 array of shape (num_train, 3072)
    - X_val: float32 array of shape (num_val, 3072)
    - X_test: float32 array of shape (num_test, 3072)
    - y_train: int64 array of shape (num_train,) in the range [0, 10)
    - y_val: int64 array of shape (num_val,) in the range [0, 10)
    - y_test: int64 array of shape (num_test,) in the range [0, 10)
    """
    if not os.path.isdir(data_dir):
        print(f'Directory {data_dir} not found.')
        print('Did you run download_cifar.sh?')
        raise ValueError

    # Load training data
    X_train, y_train = [], []
    for i in [1, 2, 3, 4, 5]:
        filename = os.path.join(data_dir, f'data_batch_{i}')
        with open(filename, 'rb') as f:
            batch = pickle.load(f, encoding='latin1')
        X_train.append(batch['data'])
        y_train.append(batch['labels'])
    X_train = np.concatenate(X_train, axis=0)
    y_train = np.concatenate(y_train, axis=0)

    # Load test data
    filename = os.path.join(data_dir, 'test_batch')
    with open(filename, 'rb') as f:
        batch = pickle.load(f, encoding='latin1')
    X_test = batch['data']
    y_test = np.asarray(batch['labels'])

    # Shuffle the training and test sets
    rng = np.random.default_rng(seed)
    idx = rng.permutation(X_train.shape[0])
    X_train = X_train[idx]
    y_train = y_train[idx]
    idx = rng.permutation(X_test.shape[0])
    X_test = X_test[idx]
    y_test = y_test[idx]

    # Split training set into train and val
    if num_train + num_val > X_train.shape[0]:
        msg = (f'Got num_train = {num_train}, num_val = {num_val}; '
               f'must have num_train + num_val <= {X_train.shape[0]}')
        raise ValueError(msg)
    if num_test > X_test.shape[0]:
        msg = (f'Got num_test = {num_test}; '
               f'must have num_test < {X_test.shape[0]}')
        raise ValueError(msg)
    X_train_orig = X_train
    y_train_orig = y_train
    X_train = X_train_orig[:num_train]
    y_train = y_train_orig[:num_train]
    X_val = X_train_orig[num_train:(num_train + num_val)]
    y_val = y_train_orig[num_train:(num_train + num_val)]
    X_test = X_test[:num_test]
    y_test = y_test[:num_test]

    # Preprocess images: Convert to float in the range [0, 1]
    X_train = X_train.astype(np.float32) / 255.0
    X_val = X_val.astype(np.float32) / 255.0
    X_test = X_test.astype(np.float32) / 255.0

    data = {
        'X_train': X_train,
        'y_train': y_train,
        'X_val': X_val,
        'y_val': y_val,
        'X_test': X_test,
        'y_test': y_test,
    }
    return data


if __name__ == '__main__':
    data = load_cifar10()
    for k, v in data.items():
        print(k, v.shape, v.dtype)
