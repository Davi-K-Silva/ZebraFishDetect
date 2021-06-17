from HeatMap import HeatMap
from cv2 import cv2

class FrameTracker:

    def __init__(self):
        pass

    def frameTracker(self,ret,grayMedianFrame,cap,reset, comparison, tracker,length,vet,countVet,getCountours,mask,color,correct,wrong,filter,FrameImplementation,countFrame,readColors,countCol,colorFishes, heatMap, maskColor, randColors, maskUnit):
        ret,frame,gframe,dframe,th,cnts,hierarchy,cnts,mask,frame,detections,color,hierarchy,reset,comparison, maskColor = FrameImplementation.implementation(ret,grayMedianFrame,cap,reset, comparison, tracker,length,vet,countVet,getCountours,mask,color,filter, maskColor, colorFishes, heatMap, randColors)
        print("Acertos: " + str(correct))
        print("Erros: " + str(wrong))
        print(countFrame,end=" ") 
        
        fishes_ids = tracker.update(detections) 
        
        #Escreve as posições dos peixes no arquivo de texto
        #write.write(fishes_ids) 


        countFrame = countFrame + 1
        verCol = True
        length,vet,countVet,fishes_ids,countCol,reset,comparison,verCol,correct,wrong,frame,colorFishes, heatMap, maskColor, maskUnit = readColors.forReadColors(length,vet,countVet,fishes_ids,countCol,reset,comparison, verCol,correct,wrong,frame,colorFishes, heatMap, maskColor, maskUnit)

        print("")

        # Display image
        cv2.imshow('Background Subtraction', dframe)
        cv2.imshow('Detection', frame)
        cv2.imshow('Individual', maskUnit)

        return ret,frame,gframe,dframe,th,cnts,hierarchy,mask,detections,color,length,vet,countVet,fishes_ids,countCol,reset, comparison, verCol,correct,wrong,frame,colorFishes,countFrame, heatMap, maskColor