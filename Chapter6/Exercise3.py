""" Chapter 6 Exercise 3: A POP-3 email filter

    Python comes with a library called poplib for downloading email messages.
    Write a script that downloads email messages from a server and attempts to classify them.  
        *see end of file for usage.

    What are the different properties of an email message, and how might you build 
    a feature-extraction function to take advantage of them?     
        *I incorporated a couple of features into the script. Also see end of file.
"""

import poplib, email, string
import getpass as getpass
import re as re

def getwords(doc):
    # Adds intact emails and urls. Removes numbers. Splits words by non-alpha.
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
    words = words + urls + emails
    # Return the unique set of words only
    return dict([(w,1) for w in words])


def read(message,fulltext,classifier):
    print message

    # Print the best guess at the current category
    guess = str(classifier.classify(fulltext))
    print '\nGuess: '+ guess

    # Ask the user to specify the correct category and train on that
    cl=raw_input('Enter category: ')
    if cl == "": 
        cl = guess                                # If the guess is correct just press enter as a timesaver
    classifier.train(fulltext,cl)

def get_mails(classifier):
    # Made for usage with gmail.
    username = str(raw_input('Enter username >'))          # 'recent:YOURUSERNAME' limits it to last months mail
    password = getpass.getpass(prompt='Enter password >')

    mailserver = poplib.POP3_SSL('pop.gmail.com')
    mailserver.user(username)                   
    mailserver.pass_(password)
    (numMsgs, totalSize) = mailserver.stat()               # Print some stats...
    print "numMsgs =",numMsgs,"\ntotalSize =",totalSize    # just so you know what's coming :)
    paused = raw_input('Press <ENTER> to continue')        # Dramatic pause

    numMessages = len(mailserver.list()[1])
    
    for i in reversed(range(numMessages)):
        fulltext = ""
        message = "_________________________________\ni =" + str(i)
        message += "\n_________________________________\n" # reversed runs the range in reverse
        msg = mailserver.retr(i+1)
        str1 = string.join(msg[1], "\n")
        mail = email.message_from_string(str1)
        try: 
            message += "From: " + mail["From"] + "\n" + "Subject: " + mail["Subject"] + "\n" + "Date: " + mail["Date"] + "\n"
            fulltext += mail["From"] + " " + mail["Subject"] + " "
        except: 
            pass
        
        for part in mail.walk():
            if part.get_content_type() == 'text/plain':
                message += "Body: " + part.get_payload()   # adds the raw text to message
                fulltext += part.get_payload()
        
        read(message,fulltext,classifier)                  # train the database


"""
###############################################################################

#############
   Usage:
#############
import docclass_ex1 as docclass
import emailfilter as emailfilter
cl=docclass.fisherclassifier(emailfilter.getwords)
cl.setdb('emails.db')

emailfilter.get_mails(cl)         # get mails and run the training function

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   Improving performance:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    set_ap() in docclass_ex1 can be used to add extra assumed probability.
#    example emails from rosalyn always come from the same address
#    and she always signs them rosalyn so we can weight them accordingly

cl.set_ap('rosalyn@foobar.com','rosalyn',7.0)
cl.set_ap('rosalyn','rosalyn',2.0)

#    URL's are saved which should help classifying if they are always used in
#    signatures or elsewhere in the messages from a certain contact.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   Some entry correcting commands:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cl.con.execute("update fc set category='french' where category='None'")
cl.con.execute("update cc set count=236 where category='french'")
cl.con.execute("delete from cc where category='None'")

###############################################################################

##############################
Properties of an email message 
##############################

Emails contain a sender address and many also contain signatures in the body
of the message. These properties will be handy in helping to classify.
The messages have a subject field that often reveals the subject of the mail;
I rarely fill it in with useful info and wouldn't base a spam filter around it.
There's a date field, and there is also a field containing the ipaddress of
the sender, in case you are getting spammed from a certain server's SMTP.
 Incorporating any feature would be simply a matter of extracting it from the
message either with the regex or email modules, and adding it to the database.

###############################################################################
"""
