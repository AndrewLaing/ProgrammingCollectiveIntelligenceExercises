
"""
Updated

  linktextscore() and pagerankscore() corrected for ZeroDivisionError's
  'X not in database' response added to getmatchrows() and query() 
  q=q.lower() added to query() because of case sensitivity
  pagelengthscore() and wordfreqscore() methods added

"""

from pysqlite2 import dbapi2 as sqlite
import urllib2
from bs4 import *
from urlparse import urljoin
import re
import nn
mynet=nn.searchnet('nn.db')

# create a list of words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

class crawler:

    # initialize with name of database
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()

    # auxiliary func for getting an entry id and adding it if not present
    def getentryid(self,table,field,value,createnew=True):
        cur=self.con.execute(
        "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
            "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]

    # index an individual page
    def addtoindex(self,url,soup):
        if self.isindexed(url): return
        print 'Indexing '+url

        # Get individual words
        text=self.gettextonly(soup)
        words=self.separatewords(text)

        # get url id
        urlid=self.getentryid('urllist','url',url)

        # link each word to this url
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) \
                values (%d,%d,%d)" % (urlid,wordid,i))


    # extract text (no tags) from html page
    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    # Separate words by any non-whitespace character
    def separatewords(self,text):
        splitter=re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

    # return true if already indexed
    def isindexed(self,url):
        u=self.con.execute \
        ("select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            # check if this is actually crawled
            v=self.con.execute(
            'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v!=None:
                return True
        return False

    # add a link between two pages
    def addlinkref(self,urlFrom,urlTo,linkText):
        words=self.separatewords(linkText)
        fromid=self.getentryid('urllist','url',urlFrom)
        toid=self.getentryid('urllist','url',urlTo)
        if fromid==toid: return
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))

    # Starting with a list of pages, do a breadth first search
    # to the given depth, indexing as we go
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    print 'Couldn\'t open %s' % page
                    continue
                soup=BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links=soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if url.find("'")!=-1: continue
                        url=url.split('#')[0] #remove location position
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)

                self.dbcommit()
            pages=newpages

    # create the database tables
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit( )

    def calculatepagerank(self,iterations=20):
        #  clear out the current PageRank tables
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')

        # Initialize every url with a PageRank of 1
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit()

        for i in range(iterations):
            print "Iteration %d" % (i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15

                # Loop through all the pages that link to this one
                for (linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    # Get the PageRank of the linker
                    linkingpr=self.con.execute('select score from pagerank where urlid=%d' % linker).fetchone()[0]

                    # Get the total number of links from the linker
                    linkingcount=self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr+=0.85*(linkingpr/linkingcount)
                self.con.execute('update pagerank set score=%f where urlid=%d' % (pr,urlid))
            self.dbcommit()

class searcher:
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self,q):
        # strings to build the query
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        # split the words by spaces
        words=q.split(' ')
        tablenumber=0

        for word in words:
            # get the word id
            wordrow=self.con.execute("select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1

        try:
            # create the query string
            fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
            cur=self.con.execute(fullquery)
            rows=[row for row in cur]
            if len(rows)==0: return "Nothing", "Nothing"
            return rows,wordids
            
        except:
            a = b = "Nothing"
        return a,b

    def getscoredlist(self,rows,wordids):
        totalscores=dict([(row[0],0) for row in rows])

        # This is where you'll late put the scoring functions
        # Frequency scoring activated
        weights=[(1.0,self.locationscore(rows)),(1.0,self.linktextscore(rows,wordids)),(1.0,self.pagerankscore(rows))]

        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]

        return totalscores

    def geturlname(self,id):
        return self.con.execute("select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self,q):
        rows,wordids=self.getmatchrows(q.lower())
        if rows == "Nothing":
            return ['%s Not in database' %q]
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items()],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score,self.geturlname(urlid))
        return wordids,[r[1] for r in rankedscores[0:10]]

    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0: maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows: counts[row[0]]+=1
        return self.normalizescores(counts)


    def locationscore(self,rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]: locations[row[0]]=loc

        return self.normalizescores(locations,smallIsBetter=1)

    def distancescore(self,rows):
        # If there's only one word, everyone wins!
        if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])

        # Initialize the dictionary with large values
        mindistance=dict([(row[0],1000000) for row in rows])

        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2, len(row))])
            if dist<mindistance[row[0]]: mindistance[row[0]]=dist
        return self.normalizescores(mindistance,smallIsBetter=1)

    def inboundlinkscore(self,rows):
        uniqueurls=set([row[0] for row in rows])
        inboundcount=dict([(u,self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])
        return self.normalizescores(inboundcount)

    def pagelengthscore(self,rows,smallisbetter=0):
        uniqueurls=set([row[0] for row in rows])
        wordscount=dict([(u,self.con.execute('select count(*) from wordlocation where urlid=%d' % u).fetchone()[0]) for u in uniqueurls])
        return self.normalizescores(wordscount,smallisbetter)

    def wordfreqscore(self,rows,wordids):
        uniqueurls=set([row[0] for row in rows])
        wordscount=dict([(u,self.con.execute('select count(*) from wordlocation where urlid=%d' % u).fetchone()[0]) for u in uniqueurls])
        wordscount2 = {}
        for word in wordids:
            wordscount1=dict([(u,self.con.execute('select count(*) from wordlocation where urlid=%d and wordid=%d' % (u, word)).fetchone()[0]) for u in uniqueurls])
            for url in wordscount1:
                if url not in wordscount2:
                    wordscount2[url]=wordscount1[url]
                else:
                    wordscount2[url] = wordscount2[url]+wordscount1[url]
        for url in wordscount:
            wordscount[url] = (wordscount2[url]/float(wordscount[url]))*100.0
        
        return self.normalizescores(wordscount)

    def pagerankscore(self,rows):
        pageranks=dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        maxrank=max(pageranks.values())
        if maxrank <= 0: maxrank = 0.00001
        normalizedscores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
        return normalizedscores
    
    def linktextscore(self,rows,wordids):
        linkscores=dict([(row[0],0) for row in rows])
        for wordid in wordids:
            cur=self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid,toid) in cur:
                if toid in linkscores:
                    pr=self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid]+=pr
        maxscore=max(linkscores.values())
        if maxscore <= 0: maxscore = 0.00001
        normalizedscores=dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
        return normalizedscores


    def nnscore(self,rows,wordids):
        # Get unique URL IDs as an ordered list
        urlids=[urlid for urlid in set([row[0] for row in rows])]
        nnres=mynet.getresult(wordids,urlids)
        scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)
