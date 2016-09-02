""" I updated the feeds and added a stoplist - Andrew"""

import feedparser as feedparser
import re as re
from numpy import * 

feedlist = ['http://feeds.reuters.com/rss/topNews',
            'http://feeds.reuters.com/rss/domesticNews',
            'http://feeds.reuters.com/rss/worldNews',
            'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305',
            'http://hosted2.ap.org/atom/APDEFAULT/386c25518f464186bf7a2ac026580ce7',
            'http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5',
            'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa',
            'http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml',
            'http://www.nytimes.com/services/xml/rss/nyt/International.xml',
            'http://news.google.com/?output=rss',
            'http://feeds.salon.com/salon/news',
            'http://www.foxnews.com/xmlfeed/rss/0,4313,0,00.rss',
            'http://www.foxnews.com/xmlfeed/rss/0,4313,80,00.rss',
            'http://rss.cnn.com/rss/edition.rss',
            'http://rss.cnn.com/rss/edition_world.rss',
            "http://www.npr.org/rss/rss.php?id=1003",
            "http://www.npr.org/rss/rss.php?id=1004",
            "http://rss.cbc.ca/lineup/world.xml",
            "http://feeds.feedburner.com/newscomauworldnewsndm",
            "http://www.abc.net.au/news/feed/52278/rss.xml",
            "http://news.sky.com/feeds/rss/world.xml",
            "http://feeds.feedburner.com/ndtv/TqgX",
            "http://timesofindia.feedsportal.com/c/33039/f/533917/index.rss",
            "http://feeds.abcnews.com/abcnews/internationalheadlines",
            "http://www.usnews.com/rss/news",
            "http://www.un.org/apps/news/rss/rss_top.asp",
            "http://feeds.washingtonpost.com/rss/world",
            'http://rss.cnn.com/rss/edition_us.rss']

def stripHTML(h):
    p=''
    s=0
    
    for c in h:
        if c=='<': 
            s=1
        elif c=='>':
            s=0
            p+=' '
        elif s==0: p+=c
    
    return p


def separatewords(text):
    ignore_list = ['a', 'about', 'above', 'after', 'again', 'all', 'also', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', "even", 'every', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', 'laquo', 'lsaquo', 'ldquo', "let's", 'mdash', 'me', 'more', 'most', "mustn't", 'my', 'myself', "nbsp", 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'out', 'over', 'own', 'quot', 'raquo', 'rsaquo', 'rsquo', 'said', 'same', 'say', 'says',"shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'still', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", "will", "with", "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours']
    splitter=re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s)>3 and s.lower() not in ignore_list]


def getarticlewords():
    allwords={}
    articlewords=[]
    articletitles=[]
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
    
    return allwords, articlewords, articletitles


def makematrix(allw,articlew):
    wordvec=[]

    # Only take words that are common but not too common
    for w,c in allw.items():
        if c>3 and c<len(articlew)*0.6:
            wordvec.append(w)

    # Create the word matrix
    l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1,wordvec


def showfeatures(w,h,titles,wordvec,out='features.txt'):
    outfile=file(out,'w')
    pc,wc=shape(h)
    toppatterns=[[] for i in range(len(titles))]
    patternnames=[]

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
        outfile.write(str(n)+'\n')
        patternnames.append(n)

        # Create a list of articles for this feature
        flist=[]
        
        for j in range(len(titles)):
            # Add the article with its weight
            flist.append((w[j,i],titles[j]))
            toppatterns[j].append((w[j,i],i,titles[j]))

        # Reverse sort the list
        flist.sort()
        flist.reverse()

        # Show the top three articles
        for f in flist[0:3]:
            outfile.write(str(f)+'\n')
        
        outfile.write('\n')

    outfile.close()
    
    # Return the pattern names for later use
    return toppatterns, patternnames


def showarticles(titles,toppatterns,patternnames,out='articles.txt'):
    outfile=file(out,'w')

    # Loop over all the articles
    for j in range(len(titles)):
        outfile.write(titles[j].encode('utf8')+'\n')

        # Get the top features for this article and reverse sort them
        toppatterns[j].sort()
        toppatterns[j].reverse()

        # Print the top three patterns
        for i in range(3):
            outfile.write(str(toppatterns[j][i][0])+' '+
                          str(patternnames[toppatterns[j][i][1]])+'\n')
        outfile.write('\n')

    outfile.close()
    
