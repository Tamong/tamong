import argparse
import numpy as np
import matplotlib.pyplot as plt

from data import load_cifar10, DataSampler
from linear_classifier import LinearClassifier
from two_layer_net import TwoLayerNet
from optim import SGD
from layers import softmax_loss, l2_regularization
from utils import check_accuracy


parser = argparse.ArgumentParser()
parser.add_argument(
    "--plot-file",
    default="plot.pdf",
    help="File where loss and accuracy plot should be saved",
)
parser.add_argument(
    "--checkpoint-file",
    default="checkpoint.pkl",
    help="File where trained model weights should be saved",
)
parser.add_argument(
    "--print-every",
    type=int,
    default=25,
    help="How often to print losses during training",
)


def main(args):
    # How much data to use for training
    num_train = 20000

    # Model architecture hyperparameters.
    hidden_dim = 16

    # Optimization hyperparameters.
    batch_size = 128
    num_epochs = 10
    learning_rate = 1e-4
    reg = 1.0

    ###########################################################################
    # TODO: Set hyperparameters for training your model. You can change any   #
    # of the hyperparameters above.                                           #
    ###########################################################################

    hidden_dim = 24
    batch_size = 144
    num_epochs = 48
    learning_rate = 0.11
    reg = 0
    # Last Run's Last Accuracy - 49.00:42.44

    ###########################################################################
    #                           END OF YOUR CODE                              #
    ###########################################################################

    data = load_cifar10(num_train=num_train)
    train_sampler = DataSampler(data["X_train"], data["y_train"], batch_size)
    val_sampler = DataSampler(data["X_val"], data["y_val"], batch_size)

    # Set up the model and optimizer
    model = TwoLayerNet(hidden_dim=hidden_dim)
    optimizer = SGD(model.parameters(), learning_rate=learning_rate)

    stats = {
        "t": [],
        "loss": [],
        "train_acc": [],
        "val_acc": [],
    }

    for epoch in range(1, num_epochs + 1):
        print(f"Starting epoch {epoch} / {num_epochs}")
        for i, (X_batch, y_batch) in enumerate(train_sampler):
            loss, grads = training_step(model, X_batch, y_batch, reg)
            optimizer.step(grads)
            if i % args.print_every == 0:
                print(f"  Iteration {i} / {len(train_sampler)}, loss = {loss}")
            stats["t"].append(i / len(train_sampler) + epoch - 1)
            stats["loss"].append(loss)

        print("Checking accuracy")
        train_acc = check_accuracy(model, train_sampler)
        print(f"  Train: {train_acc:.2f}")
        val_acc = check_accuracy(model, val_sampler)
        print(f"  Val:   {val_acc:.2f}")
        stats["train_acc"].append(train_acc)
        stats["val_acc"].append(val_acc)

    print(f"Saving plot to {args.plot_file}")
    plot_stats(stats, args.plot_file)
    print(f"Saving model checkpoint to {args.checkpoint_file}")
    model.save(args.checkpoint_file)


def training_step(model, X_batch, y_batch, reg):
    """
    Compute the loss and gradients for a single training iteration of a model
    given a minibatch of data. The loss should be a sum of a cross-entropy loss
    between the model predictions and the ground-truth image labels, and
    an L2 regularization term on all weight matrices in the fully-connected
    layers of the model. You should not regularize the bias vectors.

    Inputs:
    - model: A Classifier instance
    - X_batch: A numpy array of shape (N, D) giving a minibatch of images
    - y_batch: A numpy array of shape (N,) where 0 <= y_batch[i] < C is the
      ground-truth label for the image X_batch[i]
    - reg: A float giving the strength of L2 regularization to use.

    Returns a tuple of:
    - loss: A float giving the loss (data loss + regularization loss) for the
      model on this minibatch of data
    - grads: A dictionary giving gradients of the loss with respect to the
      parameters of the model. In particular grads[k] should be the gradient
      of the loss with respect to model.parameters()[k].
    """
    loss, grads = None, None
    ###########################################################################
    # TODO: Compute the loss and gradient for one training iteration.         #
    ###########################################################################

    scores, cache = model.forward(X_batch)

    data_loss, dscores = softmax_loss(scores, y_batch)

    reg_loss = 0.0
    reg_grads = {}
    for param_name, param_value in model.parameters().items():
        if "W" in param_name:
            l2_loss, l2_grad = l2_regularization(param_value, reg)
            reg_loss += l2_loss
            reg_grads[param_name] = l2_grad

    loss = data_loss + reg_loss

    grads = model.backward(dscores, cache)

    for param_name in grads:
        if "W" in param_name:
            grads[param_name] += reg_grads[param_name]

    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return loss, grads


def plot_stats(stats, filename):
    plt.subplot(1, 2, 1)
    plt.plot(stats["t"], stats["loss"], "o", alpha=0.5, ms=4)
    plt.title("Loss")
    plt.xlabel("Epoch")
    loss_xlim = plt.xlim()

    plt.subplot(1, 2, 2)
    epoch = np.arange(1, 1 + len(stats["train_acc"]))
    plt.plot(epoch, stats["train_acc"], "-o", label="train")
    plt.plot(epoch, stats["val_acc"], "-o", label="val")
    plt.xlim(loss_xlim)
    plt.title("Accuracy")
    plt.xlabel("Epoch")
    plt.legend(loc="upper left")

    plt.gcf().set_size_inches(12, 4)
    plt.savefig(filename, bbox_inches="tight")
    plt.clf()


if __name__ == "__main__":
    main(parser.parse_args())
