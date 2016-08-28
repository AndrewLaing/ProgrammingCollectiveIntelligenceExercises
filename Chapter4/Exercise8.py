""" Chapter 4 Exercise 8: Additional layers. Your neural network has only one hidden layer.
    Update the class to support an arbitrary number of hidden layers, which can be specified upon initialization.
"""

from math import tanh
from pysqlite2 import dbapi2 as sqlite

def dtanh(y):
    return 1.0-y*y

class searchnet:
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self, hlayer=0):
        for a in range(hlayer):
            self.con.execute('create table hiddennode%s(create_key)' % a)
            self.con.execute('create table wordhidden%s(fromid,toid,strength)' % a)
            self.con.execute('create table hiddenurl%s(fromid,toid,strength)' % a)
        self.con.commit()

    def getstrength(self,fromid,toid,layer,hlayer):
        if layer==0: table='wordhidden%s' % hlayer
        else: table='hiddenurl%s' % hlayer
        res=self.con.execute('select strength from %s where fromid=%d and toid=%d' % (table,fromid,toid)).fetchone()
        if res==None:
            if layer==0: return -0.2
            if layer==1: return 0
        return res[0]

    def setstrength(self,fromid,toid,layer,strength,hlayer):
        if layer==0: table='wordhidden%s' % hlayer
        else: table='hiddenurl%s' % hlayer
        res=self.con.execute('select rowid from %s where fromid=%d and toid=%d' % (table,fromid,toid)).fetchone()
        if res==None:
            self.con.execute('insert into %s (fromid,toid,strength) values (%d,%d,%f)' % (table,fromid,toid,strength))
        else:
            rowid=res[0]
            self.con.execute('update %s set strength=%f where rowid=%d' % (table,strength,rowid))

    def generatehiddennode(self,wordids,urls,hlayer):
        if len(wordids)>3: return None
        # Check if we already created a node for this set of words
        createkey='_'.join(sorted([str(wi) for wi in wordids]))
        res=self.con.execute("select rowid from hiddennode%s where create_key='%s'" % (hlayer,createkey)).fetchone()

        # If not create it
        if res==None:
            cur=self.con.execute("insert into hiddennode%s (create_key) values ('%s')" % (hlayer,createkey))
            hiddenid=cur.lastrowid
            # Put in some default weights
            for wordid in wordids:
                self.setstrength(wordid,hiddenid,0,1.0/len(wordids),hlayer)
            for urlid in urls:
                self.setstrength(hiddenid,urlid,1,0.1,hlayer) 
            self.con.commit()

    def getallhiddenids(self,wordids,urlids,hlayer):
        l1={}
        for wordid in wordids:
            cur=self.con.execute('select toid from wordhidden%s where fromid=%d' % (hlayer,wordid))
            for row in cur: l1[row[0]]=1
        for urlid in urlids:
            cur=self.con.execute('select fromid from hiddenurl%s where toid=%d' % (hlayer,urlid))
            for row in cur: l1[row[0]]=1
        return l1.keys()

    def setupnetwork(self,wordids,urlids,hlayer):
        # Value lists
        self.wordids=wordids
        self.hiddenids=self.getallhiddenids(wordids,urlids,hlayer)
        self.urlids=urlids

        # Node outputs         strengths set to default values
        self.ai = [1.0]*len(self.wordids)
        self.ah = [1.0]*len(self.hiddenids)
        self.ao = [1.0]*len(self.urlids)

        # Create weights matrix
        self.wi =[[self.getstrength(wordid,hiddenid,0,hlayer) for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.wo =[[self.getstrength(hiddenid,urlid,1,hlayer) for urlid in self.urlids] for hiddenid in self.hiddenids]

    def feedforward(self):
        # the only inputs are the query words
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # hidden activations
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        # output activations
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)

        return self.ao[:]

    def getresult(self,wordids,urlids,hlayer):
        self.setupnetwork(wordids,urlids,hlayer)
        return self.feedforward()

    def backPropagate(self,targets, N=0.5):
        # calculate errors for output
        output_deltas = [0.0]*len(self.urlids)
        for k in range(len(self.urlids)):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dtanh(self.ao[k])*error

        # calculate errors for hidden layer
        hidden_deltas = [0.0]*len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error = error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j])*error

        # update output weights
        for j in range(len(self.hiddenids)): 
            for k in range(len(self.urlids)):
                change=output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change

        # update input weights
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change

    def trainquery(self,wordids,urlids,selectedurl,hlayer):
        # generate a hiddennode if neccessary
        self.generatehiddennode(wordids,urlids,hlayer)

        self.setupnetwork(wordids,urlids,hlayer)
        self.feedforward()
        targets=[0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        error = self.backPropagate(targets)
        self.updatedatabase(hlayer)

    def updatedatabase(self,hlayer):
        # set them to database values
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.wordids[i],self.hiddenids[j],0,self.wi[i][j],hlayer)
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids[j],self.urlids[k],1,self.wo[j][k],hlayer)
        self.con.commit()



"""
####################
# Testing it works #
####################
With one hidden layer -first save as nn_redux.py obviously
**********************************************************
import nn_redux as nn
mynet=nn.searchnet('nn_redux.db')
mynet.maketables(1)       --- when number of hiddenlayers is 1 hlayer=0
                          --- either that or use ...hiddennode%s(create_key)' % a+1)
wWorld,wRiver,wBank=101,102,103
uWorldBank,uRiver,uEarth=201,202,203
mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth],0)

# test hiddennode exists
for c in mynet.con.execute('select * from hiddennode0'): print c
for c in mynet.con.execute('select * from wordhidden0'): print c
for c in mynet.con.execute('select * from hiddenurl0'): print c
mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth],0)

# train the neural net
mynet.trainquery([wWorld,wBank],[uWorldBank,uRiver,uEarth],uWorldBank,0)
mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth],0)
-------------------------------------------------------------------------------

With two hidden layer -first save as nn_redux.py obviously
***********************************************************
import nn_redux as nn
mynet=nn.searchnet('nn_redux.db')
mynet.maketables(2)

wWorld,wRiver,wBank=101,102,103
uWorldBank,uRiver,uEarth=201,202,203
mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth],0)
mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth],1)

# test hiddennode exists
for c in mynet.con.execute('select * from hiddennode0'): print c
for c in mynet.con.execute('select * from hiddennode1'): print c
mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth],0)
mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth],1)

# train the neural net
mynet.trainquery([wWorld,wBank],[uWorldBank,uRiver,uEarth],uWorldBank,0)
mynet.trainquery([wWorld,wBank],[uWorldBank,uRiver,uEarth],uRiver,1)
mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth],0)
mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth],1)
-------------------------------------------------------------------------------

#################################################
# Adding the hlayer variable to searchengine.py #
#################################################

    The hlayer could be used like a unique user id to give
    specifically tailored results.

    def query(self,q,hlayer):
        rows,wordids=self.getmatchrows(q.lower())
        if rows == "Nothing":
            return ['%s Not in database' %q]
        scores=self.getscoredlist(rows,wordids,hlayer)...........

    def getscoredlist(self,rows,wordids,hlayer):
        totalscores=dict([(row[0],0) for row in rows])...........
..........
        weights=[(1.0,self.nnscore(rows, wordids, hlayer))] 


    def nnscore(self,rows,wordids,hlayer):
        # Get unique URL IDs as an ordered list
        urlids=[urlid for urlid in set([row[0] for row in rows])]
        nnres=mynet.getresult(wordids,urlids,hlayer)
        scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)
        
-------------------------------------------------------------------------------
"""
