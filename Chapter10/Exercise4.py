""" Chapter 10 Exercise 4: Stopping criteria.

    The NMF algorithm in this chapter stops when the cost has dropped to 0 or when it reaches 
    the maximum number of iterations.
    Sometimes improvement will almost entirely stop once a very good though not perfect solution has been reached.
    Modify the code so it stops when the cost is not improving by more than one percent per iteration

"""

def factorize(v, pc=10, iter=50):
    ic, fc = shape(v)
    cost=0
    previouscost = 9999999999999
    w = matrix([[random.random() for j in range(pc)] for i in range(ic)])
    h = matrix([[random.random() for i in range(fc)] for i in range(pc)])

    for i in range(iter):
        wh = w * h

        cost = difcost(v, wh)
        if i % 10 == 0:
            print("%d: %f" % (i, cost))

        if cost == 0 or math.isnan(cost):
            print("%d: %f" % (i, cost))
            break

        hn = transpose(w) * v
        hd = transpose(w) * w * h
        h = matrix(array(h) * array(hn) / array(hd))

        wn = v * transpose(h)
        wd = w * h * transpose(h)

        # RuntimeWarning: invalid value encountered in divide
        wn = [[1e-20 if (x - 1e-20 < 0) else x for x in lst] for lst in wn.tolist()]
        wd = [[1e-20 if (x - 1e-20 < 0) else x for x in lst] for lst in wd.tolist()]

        w = matrix(array(w) * array(wn) / array(wd))

        if i == 0: 
            pass
        else:
            if (previouscost-cost)/previouscost < 0.01:
                print("%d: %f" % (i, cost)),'\nCost improved by less than 1%'
                break
        
        previouscost = cost

    return w, h
    
