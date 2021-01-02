"""
Created on Sun Dec 24 17:40:22 2020

@author: cyann
"""
import tkinter as tk
import numpy as np
import math
import time

#__________création de la fenêtre de jeu__________

fn = tk.Tk()
fn.title("John Conway's Game of Life")

# __________creation de la grille de jeu__________

w=1000 #width
h=700 #height
p=20 # pas de la grille
grille=tk.Canvas(fn,bg="white",width=w,height=h)
grille.grid(row=1, column=0, columnspan=5)

for i in range (0, w, p):
    grille.create_line((i,0),(i,w)) #colonnes
    grille.create_line((0,i),(w,i)) #lignes

#__________initialisation : placer les cellules sur la grille__________

Xmax=math.floor(w/p) #nbr cubes dans longueur grille = taille matrice monde
Ymax=math.floor(h/p) #nbr cubes dans hauteur grille = taille matrice monde
Monde=np.zeros((Xmax,Ymax)) #tableau du Monde initial
Monde2=np.zeros((Xmax,Ymax)) #tableau calculé

d = {} #dictionnaire pour enregistrer le nombre de clics initiaux

def naissance(event):
    global d
    global Monde 
    
    x, y = event.x, event.y #clic coordinates
    
    #tous les clics dans la même case ont le même x2,y2
    x2=(x//p)*p
    y2=(y//p)*p

    if (x2,y2) in d.keys(): #si on reclique dans la même case
        d[(x2,y2)]+=1
    else: #si on clique pour la première fois dans la case
        d[(x2,y2)]=1
    if d[(x2,y2)]%2==0:
        grille.create_rectangle(x2, y2, x2+p, y2+p, fill="white")#la case redevient blanche
        Monde[y//p,x//p]=0
    else:
        grille.create_rectangle(x2, y2, x2+p, y2+p, fill="black")#la case devient noire
        Monde[y//p,x//p]=1 

grille.bind('<Button-1>', naissance) 


#__________le jeu démarre__________

def vois1(M,i,j):
    if M[i,j]==1: #la cellule est vivante
        nbrV=-1 #pour ne pas compter la cellule vivante elle-même
    if M[i,j]==0: #la cellule est non vivante
        nbrV=0
    for o in range (i-1,i+2):
        for p in range (j-1,j+2):
            if o>=Xmax or p>=Ymax or o<0 or p<0: #si l'index sort du tableau
                nbrV=nbrV #n'affecte pas le nombre de voisins
            else:
                if M[o,p]==1:
                    nbrV+=1
    return nbrV

ite=0 #nbr iteration

def game():
    #modification affichage
    global pause
    grille.unbind('<Button-1>')
    pause.grid(row=3,column=0)
    
    global Monde,Monde2
    global onoff,ite
    onoff=1 #booléen pour l'itération    

    while onoff==1:
        ite+=1 
        #calcul du monde initial dans le monde suivant
        for i in range (Xmax):
            for j in range (Ymax):
                if Monde[i,j]==1: #traitement d'une cellule vivante
                    if vois1(Monde,i,j)==2 or vois1(Monde,i,j)==3:
                        Monde2[i,j]=1 #la cellule reste vivante
                    else:
                        Monde2[i,j]=0 #la cellule meurt
                        grille.create_rectangle(j*p, i*p, j*p+p, i*p+p, fill="white")#la case devient blanche
                            
                else: #traitement d'une cellule non vivante
                    if vois1(Monde,i,j)==3:
                        Monde2[i,j]=1 #la cellule nait
                        grille.create_rectangle(j*p, i*p, j*p+p, i*p+p, fill="black")#la case devient noire

        if  np.array_equiv(Monde, Monde2):
            onoff=0 #break le while
        else:
            #Copie du monde créé vers le monde initial:
            for i in range (Xmax) :
                for j in range (Ymax) :
                    Monde[i,j]=Monde2[i,j]

        #affichage itération-temps:
        iteration.configure(text='Temps = {}'.format(ite))
        #gérer la vitesse d'itération
        time.sleep(speed)
        #affichage visible des carrés:
        fn.update()

#__________pause/arret du jeu__________

def pause():
    global onoff
    onoff=0
    
    pause.grid_forget()

def stop():
    global ite,speed,d
    d={}
    ite=0
    speed=1
    global Monde,Monde2
    for i in range (Xmax):
        for j in range (Ymax):
            if Monde[i,j]==1:
                Monde[i,j]=0
                Monde2[i,j]=0
                grille.create_rectangle(j*p, i*p, j*p+p, i*p+p, fill="white")
    grille.bind('<Button-1>', naissance)
    
#__________variation vitesse du jeu__________

speed=1
def speedless():
    global speed
    speed=speed+0.25
    
def speedplus():
    global speed
    speed=speed-0.25

#__________éléments graphiques de jeu__________

#boutons du jeu
start=tk.Button(fn, text="Start ",command=game) #lance les itérations du jeu
pause=tk.Button(fn, text="Pause",command=pause) #pause dans l'itération du jeu 
stop=tk.Button(fn, text="Stop", command=stop) #stop and restart le jeu
leave=tk.Button(fn,text="Quitter",command=fn.destroy) #quitte le jeu
start.grid(row=3,column=0)
stop.grid(row=3,column=2)
leave.grid(row=3,column=4)
#pause sera grid dans la fonction game, et ungrid dans la fonction pause

#régler la vitesse d'itération
speed_canvas=tk.Canvas(fn, width=130, height=21)
speed_canvas.grid(row=2,column=3)

speedm=tk.Button(speed_canvas, text="-", command=speedless)
speedm.configure(bg="white")
speedm_window=speed_canvas.create_window(0,15, anchor=tk.W, window=speedm)

speedp=tk.Button(speed_canvas, text="+",command=speedplus)
speedp.configure( bg="white")
speedp_window=speed_canvas.create_window(90,15, anchor=tk.W, window=speedp)

speedt=tk.Label(speed_canvas,padx=4,pady=3,text="Speed")
speedt_window=speed_canvas.create_window(40,15, anchor=tk.W, window=speedt)

# Itérations du jeu
iteration=tk.Label(fn, text="Time = 0") #donne le numéro d'itération
expl=tk.Label(fn, text="Click on the white cases to make them live, and observe their evolution!")

iteration.grid(row=2,column=1)
expl.grid(row=0,column=0,columnspan=4)


#__________ Lancement du jeu__________
fn.mainloop()
