class Escrita:

    #
    # Recebe um vetor contendo as coordenada dos peixes em ordem crescente de Id
    # Após isso, escreve no arquivo peixe.txt o conteúdo do vetor
    #

    def __init__(self):
        pass
    def write(self,fishes_ids):
        for fish_id in fishes_ids:
            x,y,id_ = fish_id
            with open("peixe.txt",'a') as arquivo:                       
                arquivo.write(str(x)+";"+str(y)+";")
   
        with open("peixe.txt",'a') as arquivo:                        
            arquivo.write("\n") 