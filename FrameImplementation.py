class FrameImplementation:

    def __init__(self):
        pass

    def implementation(self,ret,grayMedianFrame,cap,reset,tracker,length,vet,countVet,getCountours,mask,color,correct,wrong,filter):
        print("Acertos: " + str(correct))
        print("Erros: " + str(wrong))

        ret,frame,gframe,dframe,th,cnts,hierarchy = filter.filters(ret,grayMedianFrame,cap)
        
        i = -1

        detections = []
        
        if reset == True:
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
            print("AAA")
        else:
            print("BBB")
            cnts,mask,frame,detections,color,hierarchy = getCountours.getCountours(cnts,mask,frame,detections,color,hierarchy)

        return ret,frame,gframe,dframe,th,cnts,hierarchy,cnts,mask,frame,detections,color,hierarchy,reset