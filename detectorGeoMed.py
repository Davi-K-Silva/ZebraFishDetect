import numpy as np
from cv2 import cv2
from skimage import data, filters
from tracker import  EuclideanDistTracker, GeoMTracker
from scipy.spatial.distance import cdist, euclidean

def geometric_median(X, eps=1e-5):
    y = np.mean(X, 0)

    while True:
        D = cdist(X, [y])
        nonzeros = (D != 0)[:, 0]

        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)

        num_zeros = len(X) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*T + min(1, rinv)*y

        if euclidean(y, y1) < eps:
            return y1

        y = y1

#
Colors = [[255,0,0],[0,255,0],[0,0,255],
          [255,255,0],[255,0,255],[0,255,255],
          [128,0,255],[0,128,255],[255,0,128],
          [255,128,0]]

# Open Video
cap = cv2.VideoCapture('Video1.avi')

#Create tracker object
Gtracker = GeoMTracker()

medianFrame = cv2.imread("BaseBkg.jpg")    

# Display median frame
cv2.imshow('frame', medianFrame)
cv2.waitKey(0)
cv2.imwrite("BaseBkg.jpg", medianFrame)
# Reset frame number to 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Convert background to grayscale
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)
# Loop over all frames
ret = True
hasbeenrun = False
mask = np.zeros(grayMedianFrame.shape, dtype=np.uint8)

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

  
  # Perform the distance transform algorithm
  dist = cv2.distanceTransform(dframe, cv2.DIST_L2, 3)
  # Normalize the distance image for range = {0.0, 1.0}
  # so we can visualize and threshold it
  cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
 
  
  contours, _ = cv2.findContours(dframe, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  detections = []

  for cnt in contours:
      area = cv2.contourArea(cnt)
      if area > 70:
        cv2.drawContours(frame,[cnt], -1, (0,255,50),2)
        cv2.drawContours(mask,[cnt], -1, (255,255,255),-1)
        coords = np.column_stack(np.where(mask>0))
        geoM = geometric_median(coords)
        
        mask = np.zeros(frame.shape, dtype=np.uint8)
        
        detections.append([int(geoM[1]),int(geoM[0])])

  if not hasbeenrun:
    Gtracker.start(detections)
    hasbeenrun = True

  fishes_ids = Gtracker.update(detections)
  
  for fish_id in fishes_ids:
    cx,cy,id_ = fish_id
    cv2.putText(frame, "id: "+ str(id_), (cx,cy -15), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    print(str(cx)+","+str(cy),end=";")
     
   
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
