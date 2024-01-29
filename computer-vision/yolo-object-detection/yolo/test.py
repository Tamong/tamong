"""
CS 4391 Homework 5 Programming
Run this script for YOLO testing
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
from voc_eval import voc_eval


# from the network prediction, extract the bounding boxes with confidences larger than threshold
# pred_box: (batch_size, num_boxes * 5 + num_classes, 7, 7), predicted bounding boxes from the network (see the forward() function)
def extract_detections(pred_box, threshold, num_boxes):

    # extract boxes
    boxes_all = np.zeros((0, 5), dtype=np.float32)
    for i in range(num_boxes):
        confidence = pred_box[0, 5*i+4].detach().numpy()
        y, x = np.where(confidence > threshold)
        boxes = pred_box[0, 5*i:5*i+5, y, x].detach().numpy().transpose()        
        boxes_all = np.concatenate((boxes_all, boxes), axis=0)

    # convert to (x1, y1, x2, y2)
    boxes = boxes_all.copy()
    boxes[:, 0] = boxes_all[:, 0] - boxes_all[:, 2] * 0.5
    boxes[:, 2] = boxes_all[:, 0] + boxes_all[:, 2] * 0.5
    boxes[:, 1] = boxes_all[:, 1] - boxes_all[:, 3] * 0.5
    boxes[:, 3] = boxes_all[:, 1] + boxes_all[:, 3] * 0.5
    return boxes


# visualize the detections
def visualize(image, gt, detections):
    
    im = image[0].permute(1, 2, 0).numpy()
    pixel_mean = np.array([[[102.9801, 115.9465, 122.7717]]], dtype=np.float32)

    # show ground truth
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    im = im * 255.0 + pixel_mean
    im = im.astype(np.uint8)
    plt.imshow(im[:, :, (2, 1, 0)])
    rect = patches.Rectangle((gt[0, 0], gt[0, 1]), gt[0, 2]-gt[0, 0], gt[0, 3]-gt[0, 1], linewidth=2, edgecolor='g', facecolor="none")
    ax.add_patch(rect) 
    plt.title('ground truth')   
    
    # show detection
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(im[:, :, (2, 1, 0)])
    plt.title('prediction')
    for i in range(detections.shape[0]):   
        x1 = detections[i, 0]
        x2 = detections[i, 2]
        y1 = detections[i, 1]
        y2 = detections[i, 3]
        score = detections[i, 4]
        rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=2, edgecolor='g', facecolor="none")
        ax.add_patch(rect)
        plt.plot((x1+x2)/2, (y1+y2)/2, 'ro')
        ax.text(x1, y1, '%.2f' % score, color = 'y')
    plt.show()


# main function for testing
if __name__ == '__main__':

    # dataset
    dataset = CrackerBox('val')  
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=True, num_workers=0)
    epoch_size = len(data_loader)

    # network
    num_classes = 1
    num_boxes = 2
    network = YOLO(num_boxes, num_classes)
    image_size = network.image_size
    grid_size = network.grid_size

    # load checkpoint
    output_dir = 'checkpoints'
    filename = 'yolo_final.checkpoint.pth'
    filename = os.path.join(output_dir, filename)
    network.load_state_dict(torch.load(filename))
    network.eval()
    
    # detection threshold
    threshold = 0.1

    # main test loop
    results_gt = []
    results_pred = []
    for i, sample in enumerate(data_loader):
        
        image = sample['image']
        gt_box = sample['gt_box']
        gt_mask = sample['gt_mask']

        # forward pass
        output, pred_box = network(image)
        
        # convert gt box
        gt_box = sample['gt_box'][0].numpy()
        gt_mask = sample['gt_mask'][0].numpy()
        y, x = np.where(gt_mask == 1)
        cx = gt_box[0, y, x] * dataset.yolo_grid_size + x * dataset.yolo_grid_size
        cy = gt_box[1, y, x] * dataset.yolo_grid_size + y * dataset.yolo_grid_size
        w = gt_box[2, y, x] * dataset.yolo_image_size
        h = gt_box[3, y, x] * dataset.yolo_image_size
        x1 = cx - w * 0.5
        x2 = cx + w * 0.5
        y1 = cy - h * 0.5
        y2 = cy + h * 0.5        
        gt = np.array([x1, y1, x2, y2]).reshape((1, 4))
        results_gt.append(gt)
        
        # extract predictions
        detections = extract_detections(pred_box, threshold, num_boxes)
        results_pred.append(detections)
        print('image %d/%d, %d objects detected' % (i+1, epoch_size, detections.shape[0]))

        # visualization, uncomment the follow line to see the detection results
        # visualize(image, gt, detections)
        
    # evaluation
    rec, prec, ap = voc_eval(results_gt, results_pred)
    print('Detection AP', ap)
    
    # save the PR curve
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(rec, prec)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('AP: %.2f' % ap)
    plt.gcf().set_size_inches(6, 4)
    plt.savefig('test_ap.pdf', bbox_inches='tight')
    plt.clf()
