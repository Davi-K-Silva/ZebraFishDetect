import math
import numpy as np
import random as rng
from cv2 import cv2
from skimage import data, filters
from Leitura import Leitura
from tracker import *
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

def onMouse(event, x, y, flags, param):# Função de detecção de click do mouse
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here (etc...)
       print(str(x)+";"+str(y))

color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))

# Open Video
cap = cv2.VideoCapture('video1.mp4')


#Create tracker object
tracker = GeoMEuclideanDistTracker()

# Set median frame
medianFrame = cv2.imread('BaseBkg.jpg')

# Display median frame
cv2.imshow('Median Background Frame', medianFrame)
cv2.waitKey(0)

# Reset frame number to 0
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Convert background to grayscale
grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

# Variaveis do leitor 
countVet = 0
vet = Leitura().leitura()


#Evento de click do mouse
cv2.namedWindow('Detection')
cv2.setMouseCallback('Detection',onMouse)

countFrame = 1
# Loop over all frames
ret = True
countCol = 0
mask = np.zeros(grayMedianFrame.shape, dtype=np.uint8)
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

  detections = []
  
  
  # loop over the contours
  for c in cnts:
    i = i + 1
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < 60:
      continue

    cv2.drawContours(mask,[c], -1, (255,255,255),-1)
    coords = np.column_stack(np.where(mask>0))
    geoM = geometric_median(coords)

    mask = np.zeros(frame.shape, dtype=np.uint8)
        
    x = int(geoM[1])
    y = int(geoM[0])
    detections.append([x,y,cv2.contourArea(c)])

    cord = "x:" + str(x) + "y:" + str(y)


    cv2.putText(frame, cord, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
    cv2.drawContours(frame, cnts, i, color, 2, cv2.LINE_8, hierarchy, 0)
  print(countFrame,end=" ") 
  
  fishes_ids = tracker.update(detections) 
  
  """ for fish_id in fishes_ids:
    x,y,id_ = fish_id
     
    with open("peixe.txt",'a') as arquivo:                       
            arquivo.write(str(x)+";"+str(y)+";")
   
  with open("peixe.txt",'a') as arquivo:                        
            arquivo.write("\n") """


  countFrame = countFrame + 1
  
  """ length = len(vet[countVet])/2
  
  verCol = True
  for i in range(int(length)):
    if i == 0:
      vetX = int(vet[countVet][0])
      vetY = int(vet[countVet][1])
    else:
      vetX = int(vet[countVet][i*2])
      vetY = int(vet[countVet][i*2+1])

    if verCol is True and vetX == 1:
      countCol += 1
      print(" - Houve colisão",end="")
      verCol = False
    

    if i == 0:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(0,0,255), -1)   # Vermelho  ID = 1
    elif i == 1:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(0,255,0), -1)   # Verde     ID = 2
    elif i == 2:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(255,0,0), -1)   #Azul       ID = 3
    elif i == 3:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(255,0,255), -1) #Roxo       ID = 4
    elif i == 4:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(255,255,0), -1) #Azul claro ID = 5
    elif i == 5:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(0,255,255), -1) #Amarelo    ID = 6
    elif i == 6:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(120,150,0), -1) #Ciano      ID = 7
    elif i == 7:
      if vetX != 1:
        cv2.circle(frame,(vetX,vetY),5,(60,70,190), -1) #Marrom     ID = 8 """
 
  print("")

  # Display image
  cv2.imshow('Background Subtraction', dframe)
  cv2.imshow('Detection', frame)

  #Count for file
  countVet = countVet + 1

  key = cv2.waitKey(0)
  
  if key == 27:
      break

print("Número de colisões: "+ str(countCol)) # 20 = 172 frames 501 / 16 = 223 frame 502 / 23 = 213 frames 503 / 18 = 259 frames 501 / 19 = 228 502 frames / 21 = 185 frame 504 / 19.5 = 234 frame 504
# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
