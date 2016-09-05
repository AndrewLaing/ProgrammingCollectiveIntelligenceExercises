""" Chapter 12 Programming Collective Intelligence: Optimization.

    As the chapter has no exercises in it I have decided to create a practical
    application for each of the Algorithms and Methods described.
    Lastly Optimization.

    This performs optimization on the Titanic dataset using four successive methods;
       annealing, genetic, hillclimb and random-restart annealing.
    I used leave-one-out-cross-validation in the cost function and psyco to speed things up.

    I have had fun working through this book and have improved upon my knowledge of Python.
    Thanks Toby :)
"""

import math
import random as random


def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    
    return math.sqrt(d)


def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2)) 

def getdistances(data,vec1):
    distancelist=[]
    
    for i in range(len(data)):
        vec2=data[i]['input']
        distancelist.append((euclidean(vec1,vec2),i))
    
    distancelist.sort()
    return distancelist


def weightedknn(data,vec1,k=5,weightf=gaussian):
    # Get distances
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0

    # Get weighted average
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    
    if totalweight==0: 
        return 0
    
    avg=avg/totalweight
    return avg


def rescale(data,scale):
    scaledata=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
        scaledata.append({'input':scaled,'result':row['result']})
    return scaledata


def createcostfunction(algf,data):
    def costf(scale):
        print "scale =",scale
        sdata=rescale(data,scale)
        return loo_crossvalidate(algf,data)
    return costf       # Returns the function itself


def testalgorithm(algf,trainset,testset):
    error=0.0
    
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    
    if len(testset)==0: 
        return 0.0   # If no testset is produced
    
    return error/len(testset)


def loo_crossvalidate(algf,data):
    error=0.0
    
    for row in range(len(data)):
        trainset = []
        trainset = trainset+data
        testset=[]
        testset.append(data[row])
        trainset.remove(data[row])
        error+=testalgorithm(algf,trainset,testset)
    return error/len(data)


def hillclimb(domain,costf):
    sol=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
    while 1:
        neighbors=[]
        for j in range(len(domain)):
            if (domain[j][0] == 0) and (domain[j][1] == 0): 
                pass   # Workaround for when domain is (0,0)
            else:
                if sol[j] > domain[j][0] and sol[j] < domain[j][1]:
                    neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
                    neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
                
                if sol[j] == domain[j][0]:
                    neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
                
                if sol[j] == domain[j][1]:
                    neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
        
        current=costf(sol)
        best=current
        
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]
        
        if best==current:
            break
    return sol


