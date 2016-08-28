""" Chapter 4 Exercise 6: Inbound link searching.

    Your code can rank items based on the text of the inbound links, but they must already be results 
    based on the content of the page. Sometimes the most relevant page doesn't contain the query text at all, 
    but rather a lot of links with text pointing to it - this is often the case with links to images.

    Modify the search code to include results where an inbound link contains some of the search terms.

    Note: inboundlinks has no word positions unlike row in rows so I included the word positions from their parent. 
    Thus the children may become as important as their parents.
"""

    def query(self,q):
        rows,wordids=self.getmatchrows(q.lower())
        if rows == "Nothing":
            return ['%s Not in database' %q]

        inboundlinks = []
        for row in rows:
            instance = (self.con.execute('select toid from link where fromid=%d' % row[0]).fetchone()[0],)+row[1:]
            if instance not in inboundlinks: inboundlinks.append(instance)
        for inbound in inboundlinks: rows.append(inbound)
        
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items()],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score,self.geturlname(urlid))
        return wordids,[r[1] for r in rankedscores[0:10]]
