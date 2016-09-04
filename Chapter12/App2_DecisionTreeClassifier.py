""" Chapter 12 Programming Collective Intelligence: Decision Tree Classifier.

   As the chapter has no exercises in it I have decided to create a practical
   application for each of the Algorithms and Methods described.
   
   Next up the Decision Tree Classifier.
   For this I have created a simple application that reads a dataset,containing
   details for passengers on the Titanic who either died or survived, creates
   a decision tree from the dataset, gets input from the user, classifies with
   the decision tree showing the survival or death of similar passengers to
   the user. I am a survivor. :)

"""

import titanic_dataset as md
import os as os

class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb


# Divides a set on a specific column. Can handle numeric or nominal values
def divideset(rows,column,value):
    try: 
        value = int(value) # The numerical data is saved as strings within my_data
    except: 
        pass

    # Make a function that tells us if a row is in the first group (true) or the second (false)
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row: int(row[column])>=value
    else:
        split_function=lambda row:row[column]==value
        
    # Divide the rows into two sets and return them
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)


def uniquecounts(rows):
    results={}
    for row in rows:
        # The result is the last column
        r=row[len(row)-1]
        if r not in results: 
            results[r]=0
        results[r]+=1
    return results


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
            (set1,set2)=divideset(rows,col,value)

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

def did_i_survive(my_data,tree):
    while True:
        list1=[]
        os.system('clear')
        print "-"*44
        try:
            print "    WOULD I SURVIVE THE TITANIC SINKING?"
            print "-"*44
            list1.append((str(raw_input('What class are you? upper,middle or lower? >'))).lower())
            list1.append((str(raw_input('What gender are you? male or female? >'))).lower())
            list1.append(int(raw_input('What is your age? >')))
            
            a=(str(raw_input('Are you travelling with your spouse or your brother/sister? (y/n) >'))).lower()
            
            if a=="y": 
                list1.append('ysibsp')
            elif a!="y": 
                list1.append('nsibsp')
            
            a=(str(raw_input('Are you travelling with your parents or your children? (y/n) >'))).lower()
            
            if a=="y": 
                list1.append('yparch')
            elif a!="y": 
                list1.append('nparch')
            
            list1.append((str(raw_input('Which port will you be embarking from? (c)herbourg,(q)ueenstown or (s)outhampton? >'))).upper())
            print "-"*44,"\n"
            a = mdclassify(list1,tree)
            print "When the Titanic sank..."
            
            for a1 in a: 
                print a[a1],"people like you",a1
        except:
            print "-"*44,"\n"
            print "Try inputting the data properly"

        print "\n","-"*44
        
        again=str(raw_input('Enter q to QUIT or anything else to see if somebody else survived >'))
        if again=='q': 
            break


if __name__ == "__main__":
    my_data=md.my_data
    tree = buildtree(my_data)
    did_i_survive(my_data,tree)
