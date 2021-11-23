from tkinter import *

taille=70

def init_plateau(canvas):
    for i in range(4,15):
        for j in range(3,8):
            canvas.create_oval(i*taille,j*taille,i*taille+taille,j*taille+taille,tag="plateau")

fen=Tk()

fen.wm_state(newstate="zoomed")
canvas= Canvas(fen, width=1920, height=1080, bg='white')
canvas.pack()

##class forme:
##    def __init__(self,tab,

init_plateau(canvas)
tab=[[1,1,1,0,0],[0,0,1,1,0],[0,0,0,0,0]]
tab2=[[1,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]
tab3=[[1,1,0,0,0],[0,1,1,0,0],[0,0,1,0,0]]

tabform=[tab,tab2,tab3]
tagform=["f1","f2","f3"]
coulform=['red','blue','green']

for h in range(3):
    j=100*h
    for n in tabform[h]:
        i=100
        for m in n:
            if m==1:
                canvas.create_oval(i,j,i+taille,j+taille,fill=coulform[h],tag=tagform[h])
            i+=taille
        j+=taille

def clic(event,idf):
    canvas.move(idf,event.x-canvas.coords(idf)[0],event.y-canvas.coords(idf)[1])

def relache(event,idf):
    if canvas.coords("plateau")[0]<=canvas.coords(idf)[0]<canvas.coords("plateau")[0]+taille*11 and canvas.coords("plateau")[1]<=canvas.coords(idf)[1]<canvas.coords("plateau")[1]+taille*11:
        newcoordx=round(canvas.coords(idf)[0]/taille)*taille
        newcoordy=round(canvas.coords(idf)[1]/taille)*taille
        canvas.move(idf,-canvas.coords(idf)[0]+newcoordx,-canvas.coords(idf)[1]+newcoordy)



canvas.tag_bind("f1",'<B1-Motion>',lambda event:clic(event,"f1"))
canvas.tag_bind("f1",'<B1-ButtonRelease>',lambda event:relache(event,"f1"))
canvas.tag_bind("f2",'<B1-Motion>',lambda event:clic(event,"f2"))
canvas.tag_bind("f2",'<B1-ButtonRelease>',lambda event:relache(event,"f2"))
canvas.tag_bind("f3",'<B1-Motion>',lambda event:clic(event,"f3"))
canvas.tag_bind("f3",'<B1-ButtonRelease>',lambda event:relache(event,"f3"))

fen.mainloop()
