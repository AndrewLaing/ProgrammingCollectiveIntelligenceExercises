""" Chapter 5 Exercise 2: Annealing Starting Points.

    The outcome of simulated annealing depends heavily on the starting point. 
    Build a new optimization function that does simulated annealing from multiple starting solutions 
    and returns the best one.

"""

def randomrestart_annealing(domain,costf,T1=10000.0,cool=0.95,step=1,maxiter=100):
    T = T1
    best=999999999
    bestr=None
    for i in range(maxiter):
        # Initialize the values randomly
        vec=[(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
        
        while T>0.1:
            # Choose one of the indices
            i=random.randint(0,len(domain)-1)

            # Choose a direction to change it
            dir=random.randint(-step,step)

            # Create a new list with one of the values changed
            vecb=vec[:]
            vecb[i]+=dir
            if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
            elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]

            # Calculate the current cost and the new cost
            ea=costf(vec)
            eb=costf(vecb)
            p=pow(math.e,(-eb-ea)/T)

            # Is it better, or does it make the probability cutoff?
            if (eb<ea or random.random()<p):
                vec=vecb

            # Decrease the temperature
            T=T*cool
            
        cost = costf(vec)

        # reinitialize the variable T
        T = T1
        
        if cost<best:
            best=cost
            bestr=vec
    
    return bestr
