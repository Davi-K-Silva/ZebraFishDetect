import math
 


class GeoMEuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        print("init")
        self.center_points = {}
        self.center_points_ant = {}
        self.verify_start = True
        self.length_cord = 0
        self.colisoes = {}
        
        
    def update(self, objects_cord):
        # Objects boxes and ids
        objects_bbs_ids = []   
        self.center_points_ant = self.center_points.copy()
        
        possiv_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13] #Lista com os possíveis Ids
   
        
        if self.verify_start is True: #Primeiro Frame, instância as posições dos peixes
            for cord in objects_cord:
                cx,cy,ap = cord
   
                id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids
                del(possiv_ids[possiv_ids.index(id_)])

                self.center_points[id_] = [cx, cy, ap]
                objects_bbs_ids.append([cx, cy, id_, ap])
            self.length_cord = len(objects_cord)
        
        list_id_D = []
        list_as = []

        
        if self.verify_start is False:
            # Get center point of new object
            for cord in objects_cord:
                cx,cy,ap = cord   
                 
                min_dist = 1000
                id_D = 0
                # Find out if that object was detected already
                same_object_detected = False
                
                for id, pt in self.center_points.items():
                    dist = math.hypot(cx - pt[0], cy - pt[1])

                    
                    if min_dist > dist:
                        
                        id_D = id
                        min_dist = dist
                    
                if id_D in possiv_ids:
                        del(possiv_ids[possiv_ids.index(id_D)]) # Se um peixe já existir com o Id, então retira da lista de possíveis Ids
                
                if id_D in list_id_D:
                    
                    same_object_detected = True
                    list_as.append([cx, cy, id_D,ap])       
                else: 
                    list_id_D.append(id_D)
                    list_as.append([cx, cy, id_D,ap])


                list_same_id = []
                x_y = []
                id_rev = 0

             # New object is detected we assign the ID to that object
                if same_object_detected is True:
                    
                    for x in list_as:
                        
                        if x[2] in list_same_id:
                            x_y.append(x)
                            for y in list_as:
                                if x_y[0][2] == y[2]:
                                    x_y.append(y)
                                    id_rev = y[2]
                                    del(list_as[list_as.index(x)])
                                    del(list_as[list_as.index(y)])
                                    break
                        else:
                           list_same_id.append(x[2])
                    
                    xs = self.center_points[x_y[0][2]]

                    x1 = x_y[0][0]
                    y1 = x_y[0][1]

                    x2 = x_y[1][0]
                    y2 = x_y[1][1]

                    dist1 = math.hypot(xs[0] - x1, xs[1]-y1)
                    dist2 = math.hypot(xs[0] - x2, xs[1]-y2)

                    if dist1 < dist2:
                        list_as.append([x1,y1,id_rev,ap])
                        self.center_points[id_rev] = [x2, y2, ap]

                        id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids
                        del(possiv_ids[possiv_ids.index(id_)])
                        list_id_D.append(id_)
                        list_as.append([x2,y2,id_,ap])

                    else:  
                        list_as.append([x2,y2,id_rev,ap])
                        
                        id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids
                        del(possiv_ids[possiv_ids.index(id_)])
                        list_id_D.append(id_)
                        list_as.append([x1,y1,id_,ap])
                    
            for x in list_as:
                self.center_points[x[2]] = (x[0],x[1],x[3])
                objects_bbs_ids.append([x[0],x[1], x[2], x[3]])
        
        self.verify_start = False

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, object_id, _ = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()

        #-------------------------------------
        #   VERIFICAÇÃO DE COLISÃO
        #-----------------------------------
        colisao = {}#Quantidade de peixes a mais sobre um unico espaço

        if len(objects_cord) < self.length_cord:
            chavesCol = list(self.center_points_ant)
            quantElem = self.length_cord-len(objects_cord)
            count = 0
            for x in self.center_points:
                try:
                    del(chavesCol[chavesCol.index(x)])
                except ValueError:
                    continue
                
                colisao[x] = 0
                for e in range(1,quantElem+1):
                    if e == 1:
                        if ((self.center_points[x])[2] - (self.center_points_ant[x])[2])>e*65:
                            colisao[x] +=  1
                            count += 1
                        else:
                            break
                    else:
                        if ((self.center_points[x])[2] - (self.center_points_ant[x])[2])>e*85:
                            colisao[x] +=  1
                        else:
                            break
            for e in chavesCol:
                print(colisao)
                dist = 1000
                idCol = 0
                for c in colisao:
                    if colisao[c] > 0:
                        x1 = (self.center_points_ant[c])[0]
                        y1 = (self.center_points_ant[c])[1]

                        x2 = (self.center_points_ant[e])[0]
                        y2 = (self.center_points_ant[e])[1]
                        if math.hypot( x1-x2 , y1-y2) < dist:
                            idCol = c
                            dist = math.hypot( x1-x2 , y1-y2)
                colisao[idCol] -= 1
                if idCol in self.colisoes.keys():
                    
                    list_col = self.colisoes[idCol]
                    list_col.append(e)
                    self.colisoes[idCol] = list_col
                else:
                    self.colisoes[idCol] = [e]
        colisoesVazias = []    
   
        for x in self.colisoes:
            for e in self.colisoes[x]:
                if e in self.center_points:                   
                    del(self.colisoes[x][self.colisoes[x].index(e)])
                    if self.colisoes[x] == []:
                        colisoesVazias.append(x)
                       
        for x in colisoesVazias:
            del(self.colisoes[x])  

        print(self.colisoes)

        """ O dicionário self.colisoes contem o centro da colisão que é representada pelo id e como valores um lista com os ids que  se perderam dentro da colisão.
        {IdDaColisão:[IdPerdido,IdPerdido]}

        O peixe 8 e 2 se colidiram, o id 2 sumiu e a aglomeração de peixes recebeu o id 8. Logo seria {8:[2]} e se mais peixes tivessem sobre
        o id 8 ficaria {8:[2,5]} e se ocorresse mais de uma colisão ficaria {8:[2,5],7:[1]}

        self.colisoes          => Dicionário com o id das colisões e ids perdidos
        self.center_points     => Dicionário com os {id : [x,y,áreaDePixel]} do frame atual
        self.center_points_ant => Dicionário com os {id : [x,y,áreaDePixel]} do frame anterior"""

        #------------------+++++++++++++------------#
        dic = {} #Cria um dicionário
        for x in objects_bbs_ids: #Adiciona um lista no dionário baseado no id presente na lista
            dic[x[2]] = [x[0],x[1],x[2]]

        objects_bbs_ids.clear() # Limpa a lista

        for i in range(1,9): #Verifica se há algum id faltando de 1 a 8  e se estiver faltando adiciona uma lista no id faltando
            if i in dic.keys(): 
                continue
            else:
                dic[i] = [1,1,-i]

        for key in sorted(dic.keys()) : # Ordena o dionário baseado nos ids adionando-os em uma lista
            objects_bbs_ids.append(dic[key])

        lista = []
        count = 0
        for x in objects_bbs_ids: # Separa os 8 primeiros elementos da lista e cria uma nova
            if count <= 7:
                lista.append(x)
                count += 1
            else:
                break
        
        return lista

