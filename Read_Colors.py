from cv2 import cv2
from Countours import Countours
import numpy as np


class Read_Colors:

    def __init__(self):
        pass
    
    # Recebe como parametro:
    # length: Int referente ao tamanho do vetor de id de peixes
    # vet: vetor contendo as coordenadas lidas no arquivo 
    # countVet: contador do frame 
    # fishes_ids: vtor contendo as cooredenas calculadas pelo tracker
    # countCol: Contador de colisões até o momento
    # reset: sinalizador para fazer o reset dos ids de acordo com o ground truth apos uma colisão
    # comparison: sinalizador de que o algoritmo está rodando em modo de comparação
    # verCol: Verificador de ocorrência de colisão

    # correct: posições corretas dos peixes
    # wrong: posições incorretas dos peixes
    # frame: O frame em questão
    # colorFishes: Vetor contendo a cor especifica para cada peixe

    def forReadColors(self,length,vet,countVet,fishes_ids,countCol,reset, comparison, verCol,correct,wrong,frame,colorFishes, heatMap, maskColor, maskUnit):
        length = length
        vet  = vet
        countVet = countVet
        fishes_ids = fishes_ids
        countCol = countCol
        reset = reset
        comparison = comparison
        verCol = verCol
        correct = correct 
        wrong = wrong
        frame = frame 
        colorFishes = colorFishes
        maskColor = maskColor
        

        #para cada peixe
        for i in range(int(length)):
                    
            #guarda os valores do algoritmo para este peixe
            algX = fishes_ids[i][0]
            algY = fishes_ids[i][1]

            #guarda os valores do ground truth para este peixe
            if i == 0:
                vetX = int(vet[countVet][0])
                vetY = int(vet[countVet][1])
            else:
                vetX = int(vet[countVet][i*2])
                vetY = int(vet[countVet][i*2+1])
            
            #verCol: se alguma colisão for registrada a comparação já não é mais feita para este frame
            if verCol is True and int(vet[countVet][16]) == 1:
                countCol += 1
                print(" - Houve colisão",end="")
                reset = True
                verCol = False
            #enquanto não ocorrer uma colisão neste frame ele compara a posição de cada peixe de acordo com o algoritmo e de acordo com o ground truth
            if comparison is True:
                #calcula a mediana geometrica a partir do blob no ponto do ground truth
                b,g,r = maskColor[vetY, vetX]
                coords = np.column_stack(np.where(maskColor == [b,g,r]))

                geoM = Countours.geometric_median(Countours, coords)

                vetX = int(geoM[1])
                vetY = int(geoM[0])            

                if verCol is True:
                    if (algX <= vetX + 3 and algX >= vetX - 3) and (algY <= vetY + 3 and algY >= vetY - 3):
                        correct += 1
                    else:
                        wrong += 1   
            if vetX != 1:
                if i == 2:
                    heatMap.AttMap(algX,algY)

                    b,g,r = maskColor[algY, algX]
                    coords = np.column_stack(np.where(maskColor == [b,g,r]))

                    for coord in coords:             
                        maskUnit[coord[0], coord[1]] = frame[coord[0], coord[1]]

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
        return length,vet,countVet,fishes_ids,countCol,reset, comparison, verCol,correct,wrong,frame,colorFishes, heatMap, maskColor, maskUnit