""" Chapter 12 Programming Collective Intelligence: Bayesian Classifier.

    As the chapter has no exercises in it I have decided to create a practical
    application for each of the Algorithms and Methods described.
    First up is the Bayesian Classifier.
    For this I have created a simple gmail client with a Trainable Bayesian Classifier.
    There is lots of space for adding features, but I am sticking to the subject matter
    of the book :)
    """

import imaplib
import htmlentitydefs
import poplib, email, string
import getpass as getpass
import re as re
import math as math
from pysqlite2 import dbapi2 as sqlite
import os as os


def htmlentitydecode(s):
    def entity2char(m):
        entity = m.group(1)
        if entity in htmlentitydefs.name2codepoint:
            return unichr(htmlentitydefs.name2codepoint[entity])
        return u" "  # Unknown entity: We replace with a space.
    
    t = re.sub(u'&(%s);' % u'|'.join(htmlentitydefs.name2codepoint), entity2char, s)
    t = re.sub(u'&#(\d+);', lambda x: unichr(int(x.group(1))), t)
    return re.sub(u'&#x(\w+);', lambda x: unichr(int(x.group(1),16)), t)


def stripTags(s):
    intag = [False]
    
    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True
    
    return ''.join(c for c in s if chk(c))


def getwords(doc):
    splitter=re.compile('\\W*')
    
    # Split the words by non-alpha characters
    words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    
    # Return the unique set of words only
    return dict([(w,1) for w in words])


