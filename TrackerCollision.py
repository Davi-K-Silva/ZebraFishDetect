import math

class TrackerCollision:

    def __init__(self):
        pass
    # Função que verifica se houveram colisões e retorna os Ids participantes
    # Recebe:
    # objects_cord: Lista com a posição de todos os peixes no frame atual
    # length_cord: Quantidade de peixes no frame anterior
    # center_points_ant: Dicionário que contêm a posição dos peixes e seus IDs [ID : (x,y)] no frame anterior
    # center_points: Dicionário que contêm a posição dos peixes e seus IDs [ID : (x,y)] no frame atual
    # colisoes: Dicionário contendo as colisões
    def Collision(self,objects_cord,length_cord,center_points_ant,center_points,colisoes):
        colisao = {}#Quantidade de peixes a mais sobre um unico espaço
        if len(objects_cord) < length_cord:
            chavesCol = list(center_points_ant)
            quantElem = length_cord-len(objects_cord)
            count = 0
            for x in center_points:
                try:
                    del(chavesCol[chavesCol.index(x)])
                except ValueError:
                    continue
                
                colisao[x] = 0
                for e in range(1,quantElem+1):
                    if e == 1:
                        if ((center_points[x])[2] - (center_points_ant[x])[2])>e*65:
                            colisao[x] +=  1
                            count += 1
                        else:
                            break
                    else:
                        if ((center_points[x])[2] - (center_points_ant[x])[2])>e*85:
                            colisao[x] +=  1
                        else:
                            break
            for e in chavesCol:
                dist = 1000
                idCol = 0
                for c in colisao:
                    if colisao[c] > 0:
                        x1 = (center_points_ant[c])[0]
                        y1 = (center_points_ant[c])[1]

                        x2 = (center_points_ant[e])[0]
                        y2 = (center_points_ant[e])[1]
                        if math.hypot( x1-x2 , y1-y2) < dist:
                            idCol = c
                            dist = math.hypot( x1-x2 , y1-y2)
                colisao[idCol] -= 1
                if idCol in colisoes.keys():
                    
                    list_col = colisoes[idCol]
                    list_col.append(e)
                    colisoes[idCol] = list_col
                else:
                    colisoes[idCol] = [e]
        colisoesVazias = []    

        for x in colisoes:
            for e in colisoes[x]:
                if e in center_points:               
                    del(colisoes[x][colisoes[x].index(e)])
                    if colisoes[x] == []:
                        colisoesVazias.append(x)
        
        for x in colisoesVazias:
            del(colisoes[x])  

        return colisoes