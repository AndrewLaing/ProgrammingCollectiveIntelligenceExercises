""" Chapter 7 Exercise 1: Result probabilities.

    Currently, the classify and mdclassify functions give their results as total counts.
    Modify them to give the probabilities of the results being one of the categories.
"""

def classify(observation,tree):
    if tree.results!=None:
        for a in tree.results:
            tree.results[a] = tree.results[a]/float(len(my_data))  # Returns Probability using...
        return tree.results                                        # totalcounts / totalrows
    else:
        v=observation[tree.col]
        branch=None
        if isinstance(v,int) or isinstance(v,float):
            if v>=tree.value: branch=tree.tb
            else: branch=tree.fb
        else:
            if v==tree.value: branch=tree.tb
            else: branch=tree.fb
        return classify(observation,branch)


def mdclassify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        if v==None:
            tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
            tcount=sum(tr.values())
            fcount=sum(fr.values())
            tw=float(tcount)/(tcount+fcount)
            fw=float(fcount)/(tcount+fcount)
            result={}
            for k,v in tr.items(): 
                result[k]=v*tw
            for k,v in fr.items(): 
                result[k]=v*fw
            return result
        else:
            if isinstance(v,int) or isinstance(v,float):
                if v>tree.value: 
                    branch=tree.tb
                else: 
                    branch=tree.fb
            else:
                if v==tree.value: 
                    branch=tree.tb
                else: 
                    branch=tree.fb
            return mdclassify(observation,branch)
