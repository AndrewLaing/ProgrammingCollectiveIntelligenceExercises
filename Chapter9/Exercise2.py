""" 
    Chapter 9 Exercise 2: Optimizing a dividing line.

    "Do you think it's possible to choose a dividing line using the optimization methods you learned in chapter 5, 
    instead of just using the averages?
    What cost function would you use?"

    I created a cost function and a method to create a rescaled avgs for use with dpclassify()
    I cross-validate by checking the result supplied by dpclassify() against agesonly[X].match
     for the entire dataset.
"""

import optimization as optimization
from copy import deepcopy
import advancedclassify1 as advancedclassify
agesonly=advancedclassify.loadmatch('agesonly.csv',allnum=True)

# cost function
def createcostfunction1(data):
    avgs=advancedclassify.lineartrain(data)
    
    def costf(scale):
        print "scale =",scale
        savgs = deepcopy(avgs)
        
        for a in savgs:
            for b in range(len(savgs[a])):
                savgs[a][b]+=scale[b]        # rescale avgs
        error=0                              # calculate error 
        
        for a in range(len(data)):
            pred = advancedclassify.dpclassify(data[a].data,savgs)
            b = data[a].match
            if pred!=b: 
                error +=1
        return error
    
    return costf



# function to produce a rescaled avgs after getting the optimized results
def rescale_avgs(data,scale):
    avgs=advancedclassify.lineartrain(data)
    savgs = deepcopy(avgs)
    
    for a in savgs:
        for b in range(len(savgs[a])):
            savgs[a][b]+=scale[b]
    
    return savgs


""" 
-------------------------------------------------------------------------
Usage
-------------------------------------------------------------------------
domain = [(-14,14)]*2
costf = createcostfunction1(agesonly)
optimization.randomoptimize(domain,costf)
optimization.hillclimb(domain,costf)
optimization.geneticoptimize(domain,costf,step=0.25,maxiter=10)

costf([-3,12])
savgs = rescale_avgs(agesonly,[-3,12])
advancedclassify.dpclassify([25,30],savgs)

"""
