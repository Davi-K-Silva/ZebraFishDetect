
class Leitura:
    #
    #   Lê o arquivo peixe.txt, separando em um vetor as coordenadas pelo ;
    #
    #   Return: Um vetor contendo as coordenadas dos peixes pelo id em ordem crescente 
    #   e na ultima posição um valor de 0 a 1 para representar a ocorrência de colisões
    #
    def __init__(self):
        self.count = 0
        self.vet_linhas = []
    def leitura(self):
        with open('peixe.txt','r') as arquivo:
            for peixe in arquivo:
                a = peixe.split(";")
                
                while True:
                    try:
                        self.vet_linhas.append([a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],a[14],a[15], a[16]])
                        break
                    
                    except IndexError:
                        print("Erro de Index")
                        break
        return self.vet_linhas


        
