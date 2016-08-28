""" 
  User-based efficiency.
  
  The user-based filtering algorithm is inefficient because it compares a user to all other users 
  every time a recommendation is needed. Write a function to precompute user similarities, and 
  alter the recommendation code to use only the top five other users to get recomendations

  Variables.

  person - the person to get recommendations for
  prefs  - the dataset
  n      - the number of critics to get recommendations from

"""

import recommendations as recommendations

def getn_similarcritics(prefs,person,n=5):
    dict1 = {}
    high = 0
    # Compare critics to person and add to dict1
    for b in prefs:
        if b != person:
            crit2 = str(b)
            pear = recommendations.sim_pearson(prefs, person, crit2)
            if pear not in dict1:
                dict1[pear] = [person, crit2]

    # return top n critics
    res = dict1.keys()
    res.sort()
    res.reverse()
    listout = []
    for a in range(n):
        listout.append(dict1[res[a]][1])

    return listout


def getRecommendations1(prefs, person, similarity=recommendations.sim_pearson):
    totals = {}
    simSums = {}

    others = getn_similarcritics(prefs,person)
    for other in others:
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:

                # Similarity * Score
                totals.setdefault(item,0)
                totals[item] += prefs[other][item]*sim

                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total/simSums[item],item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


if __name__ == "__main__":
    prefs = recommendations.loadMovieLens()
    print getRecommendations1(prefs, '87')[0:30]
