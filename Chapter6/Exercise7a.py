""" Chapter 6 Exercise 7a: Neural network classifier.

    Modify the neural network from Chapter 4 to be used for document classification. 
    How do its results compare?

    This version of the neural net works but as it grows larger, it slows down 
    (after about 20 trainquery() calls it starts to be longer than a minute per call), 
    because it has to update every node in the db. 
    The answer to this is to be selective in adding features, only adding known specifics 
    to save time.(Or using a faster db.) Resultwise it learns pretty well.
    """

from math import tanh
from pysqlite2 import dbapi2 as sqlite
import re as re
import feedparser as feedparser
from string import punctuation

def dtanh(y):
    return 1.0-y*y

def sampletrain(cl):
    cl.trainquery(['Nobody','owns','the','water'],['good','bad'],'good')
    cl.trainquery(['the','quick','rabbit','jumps','fences'],['good','bad'],'good')
    cl.trainquery(['buy','pharmeceuticals','now'],['good','bad'],'bad')
    cl.trainquery(['make','quick','money','at','the','online','casino'],['good','bad'],'bad')
    cl.trainquery(['the','quick','brown','fox','jumps','over','the','lazy','dog'],['good','bad'],'good')


class searchnet:
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table feathidden(fromid,toid,strength)')
        self.con.execute('create table hiddencat(fromid,toid,strength)')
        self.con.commit()

    def getstrength(self,fromid,toid,layer):
        if layer==0:
            table='feathidden'
            res=self.con.execute('select strength from %s where fromid="%s" and toid=%d' % (table,fromid,toid)).fetchone()
        else:
            table='hiddencat'
            res=self.con.execute('select strength from %s where fromid=%d and toid="%s"' % (table,fromid,toid)).fetchone()
        
        if res==None:
            if layer==0: 
                return -0.2
            if layer==1: 
                return 0
        return res[0]

    def setstrength(self,fromid,toid,layer,strength):
        if layer==0:
            table='feathidden'
            res=self.con.execute("select rowid from %s where fromid='%s' and toid=%d" % (table,fromid,toid)).fetchone()
        else:
            table='hiddencat'
            res=self.con.execute('select rowid from %s where fromid=%d and toid="%s"' % (table,fromid,toid)).fetchone()
        
        if res==None:
            if table=='feathidden':
                self.con.execute('insert into %s (fromid,toid,strength) values ("%s",%d,%f)' % (table,fromid,toid,strength))
            elif table=='hiddencat':
                self.con.execute('insert into %s (fromid,toid,strength) values (%d,"%s",%f)' % (table,fromid,toid,strength))
        else:
            rowid=res[0]
            self.con.execute('update %s set strength=%f where rowid=%d' % (table,strength,rowid))

    def generatehiddennode(self,featids,catids):
