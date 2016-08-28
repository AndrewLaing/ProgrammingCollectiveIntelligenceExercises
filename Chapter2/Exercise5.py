""" Now recommends albums from artists """
import os as os
import urllib
import json                        # we are after all importing json
from time import sleep
from recommendations import *

def sim_tanimoto(prefs, p1, p2):
    Na = Nb = Nc = 0.0
    # count elements
    for item in prefs[p1]:
        Na += 1.0
        if item in prefs[p2]: Nc += 1.0
    for item in prefs[p2]:
        Nb += 1.0
    # calculate tanimoto score
    num = Nc
    den = (Na + Nb) - Nc
    r = float(num/den)
    return r
    
def user_getTopArtists(username):
    global banddic, api_key
    urlstart = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="
    urllimit = "&limit="
    urlpage = "&page="
    urlend = "&api_key="+api_key+"&format=json"
    url = urlstart

    def download_it(url):
        global banddic
        dic = {}
        conn = urllib.urlopen(url)
        for line in conn:              # comes as a unicode string
            dic = json.loads(line)     # load json into dic
        for f in range(len(dic['topartists']['artist'])):
            bandname = dic['topartists']['artist'][f]['name']
            rank = dic['topartists']['artist'][f]['@attr']['rank']
            # Give scores to each users top ten ranked artists
            if int(rank) == 1: score = 10
            elif int(rank) == 2 : score = 9
            elif int(rank) == 3: score = 8
            elif int(rank) == 4 : score = 7
            elif int(rank) == 5: score = 6
            elif int(rank) == 6 : score = 5
            elif int(rank) == 7: score = 4
            elif int(rank) == 8 : score = 3
            elif int(rank) == 9: score = 2
            elif int(rank) == 10 : score = 1
            else: score = 0
            try:
                if score > 0:
                    if username not in banddic:
                        banddic[username] = {}
                        banddic[username][bandname] = score
                    else:
                        banddic[username][bandname] = score
                else: pass
            except: pass
    url += username
    url += urlend
    download_it(url)

def artist_getTopAlbums(artist):
    global api_key
    urlstart = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist="
    urlend = "&api_key="+api_key+"&format=json"
    url = urlstart

    def download_it(url):
        global resultdic
        dic = {}
        try:
            conn = urllib.urlopen(url)
            for line in conn:              # comes as a unicode string
                dic = json.loads(line)     # load json into dic
            count1 = 0
            print "Recommended albums by",artist
            for a in range(len(dic['topalbums']['album'])):
                albumname = dic['topalbums']['album'][a]['name']
                rank = dic['topalbums']['album'][a]['@attr']['rank']
                print rank,":",albumname
                count1 += 1
                if count1 == 5: break
        except: pass
        print "------------------"
    url += artist
    url += urlend
    download_it(url)

def artist_gettopfans():
    global firstband
    ch = """
###############################################################
#      artist.getTopFans                                      #
#                                                             #
###############################################################
Enter name of Artist : """

    global api_key
    urlstart = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopfans&artist="
    urlend = "&autocorrect=1&api_key="+api_key+"&format=json"
    url = urlstart
    os.system('clear')
    def download_it(url):
        dic = {}
        conn = urllib.urlopen(url)
        print "\nProcessing recommendations from..."
        for line in conn:              # comes as a unicode string
            dic = json.loads(line)     # load json into dic
            try:
                count2 = 0
                for f in range(len(dic['topfans']['user'])):
                    print dic['topfans']['user'][f]['name']
                    username = dic['topfans']['user'][f]['name']
                    user_getTopArtists(username)
                    count2 += 1
                    if count2 == 21: break
                    sleep(0.7)
                return True
            except: return False
    os.system('clear')
    firstband = raw_input(ch)
    url += firstband
    url += urlend
    frog = download_it(url)
    return int(frog)

def main():
    global banddic, firstband
    bruce = int(artist_gettopfans())
    while bruce == False:
        bruce = int(artist_gettopfans())

    dict1 = {}
    high = 0
    # Compare banddic and add to dict1
    for a in banddic:
        for b in banddic:
            if b != a:
                crit1 = str(a)
                crit2 = str(b)
                tani = sim_tanimoto(banddic, crit1, crit2)
                if tani not in dict1:
                    dict1[tani] = [crit1, crit2]

    # Find high score and print results
    for a in dict1:
        if a > high: high = a
    os.system('clear')
    print "\nThe two most similar Last-fm users who are fans of",firstband,"are;\n    ",dict1[high][0],"and",dict1[high][1]
    print "with a Tanimoto_similarity Score of",high

    criti1 = str(dict1[high][0])
    criti2 = str(dict1[high][1])

    minidic = {}
    for a in banddic[criti1]:
        try:
            a2 = ((banddic[criti1][a])+(banddic[criti2][a]))/2.0
            if a2 not in minidic:
                minidic[a2] = [a]
            else: minidic[a2].append(a)
        except: pass
    a3 = minidic.keys()
    a3.sort()
    a3.reverse()
    print "\nAnd they recommend\n------------------"
    for a in a3:
        for b in range (len(minidic[a])):
            artist = minidic[a][b]
            print "---",minidic[a][b],a,"---"
            artist_getTopAlbums(artist)
    d = raw_input('Press <enter> to continue')

welcomeScreen = """
########################################################################
#        _           _                _      ___               _       #
#       /_\  _ _  __| |_ _ _____ __ _( )___ | _ ) __ _ _ _  __| |      #
#      / _ \| ' \/ _` | '_/ -_) V  V //(_-< | _ \/ _` | ' \/ _` |      #
#     /_/ \_\_||_\__,_|_| \___|\_/\_/  /__/ |___/\__,_|_||_\__,_|      #
#          | _ \___ __ ___ _ __  _ __  ___ _ _  __| |___ _ _           #
#          |   / -_) _/ _ \ '  \| '  \/ -_) ' \/ _` / -_) '_|          #
#          |_|_\___\__\___/_|_|_|_|_|_\___|_||_\__,_\___|_|            #
#                                                                      #
# This application recommends bands for you to listen to based upon    #
# the listening habits of Last-fm users. Just enter the name of a band #
# and the application will get a recommended band from two fans of     #
# band who have the most similar tastes, according to their Tanimoto   #
# similarity score. It is pretty simple to use.                        #
########################################################################
"""
os.system('clear')
api_key = str(raw_input('Please enter your Last-fm api_key >'))
os.system('clear')
d = ""
while (d != "q") or (d != "Q"):
    os.system('clear')
    firstband = ""
    banddic = {}
    print welcomeScreen
    d = str(raw_input('Press <enter> to start or enter <q> to quit > '))
    if d != "q":
        main()
    else: break
