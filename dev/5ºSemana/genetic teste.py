# -*- coding: utf-8 -*-

import os
import csv
import random
import numpy as np
import time as Time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

def printlock(ax,block,clr):
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

def MatrixOfPrecedence(name):
    ListOfPrecedence = csv_read(name)
    n= len(ListOfPrecedence)
    M = np.zeros((n,n))
    M.tolist()
    for j in ListOfPrecedence:
        
        if ListOfPrecedence.index(j)!=0:    #jump the first (title)
            try:
                elements = j[1].split(' - ')
            except:
                elements = [j[1]]
            elements = map(float,elements)
            
            for i in elements:
                M[int(i)][int(j[0])] = 1

    for j in range(n):
        s = sum(M[:,j])
        if s!=0:
            M[:,j] = M[:,j]*1./s
    
    return M
    

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

def Ship3Dplot(fig,blocksList,color):

    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")
    
    for block in blocksList:
        printlock(ax,block,color)
    
    # Create cubic bounding box to simulate equal aspect ratio #
    Xb = 0.5*250*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 125
    Yb = 0.5*200*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0
    Zb = 0.5*200*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 20    
    for xb, yb, zb in zip(Xb, Yb, Zb):
       ax.plot([xb], [yb], [zb], 'w')
    fig.tight_layout(pad=0.5)

class Genetic:

    def __init__(self,teta,Teta,n,N,bNumb,vicinity,m):
        
        self.teta = teta
        self.Teta = Teta
        self.n = n
        self.N = N
        self.bNumb = bNumb
        self.vicinity = vicinity
        self.m = m
    
    def run(self,population = None):

        if population == None:
            first = [self.gen_chromosome(self.m) for i in range(self.N)]
            time = [self.time(bNumb,vicinity,chromo) for chromo in first]
            self.population = [ [t,c] for t,c in zip(time,first)]
            
        else:
            self.population = population
        best = min(self.population, key = lambda x:x[0]) 
        cont = 0
        old_best = 0
        while round(best[0],8)> 70:
            cont+=1
            self.population = self.new_population(self.n,self.teta,self.Teta,self.population,self.m)
            best = min(self.population, key = lambda x:x[0]) 
            print cont,best[0]
                
            if cont%20==0:
                if cont==40 or best[0] == old_best:
                    print cont,best[0]
                    print 'break'
                    break
                else:
                    old_best = best[0]
        if round(best[0],8)< 1000:
            print '!!!!!!!!!!!'
        
        return best 
            
        
     
    def gen_chromosome(self,m):
        
        n = len(m)
        itens = [0]
        chromo = np.array([])
        
        while itens!=[]:
            gene = random.choice(itens)
            if gene!=0 :chromo = np.append(chromo,gene)
            itens.remove(gene)
            
            for j in range(n):
                if m[gene,j]>0:
                    s = 0
                    for i in set(np.append(chromo,gene)):
                        s += m[i][j]
                    if s==1:
                        itens.append(j)
                        
        return chromo
    
    def mutation(self,chromosome,m):
        
        x = random.choice(chromosome)
        
        n =  len(m)
        pre = [a for a in range(n) if m[a,x]>0]
        pos = [a for a in range(n) if m[x,a]>0]
        
        ind = chromosome.tolist().index(x)
    
        ant = chromosome[:ind]
        suc = chromosome[ind+1:]
        ant = ant[::-1]
        
        Ant = []
        for g in ant:
            if g in pre:
                break
            else:
                Ant.append(g)
                        
        Suc = []
        for g in suc:
            if g in pos:
                break
            else:
                Suc.append(g)
        
        possibles_mutations = []
        
        l = len(Ant)
        for i in range(l):
            y = Ant[i]
            pos_y = [a for a in range(n) if m[y,a]>0]
            
            alfa = 'ok'
            for j in range(i+1):
                z = Ant[j]
                if z in pos_y:
                    alfa = 'stop'
            if alfa == 'ok':
                possibles_mutations.append(y)
        
        l = len(Suc)
        for i in range(l):
            y = Suc[i]
            pre_y = [a for a in range(n) if m[a,y]>0]
            alfa = 'ok'
            
            
            
            for j in range(i+1):
                z = Suc[j]
                if z in pre_y:
                    alfa = 'stop'
            if alfa == 'ok':
                possibles_mutations.append(y)
        if possibles_mutations!=[]:           
            w = random.choice(possibles_mutations)        
            ind_w = chromosome.tolist().index(w)
            chromosome[ind] = w
            chromosome[ind_w] = x
        else:
            print 'No possible mutation find!'    
        
        return chromosome
        
        
    
    def crossover(self,teta,Teta,chromo1,chromo2,m):

        if random.random()<Teta:
                
            
            n = len(chromo1)
            i = random.choice(range(n))
            
            p1_a = chromo1[:i]
            p2_a = chromo2[:i]
            
            p1_b = chromo1[i:]
            p2_b = chromo2[i:]
            
            diff_1 = np.extract(-np.in1d(p2_a,p1_a),p2_a)
            diff_2 = np.extract(-np.in1d(p1_a,p2_a),p1_a)
            
            p1_a = np.append(p1_a,diff_1)
            p2_a = np.append(p2_a,diff_2)
        
            for element in diff_2:
                ind = np.where(p2_b == element)
                p2_b = np.delete(p2_b,ind)
            
            for element in diff_1 :
                ind = np.where(p1_b == element)
                p1_b = np.delete(p1_b,ind)
            
            c1 = np.append(p1_a,p2_b)
            c2 = np.append(p2_a,p1_b)
        else:
            c1 = chromo1
            c2 = chromo2
            
        if random.random()<teta:
            c1 = self.mutation(c1,m)
        
        if random.random()<teta:
            c2 = self.mutation(c2,m)
        
        return c1,c2
        
        
        
    def time(self,bNumb,vicinity,chromo):
        
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
         
    
    def tournament(self,population,n):
        
        t_tou = Time.time()
        specimens = [random.choice(population) for i in range(n)]
        specimens.sort(key = lambda x:x[0])
        parent1,parent2 = specimens[0][1],specimens[1][1]
        t1,t2 = specimens[0][0],specimens[1][0]

        return parent1,parent2,t1,t2
        
        
    def new_population(self,n,teta,Teta,population,m):
        
        size =  len(population)
        new_population= []
        while len(new_population) != size:
            p1,p2,t_p1,t_p2 = self.tournament(population,n)
            ch1,ch2 = self.crossover(teta,Teta,p1,p2,m)

            if (ch1 == p1).all():
                t1 = t_p1
            elif (ch1 == p2).all():
                t1 = t_p2
            else:
                t1 = self.time(bNumb,vicinity,ch1)
                
            if (ch2 == p1).all():
                t2 = t_p1
            elif (ch2 == p2).all():
                t2 = t_p2
            else:
                t2 = self.time(bNumb,vicinity,ch2)
            
            new_population+=[[t1,ch1],[t2,ch2]]
        return new_population
       
