import math
from operator import itemgetter

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []    
        
        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2      
            cy = (y + y + h) // 2      

            possiv_ids = [1,2,3,4,5,6,7,8,9,10,11]

            # Find out if that object was detected already
            same_object_detected = False
            
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                
                if id in possiv_ids:
                    del(possiv_ids[possiv_ids.index(id)])
                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                
                id_ = possiv_ids[0]

                self.center_points[id_] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, id_])
                

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()

        dic = {}
        for x in objects_bbs_ids:
            dic[x[4]] = x

        objects_bbs_ids.clear()

        for i in range(1,9):
            if i in dic.keys():
                continue
            else:
                dic[i] = [1,1,1,1,0]

        for key in sorted(dic.keys()) :
            objects_bbs_ids.append(dic[key])

        lista = []
        count = 0
        for x in objects_bbs_ids:
            if count <= 7:
                lista.append(x)
                count += 1
            else:
                break

        return lista



