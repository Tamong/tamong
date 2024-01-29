"""
CS 4391 Homework 5 Programming
Run this script for YOLO training
"""
import torch
import torch.utils.data as data
import os, math
import sys
import time
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from data import CrackerBox
from model import YOLO
from loss import compute_loss


# plot losses
def plot_losses(losses, filename='train_loss.pdf'):

    num_epoches = losses.shape[0]
    l = np.mean(losses, axis=1)

    plt.subplot(1, 1, 1)
    plt.plot(range(num_epoches), l, marker='o', alpha=0.5, ms=4)
    plt.title('Loss')
    plt.xlabel('Epoch')
    loss_xlim = plt.xlim()

    plt.gcf().set_size_inches(6, 4)
    plt.savefig(filename, bbox_inches='tight')
    print('save training loss plot to %s' % (filename))
    plt.clf()


if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)


    # hyper-parameters
    # you can tune these for your training
    num_epochs = 100
    batch_size = 4
    learning_rate = 1e-4
    num_workers = 2

    # dataset
    dataset_train = CrackerBox('train')  
    train_loader = torch.utils.data.DataLoader(dataset_train, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    epoch_size = len(train_loader)

    # network
    num_classes = 1
    num_boxes = 2
    network = YOLO(num_boxes, num_classes).to(device)
    image_size = network.image_size
    grid_size = network.grid_size
    network.train()

    # Optimizer: Adam
    optimizer = torch.optim.Adam(network.parameters(), lr=learning_rate)
    
    # create output directory
    output_dir = 'checkpoints'
    print('Output will be saved to `{:s}`'.format(output_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # save the losses
    losses = np.zeros((num_epochs, epoch_size), dtype=np.float32)
    # for each epoch
    for epoch in range(num_epochs):

        # for each sample
        for i, sample in enumerate(train_loader):
        
            image = sample['image'].to(device)
            gt_box = sample['gt_box'].to(device)
            gt_mask = sample['gt_mask'].to(device)

            # forward pass
            output, pred_box = network(image)

            # compute loss
            loss = compute_loss(output, pred_box, gt_box, gt_mask, num_boxes, num_classes, grid_size, image_size)

            # optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print('epoch %d/%d, iter %d/%d, lr %.6f, loss %.4f' % (epoch, num_epochs, i, epoch_size, learning_rate, loss))
            losses[epoch, i] = loss

        """
        # save checkpoint for every epoch
        state = network.state_dict()
        filename = 'yolo_epoch_{:d}'.format(epoch+1) + '.checkpoint.pth'
        torch.save(state, os.path.join(output_dir, filename))
        print(filename)
        """
        
        
    # save the final checkpoint
    state = network.state_dict()
    filename = 'yolo_final.checkpoint.pth'
    torch.save(state, os.path.join(output_dir, filename))
    print(filename)

    # plot loss
    plot_losses(losses)
