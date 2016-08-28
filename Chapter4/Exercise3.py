""" Chapter 4 Exercise 3: Exact matches.

    Search engines often support "exact match" queries where the words in the page must match the words 
    in the query in the same order with no additional words in between. 
    Create a new version of getmatchrows() that only returns results that are exact matches.
    (Hint: you can use subtraction in SQL to get the difference between the word locations.)

  I thought it would be better to do a regular search then go through 'cur' looking for sequential wordlocations.
  adding them to rows as they're found.

  Example row instances from cur
  (298, 334, 353) 1 url, 2 loc, 3 loc not sequential
  (298, 334, 335) 1 url, 2 loc, 3 loc sequential

"""

    def getmatchrows(self,q):
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        words=q.split(' ')
        tablenumber=0

        for word in words:
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
            fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
            cur=self.con.execute(fullquery)
            rows = []                                    #  Replacement
            for row in cur:                              #     code
                if len(row) < 3:                         #      ""
                    return "Nothing", "Nothing"          #      ""
                elif int(row[1]) == int((row[2])-1):     #      ""
                    rows.append(row)                     #      ""
            # See my version of searchengine.py
            # I added to this and query to deal with 'no matches found'
            if len(rows)==0:                             #      ""
                return "Nothing", "Nothing"              #      ""
            return rows,wordids
        except:
            a = b = "Nothing"
        print "a=",a,"\n","b=",b
        return a,b
  
