""" Chapter 11 Exercise 3: Random crossover.

    The current crossover function chooses branches from two trees at the same level.
    Write a different crossover function that crosses two random branches.
    How does this affect evolution?

"""

from copy import deepcopy
import random
import gp as gp


def newCrossover(t1,t2,probswap=0.7,top=1):
    if hasattr(t1,'children') and random.random()<probswap and not top:
        return deepcopy(t2),0
    else:
        result=deepcopy(t1)
        result.children=[]
        
        if hasattr(t1, 'children'): 
            for c in t1.children:
                a,b = newCrossover(c,t2,probswap,0)
                if b==0:
                    result.children.append(a)
                    probswap=0.0
                else:
                    result.children.append(c)
        return result,1


def getRandomBranch(t3,probswap,top=1):
   if hasattr(t3,'children') and random.random()<probswap and not top:
       return t3
   else:
       if hasattr(t3,'children'):
           c = random.choice(t3.children)
           return getRandomBranch(c,probswap,0)
       else: return t3

def doNewCrossover(t1,t2,probswap=0.2):
    t3=getRandomBranch(t2,0.3)
    t11=deepcopy(t1)
    a,b=newCrossover(t11,t3,probswap)
    return a


"""
-------------------------------------------------------------------------------
The branches that this function produces may be smaller or larger than
the branches that they replace. If the branches being produced are consistently
longer try reducing the probchange for t3 in doNewCrossover.


============
 Test usage
============
exampletree = gp.exampletree()
exampletree2 = gp.makerandomtree(2)

for a in range(50):
    exampletree2=gp.makerandomtree(2)
    crossed=doNewCrossover(exampletree,exampletree2,probswap=0.2)
    crossed.display()
    print "-"*33


I also tested how the two versions of crossover worked given the same
initial populations. Given the fact that they are both doing their
crossing randomly not surprisingly the results reflected that fact.

All solved within 500 generations.

runtime using original crossover = 63.218499898 seconds.      Shorter
runtime using new crossover      = 20.252122879 seconds.      Longer

runtime using original crossover = 22.112336874 seconds.      Shorter
runtime using new crossover      = 1079.0829510 seconds.      Longer

runtime using original crossover = 513.59018707 seconds.      Shorter
runtime using new crossover      = 168.15006995 seconds.      Longer

runtime using original crossover = 2430.2017447 seconds.      Longer
runtime using new crossover      = 35.639962196 seconds.      Shorter

runtime using original crossover = 574.03915596 seconds.      Shorter
runtime using new crossover      = 50.552052974 seconds.      Longer

"""
