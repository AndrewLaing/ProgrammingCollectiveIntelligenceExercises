""" Chapter 4 Exercise 2

    Boolean operations.
    Many search engines support Boolean queries, which allow users to construct searches like "python OR pearl."
    An OR search can work by doing the queries separately and combining the results,
    but what about "python AND (program OR code)."?
    Modify the query methods to support some basic Boolean operations.

    Accepted methods
    1: foo and bar
    2: foo or bar  3: foo and (bar or blah)  4: (bar or blah) and foo
    5: foo not bar
    
"""
    def and_op_query(self,q):
        wordids = []
        q1 = q.split(' ') 
        for q2 in q1:
            if q2 != '':
                passthescores = {}
                rows,words=self.getmatchrows(q2)
                if rows == "Nothing":
                    wordids = passthescores = "Nothing"
                    return wordids, passthescores
                scores=self.getscoredlist(rows,wordids)
                for a in scores:
                    passthescores[a] = scores[a]
                wordids += words
        return wordids, passthescores


    def query(self,q):
        passthescores = {}
        or_list = []

        # Just in case an ignored word gets put into the query
        for a in ignorewords:        
            if (a!='and') and (a!='or'): q = q.replace(' '+a+' ',' ')

        # An A AND B query that needs both in it
        if (' or ' not in q)  and (' and ' in q):
            q1 = q.replace(' and ',' ')
            wordids, passthescores = self.and_op_query(q1)
            if (wordids == 'Nothing'):
                return ['%s Not in database' %q]

        # AND/OR's are treated like AND's
        elif (' and ' in q) and (' or ' in q):
            wordids = []
            and_list = q.split(' and ')
            for and1 in range(len(and_list)):
                if ' or ' in and_list[and1]:
                    if and1 > 0:
                        or_list = and_list[and1].replace('(','').replace(')','').split(' or ')
                        for or1 in or_list:
                            q1 = and_list[and1-1]+' '+or1
                            words, q1dic = self.and_op_query(q1)
                            if words == 'Nothing': pass
                            else:
                                wordids += words
                                for res in q1dic:
                                    passthescores[res] = q1dic[res]
                    if and1 == 0:
                        or_list = and_list[and1].replace('(','').replace(')','').split(' or ')
                        for or1 in or_list:
                            q1 = or1+' '+and_list[and1+1]
                            words, q1dic = self.and_op_query(q1)
                            if words == 'Nothing': pass
                            else:
                                wordids += words
                                for res in q1dic:
                                    passthescores[res] = q1dic[res]
            if (len(wordids) == 0) : return ['%s Not in database' %q]

        elif (' or ' in q):
            # An A OR B is treated like a normal query so just remove the word OR
            q1 = q.replace('(','').replace(')','').replace(' or ',' ')
            rows,wordids=self.getmatchrows(q1)
            if rows == "Nothing": return ['%s Not in database' %q]
            scores=self.getscoredlist(rows,wordids)
            for a in scores:
                passthescores[a] = scores[a]

        # So I wrote simple NOT method anyway 
        elif (' not ' in q):
            passscores1 = {}
            q1 = q.split(' not ')
            for q2 in range(len(q1)):
                if q2 == 0:
                    wordids, passthescores = self.and_op_query(q1[q2])
                    if (wordids == 'Nothing'):
                        return ['%s Not in database' %q]

                elif (q2 > 0) and (q1[q2]!=''):
                    wordids1, passscores1 = self.and_op_query(q1[q2])
                    if (wordids == 'Nothing'):
                        pass
                    else:
                        for notdic in passscores1:
                            if notdic in passthescores:
                                passthescores.pop(notdic)
            if len(passthescores)==0:
                return ['%s Not in database' %q]

        else:
            # if this is just a normal query pass normally
            rows,wordids=self.getmatchrows(q)
            if rows == "Nothing": return ['%s Not in database' %q]
            scores=self.getscoredlist(rows,wordids)
            for a in scores:
                passthescores[a] = scores[a]

        # return top ten scores
        rankedscores=sorted([(score,url) for (url,score) in passthescores.items()],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score,self.geturlname(urlid))
        return wordids,[r[1] for r in rankedscores[0:10]]
  