class classifier:
    def __init__(self,getfeatures,filename=None):
        self.getfeatures=getfeatures

    def setdb(self,dbfile):
        self.con=sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count,ap)')
        self.con.execute('create table if not exists cc(category,count)')
        
    # Increase the count of a feature/category pair
    def incf(self,f,cat):
        count=self.fcount(f,cat)
        try:
            if count==0:
                self.con.execute("insert into fc values ('%s','%s',1,0.5)" % (f,cat)) # default ap value is 0.5
            else:
                self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count+1,f,cat))
        except: print "error adding",f,"in category",cat

    def set_ap(self,f,cat,ap):
        changeit = "update fc set ap="+str(ap)+" where feature='"+f+"' and category='"+cat+"'"
        self.con.execute(changeit)

    def get_ap(self,f,cat):
        res=self.con.execute('select ap from fc where feature="%s" and category="%s"' % (f,cat)).fetchone()
        if res==None: 
            return 0   # default ap value
        else: 
            return float(res[0])

    # Increase the count of a category
    def incc(self,cat):
        count=self.catcount(cat)
        try:
            if count==0:
                self.con.execute("insert into cc values ('%s',1)" % (cat))
            else:
                self.con.execute("update cc set count=%d where category='%s'" % (count+1,cat))
        except: 
            print "error adding",f,"in category",cat

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        res=self.con.execute('select count from fc where feature="%s" and category="%s"' % (f,cat)).fetchone()
        if res==None: 
            return 0
        else: 
            return float(res[0])

    # The number of items in a category
    def catcount(self,cat):
        res=self.con.execute('select count from cc where category="%s"' % (cat)).fetchone()
        if res==None: 
            return 0
        else: 
            return float(res[0])

    # The total number of items
    def totalcount(self):
        res=self.con.execute('select sum(count) from cc').fetchone()
        if res==None: 
            return 0
        return res[0]

    # The list of all the categories
    def categories(self):
        cur=self.con.execute('select category from cc')
        return [d[0] for d in cur]

    def train(self,item,cat):
        features=self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)

        # Increment the count for this category
        self.incc(cat)
        self.con.commit()

    def fprob(self,f,cat):
        if self.catcount(cat)==0: 
            return 0

        # The total number of times this feature appeared in this category
        # divided by the total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0):
        # Calculate current probability
        basicprob=prf(f,cat)
        # Count the number of times this feature has appeared in all categories
        totals=sum([self.fcount(f,c) for c in self.categories()])

        # Get the assumed probability for the feature
        ap = self.get_ap(f,cat)
        if ap==0: 
            ap=0.5                    # If feature not in db give it the default value
        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

    # See what features are in a certain category
    def examine_category(self):
        catnam = str(raw_input('Type category name to examine features for>'))
        cur = self.con.execute('select * from fc where category="%s"' % catnam)
        count = 0
        for a in cur:        
            count+=1
            if count == 30:
                pause=raw_input('press enter to continue')
                count=0
            print a
        cont=(raw_input('Press <ENTER> to continue'))

    # look at the category names in cc
    def get_catnames(self):
        cur = self.con.execute('select * from cc')
        print "-"*44
        for a in cur: 
            print a[0]
        cont=(raw_input('Press <ENTER> to continue'))

    # rename/correct name of a category in cc   
    def rename_category_in_fc(self):
        catnam = str(raw_input('Enter category to rename >'))
        newcatname = str(raw_input('Enter new category name >'))
        self.con.execute("update fc set category='%s' where category='%s'" % (newcatname,catnam))
        print catnam,"renamed as",newcatname
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    # rename/correct name of a category in cc   
    def rename_category_in_fc(self):
        catnam = str(raw_input('Enter category to rename >'))
        newcatname = str(raw_input('Enter new category name >'))
        self.con.execute("update fc set category='%s' where category='%s'" % (newcatname,catnam))
        print catnam,"renamed as",newcatname
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    # rename/correct name of a category in cc
    def rename_category_in_cc(self):
        catnam = str(raw_input('Enter category name to rename >'))
        newcatname = str(raw_input('Enter new category name >'))
        self.con.execute("update cc set category='%s' where category='%s'" % (newcatname,catnam))
        print catnam,"renamed as",newcatname
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    # change the weight of a feature in fc
    def change_featweight(self):
        featnam = str(raw_input('Enter feature name >'))
        catnam = str(raw_input('Enter category name >'))
        newweight= float(raw_input('Enter new weight for feature >'))
        self.set_ap(featnam,catnam,newweight)
        print "New feaure weight is",newweight
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    # show all examples of a feature in fc (from all categories)
    def examine_feature(self):
        featnam = str(raw_input('Enter feature name >'))
        cur = self.con.execute('select * from fc where feature="%s"' % featnam)
        print "-"*44
        for a in cur: 
            print a 
        cont=(raw_input('Press <ENTER> to continue'))
        
    # rename/correct name of a category in cc   
    def recategorize_in_fc(self):
        featnam = str(raw_input('Enter feature to recategorize >'))
        newcatname = str(raw_input('Enter new category name >'))
        self.con.execute("update fc set category='%s' where feature='%s'" % (newcatname,featnam))
        print featnam,"recategorized as",newcatnam
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    def delete_feat(self):
        featnam = str(raw_input('Enter feature to delete >'))
        cur = self.con.execute('select * from fc where feature="%s"' % featnam)
        print "-"*44
        for a in cur: print a
        delme = str(raw_input("Is this the feature you wish to delete?(y/n) >"))
        if delme=="y" or delme=="Y":
            self.con.execute("delete from fc where feature='%s'" % featnam)
            print "Feature deleted."
        else: 
           print "Aborting delete..."
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    def delete_cat(self):
        catnam = str(raw_input('Enter category to delete >'))
        delme = str(raw_input("Are you sure you wish to delete this category and its associated features?(y/n) >"))
        if delme=="y" or delme=="Y":
            self.con.execute("delete from fc where category='%s'" % catnam)
            print "Category and its associated features deleted."
        else: 
            print "Aborting delete..."
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    def delete_cat1(self):
        catnam = str(raw_input('Enter category to delete >'))
        delme = str(raw_input("Are you sure you wish to delete this category?(y/n) >"))
        if delme=="y" or delme=="Y":
            self.con.execute("delete from cc where category='%s'" % catnam)
            print "Category deleted, make sure you delete it from fc too."
        else: 
            print "Aborting delete..."
        cont=(raw_input('Press <ENTER> to continue'))
        self.con.commit()

    def database_menu(self):
        ch = """
##################################################
#   email classifier database operations menu    #
##################################################
#                                                #
#  1 Train database                              #
#  2 Get Category Names                          #
#  3 Look at features in a category              #
#  4 Look at all instances of a feature          #
#  5 Change feature weight                       #
#  6 Rename a category in cc                     #
#  7 Rename all instances of a category in cc    #
#  8 Recategorize a feature                      #
#  9 Delete a feature from fc                    #
# 10 Delete a category from cc                   #
# 11 Delete a category and its features from fc  #
#  0 QUIT                                        #
##################################################
"""
        while True:
            os.system('clear')
            print ch
            choice=raw_input('Enter choice >')
            try: 
                choice=int(choice)
            except: 
                break
            if choice==1:
                get_mails(self)
                cont=(raw_input('Press <ENTER> to continue'))
            elif choice==2:
                self.get_catnames()
            elif choice==3:
                self.examine_category()
            elif choice==4:
                self.examine_feature()
            elif choice==5:
                self.change_featweight()
            elif choice==6:
                self.rename_category_in_cc()
            elif choice==7:
                self.rename_category_in_fc()
            elif choice==8:
                self.recategorize_in_f()
            elif choice==9:
                self.delete_feat()
            elif choice==10:
                self.delete_cat1()
            elif choice==11:
                self.delete_cat()
            elif choice==0: 
                break


