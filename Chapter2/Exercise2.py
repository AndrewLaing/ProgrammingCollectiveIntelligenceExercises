"""
Exercise 2

 Tag similarity. Using the del.icio.us API, create a dataset of tags and items. 
 Use this to calculate similarity between tags and see if you can find any that 
 are almost identical. Find some items that could have been tagged programming 
 but were not.
"""

from pydelicious import DeliciousAPI
from pydelicious import *
from getpass import getpass
from time import sleep


def invert_dict(d):
    inverse = dict()
    for key in d:
        val = d[key]
        if val not in inverse:
            inverse[val] = [key]
        else:
            inverse[val].append(key)
    return inverse


def main():
    username = str(raw_input('Username:'))
    pwd = getpass('Pwd:')
    a = DeliciousAPI(username, pwd)

    # Get list of tagged urls
    tagposts = get_tagposts('programming')
    sleep(2)

    # Put tagged urls into list
    list1 = []
    for a in range(len(tagposts)):
        count = 0
        for b in tagposts[a]:
            count += 1
            if count == 4:
                list1.append(tagposts[a][b])

    # Get all instances of urls 
    dic2 = {}
    for url in list1:
        post = get_urlposts(url)

    # Put tags into histogram
        for a in range(len(post)):
            count = 0
            for b in post[a]:
                count += 1
                if count == 3:
                    if (post[a][b] not in dic2):
                        dic2[post[a][b]] = 1
                    else:
                        dic2[post[a][b]] = dic2[post[a][b]] + 1

    # Invert the histogram and print most often first
    dic3 = invert_dict(dic2)
    # Print results
    res = dic3.keys()
    res.sort()
    res.reverse()
    print res
    for z in res:
        print dic3[z],"appears",z,"times"


if __name__ == "__main__":
    main()
