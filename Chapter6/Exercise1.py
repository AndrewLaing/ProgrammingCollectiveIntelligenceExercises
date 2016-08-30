""" Chapter 6 Exercise 1: Varying assumed probabilities.

    1 Change the classifier class so it supports different assumed probabilities for different features.
      New usage:  cl.weightedprob('quick','good',cl.fprob) # ap is called from db instead
                  cl.get_ap('quick','good')                # returns ap from fc table in db (default is 0.5)
                  cl.set_ap('quick','good',0.89)           # sets the ap
                  cl.set_ap('quick','bad',0.26)           
"""

import re as re
import math as math
from pysqlite2 import dbapi2 as sqlite

def sampletrain(cl):
    cl.train('Nobody owns the water','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmeceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps over the lazy dog','good')

def getwords(doc):
    splitter=re.compile('\\W*')
    # Split the words by non-alpha characters
    words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    # Return the unique set of words only
    return dict([(w,1) for w in words])

class classifier:
    def __init__(self,getfeatures):
        self.getfeatures=getfeatures

    def setdb(self,dbfile):
        self.con=sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count,ap)')
        self.con.execute('create table if not exists cc(category,count)')

    # Increase the count of a feature/category pair
    def incf(self,f,cat):
        count=self.fcount(f,cat)
        
        try:
            if count==0:
                self.con.execute("insert into fc values ('%s','%s',1,0.5)" % (f,cat)) # default ap value is 0.5
            else:
                self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count+1,f,cat))
        except: 
            print "error adding",f,"in category",cat

    def set_ap(self,f,cat,ap):
        changeit = "update fc set ap="+str(ap)+" where feature='"+f+"' and category='"+cat+"'"
        self.con.execute(changeit)

    def get_ap(self,f,cat):
        res=self.con.execute('select ap from fc where feature="%s" and category="%s"' % (f,cat)).fetchone()
        
        if res==None: 
            return 0   # default ap value
        else: 
            return float(res[0])

    # Increase the count of a category
    def incc(self,cat):
        count=self.catcount(cat)
        
        try:
            if count==0:
                self.con.execute("insert into cc values ('%s',1)" % (cat))
            else:
                self.con.execute("update cc set count=%d where category='%s'" % (count+1,cat))
        except: 
            print "error adding",f,"in category",cat

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        res=self.con.execute('select count from fc where feature="%s" and category="%s"' % (f,cat)).fetchone()
        if res==None: 
            return 0
        else: 
            return float(res[0])

    # The number of items in a category
    def catcount(self,cat):
        res=self.con.execute('select count from cc where category="%s"' % (cat)).fetchone()
        
        if res==None: 
            return 0
        else: 
            return float(res[0])

    # The total number of items
    def totalcount(self):
        res=self.con.execute('select sum(count) from cc').fetchone()
        
        if res==None: 
            return 0
        
        return res[0]

    # The list of all the categories
    def categories(self):
        cur=self.con.execute('select category from cc')
        return [d[0] for d in cur]

    def train(self,item,cat):
        features=self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)

        # Increment the count for this category
        self.incc(cat)
        self.con.commit()

    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0

        # The total number of times this feature appeared in this category
        # divided by the total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0):
        # Calculate current probability
        basicprob=prf(f,cat)
        # Count the number of times this feature has appeared in all categories
        totals=sum([self.fcount(f,c) for c in self.categories()])

        # Get the assumed probability for the feature
        ap = self.get_ap(f,cat)
        
        if ap == 0: 
            ap = 0.5       # If not in database set to default value

        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        
        return bp

class naivebayes(classifier):

    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds={}

    def docprob(self,item,cat):
        features=self.getfeatures(item)

        # Multiply the probabilities of all the features together
        p=1
        for f in features: 
            p *= self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds: 
            return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        probs={}
        # Find the category with the highest probability
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        # Make sure the probability exceeds threshold*next best
        for cat in probs:
            if cat==best: 
                continue
            if probs[cat]*self.getthreshold(best)>probs[best]: 
                return default
        return best

class fisherclassifier(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums={}

    def setminimum(self,cat,min):
        self.minimums[cat]=min

    def getminimum(self,cat):
        if cat not in self.minimums: 
            return 0
        return self.minimums[cat]

    def cprob(self,f,cat):
        # The frequency of this feature in this category
        clf=self.fprob(f,cat)
        if clf==0: 
            return 0

        # The frequency of this feature in all the categories
        freqsum=sum([self.fprob(f,c) for c in self.categories()])

        # The probability is the frequency in this category divided by the overall frequency
        p=clf/(freqsum)

        return p

    def fisherprob(self,item,cat):
        # Multiply all the probabilities together
        p=1
        features=self.getfeatures(item)
        
        for f in features:
            p *= (self.weightedprob(f,cat,self.cprob))

        # Take the natural log and multiply by -2
        try: 
            fscore=-2*math.log(p)   # if db returns none for ap because feature not in fc
        except: 
            return 0
        
        # Use the inverse chi2 function to get a probability
        return self.invchi2(fscore,len(features)*2)

    def invchi2(self,chi,df):
        m=chi/2.0
        sum = term = math.exp(-m)
        
        for i in range(1, df//2):
            term *= m/i
            sum += term
        
        return min(sum, 1.0)

    def classify(self,item,default=None):
        # Loop through looking for the best result
        best=default
        max=0.0
        for c in self.categories():
            p=self.fisherprob(item,c)
            # Make sure it exceeds the minimum
            
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
                
        return best
    
