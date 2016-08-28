import feedparser
import re

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
    # Parse the feed
    d=feedparser.parse(url)
    # Loop over all the entries
    wc1 = {}
    for e in d.entries:
        wc={}
        if 'summary' in e: summary=e.summary
        else: summary=e.description
        if 'updated' in e: updated=e.updated.split('T')[0]
        elif 'published' in e: updated='do summit'
        else: updated = 'I dunno when it was published'

        title = str(updated+'/'+d['feed']['title']+' - '+e.title)
        # Extract a list of words
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
        wc1[title] = wc
    return wc1


def getwords(html):
    # Remove all the HTML tags
    txt=re.compile(r'<[^>]+>').sub('',html)

    # Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word!='']


apcount={}
wordcounts={}
wordlist=[]
feedlist=[line for line in file('feedlist.txt')]
for feedurl in feedlist:
    try:
        wc1 = getwordcounts(feedurl.strip())
        if len(wc1) <= 0: pass
        else:
            for title in wc1:
                wordcounts[title] = wc1[title]
                for word,count in wc1[title].items():
                    apcount.setdefault(word,0)
                    if count>1:
                        apcount[word]+=1
            for w,bc in apcount.items():
                frac=float(bc)/len(wc1)
                if frac>0.1 and frac<0.5:
                    wordlist.append(w)
    except:
        print 'Failed to parse feed %s' % feedurl

# Create a textfile containing matrix of all wordcounts from all blogs
out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
  print blog
  out.write(blog.encode('utf8'))
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')


"""
  Using a smaller feedlist, the original generated blogdata was 32M.
  
  ************************
  Printing out the cluster
  ************************
  import clusters as clusters
  blogentries, words, data = clusters.readfile('blogdata5.txt')
  coords = clusters.scaledown(data)
  clusters.draw2d(coords, blogentries, jpeg='blog_entries.jpg')
"
