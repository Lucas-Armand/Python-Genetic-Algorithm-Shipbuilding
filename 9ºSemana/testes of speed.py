# -*- coding: utf-8 -*-

import os
import csv
import random
import numpy as np
import timeit
import time as Time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import product, combinations

class Block:
    def __init__(self,point,a,b,c,weight,btype):
        self.p=point
        self.a=a
        self.b=b
        self.c=c
        self.w=weight
        self.t=btype
        

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

def defineGeometry(name):

    vect = csv_read(name)
    blockNumber ={}
    for i in vect:
        a = i[1]
        b = i[2]
        c = i[3]
        point = [i[4],i[5],i[6]]
        weight = i[7]
        btype = i[-1]
        block = Block(point,a,b,c,weight,btype)
        blockNumber[i[0]] = block

    return blockNumber

bNumb=defineGeometry('GeometriaNavio.csv')
    
# Define vicinity

#deck
vicinity={1:[2]}    
for i in range(2,16):
    vicinity[i]  = [i-1,i+1]    
vicinity[16] = [15]  

#side
vicinity[17] = [18,19]  
vicinity[18] = [17,20]  
for i in range(19,31):
    v = i-1 if i%2==0 else i+1
    vicinity[i] = [v,i-2,i+2]
vicinity[31] = [29,32]  
vicinity[32] = [30,31] 

#bott
vicinity[33] = [34,35]  
vicinity[34] = [33,36]  
for i in range(35,63):
    v = i-1 if i%2==0 else i+1
    vicinity[i] = [v,i-2,i+2]
vicinity[63] = [61,64]  
vicinity[64] = [63,62] 

#coff
vicinity[65] = [66]    
for i in range(66,70):
    vicinity[i]  = [i-1,i+1]    
vicinity[70] = [69]  


alfa = 10
beta = 1
built = []
time = 0
append = built.append

def order(x): return vicinity[x]


def time(bNumb,vicinity,chromo):
    
    
    t_time = Time.time()
    
    alfa = 1
    built = []
    time = 0
    append = built.append
    
    def time_vector(x,y):
        for i in y:
            if i in built:
                time = alfa
                break
        try:time
        except: time = 10*alfa
        append(x)
        return time              
        
    vic = [vicinity[x] for x in chromo]
    time = sum((time_vector(x,y) for x,y in zip(chromo,vic)))

    return time

chromo = [44, 39, 56, 47, 49, 37, 42, 46, 51, 58, 60, 62, 52, 41, 35, 33, 50, 61, 54, 34, 59, 43, 48, 45, 55, 53, 38, 57, 64, 67, 68, 63, 40, 36, 21, 66, 22, 6, 20, 65, 18, 5, 17, 69, 28, 27, 70, 29, 1, 12, 30, 13, 14, 26, 31, 24, 19, 2, 3, 4, 25, 11, 32, 10, 15, 16, 9, 23, 7, 8]


import cProfile
cProfile.run('time(bNumb,vicinity,chromo)')
##
##print timeit.timeit(setup='from __main__ import chromo;'+
##                       'from __main__ import bNumb;'+
##                       'from __main__ import time;'+
##                       'from __main__ import vicinity '
##                       ,stmt='time(bNumb,vicinity,chromo)') 
#print t.timeit(number = 1000000)

