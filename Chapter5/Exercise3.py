""" Chapter 5 Exercise 3: Genetic optimization stopping criteria.

    A function in this chapter runs the genetic optimizer for a fixed number of iterations. 
    Change it so that it stops when there has been no improvement in any of the best solutions for 10 iterations

"""

def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
    currentbest = 0       # Added for Chapter 5 Exercise 3
    count = 0             # Added for Chapter 5 Exercise 3
    
    # Mutation Operation
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        # Corrected so different step values can be added
        if random.random()<0.5 and vec[i]-step>domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i]+step<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
        else:
            return vec           # Corrected otherwise if vec[i] is unsatisfactory nothing returns

    # Crossover Operation
    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]

    # Build the initial population
    pop=[]
    
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
        pop.append(vec)

    # How many winners from each generation?
    topelite=int(elite*popsize)

    # Main loop
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        
        if i == maxiter-1: pass            # Corrected from here for last iteration
        else:
            ranked=[v for (s,v) in scores]

            # Start with the pure winers
            pop=ranked[0:topelite]

            # Add mutated and bred forms of the winners
            while len(pop)<popsize:
                if random.random()<mutprob:

                    # Mutation
                    c=random.randint(0,topelite)
                    pop.append(mutate(ranked[c]))
                else:

                    # Crossover
                    c1=random.randint(0,topelite)
                    c2=random.randint(0,topelite)
                    pop.append(crossover(ranked[c1],ranked[c2]))

            # Print current best score
            print scores[0][0]

            # if there has been no change with best score in 10 iterations exit   # Added for Chapter 5 Exercise 3
            if scores[0][0] == currentbest: count+=1
            else: count = 0
            
            if count == 10:
                return scores[0][1]
                
            currentbest = scores[0][0]

    return scores[0][1]
    