def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
    vec=[(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
    while T>0.1:
        i=random.randint(0,len(domain)-1)
        dir=random.randint(-step,step)
        vecb=vec[:]
        vecb[i]+=dir
        
        if vecb[i]<domain[i][0]: 
            vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]: 
            vecb[i]=domain[i][1]
        
        ea=costf(vec)
        eb=costf(vecb)
        p=pow(math.e,(-eb-ea)/T)
        
        if (eb<ea or random.random()<p):
            vec=vecb
        T=T*cool
    return vec


def randomrestart_annealing(domain,costf,T1=10000.0,cool=0.95,step=1,maxiter=100):
    T = T1
    best=999999999
    bestr=None
    for i in range(maxiter):
        vec=[(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
        while T>0.1:
            i=random.randint(0,len(domain)-1)
            dir=random.randint(-step,step)
            vecb=vec[:]
            vecb[i]+=dir
            
            if vecb[i]<domain[i][0]: 
                vecb[i]=domain[i][0]
            elif vecb[i]>domain[i][1]: 
                vecb[i]=domain[i][1]
            
            ea=costf(vec)
            eb=costf(vecb)
            p=pow(math.e,(-eb-ea)/T)
            
            if (eb<ea or random.random()<p):
                vec=vecb
            
            T=T*cool  # Decrease the temperature
        cost = costf(vec)
        T = T1
        
        if cost<best:
            best=cost
            bestr=vec
    
    return bestr


def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        
        if random.random()<0.5 and vec[i]-step>domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i]+step<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
        else:
            return vec           # Corrected otherwise if vec[i] is unsatisfactory nothing returns
    def crossover(r1,r2):
        if len(domain)-2>=1:
            i=random.randint(1,len(domain)-2)
            return r1[0:i]+r2[i:]
        else:
            i=random.randint(1,len(domain))
            return r1[0:i]+r2[i:]
    
    pop=[]
    
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
        pop.append(vec)
    
    topelite=int(elite*popsize)            # How many winners from each generation?
    
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        
        if i == maxiter-1: 
            pass            # Corrected from here for last iteration
        else:
            ranked=[v for (s,v) in scores]
            
            # Start with the pure winners
            pop=ranked[0:topelite]
            
            # Add mutated and bred forms of the winners
            while len(pop)<popsize:
                if random.random()<mutprob:
                    c=random.randint(0,topelite)           # Mutation
                    pop.append(mutate(ranked[c]))
                else:
                    c1=random.randint(0,topelite)          # Crossover
                    c2=random.randint(0,topelite)
                    pop.append(crossover(ranked[c1],ranked[c2]))
            
            print scores[0][0]
    
    return scores[0][1]


datalist=[{'input': [3, 0, 22.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 38.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 26.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 35.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 35.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [1, 0, 54.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 2.0, 3, 1, 2], 'result': 0}, {'input': [3, 1, 27.0, 0, 2, 2], 'result': 1}, {'input': [2, 1, 14.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 4.0, 1, 1, 2], 'result': 1}, {'input': [1, 1, 58.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 39.0, 1, 5, 2], 'result': 0}, {'input': [3, 1, 14.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 55.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 2.0, 4, 1, 1], 'result': 0}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 31.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 0], 'result': 1}, {'input': [2, 0, 35.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 34.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 15.0, 0, 0, 1], 'result': 1}, {'input': [1, 0, 28.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 8.0, 3, 1, 2], 'result': 0}, {'input': [3, 1, 38.0, 1, 5, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 19.0, 3, 2, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 40.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 0.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [2, 0, 66.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 28.0, 1, 0, 0], 'result': 0}, {'input': [1, 0, 42.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 18.0, 2, 0, 2], 'result': 0}, {'input': [3, 1, 14.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 40.0, 1, 0, 2], 'result': 0}, {'input': [2, 1, 27.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [2, 1, 3.0, 1, 2, 0], 'result': 1}, {'input': [3, 1, 19.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 1, 0, 1], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 2, 0, 0], 'result': 0}, {'input': [3, 1, 18.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 7.0, 4, 1, 2], 'result': 0}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 49.0, 1, 0, 0], 'result': 1}, {'input': [2, 1, 29.0, 1, 0, 2], 'result': 1}, {'input': [1, 0, 65.0, 0, 1, 0], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 21.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 28.5, 0, 0, 0], 'result': 0}, {'input': [2, 1, 5.0, 1, 2, 2], 'result': 1}, {'input': [3, 0, 11.0, 5, 2, 2], 'result': 0}, {'input': [3, 0, 22.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 38.0, 0, 0, 0], 'result': 1}, {'input': [1, 0, 45.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 4.0, 3, 2, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 0.0, 1, 1, 0], 'result': 1}, {'input': [2, 1, 29.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 17.0, 4, 2, 2], 'result': 1}, {'input': [3, 0, 26.0, 2, 0, 2], 'result': 0}, {'input': [2, 0, 32.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 16.0, 5, 2, 2], 'result': 0}, {'input': [2, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 26.0, 1, 0, 0], 'result': 0}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 0.82999999999999996, 0, 2, 2], 'result': 1}, {'input': [3, 1, 30.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 29.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [1, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 17.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 33.0, 3, 0, 2], 'result': 1}, {'input': [3, 0, 16.0, 1, 3, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 23.0, 3, 2, 2], 'result': 1}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 29.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 46.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 26.0, 1, 2, 2], 'result': 0}, {'input': [3, 0, 59.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 71.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 23.0, 0, 1, 0], 'result': 1}, {'input': [2, 1, 34.0, 0, 1, 2], 'result': 1}, {'input': [2, 0, 34.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 21.0, 0, 1, 2], 'result': 0}, {'input': [3, 0, 33.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 37.0, 2, 0, 2], 'result': 0}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 21.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 38.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 1, 0, 1], 'result': 1}, {'input': [1, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 14.5, 1, 0, 0], 'result': 0}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 20.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 17.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 70.5, 0, 0, 1], 'result': 0}, {'input': [2, 0, 29.0, 1, 0, 2], 'result': 0}, {'input': [1, 0, 24.0, 0, 1, 0], 'result': 0}, {'input': [3, 1, 2.0, 4, 2, 2], 'result': 0}, {'input': [2, 0, 21.0, 2, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 32.5, 1, 0, 0], 'result': 0}, {'input': [2, 1, 32.5, 0, 0, 2], 'result': 1}, {'input': [1, 0, 54.0, 0, 1, 2], 'result': 0}, {'input': [3, 0, 12.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 1, 1, 0], 'result': 1}, {'input': [3, 0, 45.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 33.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 47.0, 1, 0, 2], 'result': 0}, {'input': [2, 1, 29.0, 1, 0, 2], 'result': 1}, {'input': [2, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 23.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 19.0, 0, 2, 2], 'result': 1}, {'input': [1, 0, 37.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 16.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 24.0, 0, 0, 0], 'result': 0}, {'input': [3, 1, 0.0, 0, 2, 0], 'result': 0}, {'input': [3, 1, 22.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 24.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 19.0, 0, 0, 1], 'result': 0}, {'input': [2, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 19.0, 1, 1, 2], 'result': 0}, {'input': [3, 0, 27.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 9.0, 2, 2, 2], 'result': 0}, {'input': [2, 0, 36.5, 0, 2, 2], 'result': 0}, {'input': [2, 0, 42.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 51.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 22.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 55.5, 0, 0, 2], 'result': 0}, {'input': [3, 0, 40.5, 0, 2, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 51.0, 0, 1, 0], 'result': 0}, {'input': [3, 1, 16.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 8, 2, 2], 'result': 0}, {'input': [3, 0, 44.0, 0, 1, 2], 'result': 0}, {'input': [2, 1, 40.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 26.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 17.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 1.0, 4, 1, 2], 'result': 0}, {'input': [3, 0, 9.0, 0, 2, 2], 'result': 1}, {'input': [1, 1, 0.0, 0, 1, 2], 'result': 1}, {'input': [3, 1, 45.0, 1, 4, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 61.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 4.0, 4, 1, 1], 'result': 0}, {'input': [3, 1, 1.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 56.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 18.0, 1, 1, 2], 'result': 0}, {'input': [3, 0, 0.0, 3, 1, 2], 'result': 0}, {'input': [1, 1, 50.0, 0, 0, 0], 'result': 0}, {'input': [2, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 36.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 8, 2, 2], 'result': 0}, {'input': [2, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 9.0, 4, 2, 2], 'result': 0}, {'input': [2, 0, 1.0, 2, 1, 2], 'result': 1}, {'input': [3, 1, 4.0, 0, 2, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 1, 0, 1], 'result': 1}, {'input': [1, 0, 45.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 40.0, 1, 1, 1], 'result': 0}, {'input': [3, 0, 36.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 32.0, 0, 0, 2], 'result': 1}, {'input': [2, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 19.0, 1, 0, 2], 'result': 1}, {'input': [2, 0, 3.0, 1, 1, 2], 'result': 1}, {'input': [1, 1, 44.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 58.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 42.0, 0, 1, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [2, 1, 24.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 8, 2, 2], 'result': 0}, {'input': [3, 0, 34.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 45.5, 0, 0, 0], 'result': 0}, {'input': [3, 0, 18.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 2.0, 0, 1, 2], 'result': 0}, {'input': [3, 0, 32.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 26.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 16.0, 0, 0, 1], 'result': 1}, {'input': [1, 0, 40.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 35.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 1, 0, 1], 'result': 0}, {'input': [1, 1, 31.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 27.0, 0, 0, 2], 'result': 1}, {'input': [2, 0, 42.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 32.0, 0, 0, 0], 'result': 1}, {'input': [2, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 16.0, 0, 0, 2], 'result': 1}, {'input': [2, 0, 27.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 51.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 38.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 19.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 20.5, 0, 0, 2], 'result': 0}, {'input': [2, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 3, 1, 2], 'result': 0}, {'input': [1, 1, 35.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 29.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 59.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 5.0, 4, 2, 2], 'result': 1}, {'input': [2, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 44.0, 1, 0, 2], 'result': 0}, {'input': [2, 1, 8.0, 0, 2, 2], 'result': 1}, {'input': [2, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 33.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 1, 0, 0], 'result': 0}, {'input': [3, 1, 0.0, 1, 0, 1], 'result': 1}, {'input': [2, 0, 29.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 30.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 44.0, 2, 0, 1], 'result': 0}, {'input': [3, 1, 25.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 24.0, 0, 2, 2], 'result': 1}, {'input': [1, 0, 37.0, 1, 1, 2], 'result': 1}, {'input': [2, 0, 54.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 29.0, 1, 1, 2], 'result': 0}, {'input': [1, 0, 62.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 30.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 41.0, 0, 2, 2], 'result': 0}, {'input': [3, 1, 29.0, 0, 2, 0], 'result': 1}, {'input': [1, 1, 0.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 30.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 35.0, 0, 0, 0], 'result': 1}, {'input': [2, 1, 50.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 3.0, 4, 2, 2], 'result': 1}, {'input': [1, 0, 52.0, 1, 1, 2], 'result': 0}, {'input': [1, 0, 40.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 0}, {'input': [2, 0, 36.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 16.0, 4, 1, 2], 'result': 0}, {'input': [3, 0, 25.0, 1, 0, 2], 'result': 1}, {'input': [1, 1, 58.0, 0, 1, 2], 'result': 1}, {'input': [1, 1, 35.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 25.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 41.0, 0, 1, 2], 'result': 1}, {'input': [1, 0, 37.0, 0, 1, 0], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [1, 1, 63.0, 1, 0, 2], 'result': 1}, {'input': [3, 1, 45.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 7.0, 4, 1, 1], 'result': 0}, {'input': [3, 1, 35.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 65.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 16.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 33.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 30.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 42.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 22.0, 0, 0, 1], 'result': 1}, {'input': [1, 1, 26.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 19.0, 1, 0, 0], 'result': 1}, {'input': [2, 0, 36.0, 0, 0, 0], 'result': 0}, {'input': [3, 1, 24.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 23.5, 0, 0, 0], 'result': 0}, {'input': [1, 1, 2.0, 1, 2, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 50.0, 0, 1, 0], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 2, 0, 1], 'result': 1}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.92000000000000004, 1, 2, 2], 'result': 1}, {'input': [1, 1, 0.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 17.0, 1, 0, 0], 'result': 1}, {'input': [2, 0, 30.0, 1, 0, 0], 'result': 0}, {'input': [1, 1, 30.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 24.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 18.0, 2, 2, 0], 'result': 1}, {'input': [2, 1, 26.0, 1, 1, 2], 'result': 0}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 43.0, 1, 1, 2], 'result': 0}, {'input': [3, 1, 26.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 24.0, 1, 0, 2], 'result': 1}, {'input': [2, 0, 54.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 31.0, 0, 2, 2], 'result': 1}, {'input': [1, 1, 40.0, 1, 1, 0], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 27.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 30.0, 0, 0, 1], 'result': 1}, {'input': [2, 1, 22.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 0.0, 8, 2, 2], 'result': 0}, {'input': [1, 1, 36.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 61.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 36.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 31.0, 1, 1, 2], 'result': 1}, {'input': [1, 1, 16.0, 0, 1, 0], 'result': 1}, {'input': [3, 1, 0.0, 2, 0, 1], 'result': 1}, {'input': [1, 0, 45.5, 0, 0, 2], 'result': 0}, {'input': [1, 0, 38.0, 0, 1, 2], 'result': 0}, {'input': [3, 0, 16.0, 2, 0, 2], 'result': 0}, {'input': [1, 1, 0.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 29.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 41.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 45.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 45.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 2.0, 1, 1, 2], 'result': 1}, {'input': [1, 1, 24.0, 3, 2, 2], 'result': 1}, {'input': [2, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 36.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 24.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 40.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 3.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 42.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 15.0, 1, 1, 0], 'result': 0}, {'input': [3, 0, 25.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 22.0, 0, 1, 2], 'result': 1}, {'input': [2, 1, 38.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 40.0, 1, 4, 2], 'result': 0}, {'input': [2, 0, 29.0, 1, 0, 0], 'result': 0}, {'input': [3, 1, 45.0, 0, 1, 0], 'result': 0}, {'input': [3, 0, 35.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 1, 0, 1], 'result': 0}, {'input': [3, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 60.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [1, 1, 24.0, 0, 0, 0], 'result': 1}, {'input': [1, 0, 25.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 18.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 22.0, 0, 0, 0], 'result': 0}, {'input': [3, 1, 3.0, 3, 1, 2], 'result': 0}, {'input': [1, 1, 0.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 22.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 27.0, 0, 2, 0], 'result': 0}, {'input': [3, 0, 20.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 42.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 1.0, 0, 2, 0], 'result': 1}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 35.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 1.0, 5, 2, 2], 'result': 0}, {'input': [2, 1, 36.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [2, 1, 17.0, 0, 0, 0], 'result': 1}, {'input': [1, 0, 36.0, 1, 2, 2], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 28.0, 2, 0, 2], 'result': 0}, {'input': [1, 1, 23.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 24.0, 0, 2, 2], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 31.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 46.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 28.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 39.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 26.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 21.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 28.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 20.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 34.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 51.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 3.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 3, 1, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [1, 1, 33.0, 1, 0, 1], 'result': 1}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 44.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 34.0, 1, 1, 2], 'result': 1}, {'input': [2, 1, 18.0, 0, 2, 2], 'result': 1}, {'input': [2, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 10.0, 0, 2, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 21.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 29.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 28.0, 1, 1, 2], 'result': 0}, {'input': [3, 0, 18.0, 1, 1, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 28.0, 1, 0, 2], 'result': 1}, {'input': [2, 1, 19.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 28.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 1, 0, 2], 'result': 1}, {'input': [2, 1, 42.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 17.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 50.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 14.0, 1, 2, 2], 'result': 1}, {'input': [3, 1, 21.0, 2, 2, 2], 'result': 0}, {'input': [2, 1, 24.0, 2, 3, 2], 'result': 1}, {'input': [1, 0, 64.0, 1, 4, 2], 'result': 0}, {'input': [2, 0, 31.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 45.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 25.0, 1, 0, 2], 'result': 0}, {'input': [2, 1, 28.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 4.0, 0, 2, 2], 'result': 1}, {'input': [2, 1, 13.0, 0, 1, 2], 'result': 1}, {'input': [1, 0, 34.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 5.0, 2, 1, 0], 'result': 1}, {'input': [1, 0, 52.0, 0, 0, 2], 'result': 1}, {'input': [2, 0, 36.0, 1, 2, 2], 'result': 0}, {'input': [3, 0, 0.0, 1, 0, 2], 'result': 0}, {'input': [1, 0, 30.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 49.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 29.0, 0, 0, 0], 'result': 1}, {'input': [1, 0, 65.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 0.0, 1, 0, 2], 'result': 1}, {'input': [2, 1, 50.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [1, 0, 48.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 34.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 48.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 38.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 56.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 1, 0.75, 2, 1, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 38.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 33.0, 1, 2, 2], 'result': 1}, {'input': [2, 1, 23.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 22.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 34.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 29.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 2.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 9.0, 5, 2, 2], 'result': 0}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 50.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 63.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 25.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 0.0, 3, 1, 2], 'result': 0}, {'input': [1, 1, 35.0, 1, 0, 2], 'result': 1}, {'input': [1, 0, 58.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 9.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 0.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 55.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 71.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 54.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 25.0, 1, 2, 2], 'result': 0}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 17.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 21.0, 0, 0, 1], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 1, 37.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 16.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 18.0, 1, 0, 0], 'result': 0}, {'input': [2, 1, 33.0, 0, 2, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 26.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 29.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 36.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 54.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 34.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [2, 1, 36.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 30.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 44.0, 0, 1, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 40.5, 0, 0, 1], 'result': 0}, {'input': [2, 1, 50.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 39.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 23.0, 2, 1, 2], 'result': 0}, {'input': [2, 1, 2.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 17.0, 1, 1, 0], 'result': 0}, {'input': [3, 1, 0.0, 0, 2, 0], 'result': 1}, {'input': [3, 1, 30.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 7.0, 0, 2, 2], 'result': 1}, {'input': [1, 0, 45.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 30.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 22.0, 0, 2, 0], 'result': 1}, {'input': [1, 1, 36.0, 0, 2, 2], 'result': 1}, {'input': [3, 1, 9.0, 4, 2, 2], 'result': 0}, {'input': [3, 1, 11.0, 4, 2, 2], 'result': 0}, {'input': [2, 0, 32.0, 1, 0, 2], 'result': 1}, {'input': [1, 0, 50.0, 1, 0, 0], 'result': 0}, {'input': [1, 0, 64.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 19.0, 1, 0, 2], 'result': 1}, {'input': [2, 0, 0.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 33.0, 1, 1, 2], 'result': 0}, {'input': [2, 0, 8.0, 1, 1, 2], 'result': 1}, {'input': [1, 0, 17.0, 0, 2, 0], 'result': 1}, {'input': [2, 0, 27.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 22.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 22.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 62.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 48.0, 1, 0, 0], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 39.0, 1, 1, 2], 'result': 1}, {'input': [3, 1, 36.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 40.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 24.0, 2, 0, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 29.0, 0, 4, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 1}, {'input': [2, 0, 62.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 53.0, 2, 0, 2], 'result': 1}, {'input': [1, 0, 36.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 0, 16.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 34.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 39.0, 1, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 1, 0, 0], 'result': 0}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 25.0, 1, 1, 2], 'result': 1}, {'input': [1, 1, 39.0, 1, 1, 0], 'result': 1}, {'input': [2, 0, 54.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 36.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [1, 1, 18.0, 0, 2, 2], 'result': 1}, {'input': [2, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 60.0, 1, 1, 0], 'result': 1}, {'input': [3, 0, 22.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 35.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 52.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 2, 1], 'result': 0}, {'input': [2, 0, 37.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 36.0, 1, 1, 2], 'result': 0}, {'input': [2, 1, 0.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 49.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 49.0, 1, 0, 0], 'result': 1}, {'input': [2, 1, 24.0, 2, 1, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 44.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 35.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 36.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 30.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 27.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 22.0, 1, 2, 0], 'result': 1}, {'input': [1, 1, 40.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 39.0, 1, 5, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 1, 0, 1], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 35.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 24.0, 1, 2, 2], 'result': 1}, {'input': [3, 0, 34.0, 1, 1, 2], 'result': 0}, {'input': [3, 1, 26.0, 1, 0, 2], 'result': 0}, {'input': [2, 1, 4.0, 2, 1, 2], 'result': 1}, {'input': [2, 0, 26.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 27.0, 1, 0, 0], 'result': 0}, {'input': [1, 0, 42.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 20.0, 1, 1, 0], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 61.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 57.0, 0, 0, 1], 'result': 0}, {'input': [1, 1, 21.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 26.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [1, 0, 80.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 51.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 32.0, 0, 0, 0], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 9.0, 3, 2, 2], 'result': 0}, {'input': [2, 1, 28.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 31.0, 1, 1, 2], 'result': 0}, {'input': [3, 1, 41.0, 0, 5, 2], 'result': 0}, {'input': [3, 0, 0.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 24.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 2.0, 3, 2, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.75, 2, 1, 0], 'result': 1}, {'input': [1, 0, 48.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 56.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 23.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 18.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [3, 1, 18.0, 0, 0, 1], 'result': 0}, {'input': [2, 0, 24.0, 2, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 32.0, 1, 1, 1], 'result': 0}, {'input': [2, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 58.0, 0, 2, 0], 'result': 0}, {'input': [1, 0, 50.0, 2, 0, 2], 'result': 1}, {'input': [3, 0, 40.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 36.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 20.0, 1, 0, 2], 'result': 1}, {'input': [2, 0, 32.0, 2, 0, 2], 'result': 0}, {'input': [2, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 43.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 0.0, 1, 0, 2], 'result': 1}, {'input': [2, 1, 40.0, 1, 1, 2], 'result': 1}, {'input': [1, 0, 31.0, 1, 0, 2], 'result': 0}, {'input': [2, 0, 70.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 31.0, 0, 0, 2], 'result': 1}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 24.5, 0, 0, 2], 'result': 0}, {'input': [3, 1, 18.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 43.0, 1, 6, 2], 'result': 0}, {'input': [1, 0, 36.0, 0, 1, 0], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 0}, {'input': [1, 0, 27.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 14.0, 5, 2, 2], 'result': 0}, {'input': [2, 0, 60.0, 1, 1, 2], 'result': 0}, {'input': [2, 0, 25.0, 1, 2, 0], 'result': 0}, {'input': [3, 0, 14.0, 4, 1, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 15.0, 0, 1, 2], 'result': 1}, {'input': [1, 0, 31.0, 1, 0, 2], 'result': 1}, {'input': [3, 1, 4.0, 0, 1, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 25.0, 0, 0, 0], 'result': 0}, {'input': [1, 0, 60.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 52.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 44.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [1, 0, 49.0, 1, 1, 0], 'result': 0}, {'input': [3, 0, 42.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 18.0, 1, 0, 0], 'result': 1}, {'input': [1, 0, 35.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 18.0, 0, 1, 0], 'result': 0}, {'input': [3, 0, 25.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 26.0, 1, 0, 2], 'result': 0}, {'input': [2, 0, 39.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 45.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 42.0, 0, 0, 2], 'result': 1}, {'input': [1, 1, 22.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 1, 1, 0], 'result': 1}, {'input': [1, 1, 24.0, 0, 0, 0], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 48.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 29.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 52.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 38.0, 0, 0, 0], 'result': 1}, {'input': [2, 1, 27.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 33.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 6.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 17.0, 1, 0, 2], 'result': 0}, {'input': [2, 0, 34.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 50.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 27.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 30.0, 3, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 0, 0, 1], 'result': 1}, {'input': [2, 0, 25.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 25.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 29.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 11.0, 0, 0, 0], 'result': 0}, {'input': [2, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 28.5, 0, 0, 2], 'result': 0}, {'input': [3, 1, 48.0, 1, 3, 2], 'result': 0}, {'input': [1, 0, 35.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 36.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 21.0, 2, 2, 0], 'result': 1}, {'input': [3, 0, 24.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 31.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 70.0, 1, 1, 2], 'result': 0}, {'input': [3, 0, 16.0, 1, 1, 2], 'result': 0}, {'input': [2, 1, 30.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 19.0, 1, 0, 2], 'result': 0}, {'input': [3, 0, 31.0, 0, 0, 1], 'result': 0}, {'input': [2, 1, 4.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 6.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 33.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 48.0, 1, 2, 2], 'result': 1}, {'input': [2, 0, 0.67000000000000004, 1, 1, 2], 'result': 1}, {'input': [3, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 34.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 33.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 41.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 20.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 36.0, 1, 2, 2], 'result': 1}, {'input': [3, 0, 16.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 51.0, 1, 0, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 1, 30.5, 0, 0, 1], 'result': 0}, {'input': [3, 0, 0.0, 1, 0, 1], 'result': 0}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 48.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 57.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [2, 1, 54.0, 1, 3, 2], 'result': 1}, {'input': [3, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 1, 5.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [1, 1, 43.0, 0, 1, 2], 'result': 1}, {'input': [3, 1, 13.0, 0, 0, 0], 'result': 1}, {'input': [1, 1, 17.0, 1, 0, 2], 'result': 1}, {'input': [1, 0, 29.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 1, 2, 2], 'result': 0}, {'input': [3, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 18.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 8.0, 4, 1, 1], 'result': 0}, {'input': [3, 0, 1.0, 1, 2, 2], 'result': 1}, {'input': [1, 0, 46.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [2, 0, 16.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 0.0, 8, 2, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 39.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 49.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 31.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 30.0, 0, 0, 0], 'result': 0}, {'input': [3, 1, 30.0, 1, 1, 2], 'result': 0}, {'input': [2, 0, 34.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 31.0, 1, 1, 2], 'result': 1}, {'input': [1, 0, 11.0, 1, 2, 2], 'result': 1}, {'input': [3, 0, 0.41999999999999998, 0, 1, 0], 'result': 1}, {'input': [3, 0, 27.0, 0, 0, 2], 'result': 1}, {'input': [3, 0, 31.0, 0, 0, 2], 'result': 0}, {'input': [1, 0, 39.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 18.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 39.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 33.0, 1, 0, 2], 'result': 1}, {'input': [3, 0, 26.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 39.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 35.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 6.0, 4, 2, 2], 'result': 0}, {'input': [3, 0, 30.5, 0, 0, 2], 'result': 0}, {'input': [1, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 23.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 31.0, 1, 1, 0], 'result': 0}, {'input': [3, 0, 43.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 10.0, 3, 2, 2], 'result': 0}, {'input': [1, 1, 52.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 27.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 38.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 27.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 2.0, 4, 1, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 1.0, 0, 2, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 1], 'result': 1}, {'input': [1, 1, 62.0, 0, 0, 0], 'result': 1}, {'input': [3, 1, 15.0, 1, 0, 0], 'result': 1}, {'input': [2, 0, 0.82999999999999996, 1, 1, 2], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 23.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 18.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 39.0, 1, 1, 0], 'result': 1}, {'input': [3, 0, 21.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 32.0, 0, 0, 2], 'result': 1}, {'input': [1, 0, 0.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 16.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 30.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 34.5, 0, 0, 0], 'result': 0}, {'input': [3, 0, 17.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 42.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 8, 2, 2], 'result': 0}, {'input': [3, 0, 35.0, 0, 0, 0], 'result': 0}, {'input': [2, 0, 28.0, 0, 1, 2], 'result': 0}, {'input': [1, 1, 0.0, 1, 0, 0], 'result': 1}, {'input': [3, 0, 4.0, 4, 2, 2], 'result': 0}, {'input': [3, 0, 74.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 9.0, 1, 1, 0], 'result': 0}, {'input': [1, 1, 16.0, 0, 1, 2], 'result': 1}, {'input': [2, 1, 44.0, 1, 0, 2], 'result': 0}, {'input': [3, 1, 18.0, 0, 1, 2], 'result': 1}, {'input': [1, 1, 45.0, 1, 1, 2], 'result': 1}, {'input': [1, 0, 51.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 24.0, 0, 3, 0], 'result': 1}, {'input': [3, 0, 0.0, 0, 0, 0], 'result': 0}, {'input': [3, 0, 41.0, 2, 0, 2], 'result': 0}, {'input': [2, 0, 21.0, 1, 0, 2], 'result': 0}, {'input': [1, 1, 48.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 8, 2, 2], 'result': 0}, {'input': [2, 0, 24.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 42.0, 0, 0, 2], 'result': 1}, {'input': [2, 1, 27.0, 1, 0, 0], 'result': 1}, {'input': [1, 0, 31.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 4.0, 1, 1, 2], 'result': 1}, {'input': [3, 0, 26.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 47.0, 1, 1, 2], 'result': 1}, {'input': [1, 0, 33.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 47.0, 0, 0, 2], 'result': 0}, {'input': [2, 1, 28.0, 1, 0, 0], 'result': 1}, {'input': [3, 1, 15.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 20.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 19.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 0.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 56.0, 0, 1, 0], 'result': 1}, {'input': [2, 1, 25.0, 0, 1, 2], 'result': 1}, {'input': [3, 0, 33.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 22.0, 0, 0, 2], 'result': 0}, {'input': [2, 0, 28.0, 0, 0, 2], 'result': 0}, {'input': [3, 0, 25.0, 0, 0, 2], 'result': 0}, {'input': [3, 1, 39.0, 0, 5, 1], 'result': 0}, {'input': [2, 0, 27.0, 0, 0, 2], 'result': 0}, {'input': [1, 1, 19.0, 0, 0, 2], 'result': 1}, {'input': [3, 1, 0.0, 1, 2, 2], 'result': 0}, {'input': [1, 0, 26.0, 0, 0, 0], 'result': 1}, {'input': [3, 0, 32.0, 0, 0, 1], 'result': 0}]


