# -*- coding: utf-8 -*-

import os
import math
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
import matplotlib.animation as animation

def csv_read(name):	#Metodo de leitura, transforma um arquivo CSV em  um vetor 

    CSV=open(name,'r')
    dados=CSV.read()
    dados=dados.replace(',','.')
    dados=dados.replace(';',',')
    CSV.close()
    
    CSV=open("temp.csv",'w')
    CSV.write(dados)
    CSV.close()
    
    CSV=open("temp.csv",'r')
    dados=csv.reader(CSV)
    v=[]
    for i in dados:
        I=[]    
        for j in i:
            try:
                j = float(j)
            except:
                pass
            I.append(j)
        v.append(I)
    CSV.close()
    os.remove("temp.csv")
    return (v)

def createBlock(ax,block,clr):
    point = block[0]
    a = block[1]
    b = block[2]
    c = block[3]
    for s, e in combinations(np.array(list(product([0,a],[0,b],[0,c]))), 2):
        s=s+point
        e=e+point
        alfa = round(a, 5)
        beta = round(b, 5)
        gama = round(c, 5)
        delt = round(np.linalg.norm(np.abs(s-e)),5)
        if delt in [alfa,beta,gama]:
            ax.plot3D(*zip(s,e), color=clr)

def defineGeometry(name):

    vect = csv_read(name)
    blockNumber ={}
    blockType   ={}
    for i in vect:
        a = i[1]
        b = i[2]
        c = i[3]
        point = [i[4],i[5],i[6]]
        block = [point,a,b,c,i[-1]]
        try:
            blockNumber[i[0]] = block
            blockType[i[-1]]  = [block]+blockType[i[-1]]
        except:
            blockType[i[-1]]  = [block]
        
    return blockNumber,blockType

def Ship3Dplot(fig,blocksList,color):

    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")
    
    for block in blocksList:
        createBlock(ax,block,color)
    
    # Create cubic bounding box to simulate equal aspect ratio #
    Xb = 0.5*250*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 125
    Yb = 0.5*200*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0
    Zb = 0.5*200*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 20    
    for xb, yb, zb in zip(Xb, Yb, Zb):
       ax.plot([xb], [yb], [zb], 'w')
    fig.tight_layout(pad=0.5)

def anim(i,fig,bNumb,order,color):
    try:
        Ship3Dplot(fig, [bNumb[order[i]]],color)
    except:
        pass

def changes(chromo,bNumb):
    t = None
    count = 0
    for x in chromo:
        b = bNumb[x]
        new_t = b[-1]
        print new_t
        if new_t != t:
            count+=1
        t = new_t
    print count
    
if __name__ == "__main__":
    fig = plt.figure()
    bNumb,bType =defineGeometry('GeometriaNavio.csv')

    order = csv_read('Ordens/Grande Bloco_Meio Navio-PopaProa.csv')
##    order = csv_read('Ordens/Camada_Meio Navio-PopaProa.csv')
##    order = csv_read('Ordens/Piramide_Meio Navio-PopaProa.csv')
##    order =[52, 50, 54, 48, 56, 58, 51, 46, 45, 57, 47, 60, 55, 43, 59, 61, 49, 44, 41, 39, 37, 63, 68, 64, 53, 62, 40, 35, 67, 42, 33, 38, 34, 36, 69, 66, 19, 20, 21, 23, 22, 25, 26, 24, 27, 28, 9, 65, 10, 70, 18, 29, 30, 17, 8, 11, 12, 7, 31, 32, 6, 5, 4, 3, 13, 14, 2, 15, 16, 1]
##    order =[49, 51, 53, 55, 47, 54, 50, 45, 46, 57, 48, 52, 43, 41, 44, 39, 37,
##       56, 38, 59, 36, 34, 68, 33, 67, 40, 25, 26, 61, 24, 23, 42, 22, 21,
##       35, 60,  5,  6, 58, 66, 62,  7,  8, 19, 20, 65, 64, 27, 28, 69, 63,
##        9, 10, 29, 30,  4,  3, 17, 18, 11, 12, 70, 13, 14, 32, 31,  2,  1,
##       15, 16]
    order =[int(i[0]) for i in order]
    order = [53, 54, 55, 56, 51, 52, 50, 49, 47, 48, 46, 45, 43, 44, 42, 41, 68, 27, 28, 40, 38, 39, 37, 57, 58, 59, 60, 69, 35, 33, 36, 34, 67, 62, 61, 63, 64, 12, 11, 25, 26, 24, 23, 30, 29, 66, 10, 9, 21, 22, 19, 20, 70, 13, 14, 31, 32, 65, 8, 7, 17, 18, 6, 5, 15, 16, 4, 3, 2, 1]
    
    print order
    print
    print changes(order,bNumb)
    ani = animation.FuncAnimation(fig, anim,fargs=(fig,bNumb,order,'b'), interval=200)
    plt.show()
        
