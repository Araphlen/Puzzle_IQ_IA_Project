from tkinter import *
import numpy as np
from Classe_piece import *



#initialisation des 12 pieces du jeu
def init_piece(plateau,canvas):
    pieces=[np.array([[1,1,1,0],[0,0,1,1],[0,0,0,0],[0,0,0,0]]),
            np.array([[1,1,1],[0,1,0],[0,0,0]]),
            np.array([[1,0],[1,1]]),
            np.array([[1,1,1,1],[0,1,0,0],[0,0,0,0],[0,0,0,0]]),
            np.array([[1,1,0],[1,1,0],[0,1,0]]),
            np.array([[0,0,1],[1,1,1],[0,1,0]]),
            np.array([[1,1,0],[0,1,0],[0,1,0]]),
            np.array([[1,1,1,1],[1,0,0,0],[0,0,0,0],[0,0,0,0]]),
            np.array([[1,1,1],[1,0,1],[0,0,0]]),
            np.array([[1,1,0],[0,1,1],[0,0,0]]),
            np.array([[1,1,1],[0,0,1],[0,0,1]]),
            np.array([[1,1,0],[0,1,1],[0,0,1]])]
    #position par defaut en pixels de la place des pieces lorsqu'elles ne sont pas dans la gille
    posIni=[(10,10),(300,10),(600,10),(800,10),(1200,10),(10,300),(1200,300),(10,580),(350,580),(600,580),(850,580),(1200,580)]
    #couleurs des 
    couleur=['blue','red','orange','green','purple','yellow','grey','#044','#014','#414','#042','#402']
    #création de la listes des pieces avec leur forme, couleur tag position initiale, plateau et canvas
    pieces_list=[Piece(pieces[i]*(i+1),couleur[i],"f"+str(i),posIni[i][0],posIni[i][1],plateau,canvas) for i in range(12)]
    return pieces_list

#initiation du niveau choisi
def init_niveau(plateau,listepiece,setup):
    for i in setup:
        for j in range(i[3]):
            listepiece[i[0]].turnmat()
        for j in range(i[4]):
            listepiece[i[0]].mirrormat()
        listepiece[i[0]].placeonplate(i[1],i[2])
        listepiece[i[0]].bloquer()
