import numpy as np
import random as rng
from cv2 import cv2
from skimage import data, filters


color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))

# Open Video
cap = cv2.VideoCapture('video1.avi')

# Set median frame
medianFrame = cv2.imread('BaseBkg.jpg')

# Display median frame
cv2.imshow('Median Background Frame', medianFrame)
cv2.waitKey(0)

# Reset frame number to 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Convert background to grayscale
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

# Loop over all frames
ret = True
while(ret):

  # Read frame
  ret, frame = cap.read()
  # Convert current frame to grayscale
  gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # Calculate absolute difference of current frame and 
  # the median frame
  dframe = cv2.absdiff(gframe, grayMedianFrame)
  # Treshold to binarize
  th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
  # th = cv2.dilate(th, None, iterations=2)
  cnts,hierarchy = cv2.findContours(dframe, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
  i = -1
  # loop over the contours
  for c in cnts:
    i = i + 1
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < 25:
      continue

    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
    (x, y, w, h) = cv2.boundingRect(c)
    cord = "x:" + str(x + w/2) + "y:" + str(y + h/2)
    cv2.putText(frame, cord, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    cv2.drawContours(frame, cnts, i, color, 2, cv2.LINE_8, hierarchy, 0)
    
  # Display image
  cv2.imshow('Background Subtraction', dframe)
  cv2.imshow('Detection', frame)
  cv2.waitKey(20)

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
