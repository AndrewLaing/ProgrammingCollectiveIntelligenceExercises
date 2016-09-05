""" Chapter 12 Programming Collective Intelligence: Neural Network Classifier.

   As the chapter has no exercises in it I have decided to create a practical
   application for each of the Algorithms and Methods described.
   Next up the Neural Network Classifier.

   So, I have created an app that trains a Neural Network and classifies
   whether files opened are likely to contain Python, Bash or AIML code
   based upon the presence of 8 keywords from each code.

   I used psyco to speed things up, but psyco is not obligatory :)
"""

from math import tanh
import json
from Tkinter import *
from tkFileDialog import askopenfilename
import os as os
import re as re
import time as time

def dtanh(y):
    return 1.0-y*y

class searchnet:
    def __init__(self):
        try:
            f = open('hiddennode.json', 'r')
            self.hiddennode={}
            for line in f:
                self.hiddennode = json.loads(line)           # json saves keys as strings so...
            for a in self.hiddennode.keys():
                self.hiddennode[int(a)]=self.hiddennode[a]   # ...for keeping track of hiddenid.
                del self.hiddennode[a]
            
            f = open('wordhidden.json', 'r')
            self.wordhidden={}
            
            for line in f:
                self.wordhidden = json.loads(line)
            
            f = open('hiddenurl.json', 'r')
            self.hiddenurl={}
            
            for line in f:
                self.hiddenurl = json.loads(line)
        except:
            print "The required dictionaries don't exist in this folder."
            shall=str(raw_input('Shall I create them for you? (y/n) >'))
            
            if shall=='y' or shall=='Y':
                self.create_dics()
                print"-"*44
                print '"hiddennode.json", "wordhidden.json" and "hiddenurl.json" created.'
        
        self.include_list = ['def','return','global','input','class','int','elif','except','import',
                             'pidof','grep','echo','sh','ls','cd','read','then','arr','category','pattern',
                             'topic','template','li','star','aiml','think']

    def create_dics(self):
        self.hiddennode={}
        self.wordhidden={}
        self.hiddenurl={}
        f = open('hiddennode.json', 'w')
        f.write(json.dumps(self.hiddennode))
        f.close()
        f = open('wordhidden.json', 'w')
        f.write(json.dumps(self.wordhidden))
        f.close()
        f = open('hiddenurl.json', 'w')
        f.write(json.dumps(self.hiddenurl))
        f.close()

    def save_dics(self):
        f = open('hiddennode.json', 'w')
        f.write(json.dumps(self.hiddennode))
        f.close()
        f = open('wordhidden.json', 'w')
        f.write(json.dumps(self.wordhidden))
        f.close()
        f = open('hiddenurl.json', 'w')
        f.write(json.dumps(self.hiddenurl))
        f.close()

    def getstrength(self,fromid1,toid1,layer):
        fromid=str(fromid1)  # json saves as strings
        toid=str(toid1)
        
        if layer==0:
            try: 
                res=self.wordhidden[fromid][toid]
            except: 
                res=-0.2
        else:
            try: 
                res=self.hiddenurl[fromid][toid]
            except: 
                res=0
        return float(res)

    def setstrength(self,fromid1,toid1,layer,strength):
        fromid=str(fromid1)  # json saves as strings
        toid=str(toid1)
        if layer==0:
            if str(fromid) in self.wordhidden:
                self.wordhidden[fromid][toid]=strength
            else:
                self.wordhidden[fromid]={}
                self.wordhidden[fromid][toid]=strength
        else:
            if fromid in self.hiddenurl:
                self.hiddenurl[fromid][toid]=strength
            else:
                self.hiddenurl[fromid]={}
                self.hiddenurl[fromid][toid]=strength

    def generatehiddennode(self,wordids,urls):
        createkey='_'.join(sorted([str(wi) for wi in wordids]))
        hiddenid=0
        notin=0
        
        if len(self.hiddennode)==0:
            self.hiddennode[0]=createkey
            notin=1
        else:
            for a in self.hiddennode:
                if self.hiddennode[a]==createkey:
                    hiddenid=a
                    notin=1
        
        if notin==0:
            hiddenid=int(max(self.hiddennode))+1
            self.hiddennode[hiddenid]=createkey
        
        for wordid in wordids:
            self.setstrength(wordid,hiddenid,0,1.0/len(wordids))
        
        for urlid in urls:
            self.setstrength(hiddenid,urlid,1,0.1)


    def getallhiddenids(self,wordids,urlids):
        l1={}
        for wordid in wordids:
            if str(wordid) in self.wordhidden:
                a=self.wordhidden[str(wordid)].keys()
                for row in a: 
                    l1[row]=1
        
        for urlid in urlids:
            for a in self.hiddenurl:
                if str(urlid) in self.hiddenurl[a]:
                    l1[a]=1
        
        return l1.keys()

    def setupnetwork(self,wordids,urlids):
        # Value lists
        self.wordids=wordids
        self.hiddenids=self.getallhiddenids(wordids,urlids)
        self.urlids=urlids

        # Node outputs         strengths set to default values
        self.ai = [1.0]*len(self.wordids)
        self.ah = [1.0]*len(self.hiddenids)
        self.ao = [1.0]*len(self.urlids)

        # Create weights matrix
        self.wi =[[self.getstrength(wordid,hiddenid,0) for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.wo =[[self.getstrength(hiddenid,urlid,1) for urlid in self.urlids] for hiddenid in self.hiddenids]

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

    def getresult(self,wordids,urlids):
        self.setupnetwork(wordids,urlids)
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

    def trainquery(self,wordids,urlids,selectedurl):
        # generate a hiddennode if neccessary
        self.generatehiddennode(wordids,urlids)

        self.setupnetwork(wordids,urlids)
        self.feedforward()
        targets=[0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        error = self.backPropagate(targets)
        self.updatedatabase()

    def updatedatabase(self):
        # set them to database values
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.wordids[i],self.hiddenids[j],0,self.wi[i][j])
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids[j],self.urlids[k],1,self.wo[j][k])

    def getwords(self,doc):
        splitter=re.compile('\\W*')
        words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
        dicto = dict([(w,1) for w in words])
        list1=[]
        for a in dicto:
            if a in self.include_list:
                list1.append(a)
        return list1

    def train_one(self):
        os.system('clear')
        a = time.time()
        print "Training the Neural Network..."
        print 'Current time =',str(time.localtime(a)[3])+':'+str(time.localtime(a)[4])+':'+str(time.localtime(a)[5])
        
        featlist=[['def','return','class','int','elif','global','except','import'],
                  ['echo','sh','ls','cd','read','pidof','grep','arr'],
                  ['category','pattern','template','li','star','topic','aiml','think']]
        catlist=['python','bash','aiml']
        
        for a in range(len(featlist)):
            for b in range(len(featlist[a])):
                featlist1=[featlist[a][b]]
                self.trainquery(featlist1,catlist,catlist[a])         # train single
                for c in range(len(featlist[a])):
                    featlist2=[]
                    if featlist[a][b]==featlist[a][c]:
                        pass
                    else:
                        featlist2.append(featlist[a][b])
                        featlist2.append(featlist[a][c])
                        self.trainquery(featlist2,catlist,catlist[a]) # train single
        self.save_dics()

    def classify(self):
        another = ""
        while another != 'n':
            fulltext = ""
            os.system('clear')
            root = Tk()           # This closes the askopenfilename box after it gets the filename
            root.withdraw()
            print "-"*44,"\n      Classify a file.\n","-"*44
            filename = askopenfilename(filetypes = [('All','*')])
            os.system('clear')
            
            for line in open(filename):
                fulltext += line.strip()
            
            featlist=self.getwords(fulltext)
            catlist=[]
            
            try:
                for a in self.hiddenurl:
                    for b in self.hiddenurl[a]:        
                        if b not in catlist: 
                            catlist.append(b)
            except: 
                pass
            
            print "-"*44
            print "Contains features\n",featlist
            a=self.getresult(featlist,catlist)
            
            if len(a)==0: 
                a=[0]*len(catlist)
            
            self.save_dics()
            print "-"*44
            print filename,"\nClassified as:"
            
            for z in range(len(catlist)):
                print '   ',catlist[z],'\t:',a[z]
            
            print "-"*44 
            another = raw_input('Classify another? >')


if __name__ == "__main__":
    import neural_network_example as nn
    mynet=nn.searchnet()
    try:
        import psyco
        psyco.full()
    except:
        print 'Unable to import psyco'
    doya=str(raw_input('Do you want to train/create the neural network? (y/n) >'))
    if doya=="y" or doya=="Y":
        for a in range(200):
           mynet.train_one()
    mynet.classify()

"""
---------------------------------------------------------------------------------
 #########
 # Usage #
 #########

import App3_NeuralNetworkClassifier as nn
mynet=nn.searchnet()
for a in range(200):
    mynet.train_one()

mynet.classify()

"""
