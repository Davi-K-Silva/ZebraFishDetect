class FrameImplementation:

    def __init__(self):
        pass

    def implementation(self,ret,grayMedianFrame,cap,reset, comparison, tracker,length,vet,countVet,getCountours,mask,color,filter, maskColor, colorFishes, heatMap, randColors):
        ret,frame,gframe,dframe,th,cnts,hierarchy = filter.filters(ret,grayMedianFrame,cap)
        
        i = -1

        detections = []
        #para resetar, reinicia o tracker e o fornece com os ids de acordo com o ground truth
        if reset == True and comparison == True:
            tracker.__init__()
            for i in range(int(length)):
                if i == 0:
                    vetX = int(vet[countVet][0])
                    vetY = int(vet[countVet][1])
                else:
                    vetX = int(vet[countVet][i*2])
                    vetY = int(vet[countVet][i*2+1])

                detections.append([vetX, vetY, 0])
                reset = False
        else:
            cnts,mask,frame,detections,color,hierarchy, maskColor = getCountours.getCountours(cnts,mask,frame,detections,color,hierarchy, maskColor, colorFishes, randColors)

        return ret,frame,gframe,dframe,th,cnts,hierarchy,cnts,mask,frame,detections,color,hierarchy,reset, comparison, maskColor