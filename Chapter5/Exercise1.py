""" Chapter 5 Exercise 1: Group travel cost function.

    Add total flight time as a cost equal to $0.50 per minute on the plane. 
    Next try adding a penalty of $20 for making anyone get to the airport before 8 a.m.

    The function was altered to include the costs mentioned above.
"""

def schedulecost(sol):
    totalprice=0
    latestarrival=0
    earliestdep=24*60
    
    for d in range(len(sol)/2):
        # Get the inbound and outbound flights
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(sol[2*d])]    # Corrected for iterating wrongly
        returnf = flights[(destination,origin)][int(sol[(2*d)+1])] # Corrected for iterating wrongly

        # Total price is the price of all outbound and return flights
        totalprice+=outbound[2]
        totalprice+=returnf[2]

        # Add $.0.50 for each minute spent on the plane there and back         # Chapter 5 Exercise 1
        totalprice+=((getminutes(outbound[1]))-(getminutes(outbound[0])))*0.5
        totalprice+=((getminutes(returnf[1]))-(getminutes(returnf[0])))*0.5

        # Add $20 if person arrives at the airport before 8:00 a.m             # Chapter 5 Exercise 1
        if outbound[0]<'08:00': totalprice += 20
        if returnf[0]<'08:00': totalprice += 20

        # Track the latest arrival and earliest departure
        if latestarrival<getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives.
    # They must also arrive at the same time and wait for their flights
    totalwait=0
    
    for d in range(len(sol)/2):
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[2*d])]    # Corrected for iterating wrongly
        returnf=flights[(destination,origin)][int(sol[(2*d)+1])] # Corrected for iterating wrongly
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    # Does this solution require an extra day of car rental? That'll be $50
    if latestarrival<earliestdep: totalprice+=50  # Corrected

    return totalprice+totalwait
    
