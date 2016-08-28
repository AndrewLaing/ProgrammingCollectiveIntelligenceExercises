""" Chapter 4 Exercise 5: Word frequency bias.

    The "word count" metric is biased to favor longer documents, since a long document has more words 
    and can therefore contain the target words more often. 
    Write a new metric that calculates frequency as a percentage of the number of words in the document.
"""

def wordfreqscore(self,rows,wordids):
    uniqueurls=set([row[0] for row in rows])
    # Get total number of words in url
    wordscount=dict([(u,self.con.execute('select count(*) from wordlocation where urlid=%d' % u).fetchone()[0]) for u in uniqueurls])
    wordscount2 = {}
    # Get total number of query words in url
    for word in wordids:
        wordscount1=dict([(u,self.con.execute('select count(*) from wordlocation where urlid=%d and wordid=%d' % (u, word)).fetchone()[0]) for u in uniqueurls])
        for url in wordscount1:
            if url not in wordscount2:
                wordscount2[url]=wordscount1[url]
            else:
                wordscount2[url] = wordscount2[url]+wordscount1[url]
    # Calculate percentage of query words in url and put in dictionary
    for url in wordscount:
        wordscount[url] = (wordscount2[url]/float(wordscount[url]))*100.0
    
    return self.normalizescores(wordscount)

"""
    Usage:
        weights=[(1.0,self.wordfreqscore(rows, wordids))] 
"""
