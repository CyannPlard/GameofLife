"""
Created on Sun Nov 02 17:40:22 2020

@author: Cyann
"""
import tkinter as tk
import numpy as np
import math
import time

#__________creation of the game window__________

fn = tk.Tk()
fn.title("John Conway's Game of Life")
expl=tk.Label(fn, text="Click on the white cells to make them live, and observe their evolution!")
expl.grid(row=0,column=0,columnspan=5)

# __________creation of the game grid__________

w=1000 #width
h=700 #height
p=20 # grid step
grid=tk.Canvas(fn,bg="white",width=w,height=h)
grid.grid(row=1, column=0, columnspan=5)

for i in range (0, w, p):
    grid.create_line((i,0),(i,w)) #columns
    grid.create_line((0,i),(w,i)) #lines

#__________initialisation : cells placement on the grid__________

Xmax=math.floor(w/p) #number of cubes on grid width = size of World matrix
Ymax=math.floor(h/p) #number of cubes on grid height = size of World matrix
World=np.zeros((Ymax,Xmax)) #matrix of initial World
World2=np.zeros((Ymax,Xmax)) #matrix of iteration World

d = {} #dictionary to save the number of grid clicks

def birth(event):
    global d
    global World 
    
    x, y = event.x, event.y #click coordinates
    
    #all clicks in a same cell have x2,y2 coordinates
    x2=(x//p)*p
    y2=(y//p)*p

    if (x2,y2) in d.keys(): #if click another time in the cell
        d[(x2,y2)]+=1
    else: #if click for the first time in a cell
        d[(x2,y2)]=1
    if d[(x2,y2)]%2==0: #if the number of click is even
        grid.create_rectangle(x2, y2, x2+p, y2+p, fill="white")#the cell become white
        World[y//p,x//p]=0
    else: #if the number of click is odd
        grid.create_rectangle(x2, y2, x2+p, y2+p, fill="black")#the cell become black
        World[y//p,x//p]=1 

grid.bind('<Button-1>', birth) 


#__________the game start__________


# Function to use if you want a world like a petri box
"""
def neightboor(M,i,j):
    if M[i,j]==1: #the cell is alive
        nbrV=-1 #to not count the alive cell itself
    if M[i,j]==0: #the cell is dead
        nbrV=0
    for o in range (i-1,i+2):
        for p in range (j-1,j+2):
            if o>=Xmax or p>=Ymax or o<0 or p<0: #if index is out of the matrix
                nbrV=nbrV #nothing happens
            else:
                if M[o,p]==1: #if a neightboor cell is alive
                    nbrV+=1
    return nbrV
"""
#Function to use if you want a world like a tor
# Function created by Valentin Poncet
def neightboor(T,x,y):
    nbrV=0
    jin,kin= [-1,0,1],[-1,0,1]
    global Xmax
    global Ymax
    xmax2=Xmax-1
    ymax2=Ymax-1
    xmin=ymin=0
    if x==xmax2:
        jin=[-1,0,-xmax2]
    if y==ymax2:
        kin=[-1,0,-ymax2]
    if x==xmin:
        jin=[xmax2,0,1]
    if y==ymin:
        kin=[ymax2,0,1]
    for j in jin:
        for k in kin:
            if k==j!=0 or k!=j:
                if T[y+k][x+j]==1:
                    nbrV+=1
    return nbrV

iter=0 #number of iteration

def game():
    #display modification
    global pause
    grid.unbind('<Button-1>')
    pause.grid(row=3,column=0)
    
    global World,World2
    global onoff,iter
    onoff=1 #boolean for iteration   

    while onoff==1:
        iter+=1 
        #calculation of iteration world
        for i in range (Xmax):
            for j in range (Ymax):
                nei=neightboor(World,i,j)
          
                if World[j,i]==1: #if a cell is alive
                    if nei==2 or nei==3:
                        World2[j,i]=1 #the cell stay alive
                    else:
                        World2[j,i]=0 #the cell die
                        grid.create_rectangle(i*p, j*p, i*p+p, j*p+p, fill="white")#the cell become white
                            
                else: #if a cell is dead
                    if nei==3:
                        World2[j,i]=1 #the cell become alive
                        grid.create_rectangle(i*p, j*p, i*p+p, j*p+p, fill="black")#the cell become black
                       
        if  np.array_equiv(World, World2): #if nothing happens between the two worlds
            onoff=0 #stop the iteration
        else:
            #copy of the iteration world in the initial world
            for i in range (Xmax) :
                for j in range (Ymax) :
                    World[j,i]=World2[j,i]

        #time-iteration display
        iteration.configure(text='Temps = {}'.format(iter))
        #iteration speed
        time.sleep(speed)
        #to make the cells visible on the grid
        fn.update()

#__________game pause/reset__________

def pause():
    global onoff
    onoff=0
    pause.grid_forget()

def reset():
    global iter,speed,d
    d={}
    iter=0
    speed=1
    global World,World2
    for i in range (Xmax):
        for j in range (Ymax):
            if World[j,i]==1:
                World[j,i]=0
                World2[j,i]=0
                grid.create_rectangle(i*p, j*p, i*p+p, j*p+p, fill="white")
    grid.bind('<Button-1>', birth)
    
#__________speed variation__________

speed=1
def speedless():
    global speed
    speed=speed*1.25
    
def speedplus():
    global speed
    speed = speed*0.75

#__________display features__________

#boutons du jeu
start=tk.Button(fn, text="Start",command=game) 
pause=tk.Button(fn, text="Pause",command=pause)   
reset=tk.Button(fn, text="Reset", command=reset) 
Exit=tk.Button(fn,text="Exit",command=fn.destroy)
start.grid(row=3,column=0)
reset.grid(row=3,column=2)
Exit.grid(row=3,column=4)

#to manage the speed iteration
speed_canvas=tk.Canvas(fn, width=130, height=21)
speed_canvas.grid(row=2,column=3)

speedm=tk.Button(speed_canvas, text="-", command=speedless)
speedm_window=speed_canvas.create_window(0,15, anchor=tk.W, window=speedm)

speedp=tk.Button(speed_canvas, text="+",command=speedplus)
speedp_window=speed_canvas.create_window(90,15, anchor=tk.W, window=speedp)

speedt=tk.Label(speed_canvas,padx=4,pady=3,text="Speed")
speedt_window=speed_canvas.create_window(40,15, anchor=tk.W, window=speedt)

# game iteration
iteration=tk.Label(fn, text="Time = 0")
iteration.grid(row=2,column=1)

#__________ game start__________
fn.mainloop()
