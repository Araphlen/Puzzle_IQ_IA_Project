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

        self.xOnP=None
        self.yOnP=None
        self.plateau=plateau
        self.placeon=False
        
        self.placer()
        canvas.tag_bind(self.tag,'<B1-Motion>',self.clic)
        canvas.tag_bind(self.tag,'<Button-1>',self.enlever)
        canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.relache)
        canvas.tag_bind(self.tag,'<B3-ButtonRelease>',self.turn)
        canvas.tag_bind(self.tag,'<B2-ButtonRelease>',self.mirror)

    def enlever(self,event):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        if self.placeon:
            for i in range(len(self.tab)):
                for j in range(len(self.tab)):
                    if self.tab[j][i]==1:
                        self.plateau.board[j+self.yOnP-nbl][i+self.xOnP-nbc]=0
            #self.plateau.show_plateau()
            self.placeon=False
            canvas.tag_bind(self.tag,'<B3-ButtonRelease>',self.turn)
            canvas.tag_bind(self.tag,'<B2-ButtonRelease>',self.mirror)
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
        long=len(self.tab)
        temp=self.tab.copy()
        for i in range(long):
            for j in range(long):
                self.tab[i][j]=temp[j][long-1-i]
        canvas.delete(self.tag)
        self.placer()

    def mirror(self,event):
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
        self.x,self.y=canvas.coords(self.tag)[0],canvas.coords(self.tag)[1]

    def relache(self,event):
        
        (x1,y1,x2,y2)=canvas.bbox("plateau")
        (x3,y3,x4,y4)=canvas.bbox(self.tag)
        coordonplatex,coordonplatey=(round((x3-canvas.coords("plateau")[0])/taille),round((y3-canvas.coords("plateau")[1])/taille))
        if x1<x3+taille/2 and x4-taille/2<x2 and y1<y3+taille/2 and y4-taille/2<y2 and self.verifplace(coordonplatex,coordonplatey):
            newcoordx=round(canvas.coords(self.tag)[0]/taille)*taille
            newcoordy=round(canvas.coords(self.tag)[1]/taille)*taille

            canvas.move(self.tag,-canvas.coords(self.tag)[0]+newcoordx,-canvas.coords(self.tag)[1]+newcoordy)
            
            self.place(coordonplatex,coordonplatey)
            #self.bloquer()
            #self.plateau.show_plateau()
        self.x,self.y=canvas.coords(self.tag)[0],canvas.coords(self.tag)[1]

    def bloquer(self):
        canvas.tag_unbind(self.tag,'<B1-Motion>')
        canvas.tag_unbind(self.tag,'<B1-ButtonRelease>')
        canvas.tag_unbind(self.tag,'<B3-ButtonRelease>')
        canvas.tag_unbind(self.tag,'<B2-ButtonRelease>')
        canvas.tag_unbind(self.tag,'<Button-1>')
        canvas.itemconfigure(self.tag,outline='#4ff300300',width=3)

    def debloquer(self):
        canvas.tag_bind(self.tag,'<B1-Motion>',self.clic)
        canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.relache)
        canvas.tag_bind(self.tag,'<B3-ButtonRelease>',self.turn)
        canvas.tag_bind(self.tag,'<B2-ButtonRelease>',self.mirror)
        canvas.tag_bind(self.tag,'<Button-1>',self.enlever)
        canvas.itemconfigure(self.tag,outline='black',width=1)

    def newpos(self,nx,ny):
        canvas.move(self.tag,nx-self.x,ny-self.y)
        self.x=canvas.coords(self.tag)[0]
        self.y=canvas.coords(self.tag)[1]

    def placeonplate(self,i,j):

        nx=i*taille+canvas.coords("plateau")[0]
        ny=j*taille+canvas.coords("plateau")[1]
        self.newpos(nx,ny)
        self.place(i,j)

    def verifplace(self,n,m):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if self.tab[j][i]==1:
                    if self.plateau.board[j+m-nbl][i+n-nbc]==1:
                        return False

        return True
                    
    def place(self,n,m):
        nbl,nbc=lignede0(self.tab),colonnede0(self.tab)
        for i in range(len(self.tab)):
            for j in range(len(self.tab)):
                if self.tab[j][i]==1:
                    self.plateau.board[j+m-nbl][i+n-nbc]=1

                    
        self.xOnP=n
        self.yOnP=m
        canvas.tag_unbind(self.tag,'<B3-ButtonRelease>')
        canvas.tag_unbind(self.tag,'<B2-ButtonRelease>')
        canvas.itemconfigure(self.tag,width=2)
        self.placeon=True

        
         



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
    couleur=['blue','red','orange','green','purple','yellow','grey','#000400400','#000100400','#400100400','#000400200','#400000200']
    pieces_list=[Piece(pieces[i],couleur[i],"f"+str(i),pos_ini[i][0],pos_ini[i][1],plateau) for i in range(12)]
    return pieces_list


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


def main():
    global canvas
    fen=Tk()

    fen.wm_state(newstate="zoomed")
    canvas= Canvas(fen, width=1520, height=840, bg='white')
    canvas.pack()

    Plateau=GameBoard()
    List_piece=init_piece(Plateau)
    
    fen.mainloop()
    #Plateau.show_plateau()


if __name__=="__main__":
    main()