class naivebayes(classifier):

    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds={}

    def docprob(self,item,cat):
        features=self.getfeatures(item)

        # Multiply the probabilities of all the features together
        p=1
        for f in features: 
            p *= self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds: 
            return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        probs={}
        # Find the category with the highest probability
        best=default
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        # Make sure the probability exceeds threshold*next best
        for cat in probs:
            if cat==best: 
                continue
            if probs[cat]*self.getthreshold(best)>probs[best]: 
                return default
        return best

class fisherclassifier(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums={}

    def setminimum(self,cat,min):
        self.minimums[cat]=min

    def getminimum(self,cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]
        
    def cprob(self,f,cat):
        # The frequency of this feature in this category
        clf=self.fprob(f,cat)
        if clf==0: 
            return 0

        # The frequency of this feature in all the categories
        freqsum=sum([self.fprob(f,c) for c in self.categories()])

        # The probability is the frequency in this category divided by the overall frequency
        p=clf/(freqsum)

        return p

    def fisherprob(self,item,cat):
        # Multiply all the probabilities together
        p=1
        features=self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f,cat,self.cprob))

        # Take the natural log and multiply by -2
        try: 
            fscore=-2*math.log(p)   # if db returns none for ap because feature not in fc
        except:
            return 0
        # Use the inverse chi2 function to get a probability
        return self.invchi2(fscore,len(features)*2)

    def invchi2(self,chi,df):
        m=chi/2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m/i
            sum += term
        return min(sum, 1.0)

    def classify(self,item,default=None):
        # Loop through looking for the best result
        best=default
        max=0.0
        for c in self.categories():
            p=self.fisherprob(item,c)
            # Make sure it exceeds the minimum
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
        return best


