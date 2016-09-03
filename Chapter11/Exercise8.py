""" Chapter 11 Exercise 8: Nodes with datatypes.

   "Some ideas were provided in this chapter about implementing nodes with mixed data types.
    Implement this and see if you can evolve a program that learns to return the second, third, 
    sixth and seventh characters of a string (e.g., "genetic" becomes "enic".)"

    See *end for usage
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


class paramnode:
    def __init__(self,idx):
        self.idx=idx

    def evaluate(self,inp):
        return inp[self.idx]

    def display(self,indent=0):
        print '%sp%d' % (' '*indent,self.idx)


# String functions that only take a list of string/s as arguements
# So I removed constnode


# simple split first half
def zerozerozero(l):
    if len(l[0])>1:
        return l[0][len(l[0])/2:]
    else: return l[0]

zerozerozero=fwrapper(zerozerozero,1,'split1')


# simple split second half
def zerozero(l):
    if len(l[0])>1:
        return l[0][:len(l[0])/2]
    else: return l[0]

zerozero=fwrapper(zerozero,1,'split2')


# simple concat
def zero(l):
    return l[0]+l[1]
zero=fwrapper(zero,2,'concat1')


# mix two together
def one(l):
    a0=l[0][:(len(l[0])/2)]
    
    if len(a0)==0: 
        a0 = l[0]
    
    a1=l[1][(len(l[1])/2):]
    
    if len(a1)==0: 
        a0 = l[1]
    
    return a0+a1


one=fwrapper(one,2,'concat2')


# return 'middle' letter
def two(l):
    a0=l[0][(len(l[0])/2)]
    
    if len(a0)==0: 
        a0 = l[0]
    return a0


two=fwrapper(two,1,'two')


# return first letter
def three(l):
    return l[0][0]

three=fwrapper(three,1,'three')


# return last letter
def four(l):
    return l[0][-1]

four=fwrapper(four,1,'four')


# return index[0]
def six(l):
        return l[0][0]

six=fwrapper(six,1,'six')


# return index[1]
def seven(l):
    if len(l[0])>1:
        return l[0][1]
    else:
        return l[0]

seven=fwrapper(seven,1,'seven')


# return index[2]
def eight(l):
    if len(l[0])>2:
        return l[0][2]
    else:
        return l[0]

eight=fwrapper(eight,1,'eight')


# return index[3]
def nine(l):
    if len(l[0])>3:
        return l[0][3]
    else:
        return l[0]

nine=fwrapper(nine,1,'nine')


# return index[4]
def ten(l):
    if len(l[0])>4:
        return l[0][4]
    else:
        return l[0]

ten=fwrapper(ten,1,'ten')


# return index[5]
def eleven(l):
    if len(l[0])>5:
        return l[0][5]
    else:
        return l[0]

eleven=fwrapper(eleven,1,'eleven')


# return index[6]
def twelve(l):
    if len(l[0])>6:
        return l[0][6]
    else:
        return l[0]

twelve=fwrapper(twelve,1,'twelve')


# return even indexes
def thirteen(l):
    res=""
    count=0
    for a in l[0]:
        if count%2==0: 
            res+=a
        count+=1
    if len(res)==0: 
        return l[0]
    else: 
        return res

thirteen=fwrapper(thirteen,1,'thirteen')


# return odd indexes
def fourteen(l):
    res=""
    count=1
    for a in l[0]:
        if count%2==0: 
            res+=a
        count+=1
    if len(res)==0: 
        return l[0]
    else: 
        return res

fourteen=fwrapper(fourteen,1,'fourteen')


# triple concat
def fifteen(l):
    return l[0]+l[1]+l[2]

fifteen=fwrapper(fifteen,3,'concat3')


# quad concat
def sixteen(l):
    return l[0]+l[1]+l[2]+l[3]

sixteen=fwrapper(sixteen,4,'concat4')

# return first two letters
def seventeen(l):
    if len(l[0])>2: 
        return l[0][:2]
    else: 
        return l[0]

seventeen=fwrapper(seventeen,1,'split3')


# return first two letters
def eighteen(l):
    if len(l[0])>2: 
        return l[0][-2:]
    else: 
        return l[0]

eighteen=fwrapper(eighteen,1,'split4')


# return two letters from index[2] to [4]
def nineteen(l):
    if len(l[0])>4: 
        return l[0][2:4]
    else: 
        return l[0]

nineteen=fwrapper(nineteen,1,'split5')


# return two letters from index[2] to [4]
def twenty(l):
    if len(l[0])>5: 
        return l[0][3:5]
    else: 
        return l[0]

twenty=fwrapper(twenty,1,'split6')


# return two letters from index[2] to [4]
def twentyone(l):
    if len(l[0])>6: 
        return l[0][4:6]
    else: 
        return l[0]

twentyone=fwrapper(twentyone,1,'split7')


# make l[0] repeat itself eg fru becomes frufru
def twentytwo(l):
    return l[0]*2

twentytwo=fwrapper(twentytwo,1,'double')


# trim l[0] to len(7)
def twentythree(l):
    if len(l[0])>7: 
        return l[0][:7]
    else: 
        return l[0]

twentythree=fwrapper(twentythree,1,'trim')

    
flist=[zerozerozero,zerozero,zero,one,two,three,four,six,seven,eight,nine,ten,eleven,twelve,
       thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo]


def exampletree():
    return node(zero,[node(zero,[node(seven,[paramnode(0)]),
                                 node(eight,[paramnode(0)])]),
                      node(zero,[node(eleven,[paramnode(0)]),
                                 node(twelve,[paramnode(0)])])])

                
def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
    if random()<fpr and maxdepth>0:
        f=choice(flist)
        children=[makerandomtree(pc,maxdepth-1,fpr,ppr)
                  for i in range(f.childcount)]
        return node(f,children)
    else:
        return paramnode(randint(0,pc-1))


######################### New score functions #################################

def scorefunction(tree,data):
    dif=0
    v=tree.evaluate([data[0]])
    dif+=score_it(v,data[2])     
    v=tree.evaluate([data[1]])
    dif+=score_it(v,data[2]) 
    return dif


def score_it(v,answer):
    dif=0
    if len(v)!=len(answer): dif+=10
    for a in answer:
        if a not in v:
            dif+=5
    if len(v)<len(answer): f0, f1 = v, answer
    else: f0, f1 = answer, v
    for a in range(len(f0)):
        if f0[a]!=f1[a]:
            dif+=1
    return dif

###############################################################################

def mutate(t,pc,probchange=0.1):
    if random()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
        if hasattr(t,"children"):
            result.children=[mutate(c,pc,probchange) for c in t.children]
        return result


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
    def selectindex(lenscores):
        while True:
            # Stop selectindex() from returning numbers out of index.
            ind =  int(log(random())/log(pexp))
            if (ind-lenscores>(lenscores*2)-1) or (ind>lenscores): pass
            else: return ind

    population=[makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores=rankfunction(population)
        print scores[0][0]
        if scores[0][0]==0: break
        
        newpop=[scores[0][1],scores[1][1]]

        while len(newpop)<popsize:
            if random()>pnew:
                newpop.append(mutate(
                                crossover(scores[selectindex(len(scores))][1],
                                        scores[selectindex(len(scores))][1],
                                        probswap=breedingrate),
                                pc,probchange=mutationrate))
            else:
                newpop.append(makerandomtree(pc))
        population=newpop
    scores[0][1].display()
    return scores[0][1]


"""
------------------------------------------------------------------------------
#########
# USAGE #
#########

import gp_ex8 as gp
random1=gp.makerandomtree(1)
exampletree=gp.exampletree()  

# use the word, a longer version of the word and the desired result to ensure
# that it is returning letters from specific indexes. I recommend using rainbow
# because it has no repeating letters (special,entropy,frogspawn,sexuality,...)

rf=gp.getrankfunction(['rainbow','rainbows','aiow'])
winner=gp.evolve(1,500,rf,mutationrate=0.4,breedingrate=0.6,pexp=0.4,pnew=0.5)

winner.evaluate(['genetic'])

-------------------------------------------------------------------------------

I used a lot of functions, but by looking at the results I can eliminate the
rarely used one or even add weights to the useful looking ones :)

Then we evolved a winner too...

concat4
 seven
  p0
 eight
  p0
 eleven
  concat3
   concat1
    p0
    eight
     twelve
      split4
       split5
        p0
   p0
   p0
 split1
  twelve
   p0

"""
