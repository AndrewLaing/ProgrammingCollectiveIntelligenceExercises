""" Chapter 11 Exercise 1: More function types.

    We started with a very short list of functions. What other functions can you think of?
    Implement a Euclidean distance node with four parameters.

    Starting with the distance and weighting functions in the pdf....
    Think of a mathematical formula I can probably add it :D
    Basically you can adapt any parameter/constant taking function and adapt it to work with gp.
"""

def euclidean(l):
    p=l[:2]
    q=l[2:]
    sumSq=0.0
    for i in range(len(p)):
        sumSq+=(p[i]-q[i])**2
    # take the square root
    return int(sumSq**0.5)

eucw=fwrapper(euclidean,4,'euclidean')


def manhattan(l):
    v1=l[:2]
    v2=l[2:]
    d = 0.0
    for i in range(len(v1)):
        d += abs(v1[i]-v2[i])
    return int(d)

manw=fwrapper(manhattan,4,'manhattan')


def variance(l):
    mean=float(sum(l))/len(l)
    s=sum([(v-mean)**2 for v in l])
    return int(s/len(l))

varw=fwrapper(variance,4,'variance')


# Returns potentially larger values
def dotproduct(l):
    a=l[:2]
    b=l[2:]
    return sum([a[i]*b[i] for i in range(len(a))])

dotw=fwrapper(dotproduct,4,'dotproduct')


# Returns -1 0 or 1
def pearson(l):
    x=l[:2]
    y=l[2:]
    n=len(x)
    vals=range(n)
    sumx=sum([float(x[i]) for i in vals])
    sumy=sum([float(y[i]) for i in vals])
    sumxSq=sum([x[i]**2.0 for i in vals])
    sumySq=sum([y[i]**2.0 for i in vals])
    pSum=sum([x[i]*y[i] for i in vals])
    num=pSum-(sumx*sumy/n)
    den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**0.5
    
    if den==0: 
        return 0
    r=num/den
    return int(r)

pearw=fwrapper(pearson,4,'pearson')


# Returns either 0 3 or 10 
def tanimoto(l):
    a=l[:2]
    b=l[2:]
    c=[v for v in a if v in b]
    
    if len(a)+len(b)-len(c)==0: 
        return 0
    return int(10*(float(len(c))/(len(a)+len(b)-len(c))))

taniw=fwrapper(tanimoto,4,'tanimoto')


def weightedmean(l):
    x=l[:2]
    w=l[2:]
    num=sum([x[i]*w[i] for i in range(len(w))])
    den=sum([w[i] for i in range(len(w))])
    
    if den==0: 
        return 0
    return int(num/den)

weiw=fwrapper(weightedmean,4,'weightedmean')


# Returns either 7 11 or 20
def giniimpurity(l):
    total=len(l)
    counts={}
    
    for item in l:
        counts.setdefault(item,0)
        counts[item]+=1
    
    imp=0
    
    for j in l:
        f1=float(counts[j])/total
        for k in l:
            if j==k: 
                continue
            f2=float(counts[k])/total
            imp+=f1*f2
    return int(imp*10.0)

giniw=fwrapper(giniimpurity,4,'gini')


# Returns 0 1 2 3 or 4
def entropy(l):
    from math import log
    log2=lambda x:log(x)/log(2)
    total=len(l)
    counts={}
    
    for item in l:
        counts.setdefault(item,0)
        counts[item]+=1
    ent=0
    
    for i in counts:
        p=float(counts[i])/total
        ent-=p*log2(p)
    return int(ent*2.0)

entw=fwrapper(entropy,4,'entropy')


def topnum(l):
    return max(l)

topw=fwrapper(topnum,4,'topnum')


def bottomnum(l):
    return min(l)

botw=fwrapper(bottomnum,4,'bottomnum')


def hiddenfunction(l):
    x=max(l)
    y=min(l)
    return x**2+2*y+3*x+5

hidw=fwrapper(hiddenfunction,4,'hiddenfunction')

