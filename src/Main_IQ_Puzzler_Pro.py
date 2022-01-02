


from tkinter import *
import numpy as np
from Classe_piece import *
from Classe_GameBoard import *
from ia import *
from initialisation import *

#remet les pieces a leurs position initial 
def reset(list_piece):
    for piece in list_piece:
        if not piece.isLock:
            piece.place_init()


def main():

    while True:
        try:
            nbNiv=int(input("Quel niveau:"))
            if nbNiv<4:
                break
            print("Le numéro du niveau doit etre inferieur ou egale a 3")
        except ValueError:
            nbNiv=0
            break
    #initialisation de la fenetre TKinter
    fen=Tk()
    fen.wm_state(newstate="normal")
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



    #mise en place de la matrice du jeu enb fonction du niveau choisi retourne la liste les pieces non placées
    listePiecesDispo = init_niveau(plateau,list_piece,list_niveau[nbNiv])

    resetBtn=Button(canvas,text='RESET',command=lambda:reset(list_piece))
    resetBtn.place(x=10,y=10)


    ##Test pour des matrice avec peu de pieces enlevées
    # testBoard=np.ones((5,11))
    # for i in range(3):
    #     testBoard[0][i]=0
    #     testBoard[i][2]=0
    #
    # for i in range(4):
    #     testBoard[0][i+4]=0
    #     testBoard[1][5]=0
    #
    # for i in range(3):
    #     testBoard[2][4]=0
    #     testBoard[i+1][3]=0
    #
    # listePiecesDispo=[list_piece[10],list_piece[3],list_piece[1]]
    # print(testBoard)


    print(plateau.board)

    #changer plateau.board en testBoard pour faire les tests
    solveBtn = Button(canvas,text='SOLVE',command=lambda:solve(plateau.board,listePiecesDispo))
    solveBtn.place(x=1400,y=10)

    fen.mainloop()

    
    plateau.show_plateau()


if __name__=="__main__":
    main()
