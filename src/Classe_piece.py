from tkinter import *
import numpy as np

taille=70
#classe 
class Piece:
    #constructeur de la classe piece
    def __init__(self,tab,shapeNb,couleur,tag,x,y,plateau,canvas):
        ## attribut liées a la matrice
        #forme de la piece
        self.tab=tab
        self.shapeNb=shapeNb
        self.variants = self.createVariants(tab,shapeNb)

        ##Attributs liées a l'affichage
        self.couleur=couleur
        self.tag=tag

        #place courante de la piece 
        self.x=x
        self.y=y

        #place initiale hors plateau de la piece
        self.xIni=x
        self.yIni=y

        #attribut en relation avec le plateau
        self.xOnP=None
        self.yOnP=None
        self.plateau=plateau
        self.isPlaced=False
        self.isLock=False
        self.canvas=canvas


        self.placer()


        #association d'actions a des evenement sur les pieces 
        self.canvas.tag_bind(self.tag,'<B1-Motion>',self.drag)
        self.canvas.tag_bind(self.tag,'<Button-1>',self.enlever)
        self.canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.drop)
        self.canvas.tag_bind(self.tag,'<Button-3>',self.turn)
        self.canvas.tag_bind(self.tag,'<Button-2>',self.mirror)

    #fonction qui crée l'ensemble des variantes d'une piece
    def createVariants(cls, tab,shapeNb):
        #change la valeur de 1 a shapeNb pour pouvoir observer les changement dans la résolution de l'ia
        tab=tab*shapeNb
        variants = []
        # pour la piece et la piece inversée
        for piece in [tab, np.fliplr(tab)]:
            # pour les 4 rotation
            for k in range(4):
                candidate = np.rot90(piece, k)
                for existing in variants:
                    if np.array_equal(existing, candidate):
                        break #n'ajoute pas la variante si elle est deja presente dans le tableau
                else:
                    variants.append(candidate)
        return variants


    def enlever(self,event):
        nbL,nbC=lignede0(self.tab),colonnede0(self.tab)
        if self.isPlaced:
            for i in range(len(self.tab)):
                for j in range(len(self.tab)):
                    if self.tab[j][i]==1:
                        self.plateau.board[j+self.yOnP-nbL][i+self.xOnP-nbC]=0
            self.isPlaced=False
            self.canvas.tag_bind(self.tag,'<Button-3>',self.turn)
            self.canvas.tag_bind(self.tag,'<Button-2>',self.mirror)
            self.canvas.itemconfigure(self.tag,width=1)
    
    def placer(self):#i et j correler a ligne colonnes ?
        j=self.y
        for n in self.tab:
            i=self.x
            for m in n:
                if m==1:
                    self.canvas.create_oval(i,j,i+taille,j+taille,fill=self.couleur,tag=self.tag)
                i+=taille
            j+=taille

    #fonction qui tourne la matrice dans le canevas
    def turn(self,event):
        self.turnmat()

    
    def turnmat(self):
        long=len(self.tab)
        temp=self.tab.copy()
        for i in range(long):
            for j in range(long):
                self.tab[i][j]=temp[j][long-1-i]
        self.canvas.delete(self.tag)
        self.placer()

    #fonction qui inverse la piece dans le canevas
    def mirror(self,event):
        self.mirrormat()


    def mirrormat(self):
        long=len(self.tab)
        temp=self.tab.copy()
        for i in range(long):
            for j in range(long):
                self.tab[i][j]=temp[i][long-1-j]
        self.canvas.delete(self.tag)
        self.placer()
            
    #fonction qui permet de selectionner une piece pour la bouger dans la fenetre 
    def drag(self,event):
        self.canvas.tag_raise(self.tag)
        (x3,y3,x4,y4)=self.canvas.bbox(self.tag)
        self.canvas.move(self.tag,event.x-(x3+x4)/2,event.y-(y3+y4)/2)
        self.x,self.y=x3,y3


    #fonction qui permet de relacher la piece sur le plateau de jeu si la position de relachement du click est valide 
    def drop(self,event):
        (x1,y1,x2,y2)=self.canvas.bbox("plateau")
        (x3,y3,x4,y4)=self.canvas.bbox(self.tag)
        coordOnPlateX,coordOnPlateY=(round((x3-x1)/taille),round((y3-y1)/taille))
        if x1<x3+taille/2 and x4-taille/2<x2 and y1<y3+taille/2 and y4-taille/2<y2 and self.verifplace(coordOnPlateX,coordOnPlateY):
            newCoordX=round(x3/taille)*taille
            newCoordY=round(y3/taille)*taille
            self.canvas.move(self.tag,newCoordX-x3,newCoordY-y3)
            self.Place(coordOnPlateX,coordOnPlateY)
            verif=np.array([[1]*11]*5)
            if (self.plateau.board==verif).all():
                print('c win')
        self.x,self.y=x3,y3


    def bloquer(self):
        #supprime touis les evenement disponible  sur la piece bloquée
        self.canvas.tag_unbind(self.tag,'<B1-Motion>')
        self.canvas.tag_unbind(self.tag,'<B1-ButtonRelease>')
        self.canvas.tag_unbind(self.tag,'<Button-3>')
        self.canvas.tag_unbind(self.tag,'<Button-2>')
        self.canvas.tag_unbind(self.tag,'<Button-1>')
        #met une bordure différente pour que la piece soit reconnaisable 
        self.canvas.itemconfigure(self.tag,outline='#4ff300300',width=3)
        self.isLock=True

    def debloquer(self):
        #attribu les action sur les pieces  
        self.canvas.tag_bind(self.tag,'<B1-Motion>',self.drag)
        self.canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.drop)
        self.canvas.tag_bind(self.tag,'<Button-3>',self.turn)
        self.canvas.tag_bind(self.tag,'<Button-2>',self.mirror)
        self.canvas.tag_bind(self.tag,'<Button-1>',self.enlever)
        self.canvas.itemconfigure(self.tag,outline='black',width=1)
        self.isLock=False

    def newpos(self,nx,ny):
        self.canvas.move(self.tag,nx-self.x,ny-self.y)
        (x3,y3,x4,y4)=self.canvas.bbox(self.tag)
        self.x=x3
        self.y=y3

    def placeonplate(self,i,j):
        nbL,nbC=lignede0(self.tab),colonnede0(self.tab)
        nx=(i-nbC)*taille+self.canvas.coords("plateau")[0]
        ny=(j-nbL)*taille+self.canvas.coords("plateau")[1]
        self.newpos(nx,ny)
        self.Place(i,j)
        

    def verifplace(self,n,m):
        nbL,nbC=lignede0(self.tab),colonnede0(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if self.tab[j][i]==1:
                    if self.plateau.board[j+m-nbL][i+n-nbC]==1:
                        return False

        return True
                    
    def Place(self,n,m):
        nbL,nbC=lignede0(self.tab),colonnede0(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if self.tab[j][i]==1:
                    self.plateau.board[j+m-nbL][i+n-nbC]=1

                    
        self.xOnP=n
        self.yOnP=m
        self.canvas.tag_unbind(self.tag,'<Button-3>')
        self.canvas.tag_unbind(self.tag,'<Button-2>')
        self.canvas.itemconfigure(self.tag,width=2)
        self.isPlaced=True

    def place_init(self):
        self.enlever(None)
        self.newpos(self.xIni,self.yIni)
        self.newpos(self.xIni,self.yIni)
        

#compte le nombre des premieres lignes de la matrice la piece composés uniquement de 0
def lignede0(tab):
    nb=0
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[i][j]!=0:
                return nb
        nb+=1
    return nb

#compte le nombre des premieres colonnes de la matrice la piece composés uniquement de 0
def colonnede0(tab):
    nb=0
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[j][i]!=0:
                return nb
        nb+=1
    return nb