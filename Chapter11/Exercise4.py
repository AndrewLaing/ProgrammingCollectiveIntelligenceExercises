""" Chapter 11 Exercise 4: Stopping evolution.

    Add an additional criteria to evolve that stops the process and returns the best result 
    if the best score hasn't been improved within X generations

    Implemented with the variable stopnumber :)

"""

def evolve(pc,popsize,rankfunction,stopnumber=12,maxgen=500,mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):
    def selectindex(lenscores):
        while True:
            # Stop selectindex() from returning numbers out of index.
            ind =  int(log(random())/log(pexp))
            if (ind-lenscores>(lenscores*2)-1) or (ind>lenscores): 
                pass
            else: 
                return ind

    population=[makerandomtree(pc) for i in range(popsize)]

    # Add exit if no improvement within X generations
    lastbestscore = 999999999
    repeatcount=0

    for i in range(maxgen):
        scores=rankfunction(population)
        print scores[0][0]
        if scores[0][0]==0: 
            break

        # Add exit if no improvement within X generations
        if (scores[0][0]==lastbestscore) and (repeatcount==stopnumber-1):
            break
        elif (scores[0][0]==lastbestscore) and (repeatcount!=stopnumber-1):
            repeatcount+=1
        else:
            repeatcount=0
        lastbestscore=scores[0][0]

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
  
