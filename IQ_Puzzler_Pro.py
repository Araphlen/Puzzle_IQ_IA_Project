from tkinter import *
import numpy as np

taille=70


class GameBoard:
    def __init__(self):
        for i in range(4,15):
            for j in range(3,8):
                canvas.create_oval(i*taille,j*taille,i*taille+taille,j*taille+taille,tag="plateau")
        self.board=np.zeros((5,11)).astype(int)

    def show_plateau(self):
        for i in self.board:
            for j in i:
                print(j,end='\t')
            print('\n')

class Piece:
    def __init__(self,tab,couleur,tag,x,y,plateau):
        self.tab=tab
        self.couleur=couleur
        self.tag=tag
        self.x=x
        self.y=y

        self.xini=x
        self.yini=y

        self.xOnP=None
        self.yOnP=None
        self.plateau=plateau
        self.placeon=False

        self.bloq=False
        
        self.placer()
        canvas.tag_bind(self.tag,'<B1-Motion>',self.clic)
        canvas.tag_bind(self.tag,'<Button-1>',self.enlever)
        canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.relache)
        canvas.tag_bind(self.tag,'<Button-3>',self.turn)
        canvas.tag_bind(self.tag,'<Button-2>',self.mirror)

    def enlever(self,event):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        if self.placeon:
            for i in range(len(self.tab)):
                for j in range(len(self.tab)):
                    if self.tab[j][i]==1:
                        self.plateau.board[j+self.yOnP-nbl][i+self.xOnP-nbc]=0
            #self.plateau.show_plateau()
            self.placeon=False
            canvas.tag_bind(self.tag,'<Button-3>',self.turn)
            canvas.tag_bind(self.tag,'<Button-2>',self.mirror)
            canvas.itemconfigure(self.tag,width=1)
    
    def placer(self):
        j=self.y
        for n in self.tab:
            i=self.x
            for m in n:
                if m==1:
                    canvas.create_oval(i,j,i+taille,j+taille,fill=self.couleur,tag=self.tag)
                i+=taille
            j+=taille

    def turn(self,event):
        self.turnmat()


    def turnmat(self):
        long=len(self.tab)
        temp=self.tab.copy()
        for i in range(long):
            for j in range(long):
                self.tab[i][j]=temp[j][long-1-i]
        canvas.delete(self.tag)
        self.placer()

    def mirror(self,event):
        self.mirrormat()


    def mirrormat(self):
        long=len(self.tab)
        temp=self.tab.copy()
        for i in range(long):
            for j in range(long):
                self.tab[i][j]=temp[i][long-1-j]
        canvas.delete(self.tag)
        self.placer()
            
    def clic(self,event):
        canvas.tag_raise(self.tag)
        (x3,y3,x4,y4)=canvas.bbox(self.tag)
        canvas.move(self.tag,event.x-(x3+x4)/2,event.y-(y3+y4)/2)
        #canvas.move(self.tag,event.x-canvas.coords(self.tag)[0],event.y-canvas.coords(self.tag)[1])
        #self.x,self.y=canvas.coords(self.tag)[0],canvas.coords(self.tag)[1]
        self.x,self.y=x3,y3


    def relache(self,event):
        (x1,y1,x2,y2)=canvas.bbox("plateau")
        (x3,y3,x4,y4)=canvas.bbox(self.tag)
        #coordonplatex,coordonplatey=(round((x3-canvas.coords("plateau")[0])/taille),round((y3-canvas.coords("plateau")[1])/taille))
        coordonplatex,coordonplatey=(round((x3-x1)/taille),round((y3-y1)/taille))
        if x1<x3+taille/2 and x4-taille/2<x2 and y1<y3+taille/2 and y4-taille/2<y2 and self.verifplace(coordonplatex,coordonplatey):