def getwords1(doc):
    ignore_list = ['a', 'about', 'above', 'after', 'again', 'all', 'also', 'am', 'an', 'and', 'any', 
                   'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'both', 'but', 
                   'by', "can", "can't", 'cannot', 'could', "couldn't", "couldn", 'did', "didn", "didn't", 
                   'do', 'does', 'doesn', "doesn't", 'doing', "don't", 'down', 'during', 'each', "even", 
                   'every', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven", 
                   "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'him', 
                   'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 
                   'it', "it's", 'its', 'itself', 'laquo', 'lsaquo', 'ldquo', "let's", 'mdash', 'me', 'more', 
                   'most', "mustn", "mustn't", 'my', "nbsp", 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 
                   'only', 'or', 'other', 'ought', 'our', 'ours', 'out', 'over', 'own', 'quot', 'raquo', 
                   'rsaquo', 'rsquo', 'said', 'same', 'say', 'says', "shan't", 'she', "she'd", "she'll", 
                   "she's", 'should', "shouldn", "shouldn't", 'so', 'some', 'still', 'such', 'than', 'that', 
                   "that's", 'the', 'their', 'theirs', 'them', 'then', 'there', "there's", 'these', 'they', 
                   "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 
                   'until', 'up', 'very', 'was', 'wasn', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 
                   'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 
                   'who', "who's", 'whom', 'why', "why's", "will", "with", "won't", "wouldn't", 'wouldn', 'you', 
                   "you'd", "you'll", "you're", "you've", 'your', 'yours']

    wordnum=2
    splitter=re.compile('\\W*')

    variousnumbers = re.findall(" [/(0-9/) -0-9]{11,25}", doc) + re.findall(r"[^[]*\[([^]]*)\]", doc)

    emails = re.findall("[\w.]+@[\w.]+", doc)
    for a in range(len(emails)):   
        if emails[a][-1] == '>':emails[a]= emails[a][:-1]
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', doc)
    for a in range(len(urls)):   
        if urls[a][-1] == '>':urls[a]= urls[a][:-1]

    # So these are only added the one time.
    for a in urls: 
        doc = doc.replace(a," ")
    for a in emails: 
        doc = doc.replace(a," ")
    for a in variousnumbers: 
        doc = doc.replace(a," ")

    doc = ''.join(i for i in doc if not i.isdigit())
    words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]

    # Change wordnum for word combo length
    for a in range(len(words)-wordnum+1):
        phrases = ' '.join(words[a:a+wordnum])
        words.append(phrases)

    # Put all the lists together and return a unique wordset
    words = words + urls + emails + variousnumbers
    uniqueWordset = dict([(w,1) for w in words])
    for a in ignore_list:
        if a in uniqueWordset: 
            del uniqueWordset[a]
    return uniqueWordset


def read(message,fulltext,classifier):
    print message

    # Print the best guess at the current category
    guess = str(classifier.classify(fulltext))
    print '\nCategory guess: '+ guess

    # Ask the user to specify the correct category and train on that
    cl=raw_input('Enter category (q to QUIT): ')
    if cl == "": 
        cl = guess          # If the guess is correct just press enter as a timesaver
    elif cl == "q":
        classifier.con.commit()
        return cl
    classifier.train(fulltext,cl)
    return cl


def get_mails(classifier):
    username = str(raw_input('Enter username >'))
    password = getpass.getpass(prompt='Enter password >')

    mailserver = poplib.POP3_SSL('pop.gmail.com')
    mailserver.user(username)                   
    mailserver.pass_(password)
    (numMsgs, totalSize) = mailserver.stat()               # Print some stats...
    print "numMsgs =",numMsgs,"\ntotalSize =",totalSize    # just so you know what's coming :)

    numMessages1 = len(mailserver.list()[1])
    numMessages=int(raw_input('Enter number of messages to fetch >'))
    
    for i in reversed(range(numMessages)):
        fulltext = ""
        message = "_________________________________\ni =" + str(i)
        message += "\n_________________________________\n" # reversed runs the range in reverse
        msg = mailserver.retr(i+1)
        str1 = string.join(msg[1], "\n")
        mail = email.message_from_string(str1)
        
        try: 
            message += "From: " + mail["From"] + "\n" + "Subject: " + mail["Subject"] + "\n" + "Date: " + mail["Date"] + "\n"
            fulltext += mail["From"] + " " + mail["Subject"] + " " + mail["Received"] + " "
        except: 
            pass
        
        for part in mail.walk():
            if part.get_content_type() == 'text/plain':
                message += "Body: " + part.get_payload()   # adds the raw text to message
                fulltext += part.get_payload()
        
        try:
            a=read(message,fulltext,classifier)                  # train the database
            if a=="q": break
        except: 
            print "-"*44,"\nUnable to process this e-mail\n","-"*44


