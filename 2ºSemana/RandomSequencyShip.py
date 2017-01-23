# -*- coding: utf-8 -*-

import os
import random
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations


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

def printBlock(ax,block,clr):
    point = block.p
    a = block.a
    b = block.b
    c = block.c
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
        weight = i[7]
        block = Block(point,a,b,c,weight)
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
        printBlock(ax,block,color)
        print 'ok'

    # Create cubic bounding box to simulate equal aspect ratio #
    Xb = 0.5*250*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 125
    Yb = 0.5*200*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0
    Zb = 0.5*200*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 20
    for xb, yb, zb in zip(Xb, Yb, Zb):
       ax.plot([xb], [yb], [zb], 'w')
    fig.tight_layout(pad=0.5)

def MatrixOfPrecedence(name):
    ListOfPrecedence = csv_read(name)
    M = np.zeros((70,70))
    M.tolist()
    for i in ListOfPrecedence:
        n = (len(i)-1)/2
        print i
        if ListOfPrecedence.index(i)!=0:
            for j in range(n):
                elements = i[1+2*j].split(' - ')
                print elements
                elements = [int(k) for k in elements]
            print elements
class Block:
    def __init__(self,point,a,b,c,weight):
        self.p=point
        self.a=a
        self.b=b
        self.c=c
        self.w=weight


if __name__ == "__main__":
    
    bNumb,bType =defineGeometry('GeometriaNavio.csv')
    
    # Define regions 
    
    deck=[]
    for i in range(1,17):
        deck.append(bNumb[i])
    shell=[]
    for i in range(8):
        shell.append([bNumb[17+i*2],bNumb[18+i*2]])
    bottom=[]
    for i in range(16):
        bottom.append([bNumb[33+i*2],bNumb[34+i*2]])
    cofferdam=[]
    for i in range(65,71):
        cofferdam.append(bNumb[i])   
    Region = {'Bottom':bottom,
              'Side Shell':shell,
              'Trunk deck':deck,
              'Cofferdam':cofferdam}
    
    # Define BigBlocks
    
    BigBlock = {}
    for i in range(8):
        BigBlock[i+1]={}
        BigBlock[i+1]['Bottom']=bNumb[33+4*i],bNumb[34+4*i],bNumb[35+4*i],bNumb[36+4*i]
        BigBlock[i+1]['Side Shell']=bNumb[17+2*i],bNumb[18+2*i]
        BigBlock[i+1]['Trunk deck']=bNumb[1+2*i],bNumb[2+2*i]
        if i<2:
            BigBlock[i+1]['Cofferdam']=bNumb[65+i]
        elif i<4:
            BigBlock[i+1]['Cofferdam']=bNumb[64+i]
        else:
            BigBlock[i+1]['Cofferdam']=bNumb[63+i]
        
    #Generate Random Sequency
    MoP=MatrixOfPrecedence('BigBlocksLoP.csv')
    seq = RandomBigBlocks(bNumb,bType,Region,BigBlock,MatrixOfPrecedence)
    
    
    
    