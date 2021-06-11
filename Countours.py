import numpy as np
from cv2 import cv2
from scipy.spatial.distance import cdist, euclidean

class Countours:

    def __init__(self):
        pass
    
    # Recebe como parametro:
    # cnts,hierarchy: vem da função cv2.findCountours
    # mask: Mascara do frame em questão
    # frame: O frame em questão
    # detections: Lista
    # color: (x,y,z) onde x,y,z são valores que representam uma cor
    # 

    def getCountours(self,cnts,mask,frame,detections,color,hierarchy):
        i = -1

        # loop over the contours
        for c in cnts:
            i = i + 1
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 60:
                continue

            cv2.drawContours(mask,[c], -1, (255,255,255),-1)
            coords = np.column_stack(np.where(mask>0))
            geoM = self.geometric_median(coords)

            mask = np.zeros(frame.shape, dtype=np.uint8)
            
            x = int(geoM[1])
            y = int(geoM[0])
            detections.append([x,y,cv2.contourArea(c)])

            cord = "x:" + str(x) + "y:" + str(y)

            cv2.putText(frame, cord, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
            cv2.drawContours(frame, cnts, i, color, 2, cv2.LINE_8, hierarchy, 0)
            
        return cnts,mask,frame,detections,color,hierarchy

            
    #
    # 
    # 
    # 
    # 
    # 
    def geometric_median(self,X):
        y = np.mean(X, 0)
        while True:
            D = cdist(X, [y])
            nonzeros = (D != 0)[:, 0]

            Dinv = 1 / D[nonzeros]
            Dinvs = np.sum(Dinv)
            W = Dinv / Dinvs
            T = np.sum(W * X[nonzeros], 0)

            num_zeros = len(X) - np.sum(nonzeros)
            if num_zeros == 0:
                y1 = T
            elif num_zeros == len(X):
                return y
            else:
                R = (T - y) * Dinvs
                r = np.linalg.norm(R)
                rinv = 0 if r == 0 else num_zeros/r
                y1 = max(0, 1-rinv)*T + min(1, rinv)*y

            if euclidean(y, y1) < 1e-5:
                return y1

            y = y1

    # def geometric_median(X, eps=1e-5):
    #     y = np.mean(X, 0)

    #     while True:
    #         D = cdist(X, [y])
    #         nonzeros = (D != 0)[:, 0]

    #         Dinv = 1 / D[nonzeros]
    #         Dinvs = np.sum(Dinv)
    #         W = Dinv / Dinvs
    #         T = np.sum(W * X[nonzeros], 0)

    #         num_zeros = len(X) - np.sum(nonzeros)
    #         if num_zeros == 0:
    #             y1 = T
    #         elif num_zeros == len(X):
    #             return y
    #         else:
    #             R = (T - y) * Dinvs
    #             r = np.linalg.norm(R)
    #             rinv = 0 if r == 0 else num_zeros/r
    #             y1 = max(0, 1-rinv)*T + min(1, rinv)*y

    #         if euclidean(y, y1) < eps:
    #             return y1

    #         y = y1
    