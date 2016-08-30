""" Chapter 6 Exercise 4: Arbitrary phrase length.

    This chapter showed you how to extract word pairs as well as individual words.
    Make the feature extraction configurable to extract up to a specified number of words 
    as a single feature.

    First with entryfeatures() from feedfilter.
    Added to the function itself otherwise docclass.py needs this variable adding throughout.

    Second added to getwords() from emailfilter (ch6 ex3).
"""
# +++++++++++++++++++
# ++++++ FIRST ++++++
# +++++++++++++++++++

def entryfeatures(entry):
    wordnum=3                     # wordnum = number of words to add together as many words (eg 'I Love Lola')
    splitter = re.compile('\\W*')
    f = {}

    # Extract the title words and annotate
    titlewords = [s.lower() for s in splitter.split(entry['title']) if len(s) > 2 and len(s) < 20]

    # Extract the summary words
    summarywords = [s for s in splitter.split(entry['summary']) if len(s) > 2 and len(s) < 20]

    # Count uppercase words
    uc = 0
    for i in range(len(summarywords)):
        w = summarywords[i]
        if (w.isupper()):
            uc += 1
        f[w.lower()] = 1

        # Get word pairs in summary as features
        if i < len(summarywords) - wordnum:
            manywords = ' ' . join(summarywords[i:i+wordnum])
            f[manywords.lower()] = 1

            # Keep creator and publisher whole
            f['Publisher:'+ entry['publisher']] = 1

            # UPPERCASE is a virtual word flagging too much shouting
            if (float(uc) / len(summarywords) > 0.3):
                f['UPPERCASE'] = 1

    return f


# ++++++++++++++++++++
# ++++++ SECOND ++++++
# ++++++++++++++++++++

def getwords(doc):
    wordnum=4                     # wordnum = number of words to add together as many words (eg 'Lola loves cute guys')
    splitter=re.compile('\\W*')
    emails = re.findall("[\w.]+@[\w.]+", doc)
    
    for a in range(len(emails)):   
        if emails[a][-1] == '>':
            emails[a]= emails[a][:-1]
            
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', doc)
    
    for a in range(len(urls)):   
        if urls[a][-1] == '>':
            urls[a]= urls[a][:-1]

    for a in urls:
        doc = doc.replace(a," ")
        
    for a in emails:
        doc = doc.replace(a," ")

    doc = ''.join(i for i in doc if not i.isdigit())
    words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]

    for a in range(len(words)-wordnum+1):
        phrases = ' '.join(words[a:a+wordnum])
        words.append(phrases)

    words = words + urls + emails
    
    # Return the unique set of words only
    return dict([(w,1) for w in words])
    
