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
        block = [point,a,b,c]
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
    
if __name__ == "__main__":
    fig = plt.figure()
    bNumb,bType =defineGeometry('CSV/GeometriaNavio.csv')

    order = csv_read('CSV/Grande Bloco_Meio Navio-PopaProa.csv')
#    order = csv_read('CSV/Camada_Meio Navio-PopaProa.csv')
#    order = csv_read('CSV/Piramide_Meio Navio-PopaProa.csv')
#    order = csv_read('CSV/Grande bloco_Popa-Proa.csv')
#    order = csv_read('CSV/Camada_Popa-Proa.csv')
#    order = csv_read('CSV/Piramide_Popa-Proa.csv')
    
    order = [int(i[0]) for i in order]
    print order
    ani = animation.FuncAnimation(fig, anim,fargs=(fig,bNumb,order,'b'), interval=100)
    plt.show()
    plt.show()
        
