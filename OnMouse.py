from cv2 import cv2

class OnMouse:
    
    def __init__(self):
        pass

    #
    #   Função de detecção de click do mouse
    #   E impreme na tela o resultado
    #
    def onMouse(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(str(x)+";"+str(y))
            