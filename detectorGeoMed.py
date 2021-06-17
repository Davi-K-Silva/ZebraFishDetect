import numpy as np
import random as rng
from cv2 import cv2
from Leitura import Leitura
from tracker import *
from Escrita import Escrita
from OnMouse import OnMouse
from Read_Colors import Read_Colors
from Countours import Countours
from Start import Start
from Filters import Filters
from FrameImplementation import FrameImplementation
from FrameTracker import FrameTracker

start = Start()
filter = Filters()
frameImplementation = FrameImplementation()
frameTracker = FrameTracker()

cap,medianFrame,grayMedianFrame = start.start()

# Variaveis do leitor 
countVet = 0
#Leitura do arquivo e criação do vetor vet contendo todas as coordenadas de peixes
vet = Leitura().leitura()
#Contador de frames
countFrame = 1
#Cor randomica
color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
#Vetor contendo as cores dos peixes
colorFishes = [(10,0,255),(0,255,20),(255,0,30),(255,40,255),(255,255,50),(60,255,255),(120,150,70),(60,70,190)]
numpex = 0
randColors = [0,0,0,0,0,0,0,0,0,0,0]
while (numpex < 10):
    randColors[numpex] = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    numpex = numpex + 1
# Instância do tracker
tracker = GeoMEuclideanDistTracker()
# Instância do verificador de clicks na  tela
onMouse = OnMouse()
# Instância da mediana geometrica

# Instância da delimitação de contornos e aplicação da mediana  geométrica
getCountours = Countours()
# Instância da comparação de arquivo e do tracker e coloração dos peixes
readColors = Read_Colors()

ret = True
countCol = 0
mask = np.zeros(grayMedianFrame.shape, dtype=np.uint8)
maskColor = np.zeros(medianFrame.shape, dtype=np.uint8)
correct = 0
wrong = 0
length = (len(vet[countVet])/2)
reset = False
comparison = True

#Evento de click do mouse
cv2.namedWindow('Detection')
cv2.setMouseCallback('Detection',onMouse.onMouse)

write = Escrita()
while(ret):
  maskColor = np.zeros(medianFrame.shape, dtype=np.uint8)
  ret,frame,gframe,dframe,th,cnts,hierarchy,mask,detections,color,length,vet,countVet,fishes_ids,countCol,reset, comparison, verCol,correct,wrong,frame,colorFishes,countFrame, maskColor = frameTracker.frameTracker(ret,grayMedianFrame,cap,reset, comparison, tracker,length,vet,countVet,getCountours,mask,color,correct,wrong,filter,frameImplementation,countFrame,readColors,countCol,colorFishes, maskColor, randColors)

  #Count for file
  countVet = countVet + 1
  key = cv2.waitKey(0)
  
  if key == 27:
      break

print("Número de colisões: "+ str(countCol)) 
# Release video object
cap.release()

# Destroy all windows
cv2.destroyAllWindows()
