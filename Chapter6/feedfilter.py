import feedparser as feedparser
import re as re

# Takes a filename or URL of a blog feed and classifies the entries
def read(feed,classifier):
    # Get feed entries and loop over them
    f=feedparser.parse(feed)
    
    for entry in f['entries']:
        print
        print '-----'
        # Print the contents of the entry
        print 'Title:     '+entry['title'].encode('utf-8')
        print 'Publisher  '+entry['publisher'].encode('utf-8')
        print
        print entry['summary'].encode('utf-8')

        # Combine all the text to create one item for the classifier
        fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])

        # Print the best guess at the current category
        print 'Guess: '+str(classifier.classify(fulltext))

        # Ask the user to specify the correct category and train on that
        cl=raw_input('Enter category: ')
        classifier.train(fulltext,cl)


def readentryfeatures(feed,classifier):
    # Get feed entries and loop over them
    f=feedparser.parse(feed)
    
    for entry in f['entries']:
        print
        print '-----'
        # Print the contents of the entry
        print 'Title:     '+entry['title'].encode('utf-8')
        print 'Publisher  '+entry['publisher'].encode('utf-8')
        print
        print entry['summary'].encode('utf-8')

        # Combine all the text to create one item for the classifier
        fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])

        # Print the best guess at the current category
        print 'Guess: '+str(classifier.classify(entry))

        # Ask the user to specify the correct category and train on that
        cl=raw_input('Enter category: ')
        classifier.train(entry,cl)


def entryfeatures(entry):
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
        if i < len(summarywords) - 1:
            twowords = ' ' . join(summarywords[i:i+1])
            f[twowords.lower()] = 1

            # Keep creator and publisher whole
            f['Publisher:'+ entry['publisher']] = 1

            # UPPERCASE is a virtual word flagging too much shouting (if percentage of upper >30%)
            if (float(uc) / len(summarywords) > 0.3):
                f['UPPERCASE'] = 1

    return f

    
""" entryfeatures() is corrected so it actually flags UPPERCASE's
    and readentryfeatures() is the version of read() corrected for

         cl=docclass.fisherclassifier(feedfilter.entryfeatures)
         cl.setdb('python_feed1.db')
         feedfilter.readentryfeatures('mini_python_search.xml',cl)
"""
