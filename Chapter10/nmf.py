""" 
    Non-negative Matrix Factorisation.
    I added this version of NMF that is about 15/20 times faster and in my opinion 
    more accurate in the results it gives - Andrew Laing

    NMF by alternative non-negative least squares using projected gradients
    Author: Chih-Jen Lin, National Taiwan University
    Python/numpy translation: Anthony Di Franco

    Adapted for the Chapter 10 Programming Collective Intelligence by Andrew Laing *see end for usage
"""

import random as random
from numpy import *
from numpy.linalg import norm
from time import time
from sys import stdout

def factorize(v1, pc, maxiter):
    ic, fc = shape(v1)
    temp1=v1.tolist()
    v=array(temp1)

    w = array([[random.random() for j in range(pc)] for i in range(ic)])
    h = array([[random.random() for i in range(fc)] for i in range(pc)])

    wo,ho = nmf(v, w, h, 0.00000001, 900, maxiter)

    temp2=wo.tolist()
    wo1=matrix(temp2)
    temp3=ho.tolist()
    ho1=matrix(temp3)

    return wo1, ho1


def nmf(V,Winit,Hinit,tol,timelimit,maxiter):
    """
    (W,H) = nmf(V,Winit,Hinit,tol,timelimit,maxiter)
    W,H: output solution
    Winit,Hinit: initial solution
    tol: tolerance for a relative stopping condition
    timelimit, maxiter: limit of time and iterations
    """

    W = Winit; H = Hinit; initt = time();

    gradW = dot(W, dot(H, H.T)) - dot(V, H.T)
    gradH = dot(dot(W.T, W), H) - dot(W.T, V)
    initgrad = norm(r_[gradW, gradH.T])
    print 'Init gradient norm %f' % initgrad 
    tolW = max(0.001,tol)*initgrad
    tolH = tolW

    for iter in xrange(1,maxiter):
        # stopping condition
        projnorm = norm(r_[gradW[logical_or(gradW<0, W>0)],
                                 gradH[logical_or(gradH<0, H>0)]])
        
        if projnorm < tol*initgrad or time() - initt > timelimit: 
            break
  
        (W, gradW, iterW) = nlssubprob(V.T,H.T,W.T,tolW,1000)
        W = W.T
        gradW = gradW.T
  
        if iterW==1: 
            tolW = 0.1 * tolW

        (H,gradH,iterH) = nlssubprob(V,W,H,tolH,1000)
        
        if iterH==1: 
            tolH = 0.1 * tolH

        if iter % 10 == 0: 
            stdout.write('.')

    print '\nIter = %d Final proj-grad norm %f' % (iter, projnorm)
    return (W,H)


def nlssubprob(V,W,Hinit,tol,maxiter):
    """
    H, grad: output solution and gradient
    iter: #iterations used
    V, W: constant matrices
    Hinit: initial solution
    tol: stopping tolerance
    maxiter: limit of iterations
    """
 
    H = Hinit
    WtV = dot(W.T, V)
    WtW = dot(W.T, W) 

    alpha = 1; beta = 0.1;
    for iter in xrange(1, maxiter):  
        grad = dot(WtW, H) - WtV
        projgrad = norm(grad[logical_or(grad < 0, H >0)])
        
        if projgrad < tol: 
            break

        # search step size 
        for inner_iter in xrange(1,20):
            Hn = H - alpha*grad
            Hn = where(Hn > 0, Hn, 0)
            d = Hn-H
            gradd = sum(grad * d)
            dQd = sum(dot(WtW,d) * d)
            suff_decr = 0.99*gradd + 0.5*dQd < 0;
            
            if inner_iter == 1:
                decr_alpha = not suff_decr; Hp = H;
            
            if decr_alpha: 
                if suff_decr:
                    H = Hn; break;
                else:
                    alpha = alpha * beta;
            else:
                if not suff_decr or (Hp == Hn).all():
                    H = Hp; break;
                else:
                    alpha = alpha/beta; Hp = Hn;

        if iter == maxiter:
            print 'Max iter in nlssubprob'
    
    return (H, grad, iter)


"""
-------------------------------------------------------------------------------
*************
Example Usage
*************
import newsfeatures as newsfeatures
import nmf
from numpy import *

allw,artw,artt = newsfeatures.getarticlewords()
wordmatrix,wordvec = newsfeatures.makematrix(allw,artw)
v = matrix(wordmatrix)
weights,feat = nmf.factorize(v,pc=20,maxiter=5000)
topp,pn = newsfeatures.showfeatures(weights,feat,artt,wordvec,out='todays_features.txt')
newsfeatures.showarticles(artt,topp,pn,out = 'todays_articles.txt')

-------------------------------------------------------------------------------
*******************************************
Variables in line 20: have fun with them :)
*******************************************
wo,ho = alt_nmf.nmf(v, w, h, tol, timelimit, iter)

    v is the matrix converted to an array
    w and h are the two randomly generated factors of v converted to arrays
    tol is the degree of error allowed before stopping
    timelimit is the time allowed before stopping
    iter the iterations to perform before stopping

The usage of factorize() is the same as using factorize in Chapter 10 but
about 15/20 times faster and it appears more accurate too :D
Note: can be optimized further

"""
