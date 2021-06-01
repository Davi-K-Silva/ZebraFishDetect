class Escrita:

    def __init__(self):
        pass
    def write(self,fishes_ids):
        for fish_id in fishes_ids:
            x,y,id_ = fish_id
            with open("peixe.txt",'a') as arquivo:                       
                arquivo.write(str(x)+";"+str(y)+";")
   
        with open("peixe.txt",'a') as arquivo:                        
            arquivo.write("\n") 