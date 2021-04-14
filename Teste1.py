import numpy as np
import cv2
from skimage import data, filters
from tracker import *

# Open Video
cap = cv2.VideoCapture('Video 1.avi')

#Create tracker object
tracker = EuclideanDistTracker()

# Randomly select 25 frames
frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)

# Store selected frames in an array
frames = []
for fid in frameIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    frames.append(frame)

# Calculate the median along the time axis
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)    

# Display median frame
cv2.imshow('frame', medianFrame)
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
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # Calculate absolute difference of current frame and 
  # the median frame
  dframe = cv2.absdiff(frame, grayMedianFrame)
  # Treshold to binarize
  th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)

  contours, _ = cv2.findContours(dframe, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  detections = []
  for cnt in contours:
      area = cv2.contourArea(cnt)
      if area > 70:
        cv2.drawContours(frame,[cnt], -1, (0,255,50),2)
        x,y,w,h = cv2.boundingRect(cnt)

        detections.append([x,y,w,h])

  fishes_ids = tracker.update(detections)

  for fish_id in fishes_ids:
    x,y,w,h,id_ = fish_id
    cv2.putText(frame, "id: "+ str(id_), (x,y -15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    print(str(x)+","+str(y),end=";")

    
  # Display image
  cv2.imshow('frame', dframe)
  cv2.imshow("Frame" , frame)

  print("")

  key = cv2.waitKey(0)

  if key == 27:
      break

# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
