""" Chapter 5 Exercise 5: Pairing students.

    Imagine if instead of listing dorm preferences, students had to express their preferences 
    for a roommate. How would you represent solutions to pairing students? 
    What would the cost function look like?
"""

import random as random
import math as math

# The dorms, each of which has two available spaces
dorms=['Zeus','Athena','Hercules','Bacchus','Pluto']

# People, along with their first and second choices of person
prefs1=[('Toby', ('Jeff', 'Neil')),('Steve', ('Sarah', 'Laura')),('Andrea', ('Suzie', 'Laura')),
        ('Sarah', ('Toby', 'Jeff')),('Dave', ('Neil', 'Fred')),('Jeff', ('Toby', 'Dave')),
        ('Fred', ('Steve', 'Dave')),('Suzie', ('Andrea', 'Laura')),('Laura', ('Suzie', 'Andrea')),
        ('Neil', ('Fred', 'Toby'))]


# [(0,9),(0,8),(0,7),....(0,0)]]
domain=[(0,(len(dorms)*2)-i-1) for i in range(0,len(dorms)*2)]

def printsolution(vec):
    slots=[]
    
    # Create two slots for each dorm
    for i in range(len(dorms)): 
        slots+=[i,i]

    # Loop over each students assignment printing out the results
    print "\nStudent          Assigned Dorm"
    print "------------------------------"
    
    for i in range(len(vec)):
        x=int(vec[i])
        # Choose the slots from the remaining ones
        dorm=dorms[slots[x]]
        # Show the student and assigned dorm
        print prefs[i][0],' '*(15-len(prefs[i][0])),dorm
        # Remove this slot
        del slots[x]


def partner_dormcost(vec):
    cost = 0
    count = 0   # 0 = first person in dorm, 1 = second person in dorm.
    assigned=[] # A list to be populated with assigned dorms.
    slots=[]
    
    for i in range(len(dorms)): 
        slots+=[i,i]

    # Loop over each students assignment and append to assigned.
    for i in range(len(vec)):
        x=int(vec[i])
        assigned.append(slots[x])
        del slots[x]

    # Cost the dorm assignment based on the assigned vs the preferred.
    for i in range(10):
        if count == 0:
            if prefs1[assigned[i+1]][0] in prefs1[assigned[i]][1][0]: 
                cost+=0                                                   # If first choice of sleeping partner
            elif prefs1[assigned[i+1]][0] in prefs1[assigned[i]][1][1]: 
                cost+=1                                                   # If second choice of sleeping partner
            else: 
                cost+=3                                                   # If not a chosen sleeping partner
            count += 1
        else:
            if prefs1[assigned[i-1]][0] in prefs1[assigned[i]][1]: 
                cost+=0                                                   # Same as above for the second dorm slot
            elif prefs1[assigned[i-1]][0] in prefs1[assigned[i]][1][1]: 
                cost+=1
            else: 
                cost+=3
            count = 0
            
    return cost
    
