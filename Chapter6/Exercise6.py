""" Chapter 6 Exercise 6: Other virtual features.

    There are many virtual features like UPPERCASE that can be useful in classifying documents. 
    Documents of excessive length or with a preponderance of long words may also be clues. 
    Implement these as features. Can you think of any others?

    I implemented this in feedfilter.entryfeatures() for summarywords > 100 and 37 words in doc longet than 7 letters long.
    I also added a feature for short or long average sentence length.
"""

def splitParagraphIntoSentences(paragraph):
    sentenceEnders = re.compile(r"""
        (?:  (?<=[.!?]) | (?<=[.!?]['"]) )(?<!  Mr\.   )(?<!  Mrs\.  )(?<!  Ms\.   )
        (?<!  Jr\.   )(?<!  Dr\.   )(?<!  Prof\. )(?<!  Sr\.   )\s+""",re.IGNORECASE | re.VERBOSE)
    return sentenceEnders.split(paragraph)

def entryfeatures(entry):
    splitter = re.compile('\\W*')
    f = {}

    # Check for SHORTSENTENCES or LONGSENTENCES 
    sentences = splitParagraphIntoSentences(entry['summary'])
    totalwords = 0
    for i in sentences:
        lst1 = i.split(' ')
        totalwords += len(lst1)
        
    if (totalwords+0.0)/len(sentences) < 5:
        f['SHORTSENTENCES'] = 1
    elif (totalwords+0.0)/len(sentences) > 25:
        f['LONGSENTENCES'] = 1

    titlewords = [s.lower() for s in splitter.split(entry['title']) if len(s) > 2 and len(s) < 20]
    summarywords = [s for s in splitter.split(entry['summary']) if len(s) > 2 and len(s) < 20]

    if len(summarywords) > 100: 
        f['LONGDOC'] = 1  # Add a LONGDOC entry if more than 100 summarywords in document

    # Count uppercase words and all longwords
    uc = 0
    longwords = 0
    
    for i in range(len(summarywords)):
        w = summarywords[i]

        if len(w) > 7: longwords += 1             # Count words longer than 7 chars as longwords

        if (w.isupper()):
            uc += 1
            
        f[w.lower()] = 1

        # Get word pairs in summary as features
        if i < len(summarywords) - 1:
            twowords = ' ' . join(summarywords[i:i+1])
            f[twowords.lower()] = 1
            f['Publisher:'+ entry['publisher']] = 1
            if (float(uc) / len(summarywords) > 0.3):
                f['UPPERCASE'] = 1

    if longwords > 37: f['LONGWORDS'] = 1      # Add a LONGWORDS entry if more than 37 longwords in document
    return f


"""
    #########
    # USAGE #
    #########

    Once this is added to feedfilter it is used in the normal way.

import docclass as docclass
import feedfilter as feedfilter
cl=docclass.fisherclassifier(feedfilter.entryfeatures)
cl.setdb('python_feed.db')

feedfilter.readentryfeatures('python_search.xml',cl)

###############################################################################
    +++++++++++++++++++++++
    Possible extra features
    +++++++++++++++++++++++

    Word combos that appear in the title of the document that also appear in the summary or body of the document 
      could be given higher assumed probabilities.
    Overuse of certain forms of punctuation (?!+ etc.)
    Whitelisting/Blacklisting of phrases and words (including email addys.)
    Overuse of adjectives and superlatives (specified in a list or dictionary initialized at startup.)
    Word repetition of non-common words (ie not 'the','it','or','and' etc.)
    Percentage of numbers to letters.
    Percentage of punctuation to letters.
    Words appearing in certain sentences together.
    The comma count in a sentence.........
    +++++++++++++++++++++++
"""
