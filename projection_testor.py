# Testing 3D to 2D projection
from pymongo import MongoClient
import numpy as np
import cv2
import base64
from cpsdriver.codec import DocObjectCodec
import io
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

client = MongoClient('mongodb://localhost:27017')

db = client['cps-test-01']

from BookKeeper import BookKeeper
from detector import *

productID = '632565000012'
cameraList = range(1, 9)

BK =BookKeeper()
absolutePos = BK.getProductCoordinates(productID)
print(absolutePos.x, absolutePos.y, absolutePos.z)

product = BK.getProductByID(productID)
print(product.name)

for cameraID in cameraList:
    camera = CAMERA_CALIBRATION["cameras"][str(cameraID)]

    point = camera_projection(absolutePos.x, absolutePos.y, absolutePos.z, camera)

    print(point)

    # for camera_id in range(1, 26):
    i = 1
    for item in BK._frameDB.find({'camera_id':cameraID}):
        print("Found {} item with camera ID: ".format(i), item['camera_id'])
        rgb = DocObjectCodec.decode(doc=item, collection='frame_message')
        imageStream = io.BytesIO(rgb.frame)
        im = Image.open(imageStream)
        origin_x, origin_y = im.size[0]/2, im.size[1]/2
        # imageFile.save("camera_angles/" + str(camera_id), "PNG")
        draw = ImageDraw.Draw(im)
        x, y = origin_x + point[0], origin_y + point[1]
        r = 10
        leftUpPoint = (x-r, y-r)
        rightDownPoint = (x+r, y+r)
        twoPointList = [leftUpPoint, rightDownPoint]
        draw.ellipse(twoPointList, fill=(255,0,0,255))
        plt.imshow(np.asarray(im))
        plt.show()
        
        i += 1
        if i>2:
            break