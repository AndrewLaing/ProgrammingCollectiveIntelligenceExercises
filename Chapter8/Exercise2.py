""" Chapter 8 Exercise 2: Leave-one-out cross-validation.

    Leave-one-out cross-validation is an alternative method of calculating prediction error that treats 
    every row in the dataset individually as a test set, and treats the rest of the data as a training set.
    Implement a function to do this.
    How does it compare to the method described in this chapter?

    loo_crossvalidate() returns an absolute value whilst crossvalidate() returns a value dependent upon 
    the random selection made in dividedata(), and is faster because it makes less calls to algf. 
    (Unless you set trials=2 in crossvalidate():D ).
    
    See end for Usage
"""

def loo_crossvalidate(algf,data):
    error=0.0
    
    for row in range(len(data)):
        trainset = []
        trainset = trainset+data
        testset=[]
        testset.append(data[row])
        trainset.remove(data[row])
        error+=testalgorithm(algf,trainset,testset)
    
    return error/len(data)


"""
--------------------------------------------------------------------------------------------
    Usage
    *****
Add function to numpredict
import numpredict as numpredict

data=numpredict.wineset1()
numpredict.loo_crossvalidate(numpredict.knnestimate,data)
numpredict.crossvalidate(numpredict.knnestimate,data)
numpredict.loo_crossvalidate(numpredict.weightedknn,data)
numpredict.crossvalidate(numpredict.weightedknn,data)

def knninverse(d,v):
    return numpredict.weightedknn(d,v,weightf=numpredict.inverseweight)

numpredict.loo_crossvalidate(knninverse,data)
numpredict.crossvalidate(knninverse,data)

"""
