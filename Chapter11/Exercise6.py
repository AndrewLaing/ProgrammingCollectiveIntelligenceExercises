""" Chapter 11 Exercise 6: Grid War player.

    Try to hand design your own tree program that does well at grid war.
    If you find this easy, try to write another completely different one.
    Instead of having a completely random initial population, make it mostly
    random with your hand-designed programs included.
    How do they compare to random programs, and can they be improved with evolution? 

    First I hand-designed three programs.
    Then I altered evolve to take them in a list and add them to the initial population.

    They easily outperformed the initial randomly generated programs and were
    evolved into quite good Grid War players.
"""

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@ HAND-DESIGNED PROGRAMS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

### Hand-designed program 1 ### 
# Keeps out of corners and doesn't repeat last move

def cornw(l):
    if l[0]==0 and l[1]==0:
        a=[1,3]
    
    if l[2] in a: 
        a.remove(l[2])
        return choice(a)
    elif l[0]==0 and l[1]==3:
        a=[3,0]
        if l[2] in a: 
            a.remove(l[2])
        return choice(a)
    elif l[0]==3 and l[1]==0:
        a=[1,2]
        if l[2] in a: a.remove(l[2])
        return choice(a)
    elif l[0]==3 and l[1]==3:
        a=[0,2]
        if l[2] in a: a.remove(l[2])
        return choice(a)
    else:
        a = randint(0,18)%4
        if a==l[2]: a +=1
        return a%4

cornw=fwrapper(cornw,3,'cornw')


def strategy1():
    return node(cornw,[paramnode(0),paramnode(1),paramnode(4)])

-------------------------------
### Hand-designed program 2 ### 
# Follows and doesn't repeat last move

def banzai1(l):
    list1=[]
    if l[1]>l[3]: 
        list1.append(2)
    else: 
        list1.append(3)
    
    if l[0]>l[2]: 
        list1.append(0)
    else: 
        list1.append(1)
    
    if l[4] in list1: 
        list1.remove(l[4])
    
    if len(list1)>0: 
        return choice(list1)
    else:
        a = randint(0,12)%4
        if a==l[4]: 
            a +=1
        return a%4

banzaiw=fwrapper(banzai1,5,'banzaiw')

def strategy2():
    return node(banzaiw,[paramnode(0),paramnode(1),paramnode(2),paramnode(3),paramnode(4)])

-------------------------------
### Hand-designed program 3 ### 
# Like the previous with a probability of changing strategies between following and avoiding.

def scaredy1(l):
    list1=[]
    
    if l[1]<l[3]: 
        list1.append(2)
    else: 
        list1.append(3)
    
    if l[0]<l[2]: 
        list1.append(0)
    else: 
        list1.append(1)
    
    if l[4] in list1: 
        list1.remove(l[4])
    
    if len(list1)>0: 
        return choice(list1)
    else:
        a = randint(0,12)%4
        if a==l[4]: 
            a +=1
        return a%4

scaredyw=fwrapper(scaredy1,5,'scaredyw')

def mix_em(l):
    a = randint(0,5)
    if a==3: 
        return scaredy1(l)
    else: 
        return banzai1(l)

mixemw=fwrapper(scaredy1,5,'scaredyw')

def strategy3():
    return node(mixemw,[paramnode(0),paramnode(1),paramnode(2),paramnode(3),paramnode(4)])

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@ EVOLVE ALTERED TO TAKE NEW PROGRAMS @@@@@@@@@@@@@@@@@@@@@@@@

# Now I altered evolve to take these created functions via 'addsome' that takes a list.

def evolve(pc,popsize,rankfunction,addsome,maxgen=500,mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
    def selectindex(lenscores):
        while True:
            ind =  int(log(random())/log(pexp))
            if (ind-lenscores>(lenscores*2)-1) or (ind>lenscores): 
                pass
            else: return ind

    # Create a random initial population and add addsome to it
    population=[makerandomtree(pc) for i in range(popsize-len(addsome))]
    population+=addsome
    for i in range(maxgen):
        scores=rankfunction(population)
        print scores[0][0]
        
        if scores[0][0]==0: 
            break
        
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
-------------------------------------------------------------------------------------------------------------
# USAGE #

import gp_strategy as gp
strat1 = gp.strategy1()
strat2 = gp.strategy2()
strat3 = gp.strategy3()
addsome = [strat1,strat2,strat3]
winner = gp.evolve(5,70,gp.tournament,addsome,maxgen=20)
gp.gridgame([winner,gp.humanplayer()])

"""