def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def getXNewMails(imap_server,cl):
    X = int(raw_input("Enter number of new mails to fetch >"))
    X=X-1
    result, data = imap_server.search(None, "ALL") # fetch numbers of emails 
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1] 
    mailnums=range(int(latest_email_id)-X,int(latest_email_id)+1)
    mailnums.reverse()

    for i in mailnums:
        result, data = imap_server.fetch(i, "(RFC822)") # fetch the email body (RFC822) for the given ID
        raw_email = data[0][1] # raw text of the whole email including headers and alternate payloads
        email_message = email.message_from_string(raw_email)
        print "-"*44
        fulltext=""
        print "To:",email_message['To']
        fulltext+=email_message['To']+' '
        print "From:",email_message['From']
        fulltext+=email_message['From']+' '
        print "Date:",email_message['Date']
        print "Subject:",email_message['Subject']
        fulltext+=email_message['Subject']+' '
        print ""
        a = get_first_text_block(imap_server, email_message)
        if a==None: 
            c="No message"
        else:
            b=stripTags(a)
            c=htmlentitydecode(b)
        print c
        fulltext+=c
        print '\nCategory guess: ',str(cl.classify(fulltext))
        cont=(raw_input('Press <ENTER> to continue'))


def get_newest_email(imap_server,cl):
    result, data = imap_server.search(None, "ALL") # fetch numbers of emails 
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1] 
    result, data = imap_server.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
    raw_email = data[0][1] # raw text of the whole email including headers and alternate payloads
    email_message = email.message_from_string(raw_email)
    print "-"*44
    fulltext=""
    print "To:",email_message['To']
    fulltext+=email_message['To']+' '
    print "From:",email_message['From']
    fulltext+=email_message['From']+' '
    print "Date:",email_message['Date']
    print "Subject:",email_message['Subject']
    fulltext+=email_message['Subject']+' '
    print ""
    a = get_first_text_block(imap_server, email_message)
    
    if a==None: 
        c="No message"
    else: 
        b=stripTags(a)
        c=htmlentitydecode(b)
    
    print c
    fulltext+=c
    print '\nCategory guess: ',str(cl.classify(fulltext))


def send_a_mail(username,password):
    import smtplib
    fromaddr = str(raw_input("Enter sender's email address >"))
    toaddrs  = str(raw_input("Enter recipients's email address >"))
    subj = str(raw_input("Enter subject of message >"))
    fromline = "From: %s" % fromaddr
    toline = "To: %s" % toaddrs
    subjline = "Subject: %s" % subj
    messageline = ""
    print "Enter message (enter q on a line on its own to send message.) >"
    
    while True:
        mess1 = str(raw_input())
        if mess1=='q': 
            break
        messageline+=mess1+'\n'
    
    msg = "\r\n".join([fromline, toline, subjline, "",messageline])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    print "Mail sent."


def get_emails(imap_server,cl):
    em1=int(raw_input('Enter email number >'))
    result, data = imap_server.fetch(em1, "(RFC822)") # fetch the email body (RFC822) for the given ID
    raw_email = data[0][1] # raw text of the whole email including headers and alternate payloads
    email_message = email.message_from_string(raw_email)
    print "-"*44
    fulltext=""
    
    try:
        print "To:",email_message['To']
        fulltext+=email_message['To']+' '
    except: 
        pass
    
    try:
        print "From:",email_message['From']
        fulltext+=email_message['From']+' '
    except: 
        pass
    
    try: print "Date:",email_message['Date']
    except: 
        pass
    
    try:
        print "Subject:",email_message['Subject']
        fulltext+=email_message['Subject']+' '
    except: 
        pass
        
    print ""
    a = get_first_text_block(imap_server, email_message)
    
    if a==None: 
        a="No message"
    else:
        b=stripTags(a)
        c=htmlentitydecode(b)
    
    print c
    fulltext+=c
    print '\nCategory guess: ',str(cl.classify(fulltext))


