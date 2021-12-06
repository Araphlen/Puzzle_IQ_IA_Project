from tkinter import *
import numpy as np
from Classe_piece import *
from Classe_GameBoard import *
from initialisation import *

#remet les pieces a leurs position initial 
def reset(list_piece):
    for i in list_piece:
        if not i.bloq:
            i.place_init()


def main():

    nbNiv=int(input("Quel niveau:"))
    #initialisation de la fenetre TKinter
    fen=Tk()
    fen.wm_state(newstate="zoomed")
    canvas= Canvas(fen, width=1520, height=840, bg='white')
    canvas.pack()

    #initialisation du plateau de jeu
    plateau=GameBoard(canvas)

    #initialisation de toutes les pieces du jeu
    list_piece=init_piece(plateau,canvas)

    #liste contenant la description de la position des pieces deja placées sur le plateu en fonction du niveau
    list_niveau=[[],
                [(10,0,0,1,0),(1,2,0,2,0),(2,4,0,2,0),(9,6,0,1,1),(3,7,0,0,1),(8,8,1,2,0)],
                [(3,0,0,1,0),(11,1,0,2,0),(2,2,0,2,0),(8,4,0,0,0),(0,6,2,0,0),(1,0,3,2,0)],
                [(9,0,0,1,1),(0,1,0,2,0),(6,3,0,1,1),(3,6,0,0,1),(10,0,2,3,1),(5,1,2,2,1)]]

    #mise en place de la matrice du jeu enb fonction du niveau choisi 
    init_niveau(plateau,list_piece,list_niveau[nbNiv])

    resetBtn=Button(canvas,text='RESET',command=lambda:resetBtn(list_piece))
    resetBtn.place(x=10,y=10)
    fen.mainloop()
    
    plateau.show_plateau()


if __name__=="__main__":
    main()
