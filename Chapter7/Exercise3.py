""" Chapter 7 Exercise 3: Early Stopping.

    Rather than pruning the tree, buildtree can just stop dividing when it reaches a point 
    where the entropy is not reduced enough. This may not be ideal in some cases, but it does save an extra step.
    Modify buildtree to take a minimum gain parameter and stop dividing the branch if this condition is not met.

    Example usage: buildtree(rows,mingain=60.0)
    Implemented in a more user-friendly way as a percentage of the first current score. 
    This makes it easier to play with values :)
    (If entropy is not reduced enough this results in a lower percentage)   
"""

def buildtree(rows,scoref=entropy,mingain=0.0,firstscore=0):
    if len(rows)==0: 
        return decisionnode()

    current_score=scoref(rows)

    if firstscore==0:                                                 # <--Exercise 3 here
        firstscore = float(current_score)                             # <-- " " " " " " "
    if float((current_score/firstscore)*(100.0/1))<float(mingain):    # <-- " " " " " " "
        return decisionnode(results=uniquecounts(rows))               # <-- " " " " " " "

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
        trueBranch=buildtree(best_sets[0],scoref,mingain,firstscore)                        # corrected adding scoref
        falseBranch=buildtree(best_sets[1],scoref,mingain,firstscore)                       # corrected adding scoref

        return decisionnode(col=best_criteria[0],value=best_criteria[1],
                            tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))
