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
    bNumb,bType =defineGeometry('GeometriaNavio.csv')

#    order = csv_read('Grande Bloco_Meio Navio-PopaProa.csv')
#    order = csv_read('Camada_Meio Navio-PopaProa.csv')
#    order = csv_read('Piramide_Meio Navio-PopaProa.csv')
#    order = csv_read('Grande bloco_Popa-Proa.csv')
#    order = csv_read('Camada_Popa-Proa.csv')
#    order = csv_read('Piramide_Popa-Proa.csv')
    order =[57.0, 55.0, 56.0, 54.0, 58.0, 53.0, 40.0, 51.0, 52.0, 39.0, 41.0, 59.0, 43.0, 61.0, 60.0, 63.0, 38.0, 36.0, 45.0, 47.0, 42.0, 46.0, 44.0, 49.0, 50.0, 37.0, 35.0, 48.0, 62.0, 66.0, 34.0, 33.0, 67.0, 68.0, 22.0, 21.0, 6.0, 5.0, 64.0, 19.0, 24.0, 23.0, 25.0, 7.0, 20.0, 69.0, 26.0, 4.0, 27.0, 65.0, 8.0, 28.0, 9.0, 10.0, 29.0, 70.0, 11.0, 30.0, 31.0, 32.0, 18.0, 12.0, 13.0, 17.0, 3.0, 2.0, 14.0, 15.0, 16.0, 1.0]
    order =[44, 39, 56, 47, 49, 37, 42, 46, 51, 58, 60, 62, 52, 41, 35, 33, 50, 61, 54, 34, 59, 43, 48, 45, 55, 53, 38, 57, 64, 67, 68, 63, 40, 36, 21, 66, 22, 6, 20, 65, 18, 5, 17, 69, 28, 27, 70, 29, 1, 12, 30, 13, 14, 26, 31, 24, 19, 2, 3, 4, 25, 11, 32, 10, 15, 16, 9, 23, 7, 8]
    order =[44, 64, 53, 46, 43, 62, 47, 40, 51, 52, 49, 56, 38, 60, 55, 63, 50, 41, 35, 39, 54, 36, 48, 42, 45, 34, 58, 67, 59, 27, 57, 68, 28, 26, 25, 33, 37, 66, 23, 22, 24, 21, 9, 69, 6, 30, 12, 5, 20, 61, 10, 65, 29, 8, 7, 70, 19, 11, 18, 3, 17, 32, 13, 14, 31, 2, 15, 1, 4, 16]    
    order =[ 59.,  55.,  57.,  51.,  54.,  56.,  58.,  38.,  61.,  41.,  63., 35.,  53.,  64.,  28.,  43.,  45.,  52.,  48.,  27.,  36.,  40.,
        37.,  39.,  49.,  44.,  33.,  42.,  46.,  62.,  50.,  60.,  66.,
        22.,  19.,  34.,  20.,  68.,  47.,  67.,  65.,  24.,  21.,  26.,
         6.,  23.,   5.,  69.,  29.,  30.,  70.,  14.,  25.,  10.,  31.,
        12.,  13.,  17.,  32.,   9.,   8.,  18.,  16.,   4.,   7.,  11.,
         2.,  15.,   1.,   3.]
    order =[62, 54, 64, 39, 47, 61, 37, 43, 53, 40, 38, 63, 60, 57, 66, 51, 33, 49, 50, 45, 58, 35, 46, 59, 48, 67, 52, 41, 70, 34, 68, 69, 56, 44, 36, 23, 65, 42, 25, 55, 24, 22, 18, 20, 17, 2, 21, 27, 29, 19, 3, 31, 28, 30, 13, 32, 26, 7, 15, 5, 12, 10, 4, 14, 6, 9, 8, 11, 16, 1]
    order =[53, 44, 49, 61, 39, 37, 54, 40, 34, 51, 46, 62, 60, 52, 48, 38, 42, 45, 43, 35, 33, 63, 57, 36, 47, 50, 58, 64, 68, 65, 55, 56, 18, 25, 41, 59, 27, 69, 22, 67, 70, 26, 21, 66, 23, 24, 30, 7, 20, 6, 5, 29, 10, 28, 11, 13, 32, 31, 17, 19, 12, 3, 15, 14, 16, 1, 2, 4, 8, 9]
    order =[50, 49, 47, 51, 52, 45, 54, 43, 46, 53, 41, 39, 37, 38, 42, 55, 57, 44, 35, 59, 48, 60, 68, 40, 67, 66, 58, 61, 33, 69, 63, 64, 56, 36, 34, 25, 27, 23, 62, 21, 19, 29, 70, 26, 10, 24, 20, 28, 11, 9, 65, 17, 22, 30, 31, 8, 7, 32, 12, 18, 13, 14, 6, 15, 5, 4, 16, 3, 2, 1]
    order = [int(i) for i in order]
    
    print order
    ani = animation.FuncAnimation(fig, anim,fargs=(fig,bNumb,order,'b'), interval=100)
    plt.show()
        
