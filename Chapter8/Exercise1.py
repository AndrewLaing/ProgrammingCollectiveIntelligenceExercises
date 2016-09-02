""" 
    Chapter 8 Exercise 1: Optimizing the number of neighbors.
    Create a cost function for optimization that determines the ideal number of neighbors for a sample dataset

    Seems as though we are only optimizing one value, I just wrote a function that goes through a range of values 
    for k and returns a dictionary of the best k's from the trials
    
    See end for usage.
"""

def best_k(min_k,max_k,trials,costf):
    dic={}
    
    for f in range(trials):
        best=1000000
        bestx=0
        
        for x in range(min_k,max_k+1):
            def knn_est(d,v): return costf(d,v,k=x)
            cost = numpredict.crossvalidate(knn_est,data)
            if cost<best:
                best=cost
                bestx=x
        
        print 'best cost =',best,' and best k =',bestx
        
        if bestx not in dic: 
            dic[bestx]=0
        
        dic[bestx]+=1
    
    return dic


"""
------------------------------------------------------------------------------------
    Usage:
    import best_k as best_k
    import numpredict as numpredict
    data = numpredict.wineset1()
    best_k.best_k(1,5,100,numpredict.knnestimate)
    best_k.best_k(6,12,20,numpredict.weightedknn)
"""