#        if len(featids)>3: return None
        # Check if we already created a node for this set of words
        try:
            createkey='_'.join(sorted([str(wi).encode('utf-8') for wi in featids]))
            res=self.con.execute("select rowid from hiddennode where create_key='%s'" % createkey).fetchone()
        except: 
            return
        
        # If not create it
        if res==None:
            cur=self.con.execute("insert into hiddennode (create_key) values ('%s')" % createkey)
            hiddenid=cur.lastrowid
            # Put in some default weights
            for featid in featids:
                self.setstrength(featid,hiddenid,0,1.0/len(featids))
            for catid in catids:
                self.setstrength(hiddenid,catid,1,0.1) 
            self.con.commit()

    def getallhiddenids(self,featids,catids):
        l1={}
        for featid in featids:
            cur=self.con.execute('select toid from feathidden where fromid="%s"' % featid)
            for row in cur: l1[row[0]]=1
        for catid in catids:
            cur=self.con.execute('select fromid from hiddencat where toid="%s"' % catid)
            for row in cur: l1[row[0]]=1
        return l1.keys()

    def setupnetwork(self,featids,catids):
        # Value lists
        self.featids=featids
        self.hiddenids=self.getallhiddenids(featids,catids)
        self.catids=catids

        # Node outputs         strengths set to default values
        self.ai = [1.0]*len(self.featids)
        self.ah = [1.0]*len(self.hiddenids)
        self.ao = [1.0]*len(self.catids)

        # Create weights matrix
        self.wi =[[self.getstrength(featid,hiddenid,0) for hiddenid in self.hiddenids] for featid in self.featids]
        self.wo =[[self.getstrength(hiddenid,catid,1) for catid in self.catids] for hiddenid in self.hiddenids]

    def feedforward(self):
        # the only inputs are the query words
        for i in range(len(self.featids)):
            self.ai[i] = 1.0

        # hidden activations
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.featids)):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        # output activations
        for k in range(len(self.catids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)

        return self.ao[:]

    def getresult(self,featids,catids):
        self.setupnetwork(featids,catids)
        return self.feedforward()

    def backPropagate(self,targets, N=0.5):
        # calculate errors for output
        output_deltas = [0.0]*len(self.catids)
        for k in range(len(self.catids)):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dtanh(self.ao[k])*error

        # calculate errors for hidden layer
        hidden_deltas = [0.0]*len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.catids)):
                error = error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j])*error

        # update output weights
        for j in range(len(self.hiddenids)): 
            for k in range(len(self.catids)):
                change=output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change

        # update input weights
        for i in range(len(self.featids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change

    def trainquery(self,featids,catids,selectedurl):
        # generate a hiddennode if neccessary
        self.generatehiddennode(featids,catids)

        self.setupnetwork(featids,catids)
        self.feedforward()
        targets=[0.0]*len(catids)
        targets[catids.index(selectedurl)]=1.0
        error = self.backPropagate(targets)
        self.updatedatabase()

    def updatedatabase(self):
        # set them to database values
        for i in range(len(self.featids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.featids[i],self.hiddenids[j],0,self.wi[i][j])
        for j in range(len(self.hiddenids)):
            for k in range(len(self.catids)):
                self.setstrength(self.hiddenids[j],self.catids[k],1,self.wo[j][k])
        self.con.commit()

    def guess_category(self,featurelist,catlist1):
        if len(catlist1)==0:
            list1=[]
            return list1.append('none')
        else: return self.getresult(featurelist,catlist1)

    def readentryfeatures(self,feed):
        # Get feed entries and loop over them
        splitter = re.compile('\\W*')
        f=feedparser.parse(feed)
        for entry in f['entries']:
            print '\n-----'
            # Print the contents of the entry
            print 'Title:     '+entry['title'].encode('utf-8')
            print 'Publisher  '+entry['publisher'].encode('utf-8')
            print
            print entry['summary'].encode('utf-8')
            summarywords = entry['summary'].split(' ')

            featurelist = []
            # Extract the title words and annotate
            titlewords = [s.lower() for s in splitter.split(entry['title']) if len(s) > 2 and len(s) < 20]

            # Extract the summary words
            summarywords = [s for s in splitter.split(entry['summary']) if len(s) > 2 and len(s) < 20]

            featurelist += titlewords + summarywords
            featurelist.append('Publisher:'+ entry['publisher'])
            uc = 0
            for i in range(len(summarywords)):
                w = summarywords[i]
                for p in punctuation:
                    if p in w: w = w.replace(p,"")
                if (w.isupper()):
                    uc += 1
                featurelist.append(w.lower())
                if i < len(summarywords) - 1:
                    twowords = summarywords[i].encode('utf-8')+' '+summarywords[i+1].encode('utf-8')   # Get word pairs in summary as features
                    featurelist.append(twowords.lower())
                    if (float(uc) / len(summarywords) > 0.3):
                        featurelist.append('UPPERCASE')

            # Convert to list of features here
            catlist1=[]
            # Fetch a list of categories
            for c in self.con.execute('select distinct toid from hiddencat'): catlist1.append(c[0])
            # Print the best guess at the current category
            best = 0
            bestguess = 'None'
            catlist = self.guess_category(featurelist,catlist1)
            if catlist==None: catlist=[]
            for a in range(len(catlist)):
                if (best==0) and (float(catlist[a])<0):
                    best = float(catlist[a])             # Else if all values < 0 ...
                    bestguess = catlist1[a]              # The best one will not get chosen
                elif float(catlist[a]) > best:
                    best = float(catlist[a])
                    bestguess = catlist1[a]
            print 'Guess: '+ bestguess

            # Ask the user to specify the correct category and train on that
            cl=raw_input('Enter category: ')
            if cl not in catlist1:
                catlist1.append(cl)
            try:
                self.trainquery(featurelist,catlist1,cl)
            except: print "\n---------Unable to train with this data----------\n"
        self.con.commit()

""" 
Usage.

import Exercise7a as nn
mynet=nn.searchnet('nn.db')
mynet.maketables()
mynet.readentryfeatures('python_search.xml')

"""
