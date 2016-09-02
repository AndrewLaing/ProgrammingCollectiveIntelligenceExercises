""" Chapter 11 Exercise 2: Replacement mutation.

    Implement a mutation proceedure that chooses a random node on the tree and changes it.
    Make sure it deals with function, constant and parameter nodes.
    How is evolution affected by using this function instead of the branch replacement?
    *see end

"""

import gp as gp
from random import random,randint
from copy import deepcopy


def mutateRandomNode(t,pc,probchange):
    if not hasattr(t,"children") or random.random() < probchange:
        if isinstance(t,paramnode):
            a = random.randint(0,pc-1)
            return paramnode(a)
        elif isinstance(t,constnode):
            a = random.randint(0,10)   
            return constnode(a)
        else:
            return makerandomtree(pc)
    else:
        c = random.randint(0,len(t.children)-1)
        t.children[c] = mutateRandomNode(t.children[c],pc,probchange)
    return t


def newMutate(t,pc,probchange):
    t1 = deepcopy(t)
    mutateRandomNode(t1,2,probchange) 
    return t1


exampletree = gp.exampletree()
test = newMutate(exampletree,2,0.1)
test.display()


"""
    The newMutate() function in general do not mutate programs to a much greater length
    percentagewise because there is less chance of a new function node being created.
    Sometimes it seems to get stuck on a certain level, probably because not
    enough diversity is being introduced, especially if it is trying to mutate long
    programs only changing one parameter at a time... easily corrected by highering
    the pnew parameter. Conversely though if it finds the beginnings of a good program sometimes
    it is likely to find the solution faster for the same reason.
"""