##            newcoordx=round(canvas.coords(self.tag)[0]/taille)*taille
##            newcoordy=round(canvas.coords(self.tag)[1]/taille)*taille
##
##            canvas.move(self.tag,-canvas.coords(self.tag)[0]+newcoordx,-canvas.coords(self.tag)[1]+newcoordy)

            newcoordx=round(x3/taille)*taille
            newcoordy=round(y3/taille)*taille
            canvas.move(self.tag,newcoordx-x3,newcoordy-y3)
            
            self.Place(coordonplatex,coordonplatey)
            #self.bloquer()
            #self.plateau.show_plateau()
            verif=np.array([[1]*11]*5)
            if (self.plateau.board==verif).all():
                print('c win')
        #self.x,self.y=canvas.coords(self.tag)[0],canvas.coords(self.tag)[1]
        self.x,self.y=x3,y3


    def bloquer(self):
        canvas.tag_unbind(self.tag,'<B1-Motion>')
        canvas.tag_unbind(self.tag,'<B1-ButtonRelease>')
        canvas.tag_unbind(self.tag,'<Button-3>')
        canvas.tag_unbind(self.tag,'<Button-2>')
        canvas.tag_unbind(self.tag,'<Button-1>')
        canvas.itemconfigure(self.tag,outline='#4ff300300',width=3)
        self.bloq=True

    def debloquer(self):
        canvas.tag_bind(self.tag,'<B1-Motion>',self.clic)
        canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.relache)
        canvas.tag_bind(self.tag,'<Button-3>',self.turn)
        canvas.tag_bind(self.tag,'<Button-2>',self.mirror)
        canvas.tag_bind(self.tag,'<Button-1>',self.enlever)
        canvas.itemconfigure(self.tag,outline='black',width=1)
        self.bloq=False

    def newpos(self,nx,ny):
        canvas.move(self.tag,nx-self.x,ny-self.y)
        self.x=canvas.coords(self.tag)[0]
        self.y=canvas.coords(self.tag)[1]

    def placeonplate(self,i,j):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        nx=(i-nbc)*taille+canvas.coords("plateau")[0]
        ny=(j-nbl)*taille+canvas.coords("plateau")[1]
        self.newpos(nx,ny)
        self.Place(i,j)
        

    def verifplace(self,n,m):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if self.tab[j][i]==1:
                    if self.plateau.board[j+m-nbl][i+n-nbc]==1:
                        return False

        return True
                    
    def Place(self,n,m):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if self.tab[j][i]==1:
                    self.plateau.board[j+m-nbl][i+n-nbc]=1

                    
        self.xOnP=n
        self.yOnP=m
        canvas.tag_unbind(self.tag,'<Button-3>')
        canvas.tag_unbind(self.tag,'<Button-2>')
        canvas.itemconfigure(self.tag,width=2)
        self.placeon=True

    def place_init(self):
        self.enlever(None)
        self.newpos(self.xini,self.yini)
        

        
         



def init_piece(plateau):
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
    pos_ini=[(10,10),(300,10),(600,10),(800,10),(1200,10),(10,300),(1200,300),(10,580),(350,580),(600,580),(850,580),(1200,580)]
    couleur=['blue','red','orange','green','purple','yellow','grey','#044','#014','#414','#042','#402']
    pieces_list=[Piece(pieces[i],couleur[i],"f"+str(i),pos_ini[i][0],pos_ini[i][1],plateau) for i in range(12)]
    return pieces_list

def init_niveau(plateau,listepiece,setup):
    for i in setup:
        for j in range(i[3]):
            listepiece[i[0]].turnmat()
        for j in range(i[4]):
            listepiece[i[0]].mirrormat()
        listepiece[i[0]].placeonplate(i[1],i[2])
        listepiece[i[0]].bloquer()


def lignede0(tab):
    nb=0
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[i][j]!=0:
                return nb
        nb+=1
    return nb


def colonnede0(tab):
    nb=0
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[j][i]!=0:
                return nb
        nb+=1
    return nb

def reset(Plateau,List_piece,niv):
    for i in List_piece:
        if not i.bloq:
            i.place_init()


def main():
    global canvas
    fen=Tk()

    fen.wm_state(newstate="zoomed")
    canvas= Canvas(fen, width=1520, height=840, bg='white')
    canvas.pack()

    Plateau=GameBoard()
    List_piece=init_piece(Plateau)
    List_niveau=[Plateau,List_piece,[(Plateau,List_piece,[(10,0,0,1,0),(1,2,0,2,0),(2,4,0,2,0),(9,6,0,1,1),(3,7,0,0,1),(8,8,1,2,0)]),(3,0,0,1,0),(11,1,0,2,0),(2,2,0,2,0),(8,4,0,0,0),(0,6,2,0,0),(1,0,3,2,0)],[Plateau,List_piece,[(9,0,0,1,1),(0,1,0,2,0),(6,3,0,1,1),(3,6,0,0,1),(10,0,2,3,1),(5,1,2,2,1)]]]
    #init_niveau(Plateau,List_piece,[(10,0,0,1,0),(1,2,0,2,0),(2,4,0,2,0),(9,6,0,1,1),(3,7,0,0,1),(8,8,1,2,0)])

    Reset=Button(canvas,text='RESET',command=lambda:reset(Plateau,List_piece,[(3,0,0,1,0),(11,1,0,2,0),(2,2,0,2,0),(8,4,0,0,0),(0,6,2,0,0),(1,0,3,2,0)]))
    Reset.place(x=10,y=10)
    fen.mainloop()
    
    #Plateau.show_plateau()


if __name__=="__main__":
    main()
