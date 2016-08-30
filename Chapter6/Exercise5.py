""" Chapter 6 Exercise 5: Preserving IP addresses.

    IP addresses, phone numbers, and other numerical information can be helpful in identifying spam. 
    Modify the feature extraction function to return these items as features. 
    (IP addresses have periods embedded in them, but you still need to get rid of the periods between sentences.)

    --Did this with regex.--
    First one gets ip addys and phone numbers, the second gets ip addys from inside brackets.
    Also added the variable word combos to this version. 
    (In regular emails this adds more training time before it begins to recognize features: 
       unless of course you add assumed probabilities to emails etc (:I'm considering implementing it:) )
"""

import poplib, email, string
import getpass as getpass
import re as re

# Adds intact emails, urls, ip addys and telephone numbers. Splits words by non-alpha, as singles and combos.
def getwords(doc):

    wordnum=2
    splitter=re.compile('\\W*')

    # The regular expressions for this exercise.
    variousnumbers = re.findall(" [/(0-9/) -0-9]{11,25}", doc) + re.findall(r"[^[]*\[([^]]*)\]", doc)

    emails = re.findall("[\w.]+@[\w.]+", doc)
    
    for a in range(len(emails)):   
        if emails[a][-1] == '>':
            emails[a]= emails[a][:-1]
    
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', doc)
    
    for a in range(len(urls)):   
        if urls[a][-1] == '>':
            urls[a]= urls[a][:-1]

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
    return dict([(w,1) for w in words])


# Message is for reading, fulltext is for processing
def read(message,fulltext,classifier):
    print message
    guess = str(classifier.classify(fulltext))  # Print the best guess at the current category
    print '\nGuess: '+ guess

    cl=raw_input('Enter category: ')            # Ask the user to specify the correct category and train on that
    if cl == "": 
        cl = guess                              # If the guess is correct just press enter as a timesaver
    
    classifier.train(fulltext,cl)


def get_mails(classifier):
    # Made for usage with gmail.
    username = str(raw_input('Enter username >'))          # 'recent:YOURUSERNAME' limits it to last months mail
    password = getpass.getpass(prompt='Enter password >')

    mailserver = poplib.POP3_SSL('pop.gmail.com')
    mailserver.user(username)                   
    mailserver.pass_(password)
    (numMsgs, totalSize) = mailserver.stat()               # Print some stats...
    print "numMsgs =",numMsgs,"\ntotalSize =",totalSize 
    paused = raw_input('Press <ENTER> to continue')        # Dramatic pause

    numMessages = len(mailserver.list()[1])
    for i in reversed(range(numMessages)):
        fulltext = ""
        message = "_________________________________\ni =" + str(i)
        message += "\n_________________________________\n"
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
                message += "Body: " + part.get_payload()
                fulltext += part.get_payload()
                
        read(message,fulltext,classifier)                # train the database
  
