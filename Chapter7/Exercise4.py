""" Chapter 7 Exercise 4: Building with missing data.

    You built a function that can classify a row with missing data, 
    but what if there is missing data in the training set?
    Modify buildtree so that it will check for missing data and, in cases where 
    it's not possible to send a result down a particular branch, will send it down both branches.

    To deal with missing data I created a function called find_missingvalues() that takes the training set 
    and checks it for missing data. It does this by comparing values in the short row being checked against 
    values in a dictionary from full rows.
    This assumes that all values will be in more than one row. 
    I made an exception for the integers as these are more likely to be unreplicated, so I just check 
    that an integer is in the integer column. When missing data is discovered it adds the token 
    'MISSING' to the column.

    So now in buildtree() I don't split according to 'MISSING' being in the row, but when it is put 
    into a FalseBranch I also place it into a TrueBranch, and vice-versa.

    I hope this at least makes a little sense :)
    If not just read the code :p
"""

from PIL import Image,ImageDraw

my_data=[line.split('\t') for line in file('decision_tree_example2.txt')]
# Replace '/n' or it taints the data (example:{'Basic\n': 4, 'Premium\n': 1, 'Basic': 1})
for a in range(len(my_data)):
    for b in range(len(my_data[a])):
        my_data[a][b] = my_data[a][b].replace('\n','')

# Checks my_data for missing values
def find_missingvalues(rows):
    col_contents={}
    missinglist=[]
    column_count=len(rows[0])-1
    
    for col in range(0,column_count):
        for row in rows:
            if row in missinglist: pass
            else:
                if (len(row)!=len(rows[0])) and (row not in missinglist): 
                    missinglist.append(row)
                else:
                    if col not in col_contents:
                        col_contents[col]=[]
                        col_contents[col].append(row[col])
                    elif row[col] not in col_contents[col]:
                        col_contents[col].append(row[col])
    
    for col in range(0,column_count):
        col_contents[col].append('MISSING')
    
    for a in missinglist:
        hurr = 0
        indy = rows.index(a)
        
        while hurr==0:
            for b in range(len(a)):
                try:
                    x = int(a[b]) - int(col_contents[b][0])   # Integers may not have duplicates
                except:
                    if a[b] in col_contents[b]: pass
                    else:
                        c = a
                        c.insert(int(b),'MISSING')
                        hurr = 1
                        return rows
            
            if len(rows[indy]) == len(rows[0])-1:
                c = a
                c.insert(int(b+1),'None')  # If the end result is missing classify it as None
                rows[indy]=c
                hurr=1
    
    return rows

loop = 0

while loop==0:
    count=0
    
    for row in my_data:
        if (len(row)!=len(my_data[0])):
            my_data = find_missingvalues(my_data)
    
    for row in my_data:
        if (len(row)!=len(my_data[0])): count+=1
    
    if count==0: loop=1


class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb


# Divides a set on a specific column. Can handle numeric or nominal values
def divideset(rows,column,value):
    # Make a function that tells us if a row is in
    # the first group (true) or the second (false)
    split_function=None
    
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value
        
    # Divide the rows into two sets and return them
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)

# Create counts of possible results ( the last column of each row is the result)
def uniquecounts(rows):
    results={}
    
    for row in rows:
        # The result is the last column
        r=row[len(row)-1]
        if r not in results: 
            results[r]=0
        
        results[r]+=1
    
    return results


# Probability that a randomly placed item will be in the wrong category
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


# Entropy is the sum of p(x)log(p(x)) across all the different possible results
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


def buildtree(rows,scoref=entropy):
    if len(rows)==0: 
        return decisionnode()
    current_score=scoref(rows)

    # set up some variables to track the best criteria
    best_gain=0.0
    best_criteria=None
    best_sets=None

    column_count=len(rows[0])-1
    for col in range(0,column_count):
        # Generate the list of different values in this column
        column_values={}
        
        for row in rows:
            column_values[row[col]]=1
        
        # Now try dividing the rows up for each value in this column
        for value in column_values.keys():
            # Don't split according to whether MISSING or not
            if value == 'MISSING': 
                pass
            else:
                (set1,set2)=divideset(rows,col,value)
                
                # If MISSING is in col put it in both sets
                for a in set1:
                    if (a[col]=='MISSING') and (a not in set2):
                        set2.append(a)
                
                for a in set2:
                    if (a[col]=='MISSING') and (a not in set1):
                        set1.append(a)
                
                # Information gain
                p=float(len(set1))/len(rows)
                gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
                
                if gain>best_gain and len(set1)>0 and len(set2)>0:
                    best_gain=gain
                    best_criteria=(col,value)
                    best_sets=(set1,set2)
    
    # Create the subbranches
    if best_gain>0:
        trueBranch=buildtree(best_sets[0],scoref)                        # corrected adding scoref
        falseBranch=buildtree(best_sets[1],scoref)                       # corrected adding scoref
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
                            tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))


def printtree(tree,indent='  '):
    # Is this a leaf node?
    if tree.results!=None:
        print str(tree.results)
    else:
        # Print the criteria
        print str(tree.col)+':'+str(tree.value)+'? '

        # Print the branches
        print indent+'T->',
        printtree(tree.tb,indent+'  ')
        print indent+'F->',
        printtree(tree.fb,indent+'  ')


def getwidth(tree):
    if tree.tb==None and tree.fb==None: 
        return 1
    return getwidth(tree.tb)+getwidth(tree.fb)


def getdepth(tree):
    if tree.tb==None and tree.fb==None: 
        return 0
    return max(getdepth(tree.tb),getdepth(tree.fb))+1


def drawtree(tree,jpeg='tree.jpg'):
    w=getwidth(tree)*100
    h=getdepth(tree)*100+120

    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    drawnode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')


def drawnode(draw,tree,x,y):
    if tree.results==None:
        # Get the width of each branch
        w1=getwidth(tree.fb)*100
        w2=getwidth(tree.tb)*100

        # Determine the total space required by this node
        left=x-(w1+w2)/2
        right=x+(w1+w2)/2

        # Draw the condition string
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

        # Draw links to the branches
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))

        # Draw the branch nodes
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    else:
        txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
        draw.text((x-20,y),txt,(0,0,0))


def classify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        branch=None
        if isinstance(v,int) or isinstance(v,float):
            if v>=tree.value: 
                branch=tree.tb
            else: 
                branch=tree.fb
        else:
            if v==tree.value: 
                branch=tree.tb
            else: 
                branch=tree.fb
                
        return classify(observation,branch)


def prune(tree,mingain):
    # If the branches aren't leaves prune them
    if tree.tb.results==None:
        prune(tree.tb,mingain)
    
    if tree.fb.results==None:
        prune(tree.fb,mingain)

    # If both the subbranches are now leaves, see if they should be merged
    if tree.tb.results!=None and tree.fb.results!=None:
        # Build a combined dataset
        tb,fb=[],[]
        
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c
        
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c

        # Test the reduction in entropy
        delta=entropy(tb+fb)-(entropy(tb)+entropy(fb))/2     # Xiaochen Wang CORRECTION
        if delta<mingain:
            # Merge the branches
            tree.tb,tree.fb=None,None
            tree.results=uniquecounts(tb+fb)


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


def variance(rows):
    if len(rows)==0: 
        return 0
    
    data=[float(row[len(row)-1]) for row in rows]
    mean=sum(data)/len(data)
    variance=sum([(d-mean)**2 for d in data])/len(data)
    
    return variance
