""" This is a version of Chapter 11 Exercise 2 for use with psyco that speeds it up somewhat :)
    Note display1 added to the classes is to output a nested list of the tree to
    make it a bit easier to recreate the outputted function.
"""

from random import random,randint,choice
from copy import deepcopy
from math import log
import os as os


class fwrapper:
    def __init__(self,function,childcount,name):
        self.function=function
        self.childcount=childcount
        self.name=name


class node:
    def __init__(self,fw,children):
        self.function=fw.function
        self.name=fw.name
        self.children=children

    def evaluate(self,inp):
        results=[n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self,indent=0):
        print (' '*indent)+self.name
        for c in self.children:
            c.display(indent+1)

    def display1(self):
        list1=[]
        list1.append(self.name)
        list2=[]
        for c in self.children:
            list2.append(c.display1())
        list1.append(list2)
        return list1


class paramnode:
    def __init__(self,idx):
        self.idx=idx

    def evaluate(self,inp):
        return inp[self.idx]

    def display(self,indent=0):
        print '%sp%d' % (' '*indent,self.idx)

    def display1(self):
        return 'p%d' % self.idx
        
        
class constnode:
    def __init__(self,v):
        self.v=v

    def evaluate(self,inp):
        return self.v

    def display(self,indent=0):
        print '%s%d' % (' '*indent,self.v)

    def display1(self):
        return self.v


addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')


def iffunc(l):
    if l[0]>0: 
        return l[1]
    else: 
        return l[2]

ifw=fwrapper(iffunc,3,'if')


def iffunc1(l):
    if l[0]>l[1] and l[0]<l[2]: 
        return 1
    elif l[0]>l[2] and l[0]<l[1]: 
        return 1
    else: 
        return 0

ifw1=fwrapper(iffunc1,3,'if1')


def iffunc2(l):
    lst1=[l[1],l[2]]
    if max(lst1)-min(lst1)>l[0]: 
        return 1
    else: 
        return 0

ifw2=fwrapper(iffunc2,3,'if2')


def isgreater(l):
    if l[0]>l[1]: 
        return 1
    else: 
        return 0

gtw=fwrapper(isgreater,2,'isgreater')


# Returns either 1 or 6
def tanimoto(l):
    v1=l[:2]
    v2=l[2:]
    c1,c2,shr=0,0,0
    
    for i in range(len(v1)):
        if v1[i]!=0: c1+=1
        if v2[i]!=0: c2+=1
        if v1[i]!=0 and v2[i]!=0: shr+=1
    
    return int((1.0-(float(shr)/(c1+c2-shr+0.00001))*10)%10)

taniw=fwrapper(tanimoto,4,'tanimoto')


def euclidean(l):
    p=l[:2]
    q=l[2:]
    sumSq=0.0
    
    for i in range(len(p)):
        sumSq+=(p[i]-q[i])**2
    
    # take the square root
    return int(sumSq**0.5)

eucw=fwrapper(euclidean,4,'euclidean')

flist=[addw,mulw,ifw,gtw,subw]
# flist=[addw,mulw,ifw,ifw1,ifw2,gtw,subw,eucw,taniw]


def exampletree():
    return node(ifw,[
                    node(gtw,[paramnode(0),constnode(3)]),
                    node(addw,[paramnode(1),constnode(5)]),
                    node(subw,[paramnode(1),constnode(2)]),
                    ]
                )

                
def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
    if random()<fpr and maxdepth>0:
        f=choice(flist)
        children=[makerandomtree(pc,maxdepth-1,fpr,ppr)
                  for i in range(f.childcount)]
        return node(f,children)
    elif random()<ppr:
        return paramnode(randint(0,pc-1))
    else:
        return constnode(randint(0,10))


def hiddenfunction(x,y):
    return x**2+2*y+3*x+5


def buildhiddenset():
    rows=[]
    for i in range(200):
        x=randint(0,40)
        y=randint(0,40)
        rows.append([x,y,hiddenfunction(x,y)])
    return rows


def scorefunction(tree,s):
    dif=0
    for data in s:
        v=tree.evaluate([data[0],data[1]])
        dif+=abs(v-data[2])
    return dif


def mutate(t,pc,probchange=0.1):
    if random()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
        if hasattr(t,"children"):
            result.children=[mutate(c,pc,probchange) for c in t.children]
        return result


def mutateRandomNode(t,pc,probchange):
    if not hasattr(t,"children") or random() < probchange:
        if isinstance(t,paramnode):
            a=randint(0,pc-1)
            return paramnode(a)
        elif isinstance(t,constnode):
            a=randint(0,10)   
            return constnode(a)
        else:
            return makerandomtree(pc)
    else:
        c = randint(0,len(t.children)-1)
        t.children[c]=mutateRandomNode(t.children[c],pc,probchange)
    return t


def newMutate(t,pc,probchange):
    frog=deepcopy(t)
    mutateRandomNode(frog,2,probchange) 
    return frog


def crossover(t1,t2,probswap=0.7,top=1):
    if random()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
        if hasattr(t1, 'children') and hasattr(t2, 'children'): 
            result.children=[crossover(c,choice(t2.children),probswap,0)
                             for c in t1.children]
        return result


def getrankfunction(dataset):
    def rankfunction(population):
        scores=[(scorefunction(t,dataset),t) for t in population]
        scores.sort()
        return scores
    return rankfunction


def evolve(pc,popsize,rankfunction,maxgen=500,mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
    # Returns a random number, tending towards lower numbers.
    # The lower pexp is, more lower numbers you will get
    def selectindex(lenscores):
        while True:
            # Stop selectindex() from returning numbers out of index.
            ind =  int(log(random())/log(pexp))
            if (ind-lenscores>(lenscores*2)-1) or (ind>lenscores): 
                pass
            else: 
                return ind

    # Create a random initial population
    population=[makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores=rankfunction(population)
        print scores[0][0]
        if scores[0][0]==0: 
            break
        
        # The two best will always make it
        newpop=[scores[0][1],scores[1][1]]

        # Build the next generation
        while len(newpop)<popsize:
            if random()>pnew:
                newpop.append(newMutate(
                                crossover(scores[selectindex(len(scores))][1],
                                        scores[selectindex(len(scores))][1],
                                        probswap=breedingrate),
                                pc,probchange=mutationrate))
            else:
                # Add a random node to mix things up
                newpop.append(makerandomtree(pc))
        population=newpop
    scores[0][1].display()
    return scores[0][1]


if __name__ == "__main__":
    try:
        import psyco
        psyco.full()
    except ImportError:
        print 'Unable to import psyco'

    rf = getrankfunction(buildhiddenset())
    frog = evolve(2,500,rf,mutationrate=0.2,breedingrate=0.1,pexp=0.7,pnew=0.3)
    print "frog =",frog.display1()
