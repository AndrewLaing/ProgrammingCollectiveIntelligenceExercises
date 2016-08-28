""" 
  Finds 5 similar crtics.
  
  Makes recomendations in different ways.
  Both user based (eg User based recommendations from similar critics,
  and item-based (eg Item-based recommendations based upon a users favorites.
"""

import recommendations as recommendations

def _wrap_with(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner
    # This makes colored text

def unescape(s):
    allowed = '&0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"; '
    for a in s:
        if a not in allowed:
            s.replace(a,"")
    s = s.replace(chr(96), '')
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s
    # This strips naughty non-regular characters

def convertId_to_title(werec, n=5):
    white = _wrap_with('37')
    count2 = 0
    for a in range(len(werec)):
        if count2 == n: continue
        else:
            try:
                print white(booktitles[werec[a][1]])
                count2 += 1
            except:
                print "BOOK ID",werec[a][1],"NOT IN DATABASE"
    
def create_maindic(booktitles, filename='/BX-Dump/BX-Book-Ratings.csv'):
    # {UserId: {BookId: Rating,....
    critics = {}
    fin = open(filename)
    for line in fin:
        book = line.strip().split('";"')
        userId = book[0].strip('"')
        if userId not in critics:
            stripped = book[2].strip('"')
            rated = int(stripped)
            critics[userId] = {}
            # Filter out bookIds not in BX-Books.csv
            if book[1] in booktitles:
                critics[userId][book[1]] = rated
        else:
            stripped = book[2].strip('"')
            rated = int(stripped)
            # Filter out bookIds not in BX-Books.csv
            if book[1] in booktitles:
                critics[userId][book[1]] = rated
    return critics

def create_titlesdic(filename='/BX-Dump/BX-Books.csv'):
    # {bookId: title, .....
    booktitles = {}
    fin = open(filename)
    for line in fin:
        book1 = unescape(line.strip())
        book = book1.split('";"')
        booktitles[book[0].strip('"')] = book[1].strip('"')
    return booktitles

def print_RecommendedCritics(critics, userId='60255'):
    cyan = _wrap_with('36')
    print "\n-----Similar Critics using Top Match and sim_pearson-----\n"
    top = recommendations.topMatches(critics, userId, n=5)
    for toppy in top: print cyan(toppy[1]),"with a score of",cyan(toppy[0])
    return top

def print_UBRecommendations(critics, userId='60255'):
    werec = recommendations.getRecommendations(critics, userId)[0:30]
    print "\n---------User-based Recommendations using 60255----------\n"
    # Print out n recommendations
    convertId_to_title(werec, 5)

def find_users_favoritebooks(critics, userId='60255'):
    # {rating: [bookId, ....
    scores2 = {}
    for rating1 in critics[userId]:
        if critics[userId][rating1] not in scores2:
            scores2[critics[userId][rating1]] = [rating1]
        else:
            scores2[critics[userId][rating1]].append(rating1)
    return scores2

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
    blue = _wrap_with('34')
    white = _wrap_with('37')
    cyan = _wrap_with('36')
    print blue("Creating Booktitles dictionary...")
    booktitles = create_titlesdic()                      # CREATE THE BOOKTITLES DICTIONARY
    print blue("Creating Critics dictionary...")
    critics = create_maindic(booktitles)                 # CREATE THE MAIN DICTIONARY CRITICS
    print blue("Finding Similar Critics...")
    userId = raw_input('Enter userId eg 60255 > ')
    top = print_RecommendedCritics(critics, userId)     # PRINT SOME SIMILAR CRITICS
    print "\n\n",blue("Getting recommendations from these critics..."),"\n"
    for toppy in top:                                    # Get some user based recommendations
        a = toppy[1]                                     #    from similar critics
        print "User-based recommendations from",a,"\n"
        toprecs = getRecommendations1(critics, a)[0:5]   # finds critics similar to these and gets 5 recommendations
        for film in toprecs:
            print white(booktitles[film[1]])
        print "\n--------------------------------------------------------\n"
    print_UBRecommendations(critics, userId)            # PRINT SOME USER BASED RECOMMENDATIONS
    scores2 = find_users_favoritebooks(critics, userId) # FIND USER '60255' FAVORITE BOOKS

    # MAKE SOME ITEM BASED RECOMMENDATIONS FROM USERS FAVORITE BOOKS
    print " \n----------------Item based recommendations---------------"
    # First make a list of ratings from scores2   ---- [rating, ....
    topchoices = scores2.keys()
    topchoices.sort()
    topchoices.reverse()
    count2 = 0
    # Get Item based recommendations based upon the 3 favorite books of '60255'
    for a22 in topchoices:
        for b22 in scores2[a22]:
            if count2 == 5:
                continue
            else:
                try:
                    # Get 5 item based recommendations for each book
                    bookdic = recommendations.transformPrefs(critics)
                    werec1 = recommendations.topMatches(bookdic, b22)
                    print "\nRecommendations based upon users rating of >",cyan(booktitles[b22]),"\n"
                    # Convert BookIds to booktitles
                    convertId_to_title(werec1, 10)
                    count2 += 1
                except: print "BOOK ID",b22,"NOT IN DATABASE"

