""" Chapter 11 Exercise 7: Tic-tac-toe.

   "Build a tic-tac-toe simulator for your programs to play.
    Set up a tournament similar to the Grid War tournament.
    How well do the programs do? Can they ever learn to play perfectly?"

    Here is the implementation. See *end for usage and notes
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


addw = fwrapper(lambda l:l[0]+l[1],2,'add')
subw = fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw = fwrapper(lambda l:l[0]*l[1],2,'multiply')


def iffunc(l):
    if l[0]>0: 
        return l[1]
    else: 
        return l[2]

ifw = fwrapper(iffunc,3,'if')


def isgreater(l):
    if l[0]>l[1]: 
        return 1
    else: 
        return 0

gtw=fwrapper(isgreater,2,'isgreater')

flist=[addw,mulw,ifw,gtw,subw]
# flist=[addw,mulw,ifw,ifw1,ifw2,gtw,subw,eucw,taniw]
      
                
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
            if (ind-lenscores>(lenscores*2)-1) or (ind>lenscores): pass
            else: return ind

    # Create a random initial population
    population=[makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores=rankfunction(population)
        print scores[0][0]
        if scores[0][0]==0: break
        
        # The two best will always make it
        newpop=[scores[0][1],scores[1][1]]

        # Build the next generation
        while len(newpop)<popsize:
            if random()>pnew:
                newpop.append(mutate(
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


def seeifwinner(player):
    winners=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a in range(len(winners)):
        total=0
        for b in winners[a]:
            if b in player:
                total+=1
            if total==3:
                return 1
    return 0


def print_board(players):
    edges=[2,5]
    for a in range(9):
        if a in players[0]: 
            print 'O',
        elif a in players[1]: 
            print 'X',
        else: 
            print '.',
        if a in edges: 
            print


# Example output [2,-1,0,1,0,0,0,-1,6] 
def getparams(players,i):
    winners=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    list1=[0]*8
    for a in range(len(winners)):
        for b in players[i]:
            if b in winners[a]:
                list1[a]+=1
        for b in players[1-i]:
            if b in winners[a]:
                list1[a]-=1
    return list1


def ttt1(p):
    players =[[],[]]
    possiblemoves=range(9)
    while True:
        for i in range(2):
            pml=len(possiblemoves)     # possible moves left
            if pml==0:
                return -1   # A draw
            boardstate=getparams(players,i)
            boardstate.append(pml)
            move=p[i].evaluate(boardstate)%pml
            players[i].append(possiblemoves[move])
            possiblemoves.remove(possiblemoves[move])
            if seeifwinner(players[i])==1:
                return i


def ttt_tournament(pl):
    # Count losses
    losses=[0 for p in pl]

    # Every player plays every other player
    for i in range(len(pl)):
        for j in range(len(pl)):
            if i==j: 
                continue

            # Who is the winner?
            winner=ttt1([pl[i],pl[j]])

            # Two points for a loss, one point for a tie
            if winner==0:
                losses[j]+=2
            elif winner==1:
                losses[i]+=2
            elif winner==-1:
                losses[i]+=1
                losses[j]+=1
                pass
    # Sort and return the results
    z=zip(losses,pl)
    z.sort()
    return z


def ttt2(p):
    players =[[],[]]
    possiblemoves=range(9)
    print "The board is numbered as follows;\n          012\n          345\n          678"
    letsplay=raw_input('Press <ENTER> to play')
    print '. . .\n. . .\n. . .'
    print "-"*44
    while True:
        for i in range(2):
            pml=len(possiblemoves)     # possible moves left
            if pml==0:
                return -1   # A draw

            if isinstance(p[i],humanplayer):
                move=p[i].evaluate(possiblemoves)
                players[i].append(move)
                possiblemoves.remove(move)
            else:
                boardstate=getparams(players,i)
                boardstate.append(pml)
                move=p[i].evaluate(boardstate)%pml
                players[i].append(possiblemoves[move])
                possiblemoves.remove(possiblemoves[move])

            if seeifwinner(players[i])==1:
                print_board(players)
                return i
            print_board(players)
            print
            print "-"*44


class humanplayer:
    def evaluate(self,possiblemoves):
        # Return whatever the user enters
        print "Possible moves are",possiblemoves
        move=int(raw_input('Enter number >'))
        print "-"*44
        return move


"""
#########
# Usage #
#########

import ttt_gp as gp
winner=gp.evolve(9,40,gp.ttt_tournament,maxgen=10)

gp.ttt1([winner1,winner])

gp.ttt2([winner,gp.humanplayer()])
gp.ttt2([gp.humanplayer(),winner])

-------------------------------------------------------------------------------

#########
# Notes #
#########

boardstate - Needing to find some parameters to send to the programs I came up
             with boardstate. Example [2,-1,0,1,0,0,0,-1,6] 
             The first 8 numbers of boardstate refer to the lines on the board
             in the order shown in the list 'winners'. If the current player
             has a square on that line 1 is added to the value, if the opponent
             has a square on that line 1 is deducted from the value.
             The last number refers to the possible number of moves left

ttt1       - used by ttt_tournament() for program vs program
ttt2       - used for humanplayer vs program

The programs evolved are very predictable at the moment because they have static
algorithms that always react the same way to circumstances. Still, there is
always the chance of evolving (if p8>8: return 1   else: return 0)  :)
"""