#    def check(self,chromosome,m):
#        
#        n =  len(m)
#        for x in chromosome:
#                
#            pre = [a for a in range(n) if m[a,x]>0]
#            pos = [a for a in range(n) if m[x,a]>0]
#            
#            ind = chromosome.tolist().index(x)
#        
#            ant = chromosome[:ind]
#            suc = chromosome[ind+1:]
#            
#            set_pre = set(pre) - set([0])
#            set_pos = set(pos)
#            
#            set_ant = set(ant)
#            set_suc = set(suc)
#            
#            
#            
#            
#            if set_pre != set_pre&set_ant or set_pos != set_pos&set_suc:
#                print                
#                print                
#                print chromosome
#                print 
#                print x
#                print 
#                print ant
#                print suc
#                print 
#                print pre
#                print pos
#                print 
#                print 
#                return False
#        return True
                
                
    
def anim(i,fig,bNumb,order,color):
    try:
        Ship3Dplot(fig, [bNumb[order[i]]],color)
    except:
        pass
    
class Block:
    def __init__(self,point,a,b,c,weight,btype):
        self.p=point
        self.a=a
        self.b=b
        self.c=c
        self.w=weight
        self.t=btype
        
if __name__ == "__main__":
    

    fig = plt.figure()
    
    
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
    
    #execute
    
    MoP = MatrixOfPrecedence('EstructuralLoP.csv')
    G = Genetic(0.4,.5,4,200,bNumb,vicinity,MoP)
    chromo =  G.gen_chromosome(MoP)
    #best = G.run()
        
    import cProfile
    cProfile.run('G.run()')
##    chromosome = best[1]
##    chromosome = [int(i) for i in chromosome.tolist()]
    
#    order = csv_read('Grande Bloco_Meio Navio-PopaProa.csv')
#    order = csv_read('Camada_Meio Navio-PopaProa.csv')
#    order = csv_read('Piramide_Meio Navio-PopaProa.csv')
##    order = csv_read('Grande bloco_Popa-Proa.csv')
#    order = csv_read('Camada_Popa-Proa.csv')
#    order = csv_read('Piramide_Popa-Proa.csv')
#    print order
#    
#    chromosome = [int(i[0]) for i in order]    
#    print G1.time(bNumb,vicinity,chromosome)
#    

    
##    
##    ani = animation.FuncAnimation(fig, anim,fargs=(fig,bNumb,chromosome,'b'), interval=200)
##    plt.show()
##    print 'time(execution) = ', - t_exec + Time.time()
##    
##    file = open("newfile.txt", "w")
##    file.write(text)
##    file.close()


#Beste result until now (0.3,4,600):
#[53.0, 51.0, 35.0, 55.0, 36.0, 49.0, 47.0, 34.0, 57.0, 58.0, 60.0, 59.0, 54.0, 61.0, 52.0, 50.0, 45.0, 46.0, 63.0, 44.0, 37.0, 62.0, 39.0, 33.0, 64.0, 38.0, 40.0, 43.0, 56.0, 42.0, 41.0, 48.0, 21.0, 22.0, 67.0, 23.0, 24.0, 66.0, 65.0, 68.0, 26.0, 20.0, 28.0, 8.0, 25.0, 19.0, 9.0, 7.0, 10.0, 17.0, 27.0, 69.0, 6.0, 30.0, 29.0, 5.0, 70.0, 11.0, 12.0, 4.0, 18.0, 13.0, 14.0, 3.0, 32.0, 31.0, 2.0, 15.0, 16.0, 1.0]
