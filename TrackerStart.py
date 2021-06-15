class TrackerStart:

    def __init__(self):
        pass
    
    #Função que instância a primeira posição dos peixes no frame inicial
    #Recebe:
    #objects_cord: Lista com a posição de todos os peixes
    #possiv_ids: Lista contendo os possíveis IDs que um peixe pode ter
    #objects_bbs_ids: Lista auxiliar que vai conter o [x, y, id, área peixes]
    #center_points: Dicionário que vai conter a posição dos peixes e seus IDs [ID : (x,y)]
    def start(self,objects_cord,possiv_ids,objects_bbs_ids,center_points):
        for cord in objects_cord:
            cx,cy,ap = cord

            id_ = possiv_ids[0] #Adiciona o Id que está em primeiro na lista de possíveis Ids
            del(possiv_ids[possiv_ids.index(id_)])

            center_points[id_] = [cx, cy, ap]
            objects_bbs_ids.append([cx, cy, id_, ap])
        length_cord = len(objects_cord)

        return objects_cord,possiv_ids,length_cord,objects_bbs_ids,center_points