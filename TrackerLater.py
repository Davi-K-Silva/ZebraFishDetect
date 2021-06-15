import math

class TrackerLater:

    def __init__(self):
        pass
    #Função que atualiza o ID dos peixes baseado na sua proximidade em relação aos peixes do frame anterior
    #Recebe:
    #objects_cord: Lista com a posição de todos os peixes no frame atual
    #possiv_ids: Lista contendo os possíveis IDs que um peixe pode ter
    #objects_bbs_ids: Lista auxiliar que vai conter o [x, y, id, área peixe]
    #center_points: Dicionário que contêm a posição dos peixes e seus IDs [ID : (x,y)] no frame Q - 1
    def Later(self,objects_cord,possiv_ids,center_points,objects_bbs_ids):
        list_id_D = []
        list_as = []
        # Get center point of new object
        for cord in objects_cord:
            cx,cy,ap = cord   
                
            min_dist = 1000
            id_D = 0
            # Find out if that object was detected already
            same_object_detected = False
            
            for id, pt in center_points.items():
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
                
                xs = center_points[x_y[0][2]]

                x1 = x_y[0][0]
                y1 = x_y[0][1]

                x2 = x_y[1][0]
                y2 = x_y[1][1]

                dist1 = math.hypot(xs[0] - x1, xs[1]-y1)
                dist2 = math.hypot(xs[0] - x2, xs[1]-y2)

                if dist1 < dist2:
                    list_as.append([x1,y1,id_rev,ap])
                    center_points[id_rev] = [x2, y2, ap]

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
                center_points[x[2]] = (x[0],x[1],x[3])
                objects_bbs_ids.append([x[0],x[1], x[2], x[3]])

        return objects_cord,possiv_ids,center_points,objects_bbs_ids