if __name__ == "__main__":
    def knngaussian(d,v):
        return weightedknn(d,v,k=4,weightf=gaussian)
    
    costf=createcostfunction(knngaussian,datalist)
    
    try:
        import psyco
        psyco.full()
    except:
        print 'Unable to import psyco'
    
    domain=[(0,10)]*6
    paused=raw_input('Press <ENTER> to annealingoptimize')
    a=annealingoptimize(domain,costf,step=2)
    print a
    paused=raw_input('Press <ENTER> to geneticoptimize')
    a=geneticoptimize(domain,costf,popsize=5,step=2,elite=0.2,maxiter=20)
    print a
    paused=raw_input('Press <ENTER> to hillclimb')
    a=hillclimb(domain,costf)
    print a
    paused=raw_input('Press <ENTER> to randomrestart_annealing')
    a=randomrestart_annealing(domain,costf,T1=10000.0,cool=0.95,step=2,maxiter=100)
    print a


"""
-----------------------------------------------------------------------------------
#######################
# The data dictionary #
#######################
This is an Anonymized verzion of the Dataset.

"input"
*******
 0 - 1:upper,2:middle,3:lower class
 1 - 0:male, 1:female
 2 - age
 3 - number of spouses and siblings onboard
 4 - number of parents and children onboard
 5 - point of departure 0:Cherbourg, 1:Queenstown, 2:Southhampton

"result"
********
 0 - Died
 1 - Survived

[8, 0, 0, 7, 1, 3]   - annealing
[9, 3, 2, 6, 2, 1]
[6, 5, 2, 2, 0, 9]

"""
