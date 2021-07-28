import os
import shutil

import numpy as np
import cv2


def extract_frames_from_video(filename='video.mp4', input_path='./uploads', output_path='../openMVG/data/images',
                              type_of_extraction='whole_video', extraction_number=1, interleaved_number=1):
    print('[+] In extract_frames.py, print os.getcwd(): ', os.getcwd())
    vidcap = cv2.VideoCapture(os.path.join(input_path, filename))
    success, image = vidcap.read()
    height, width, channel = image.shape

    cwd = os.getcwd()
    os.chdir(output_path)
    twd = os.getcwd()
    for filename in os.listdir(twd):
      file_path = os.path.join(twd, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

    if type_of_extraction == "whole_video":
      interleaved_number = 1
    elif type_of_extraction == "direct_number":
      interleaved_number = 1

    count = 0
    count2 = 0
    while success:
      # If there are not enough frames, get as many as possible
      if type_of_extraction == "direct_number" and count == extraction_number:
        break
      elif type_of_extraction == "interleaved_number" and count2 == extraction_number:
        break
      if count%interleaved_number != 0: # need to fix
        success, image = vidcap.read()
        count += 1
        continue
      print('[+] Frame: ', count)
      # dsize = (1366, 768)
      # image = cv2.resize(image, dsize)
      cv2.imwrite(os.path.join(twd, "frame%d.jpg" % count), image)   # save frame as JPEG file      
      success,image = vidcap.read()
      
      print('Read a new frame: ', success)
      count += 1
      count2 += 1
    os.chdir(cwd)

    return 1.2*max(height, width)


if __name__ == "__main__":
   extract_frames_from_video('video.mp4', '', './images', 1)

'''
vidcap = cv2.VideoCapture('video.mp4')
success,image = vidcap.read()
count = 0

while success:
  if count%n_interleaving_frames != 0: # need to fix
    success, image = vidcap.read()
    count += 1
    continue
  print('[+] Frame: ', count)
  # dsize = (1366, 768)
  # image = cv2.resize(image, dsize)
  cv2.imwrite(os.path.join('./images', "frame%d.jpg" % count), image)   # save frame as JPEG file      
  success,image = vidcap.read()
  
  print('Read a new frame: ', success)
  count += 1
'''