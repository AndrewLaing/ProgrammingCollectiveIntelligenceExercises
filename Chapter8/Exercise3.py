""" Chapter 8 Exercise 3: Eliminating variables.

    Rather than trying to optimize variable scales for a large set of variables that are probably useless, 
    you could try to eliminate variables that make the prediction worse before doing anything else.
    Can you think of a way to do this?

    This creates a deepcopy of 'data', so the original remains unchanged, then removes the specified indices 
    from the 'input' sections in the dictionaries,(So you can try removing variables without losing 
    the original loaded dataset.)
    The second obvious approach is not to import the variables into the dataset in the first place :)
    
    See end for usage. 
"""

def elim_variables(data,remove_list):
    from copy import deepcopy
    
    data1 = deepcopy(data)
    
    for row in range(len(data1)):
        list1=[]
        
        for a in range(len(data1[row]['input'])):     
            if a in remove_list: 
                pass
            else: 
                list1.append(data1[row]['input'][a])
        
        data1[row]['input']=list1
    
    return data1

"""
---------------------------------------------------------------------------------------------------
   usage
   *****
import numpredict as numpredict

data = numpredict.wineset1()
data1 = elim_variables(data,[0,3])     # Indices of data['input']

"""
