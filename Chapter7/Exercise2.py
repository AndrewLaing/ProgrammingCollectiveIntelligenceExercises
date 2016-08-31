""" Chapter 7 Exercise 2: Missing Data Ranges.

    mdclassify allows the use of "None" to specify a missing value. 
    For numerical values the result may not be completely unknown, 
    but may be known to be in a range. 
    Modify mdclassify to allow a tuple such as (20,25) in place of a value 
    and traverse down both branches when necessary. 
"""

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
            if isinstance(v,tuple):
                for a in v:
                    if int(a)>int(tree.value):
                        branch=tree.tb
                        observation[tree.col] = int(a)
                        return mdclassify(observation,branch)  # See if either value from tuple > tree.value
                branch=tree.fb                                 # If yes branch=tree.tb   else branch=tree.fb
            elif isinstance(v,int) or isinstance(v,float):
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
