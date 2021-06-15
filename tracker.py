from TrackerCollision import TrackerCollision
from TrackerStart import TrackerStart
from TrackerLater import TrackerLater
from TrackerCollision import TrackerCollision
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
        self.start = TrackerStart()
        self.later = TrackerLater()
        self.collision = TrackerCollision()
        
        
    def update(self, objects_cord):
        # Objects boxes and ids
        objects_bbs_ids = []   
        self.center_points_ant = self.center_points.copy()
        possiv_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13] #Lista com os possíveis Ids
   
        if self.verify_start is True: #Primeiro Frame, instância as posições dos peixes
            objects_cord,possiv_ids,self.length_cord,objects_bbs_ids,self.center_points = self.start.start(objects_cord,possiv_ids,objects_bbs_ids,self.center_points)

        if self.verify_start is False:
            objects_cord,possiv_ids,self.center_points,objects_bbs_ids = self.later.Later(objects_cord,possiv_ids,self.center_points,objects_bbs_ids)
                    
        
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

        self.colisoes = self.collision.Collision(objects_cord,self.length_cord,self.center_points_ant,self.center_points,self.colisoes)

        print(self.colisoes)

        # O dicionário self.colisoes contem o centro da colisão que é representada pelo id e como valores um lista com os ids que  se perderam dentro da colisão.
        # {IdDaColisão:[IdPerdido,IdPerdido]}

        # O peixe 8 e 2 se colidiram, o id 2 sumiu e a aglomeração de peixes recebeu o id 8. Logo seria {8:[2]} e se mais peixes tivessem sobre
        # o id 8 ficaria {8:[2,5]} e se ocorresse mais de uma colisão ficaria {8:[2,5],7:[1]}

        # self.colisoes          => Dicionário com o id das colisões e ids perdidos
        # self.center_points     => Dicionário com os {id : [x,y,áreaDePixel]} do frame atual
        # self.center_points_ant => Dicionário com os {id : [x,y,áreaDePixel]} do frame anterior

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

