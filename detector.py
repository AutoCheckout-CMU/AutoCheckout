import os
import re
import sys
sys.path.append('.')
import cv2
import math
import time
import scipy
import argparse
import matplotlib
import numpy as np
import pylab as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import OrderedDict
from scipy.ndimage.morphology import generate_binary_structure
from scipy.ndimage.filters import gaussian_filter, maximum_filter

from lib.network.rtpose_vgg import get_model
from evaluate.coco_eval import get_outputs, handle_paf_and_heat
from lib.utils.common import Human, BodyPart, CocoPart, CocoColors, CocoPairsRender, draw_humans
from lib.utils.paf_to_pose import paf_to_pose_cpp
from lib.config import cfg, update_config


parser = argparse.ArgumentParser()
parser.add_argument('--cfg', help='experiment configure file name',
                    default='./experiments/vgg19_368x368_sgd.yaml', type=str)
parser.add_argument('--weight', type=str,
                    default='pose_model.pth')
parser.add_argument('opts',
                    help="Modify config options using the command-line",
                    default=None,
                    nargs=argparse.REMAINDER)
args = parser.parse_args()

# update config file
update_config(cfg, args)

model = get_model('vgg19')     
model.load_state_dict(torch.load(args.weight))
model = torch.nn.DataParallel(model).cuda()
model.float()
model.eval()

def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap='jet')
    plt.colorbar()
    plt.show()

def detect_keypoints(oriImg):
    # Get results of original image
    with torch.no_grad():
        paf, heatmap, im_scale = get_outputs(oriImg, model,  'rtpose')
    
    # heatmap2d(paf[:,:,1])
    print(paf.shape, heatmap.shape, im_scale)
    humans = paf_to_pose_cpp(heatmap, paf, cfg)

    image_h, image_w = oriImg.shape[:2]
    human_keypoints = []
    for human in humans:
        # draw point
        centers = {}
        for i in range(CocoPart.Background.value):
            if i not in human.body_parts.keys():
                continue

            body_part = human.body_parts[i]
            center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
            centers[i] = center
        human_keypoints.append(centers)

    return human_keypoints

def calculate_association():
    """
    Input:
    Output:
    List of Association: [Associated Customer]
    """
    #TODO: Implement association algorithm 
    pass

if __name__ == '__main__':
    test_image = './ski.jpg'
    oriImg = cv2.imread(test_image) # B,G,R order
    human_keypoints = detect_keypoints(oriImg)
    print(human_keypoints)
