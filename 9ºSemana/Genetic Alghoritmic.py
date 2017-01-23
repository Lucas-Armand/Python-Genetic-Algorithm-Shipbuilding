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

        Pre,Pos = self.precedences(self.m)
        groups = self.order(Pre,self.bNumb,self.m)
        if population == None:
            first = [self.gen_chromosome(groups,self.m) for i in range(self.N)]
            time = [self.time(bNumb,vicinity,chromo) for chromo in first]
            self.population = [ [t,c] for t,c in zip(time,first)]
            
        else:
            self.population = population
        best = min(self.population, key = lambda x:x[0]) 
        cont = 0
        old_best = 0
        while round(best[0],8)> 70:
            cont+=1
            self.population = self.new_population(self.n,self.teta,self.Teta,self.population,Pre,Pos,self.m)
            best = min(self.population, key = lambda x:x[0]) 
            print cont,best[0]
                
            if cont%20==0:
                if cont==200 or best[0] == old_best:
                    print cont,best[0]
                    print 'break'
                    break
                else:
                    old_best = best[0]
        if round(best[0],8)< 1000:
            print '!!!!!!!!!!!'
        
        return best 
            
    def gen_chromosome(self,groups,m):

        n=len(m)
        chromo = range(1,n)
        random.shuffle(chromo)
        for o in groups:
            index =  [[chromo.index(i),i] for i in o.keys()]
            sorted_index = sorted(index,key = lambda x:x[0])
            order = [[o[i[1]],i[1]] for i in sorted_index]
            sorted_order = sorted(order,key = lambda x:x[0]) 
            for i,x in zip(sorted_index,sorted_order):
                chromo[i[0]] = x[1]

        chromo = np.array(chromo)
        return chromo
    
    def mutation(self,chromosome,Pre,Pos):
        
        x = random.choice(chromosome)
        
        pre = Pre[x]
        pos = Pos[x]
        
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
            pos_y = Pos[y]
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
            pre_y = Pre[y]
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
        
        
    
    def crossover(self,teta,Teta,chromo1,chromo2,Pre,Pos,m):

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
            c1 = self.mutation(c1,Pre,Pos)
        
        if random.random()<teta:
            c2 = self.mutation(c2,Pre,Pos)
        
        return c1,c2

    def time(self,bNumb,vicinity,chromo):
        
        alfa = 1
        built = set()
        time = 0
        t_vec = self.time_vector
        
        self.alfa  = alfa
        self.built = built

        vic = [set(vicinity[x]) for x in chromo]
        time = sum((t_vec(x,y,bNumb) for x,y in zip(chromo,vic)))

        return time
         
    
    
    def new_population(self,n,teta,Teta,population,Pre,Pos,m):
        
        size =  len(population)
        new_population= []
        while len(new_population) != size:
            p1,p2,t_p1,t_p2 = self.tournament(population,n)
            ch1,ch2 = self.crossover(teta,Teta,p1,p2,Pre,Pos,m)

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

##### internal functions ######

    def precedences(self,m):

        Pre,Pos = {},{}
        n = len(m)
        print 'n = ',n 
        for i in range(n):
            Pre[i] = set([a for a in range(n) if m[a,i]>0])
            Pos[i] = set([a for a in range(n) if m[i,a]>0])
        return Pre,Pos
    
    def constr(self,x,s,Pre):
        pre = Pre[x]
        if pre!=set([0]):
            for i in pre:
                s = s|self.constr(i,s,Pre)
            s = s|set([x])
            return s
        else:
            return set([x])

    def order(self,Pre,bNumb,m):

        Sets = []
        n = len(m)
        for i in range(1,n):
            s = set()
            s = self.constr(i,s,Pre)
            Sets.append(s)
        Sets = self.agrupation(0,Sets)

        Dicts = []
        for s in Sets:
            d={}
            n = len(s)
            l = list(s)
            for i in range(n):
                block = bNumb[l[i]]
                bType = block.t
                if bType == 'Bottom':
                    value = 1                   
                if bType == 'Cofferdam':
                    value = 2    
                if bType == 'Side Shell':
                    value = 3                 
                if bType == 'Trunk deck':
                    value = 4
                d[l[i]] = value
            Dicts.append(d)
        return Dicts
                
    def agrupation(self,x,sets):
        try:
            X = sets[x]
            Sets = []
            for S in sets[x+1:]:
                if S&X == set([]):
                    Sets.append(S)
                else:
                    X = S|X
            Sets = sets[:x]+[X]+Sets
            Sets = self.agrupation(x+1,Sets)
            return Sets    
        except:
            return Sets
        
    def dist(self,i,bNumb,xdst,xtyp,ary):
        b_i = bNumb[i]
        idst = ary(b_i.p[0])
        return abs(xdst-idst)
    
    
    def time_vector(self,x,vic,bNumb):
        ary = np.array
        dist = self.dist
        alfa = self.alfa 
        built = self.built
        time = None
        if vic & built != set():
                time = alfa
        if not time:
            
            time = 10*alfa
            xdst = ary(bNumb[x].p[0])
            xtyp = bNumb[x].t
            try:
                d = min([dist(i,bNumb,xdst,xtyp,ary) for i in built if bNumb[i].t == xtyp])
                time+= d
            except ValueError:
                pass
        
        built.add(x)
        return time
    
    def tournament(self,population,n):
        
        t_tou = Time.time()
        specimens = [random.choice(population) for i in range(n)]
        specimens.sort(key = lambda x:x[0])
        parent1,parent2 = specimens[0][1],specimens[1][1]
        t1,t2 = specimens[0][0],specimens[1][0]

        return parent1,parent2,t1,t2
        
    
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

    G = Genetic(0.35,.8,4,200,bNumb,vicinity,MoP)
##    Pre,Pos = G.precedences(MoP)
##    order = G.order(Pre,bNumb,MoP)
##    chromo =  G.gen_chromosome(order,MoP)
##    print list(chromo)
    best = G.run()
##    import cProfile
##    cProfile.run('G.run()')
    
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
