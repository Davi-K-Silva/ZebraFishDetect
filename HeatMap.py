from cv2 import cv2

class HeatMap:

    # Inicializa uma matriz com o tamanho da imagem
    def __init__(self,screenH,screenW):
        self.screenW = screenW
        self.screenH = screenH
        self.matriz = []
        for y in range(screenW):
            linha = []
            for x in range(screenH):
                linha.append([0,240,250])
            self.matriz.append(linha)

    # Atualiza o mapa de calor
    # Deve receber os pontos x,y do peixe em questão
    def AttMap(self,x,y):
        for mx in range(x-5,x+5):
            for my in range(y-5,y+5):
                b,g,r = self.matriz[mx][my]
                if g != 0:
                    g -= 15
                elif r != 0:
                    r -= 15
                
                if g < 0:
                    g = 0

                if r < 0:
                    r = 0
                self.matriz[mx][my] = [b,g,r]
        
    # Mostra o mapa de calor
    def ShowMap(self):
        backGround = cv2.imread("BaseBkg.jpg")

        for x in range(self.screenW):
            for y in range(self.screenH):
                if self.matriz[x][y] != [0,240,250]:
                        backGround[y,x,0] = self.matriz[x][y][0]
                        backGround[y,x,1] = self.matriz[x][y][1]
                        backGround[y,x,2] = self.matriz[x][y][2]
                            
        cv2.imshow('Heat Map', backGround)
        