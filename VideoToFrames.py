import cv2
import os
vidcap = cv2.VideoCapture('data/cps-test-videos/192.168.1.100_2020-01-28_22-24-06.mp4')
output_directory = 'data/cps-test-videos/192.168.1.100_2020-01-28_22-24-06'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(output_directory + "/frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1