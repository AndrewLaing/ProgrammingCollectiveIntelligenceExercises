""" Chapter 4 Exercise 4.
    Long/Short Document Search.

    Sometimes the length of a page will be a determining factor in whether it is relevant to a particular search application or user. A user may be interested in finding a long article about a difficult subject or a quick reference page for a command-line tool.
    Write a weighting function that will give preference to longer of shorter documents depending upon its parameters.
"""

def pagelengthscore(self,rows,smallisbetter=0):
    uniqueurls=set([row[0] for row in rows])
    wordscount=dict([(u,self.con.execute('select count(*) from wordlocation where urlid=%d' % u).fetchone()[0]) for u in uniqueurls])
    return self.normalizescores(wordscount,smallisbetter)

"""
    usage:
        weights=[(1.0,self.pagelengthscore(rows, 0))]  # for longer pages
        weights=[(1.0,self.pagelengthscore(rows, 1))]  # for shorter pages
