# Testing 3D to 2D projection
from pymongo import MongoClient
import numpy as np
import cv2
import base64
from cpsdriver.codec import DocObjectCodec
import io
from PIL import Image, ImageDraw

client = MongoClient('mongodb://localhost:27017')

db = client['cps-test-01']

import BookKeeper as BK
from detector import *

productID = '071142008582'
absolutePos = BK.getProductAbsolutePos(productID)
print(absolutePos.x, absolutePos.y, absolutePos.z)

camera = CAMERA_CALIBRATION["cameras"]["1"]

point = camera_projection(absolutePos.x, absolutePos.y, absolutePos.z, camera)

print(point)

frame_message = db['frame_message']

# for camera_id in range(1, 26):
i = 0
for item in frame_message.find({'camera_id': 6}):
    print("Found {} item with camera ID: ".format(i), item['camera_id'])
    rgb = DocObjectCodec.decode(doc=item, collection='frame_message')
    imageStream = io.BytesIO(rgb.frame)
    im = Image.open(imageStream)
    # imageFile.save("camera_angles/" + str(camera_id), "PNG")
    draw = ImageDraw.Draw(im)
    draw.point(point)
    im.show()
    i += 1
    break
