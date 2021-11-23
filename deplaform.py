from tkinter import *
import numpy as np

taille=70

def init_plateau(canvas):
    for i in range(4,15):
        for j in range(3,8):
            canvas.create_oval(i*taille,j*taille,i*taille+taille,j*taille+taille,tag="plateau")

def init_piece():
    pieces=[np.array([[1,1,1,0],[0,0,1,1],[0,0,0,0],[0,0,0,0]]),
            np.array([[1,1,1],[0,0,1],[0,0,1]]),
            np.array([[1,0],[1,1]]),
            np.array([[1,1,1,1],[0,1,0,0],[0,0,0,0],[0,0,0,0]]),
            np.array([[1,1,0],[1,1,0],[0,1,0]]),
            np.array([[0,0,1],[1,1,1],[0,1,0]]),
            np.array([[1,1,0],[0,1,0],[0,1,0]]),
            np.array([[1,1,1,1],[1,0,0,0],[0,0,0,0],[0,0,0,0]]),
            np.array([[1,1,1],[1,0,1],[0,0,0]]),
            np.array([[1,1,0],[0,1,1],[0,0,0]]),
            np.array([[1,1,1],[0,1,0],[0,0,0]]),
            np.array([[1,1,0],[0,1,1],[0,0,1]])]
    couleur=['blue','red','orange','green','purple','yellow','black','grey','red','blue','green','orange']
    pieces_list=[forme(pieces[i],couleur[i],"f"+str(i),i*100,0) for i in range(12)]
    return pieces_list

class forme:
    def __init__(self,tab,couleur,tag,x,y):
        self.tab=tab
        self.couleur=couleur
        self.tag=tag
        self.x=x
        self.y=y
        
        self.placer()
        canvas.tag_bind(self.tag,'<B1-Motion>',self.clic)
        canvas.tag_bind(self.tag,'<B1-ButtonRelease>',self.relache)
        canvas.tag_bind(self.tag,'<B3-ButtonRelease>',self.turn)
        
        
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
            
    def clic(self,event):
        canvas.move(self.tag,event.x-canvas.coords(self.tag)[0],event.y-canvas.coords(self.tag)[1])
        self.x,self.y=canvas.coords(self.tag)[0],canvas.coords(self.tag)[1]

    def relache(self,event):
        if canvas.coords("plateau")[0]<=canvas.coords(self.tag)[0]<canvas.coords("plateau")[0]+taille*11 and canvas.coords("plateau")[1]<=canvas.coords(self.tag)[1]<canvas.coords("plateau")[1]+taille*11:
            newcoordx=round(canvas.coords(self.tag)[0]/taille)*taille
            newcoordy=round(canvas.coords(self.tag)[1]/taille)*taille
            canvas.move(self.tag,-canvas.coords(self.tag)[0]+newcoordx,-canvas.coords(self.tag)[1]+newcoordy)
        self.x,self.y=canvas.coords(self.tag)[0],canvas.coords(self.tag)[1]        


fen=Tk()

fen.wm_state(newstate="zoomed")
canvas= Canvas(fen, width=1920, height=1080, bg='white')
canvas.pack()

init_plateau(canvas)
init_piece()
  
fen.mainloop()
