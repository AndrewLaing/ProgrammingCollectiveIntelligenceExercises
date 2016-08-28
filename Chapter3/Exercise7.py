#
#    --------------------------------------------------------------------
#    scaledown() from clusters.py 
#    rewrote for Collective Intelligence chapter 3 exercise 7
#    in 1D, 3D and 6D versions
#    --------------------------------------------------------------------
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                           1 Dimensional VERSION
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def scaledown_1D(data, distance=pearson, rate=0.01):
    n = len(data)

    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]
    outersum = 0.0

    # Randomly initialize the starting points of the locations in 2D
    loc = [[random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    
    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) for x in range(len(loc[i]))]))

        # Move points
        grad = [[0.0] for i in range(n)]
        errorterm = 0
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                try:
                    # The error is percent difference between the distances
                    errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]

                    # Each point needs to be moved away from or towards the other
                    # point in proportion to how much error it has
                    grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm

                    # Keep track of the total error
                except: pass
                totalerror += abs(errorterm)
        print totalerror

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror<totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate*grad[k][0]

    return loc

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                            3 Dimensional VERSION
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def scaledown_3D(data, distance=pearson, rate=0.01):
    n = len(data)

    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]
    outersum = 0.0

    # Randomly initialize the starting points of the locations in 2D
    # ---------------------ADD DIMENSIONS HERE---------------------------------
    loc = [[random.random(),random.random(),random.random()] for i in range(n)]
    # -------------------------------------------------------------------------
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    
    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) for x in range(len(loc[i]))]))

        # Move points
        # ---------------------ADD DIMENSIONS HERE-----------------------------
        grad = [[0.0, 0.0, 0.0] for i in range(n)]
        # ---------------------------------------------------------------------
        errorterm = 0
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                try:
                    # The error is percent difference between the distances
                    errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]

                    # Each point needs to be moved away from or towards the other
                    # point in proportion to how much error it has
                    # ---------------ADD DIMENSIONS HERE--------------------------
                    grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm           
                    grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
                    grad[k][2] += ((loc[k][2]-loc[j][2])/fakedist[j][k])*errorterm
                    # ------------------------------------------------------------

                    # Keep track of the total error
                except: pass
                totalerror += abs(errorterm)
        print totalerror

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror<totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            # --------------------ADD DIMENSIONS HERE--------------------------
            loc[k][0] -= rate*grad[k][0]
            loc[k][1] -= rate*grad[k][1]
            loc[k][2] -= rate*grad[k][2]
            # -----------------------------------------------------------------
    return loc


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                         6 Dimensional VERSION
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def scaledown_6D(data, distance=pearson, rate=0.01):
    n = len(data)

    # The real distances between every pair of items
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]
    outersum = 0.0

    # Randomly initialize the starting points of the locations in 2D
    # ---------------------ADD DIMENSIONS HERE---------------------------------
    loc = [[random.random(),random.random(),random.random(),random.random(),random.random(),random.random()] for i in range(n)]
    # -------------------------------------------------------------------------
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    
    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) for x in range(len(loc[i]))]))

        # Move points
        # ---------------------ADD DIMENSIONS HERE-----------------------------
        grad = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0] for i in range(n)]
        # ---------------------------------------------------------------------
        errorterm = 0
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                try:
                    # The error is percent difference between the distances
                    errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]

                    # Each point needs to be moved away from or towards the other
                    # point in proportion to how much error it has
                    # ---------------ADD DIMENSIONS HERE--------------------------
                    grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm           
                    grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
                    grad[k][2] += ((loc[k][2]-loc[j][2])/fakedist[j][k])*errorterm
                    grad[k][0] += ((loc[k][3]-loc[j][3])/fakedist[j][k])*errorterm           
                    grad[k][1] += ((loc[k][4]-loc[j][4])/fakedist[j][k])*errorterm
                    grad[k][2] += ((loc[k][5]-loc[j][5])/fakedist[j][k])*errorterm
                    # ------------------------------------------------------------

                    # Keep track of the total error
                except: pass
                totalerror += abs(errorterm)
        print totalerror

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror<totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            # --------------------ADD DIMENSIONS HERE--------------------------
            loc[k][0] -= rate*grad[k][0]
            loc[k][1] -= rate*grad[k][1]
            loc[k][2] -= rate*grad[k][2]
            loc[k][3] -= rate*grad[k][3]
            loc[k][4] -= rate*grad[k][4]
            loc[k][5] -= rate*grad[k][5]
            # -----------------------------------------------------------------
    return loc
