import math
 


class GeoMEuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        
        self.verify_start = True
        
    def update(self, objects_cord):
        # Objects boxes and ids
        objects_bbs_ids = []   
   
        if self.verify_start is True:
            for cord in objects_cord:
                cx = cord[0]
                cy = cord[1]     

                possiv_ids = [1,2,3,4,5,6,7,8,8,8,8,8] #Lista com os possíveis Ids

                # Find out if that object was detected already
                same_object_detected = False
                
                for id, pt in self.center_points.items():
                    dist = math.hypot(cx - pt[0], cy - pt[1])
                    
                    
                    if id in possiv_ids:
                        del(possiv_ids[possiv_ids.index(id)]) # Se um peixe já existir com o Id, então retira da lista de possíveis Ids
                        
                    if dist < 15:
                        self.center_points[id] = (cx, cy)
                        
                        objects_bbs_ids.append([cx, cy, id])
                        same_object_detected = True
                        break

                # New object is detected we assign the ID to that object
                if same_object_detected is False:
                    
                    id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids

                    self.center_points[id_] = (cx, cy)
                    objects_bbs_ids.append([cx, cy, id_])
        
        list_id_D = []
        list_as = []

        possiv_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13] #Lista com os possíveis Ids
        
        if self.verify_start is False:
            # Get center point of new object
            for cord in objects_cord:
                cx = cord[0]
                cy = cord[1]     
                
                
                min_dist = 1000
                id_D = 0
                # Find out if that object was detected already
                same_object_detected = False
                
                for id, pt in self.center_points.items():
                    dist = math.hypot(cx - pt[0], cy - pt[1])

                    if id in possiv_ids:
                        del(possiv_ids[possiv_ids.index(id)]) # Se um peixe já existir com o Id, então retira da lista de possíveis Ids
                    if min_dist > dist:
                        
                        id_D = id
                        min_dist = dist
               
                
                if id_D in list_id_D:
                    same_object_detected = True
                    list_as.append([cx, cy, id_D])
                else:
                    list_id_D.append(id_D)
                    list_as.append([cx, cy, id_D])


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
                        list_as.append([x1,y1,id_rev])
                        self.center_points[id_rev] = (x2, y2)

                        id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids
                        del(possiv_ids[possiv_ids.index(id_)])
                        list_id_D.append(id_)
                        list_as.append([x2,y2,id_])

                    else:  
                        list_as.append([x2,y2,id_rev])
                        
                        id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids
                        del(possiv_ids[possiv_ids.index(id_)])
                        list_id_D.append(id_)
                        list_as.append([x1,y1,id_])
                    
            for x in list_as:
                self.center_points[x[2]] = (x[0],x[1])
                objects_bbs_ids.append([x[0],x[1], x[2]])
                               
        self.verify_start = False

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()

        
        dic = {} #Cria um dicionário
        for x in objects_bbs_ids: #Adiciona um lista no dionário baseado no id presente na lista
            dic[x[2]] = x

        objects_bbs_ids.clear() # Limpa a lista

        for i in range(1,9): #Verifica se há algum id faltando de 1 a 8  e se estiver faltando adiciona uma lista no id faltando
            if i in dic.keys(): 
                continue
            else:
                dic[i] = [1,1,0]

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

