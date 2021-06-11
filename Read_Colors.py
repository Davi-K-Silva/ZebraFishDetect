from cv2 import cv2

class Read_Colors:

    def __init__(self):
        pass
    
    # Recebe como parametro:
    # length: Int referente ao tamanho do vetor de id de peixes
    # vet: vetor contendo as coordenadas lidas no arquivo 
    # countVet: contador do frame 
    # fishes_ids: vtor contendo as cooredenas calculadas pelo tracker
    # countCol: Contador de colisões até o momento
    # reset: 
    # verCol: Verificador de ocorrência de colisão

    # correct:
    # wrong:
    # frame: O frame em questão
    # colorFishes: Vetor contendo a cor especifica para cada peixe

    def forReadColors(self,length,vet,countVet,fishes_ids,countCol,reset,verCol,correct,wrong,frame,colorFishes):
        length = length
        vet  = vet
        countVet = countVet
        fishes_ids = fishes_ids
        countCol = countCol
        reset = reset
        verCol = verCol
        correct = correct 
        wrong = wrong
        frame = frame 
        colorFishes = colorFishes
        
        for i in range(int(length)):
    
            if i == 0:
                vetX = int(vet[countVet][0])
                vetY = int(vet[countVet][1])
            else:
                vetX = int(vet[countVet][i*2])
                vetY = int(vet[countVet][i*2+1])
                
            algX = fishes_ids[i][0]
            algY = fishes_ids[i][1]
            
            if verCol is True and int(vet[countVet][16]) == 1:
                countCol += 1
                print(" - Houve colisão",end="")
                reset = True
                verCol = False
            if verCol is True:
                if (algX <= vetX + 3 and algX >= vetX - 3) and (algY <= vetY + 3 and algY >= vetY - 3):
                    correct += 1
                else:
                    wrong += 1   
            if vetX != 1:
                cv2.circle(frame,(algX,algY),5,colorFishes[i], -1)    
            
            #ColorFishes
            #Vermelho   ID = 1 
            #Verde      ID = 2
            #Azul       ID = 3
            #Roxo       ID = 4
            #Azul claro ID = 5
            #Amarelo    ID = 6
            #Ciano      ID = 7
            #Marrom     ID = 8  
        return length,vet,countVet,fishes_ids,countCol,reset,verCol,correct,wrong,frame,colorFishes