def get_subjects(imap_server):
    email_ids=[]
    while True:
        em1=int(raw_input('Enter email id >'))
        email_ids.append(em1)
        again=str(raw_input('Enter another?(y/n) >'))
        if again=='n' or again=='N': 
            break
    
    try:
        subjects = []
        for e_id in email_ids:
            _, response = imap_server.fetch(e_id, '(body[header.fields (subject)])')
            subjects.append( response[0][1][9:] )
        
        print "-"*44
        
        for a in subjects:
            b=stripTags(a)
            print htmlentitydecode(b)
        
        print "-"*44
        return subjects
    except: 
        print "Unable to retrieve mail"


def emails_from(imap_server):
    name=str(raw_input("Enter person's name >"))
   
   # Search for all mail from name
    try:
        status, response = imap_server.search(None, '(FROM "%s")' % name)
        email_ids = [e_id for e_id in response[0].split()]
        print 'Number of emails from %s: %i. IDs: %s' % (name, len(email_ids), email_ids)
        return email_ids
    except: 
        print "Unable to retrieve mail"


def mailmenu(imap_server,username,password,cl):
    ch="""
#############################################
#              mail menu                    #
#############################################"""
    ch1="""
#############################################
#                                           #
# 1 Fetch newest mail                       #
# 2 Fetch X new mails                       #
# 3 Fetch a specific email by number        #
# 4 Fetch emails from a specific person     #
# 5 Fetch only the subject line/s           #
# 6 Send mail                               #
# 0 QUIT                                    #
#                                           #
#############################################"""
    # Count the unread emails
    status, response = imap_server.status('INBOX', "(UNSEEN)")
    unreadcount = int(response[0].split()[2].strip(').,]'))

    # Search for all new mail
    status, email_ids = imap_server.search(None, '(UNSEEN)')
    print "The numbers for these emails are",email_ids

    while True:
        os.system('clear')
        print ch
        print "You have",unreadcount,"unread mails"
        print "The ids for these emails are;"
        for a in email_ids: print a
        print ch1
        choice=raw_input('Enter choice >')
        
        try:
            choice=int(choice)
        except:
            imap_server.logout()
            break

        if choice==1:
            get_newest_email(imap_server,cl)
            cont=(raw_input('Press <ENTER> to continue'))
        elif choice==2:
            getXNewMails(imap_server,cl)
        elif choice==3:
            get_emails(imap_server,cl)
            cont=(raw_input('Press <ENTER> to continue'))
        elif choice==4:
            emails_from(imap_server)
            cont=(raw_input('Press <ENTER> to continue'))
        elif choice==5:
            get_subjects(imap_server)
            cont=(raw_input('Press <ENTER> to continue'))
        elif choice==6:
            send_a_mail(username,password)
            cont=(raw_input('Press <ENTER> to continue'))
        elif choice==0:
            imap_server.logout()
            break


def email_startup(cl):
    os.system('clear')
    username = str(raw_input('Enter username >'))
    password = getpass.getpass(prompt='Enter password >')
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
    imap_server.login(username, password)
    imap_server.select('INBOX')
    mailmenu(imap_server,username,password,cl)

def main():
    ch2="""
###############################################
#       Andrew Laing email client             #
###############################################
#                                             #
# 1: Email                                    #
# 2: Bayesian Classifier                      #
# 0: QUIT                                     #
#                                             #
###############################################"""
    os.system('clear')
    dbnam=str(raw_input('Enter full database name (eg emails1.db) >'))
    choice=raw_input('(N)aivebayes or (F)isherclassifier? >')
    
    if choice=='N' or choice=='n':
        cl=naivebayes(getwords1)
        cl.setdb(dbnam)
    else:
        cl=fisherclassifier(getwords1)
        cl.setdb(dbnam)
    while True:
        os.system('clear')
        print ch2
        choiceraw_input('Enter choice >')
        
        try: 
            choice=int(choice)
        except: 
            break
        
        if choice==1:
            email_startup(cl)
        elif choice==2:
            cl.database_menu()
        elif choice==0:
            cl.con.commit()
            break

if __name__ == "__main__":
    main()
