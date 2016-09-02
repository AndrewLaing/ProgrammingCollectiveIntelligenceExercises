""" 
    The graph-plotting functions from Chapter 8 adapted to use GNUPLOT instead of MATPLOTLIB.
    Dependencies gnuplot, gnuplot.py, numpy.
    Gnuplot is a lot lighter than matplotlib and a lot easier to install :)
    
    See end for usage
"""

from numpy import *
import Gnuplot, Gnuplot.funcutils

def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
    t1=arange(0.0,high,0.1)
    cprob=array([probguess(data,vec1,0,v,k,weightf) for v in t1])
    coords=[]
    
    for a in range(len(t1)):
        point=(t1[a],cprob[a])
        coords.append(point)
    
    # plot(t1,cprob) in gnuplot
    g = Gnuplot.Gnuplot(debug=1)
    g.title('Cumulative Graph   ')
    g('set data style lines')
    g.plot(coords)
    t=raw_input('Press enter to continue')


def probabilitygraph(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
    # Make a range for the prices
    t1=arange(0.0,high,0.1)

    # Get the probabilities for the entire range
    probs=[probguess(data,vec1,v,v+0.1,k,weightf) for v in t1]

    # Smooth them by adding the gaussian of the nearby probabilities
    smoothed=[]
    for i in range(len(probs)):
        sv=0.0
        for j in range(0,len(probs)):
            dist=abs(i-j)*0.1
            weight=gaussian(dist,sigma=ss)
            sv+=weight*probs[j]
        smoothed.append(sv)
    
    smoothed=array(smoothed)
    
    coords=[]
    
    for a in range(len(t1)):
        point=(t1[a],smoothed[a])
        coords.append(point)
    
    # plot(t1,smoothed) in gnuplot
    g = Gnuplot.Gnuplot(debug=1)
    g.title('Probability Graph   ')
    g('set data style lines')
    g.plot(coords)
    t=raw_input('Press enter to continue')


"""
--------------------------------------------------------------------------------------
Usage
*****
The usage is the same for the original functions

import numpredict4 as numpredict
data = numpredict.wineset1()

numpredict.cumulativegraph(data,(1,1),200)
numpredict.cumulativegraph(data,(95,3),300)

numpredict.probabilitygraph(data,(1,1),200)
numpredict.probabilitygraph(data,(95,4),300)
"""
