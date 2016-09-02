""" Chapter 10 Exercise 5: Alternative display methods.

    The functions given in this chapter for displaying results are simple and show important features, 
    but they lose a lot of context. Can you think of other ways of displaying results? 
    Try writing a function that displays the articles in their original text with keywords from each 
    feature highlighted, or perhaps a trading-volume chart with important dates clearly shown.

    First a remake of newsfeatures that outputs to the terminal with keywords highlighted in red.
    
    To do - rename the variables to something more meaningful
"""

import feedparser as feedparser
import re as re
from numpy import * 
import os as os

feedlist = ["http://www.npr.org/rss/rss.php?id=1003",
            "http://www.npr.org/rss/rss.php?id=1004"]

class color:
   YELLOW = '\033[93m'
   RED = '\033[91m'
   END = '\033[0m'

def stripHTML(h):
    p=''
    s=0
    for c in h:
        if c=='<': s=1
        elif c=='>':
            s=0
            p+=' '
        elif s==0: p+=c
    return p

def separatewords(text):
    ignore_list = ['a', 'about', 'above', 'after', 'again', 'all', 'also', 'am', 'an', 'and', 'any', 'are', 
                   "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 
                   'but', 'by', "can", "can't", 'cannot', 'could', "couldn't", "couldn", 'did', "didn", "didn't", 
                   'do', 'does', 'doesn', "doesn't", 'doing', "don't", 'down', 'during', 'each', "even", 'every', 
                   'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven", "haven't",
                   'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 
                   'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', 
                   "isn't", 'it', "it's", 'its', 'itself', 'laquo', 'lsaquo', 'ldquo', "let's", 'mdash', 'me', 
                   'more', 'most', "mustn", "mustn't", 'my', 'myself', "nbsp", 'no', 'nor', 'not', 'of', 'off', 
                   'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'out', 'over', 'own', 'quot', 
                   'raquo', 'rsaquo', 'rsquo', 'said', 'same', 'say', 'says', "shan't", 'she', "she'd", "she'll", 
                   "she's", 'should', "shouldn", "shouldn't", 'so', 'some', 'still', 'such', 'than', 'that', 
                   "that's", 'the', 'their', 'theirs', 'them', 'then', 'there', "there's", 'these', 'they', 
                   "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 
                   'until', 'up', 'very', 'was', 'wasn', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 
                   'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 
                   'who', "who's", 'whom', 'why', "why's", "will", "with", "won't", "wouldn't", 'wouldn', 'you', 
                   "you'd", "you'll", "you're", "you've", 'your', 'yours']
    splitter=re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s)>3 and s.lower() not in ignore_list]


def getarticlewords():
    allwords={}
    articlewords=[]
    articletitles=[]
    articles=[]
    ec=0
    
    # Loop over every feed
    for feed in feedlist:
        f=feedparser.parse(feed)

        # Loop over every article
        for e in f.entries:
            # Ignore identical articles
            if e.title in articletitles: 
                continue

            # Extract the words
            txt=e.title.encode('utf8')+stripHTML(e.description.encode('utf8'))
            arti=e.description.encode('utf8')
            articles.append(arti)
            words=separatewords(txt)
            articlewords.append({})
            articletitles.append(e.title)

            # Increase the counts for this word in allwords and in articlewords
            for word in words:
                allwords.setdefault(word,0)
                allwords[word]+=1
                articlewords[ec].setdefault(word,0)
                articlewords[ec][word]+=1
            ec+=1
    
    return allwords, articlewords, articletitles, articles


def makematrix(allw,articlew):
    wordvec=[]

    # Only take words that are common but not too common
    for w,c in allw.items():
        if c>3 and c<len(articlew)*0.6:
            wordvec.append(w)

    # Create the word matrix
    l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1,wordvec


def showarticles(titles,toppatterns,patternnames,articles):
    # Loop over all the articles
    for j in range(len(titles)):
        print (titles[j].encode('utf8')+'\n')

        # Get the top features for this article and reverse sort them
        toppatterns[j].sort()
        toppatterns[j].reverse()

        # Print the top three patterns
        for i in range(3):
            print (str(toppatterns[j][i][0])+' '+
                          str(patternnames[toppatterns[j][i][1]])+'\n')
        frog = raw_input('press <ENTER> to continue')


def showfeatures(w,h,titles,wordvec,articles):
    pc,wc=shape(h)
    toppatterns=[[] for i in range(len(titles))]
    patternnames=[]
    os.system('clear')
    
    # Loop over all the features
    for i in range(pc):
        slist=[]
        
        # Create a list of words and their weights
        for j in range(wc):
            slist.append((h[i,j],wordvec[j]))
        
        # Reverse sort the wordlist
        slist.sort()
        slist.reverse()
        
        # Print the first six elements
        n=[s[1] for s in slist[0:6]]
        print color.RED + str(n) + color.END +'\n'
        print '-'*80,"\n"
        patternnames.append(n)

        # Create a list of articles for this feature
        flist=[]
        for j in range(len(titles)):
            # Add the article with its weight
            flist.append((w[j,i],titles[j],articles[j]))
            toppatterns[j].append((w[j,i],i,titles[j]))

        # Reverse sort the list
        flist.sort()
        flist.reverse()

        # Show the top three articles
        for f in flist[0:3]:
            petit_frog = str(f).replace("u'",'').replace('u"','').replace('"','').replace("'",'').replace('(','').replace(')','').split(' ')
            
            for a in range(len(petit_frog)):
                if petit_frog[a].lower() in n:
                    print color.RED + petit_frog[a] + color.END,
                elif petit_frog[a][:-1].lower() in n:
                    print color.RED + petit_frog[a] + color.END,
                else: print petit_frog[a],

            print
            print '-'*80
            print

        frog = raw_input('Press <ENTER> to continue')
        os.system('clear')
    # Return the pattern names for later use
    return toppatterns, patternnames

""" 
---------------------------------------------------------------------------------------------
      Usage
---------------------------------------------------------------------------------------------
import newsfeatures_ex5 as newsfeatures
import json
import welcome_to_the_nmf as nmf
from numpy import *

# see end for how to save dictionaries in json
def load_dics(filename):
    f = open(filename, 'r')
    dic={}
    for line in f:
        dic = json.loads(line)
    return dic

allw=load_dics('allw.json')
artw=load_dics('artw.json')
artt=load_dics('artt.json')
articles=load_dics('articles.json')

wordmatrix,wordvec=newsfeatures.makematrix(allw,artw)
v=matrix(wordmatrix)
weights,feat=nmf.factorize(v,pc=20,maxiter=250)
topp,pn=newsfeatures.showfeatures(weights,feat,artt,wordvec,articles)
newsfeatures.showarticles(artt,topp,pn,articles)

#######
# END #
#########################################################

# saving dictionaries in json
import json
import newsfeatures

allw,artw,artt=newsfeatures.getarticlewords()

f = open('allw.json', 'w')
f.write(json.dumps(allw))
f.close()
f = open('artw.json', 'w')
f.write(json.dumps(artw))
f.close()
f = open('artt.json', 'w')
f.write(json.dumps(artt))
f.close()

#########################################################
"""
