#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
# print (torch.cuda.current_device())
# print (torch.cuda.device(torch.cuda.current_device()))
print (torch.cuda.get_device_name(torch.cuda.current_device()))


# In[2]:


# from google.colab import drive
# # drive.flush_and_unmount()
# drive.mount('/content/drive',force_remount=True)


# In[3]:


# install dependencies: (use cu100 because colab is on CUDA 10.0)
# !pip install -U torch==1.4+cu100 torchvision==0.5+cu100 -f https://download.pytorch.org/whl/torch_stable.html 
# !pip install cython pyyaml==5.1
# !pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
import torch, torchvision
print ('torch',torch.__version__)
print ('torchvision',torchvision.__version__)
# get_ipython().system('gcc --version')
# opencv is pre-installed on colab


# 

# In[4]:


# !git clone https://github.com/facebookresearch/detectron2
# !git clone https://github.com/tangsanli5201/DeepPCB


# In[5]:


# !pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu100/index.html

# Mengmeng: cu100 means cuda v10.0? If have problem please install from source:
# https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md


# In[6]:


# You may need to restart your runtime prior to this, to let your installation take effect
# Some basic setup
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import cv2
import random
import os
#from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog


# In[7]:


import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from matplotlib.pyplot import imshow
from PIL import Image
import IPython
def cv2_imshow(img):
    img = img[:,:,[2,1,0]]
    img = Image.fromarray(img)
    plt.figure(figsize=(20, 20))
    plt.imshow(img)
    plt.axis('off')
    plt.show()


# In[10]:


from detectron2.data.datasets import register_coco_instances
from detectron2.data import DatasetCatalog
image_root_path = 'data/classifier/combined-4452'
metadata_json_path = 'data/classifier/combined-4452/metadata_coco_format.json'
detectron_output_dir = "data/classifier/output"

DatasetCatalog._REGISTERED.clear()
MetadataCatalog._NAME_TO_META.clear()
register_coco_instances("my_dataset", {}, metadata_json_path, image_root_path)


# In[11]:


#check dataset
my_metadata = MetadataCatalog.get("my_dataset")
print(type(my_metadata))
my_dataset = DatasetCatalog.get('my_dataset')
for item in my_dataset:
  print (item)
  break
    
# TODO: Category ids in annotations are not in [1, #categories]! We'll apply a mapping for you.


# In[12]:


from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg

cfg = get_cfg()
cfg.OUTPUT_DIR = detectron_output_dir
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("my_dataset",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 0
cfg.MODEL.WEIGHTS = "detectron2://COCO-Detection/faster_rcnn_R_50_FPN_3x/137849458/model_final_280758.pkl"  # Let training initialize from model zoo
cfg.SOLVER.CHECKPOINT_PERIOD = 2000 # checkpoint every 20min
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.02  # pick a good LR
cfg.SOLVER.MAX_ITER = 60000    # 300 iterations seems good enough for this toy dataset; you may need to train longer for a practical dataset
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512   # faster, and good enough for this toy dataset (default: 512)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 18 

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
trainer = DefaultTrainer(cfg) 
trainer.resume_or_load(resume=True)
trainer.train()


