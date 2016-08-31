""" Chapter 7 Exercise 5: Multiway splits. (Hard)

    All the trees built in this chapter are binary decision trees.
    However, some datasets might be simpler trees if they allowed a node to split 
    into more than two branches.
    How would you represent this? How would you train the tree?

    I replaced 'tb' and 'fb' with 'allbranches' which contains a dictionary, 
    holding all of the splits for the node.
    (Example: {'New Zealand': <Ch7Ex5.decisionnode instance at 0x81a2c8c>, 
               'UK': <Ch7Ex5.decisionnode instance at 0x81a2ccc>})
    Obviously I rewrote buildtree() to make multiple splits, and printtree() to print them.
    divide_set() is replaced with make_set() which makes a single set for the value passed to it.
    make_a_dic() makes a dictionary of {value: set, ...}  for the values in the specified column 
    of the set passed to it. 
    I rewrote classify() as two connected functions classify() and main_classify(). 
    classify() can deal with missing data in the observation. 
    The using of this code is the same as for treepredict. 
    (except I haven't implemented prune() or the jpeg creating functions.) See end for example usage.

    I had lots of fun with recursion doing this exercise :)
"""

my_data=[line.split('\t') for line in file('decision_tree_example.txt')]
# Replace '/n' or it taints the data (example:{'Basic\n': 4, 'Premium\n': 1, 'Basic': 1})
for a in range(len(my_data)):
    for b in range(len(my_data[a])):
        my_data[a][b] = my_data[a][b].replace('\n','')

class decisionnode:
    def __init__(self,col=-1,results=None,allbranches=None):
        self.col=col
        self.results=results
        self.allbranches=allbranches


def uniquecounts(rows):
    results={}
    for row in rows:
        # The result is the last column
        r=row[len(row)-1]
        
        if r not in results: 
            results[r]=0
        results[r]+=1
    return results


def variance(rows):
    if len(rows)==0: 
        return 0
        
    data=[float(row[len(row)-1]) for row in rows]
    mean=sum(data)/len(data)
    variance=sum([(d-mean)**2 for d in data])/len(data)
    return variance


def giniimpurity(rows):
    total=len(rows)
    counts=uniquecounts(rows)
    imp=0
    
    for k1 in counts:
        p1=float(counts[k1])/total
        for k2 in counts:
            if k1==k2: 
                continue
            p2=float(counts[k2])/total
            imp+=p1*p2
    return imp


def entropy(rows):
    from math import log
    log2=lambda x:log(x)/log(2)
    results=uniquecounts(rows)
    # Now calculate the entropy
    ent=0.0
    
    for r in results.keys():
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent


def make_set(rows,column,value):
    split_function=None
    
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value
    
    set1=[row for row in rows if split_function(row)]
    return set1


def make_a_dic(rows,column):
    dicus = {}
    
    for a in range(len(rows)):
        value = rows[a][column]
        set1 = make_set(rows,column,value)
        dicus[value] = set1
    
    return dicus


def buildtree(rows,scoref=entropy):
    if len(rows)==0: 
        return decisionnode() 
    
    current_score=scoref(rows)
    best_gain=0.0
    best_criteria=None                 # Best criteria in multi split is just column number
    best_sets=None                     # because values are contained in the dictionary in bestsets
    column_count=len(rows[0])-1
    
    for col in range(0,column_count):
        # Generate the dictionary of different values in this column
        dicus = make_a_dic(rows,col)
        # Calculate which dicus is best_dicus here
        gain = current_score
        lensets = 0
        
        for a in (dicus):
            lena = len(dicus[a])
            lensets += lena
            score = scoref(dicus[a])
            p = float(lena)/len(rows)
            gain-=(p*score)
        
        if gain>best_gain and lensets>0:
            best_gain=gain
            best_criteria=(col)
            best_sets=dicus
    
    if best_gain>0:
        branches = {}
        for set in best_sets:
            branch = buildtree(best_sets[set],scoref)
            branches[set]=branch
        return decisionnode(col=best_criteria, allbranches=branches)
    else:
        return decisionnode(results=uniquecounts(rows))


def printtree(tree,indent='  '):
    # Is this a leaf node?
    if tree.results!=None:
        print str(tree.results)
    else:
        print str(tree.col)+':'
        for a in tree.allbranches:
            print indent+str(a)+'->',
            printtree(tree.allbranches[a],indent+'  ')


def main_classify(observation,tree):
    result_dic={}
    
    if tree.results!=None: 
        return tree.results
    else:
        v=str(observation[tree.col])
        
        if v in tree.allbranches: 
            dic_a = main_classify(observation,tree.allbranches[v])
        else:
            for a in tree.allbranches:
                dic_a = main_classify(observation,tree.allbranches[a])
                
                for a in dic_a:
                    if a not in result_dic: 
                        result_dic[a]=dic_a[a]
                    else: 
                        result_dic[a]=result_dic[a]+dic_a[a]
            
            return result_dic
    
    for a in dic_a:
        if a not in result_dic: 
            result_dic[a]=dic_a[a]
        else: 
            result_dic[a]=result_dic[a]+dic_a[a]
    
    return result_dic


def classify(observation,tree):
    count=0     # Variable to divide res scores by the number of results it is made from
    res={}
    v=observation[tree.col]
    
    if v in tree.allbranches: 
        return main_classify(observation,tree)
    
    # If v isn't in tree.allbranches move on to the next level of branches
    for a in tree.allbranches:
        v = observation[tree.allbranches[a].col]
        if tree.allbranches[a].allbranches!=None:
            if v in tree.allbranches[a].allbranches:
                result = main_classify(observation,tree.allbranches[a])
                count+=1
                
                for a in result:
                    if a not in res: 
                        res[a]=result[a]
                    else: 
                        res[a]=res[a]+result[a]
    
    if len(res)==0: 
        return main_classify(observation,tree)
    else:
        for a in res:
            res[a]=float(res[a])/count
        return res


""" 
*************
Example usage
*************
>>>import Ch7Ex5 as treepredict
>>>tree = treepredict.buildtree(treepredict.my_data,scoref=treepredict.entropy)
>>>treepredict.printtree(tree)
0:
  (direct)-> 1:
    New Zealand-> {'None': 1}
    UK-> {'Basic': 1}
  slashdot-> {'None': 3}
  kiwitobes-> 1:
    UK-> {'None': 1}
    France-> {'Basic': 2}
  digg-> 2:
    yes-> {'Basic': 2}
    no-> {'None': 1}
  google-> 3:
    24-> {'Premium': 1}
    18-> 2:
      yes-> {'Basic': 1}
      no-> {'None': 1}
    21-> {'Premium': 1}
    23-> {'Premium': 1}

>>> treepredict.classify(['(direct)','USA','yes','5'],tree)
{'None': 1, 'Basic': 1}
>>> treepredict.classify([None,'France','yes','5'],tree)
{'Basic': 2.0}
"""
