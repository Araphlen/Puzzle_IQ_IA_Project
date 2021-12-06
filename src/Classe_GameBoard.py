from tkinter import *
import numpy as np

taille=70

#classe du plateau de jeu 
class GameBoard:
    
    
    def __init__(self,canvas):
        for i in range(4,15):
            for j in range(3,8):
                canvas.create_oval(i*taille,j*taille,i*taille+taille,j*taille+taille,tag="plateau")
        self.board=np.zeros((5,11)).astype(int)

    #Afficher le plateau dans la fenetre 
    def show_plateau(self):
        for i in self.board:
            for j in i:
                print(j,end='\t')
            print('\n')