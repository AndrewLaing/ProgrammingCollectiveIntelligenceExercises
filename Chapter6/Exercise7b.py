""" Chapter 6 Exercise 7b: Neural network classifier.

    Write a program that classifies and trains on documents thousands of times.
    Time how long it takes with each of the algorithms. How do they compare?
"""

import time as time

def train1():
    import docclass as docclass
    cl=docclass.classifier(docclass.getwords)
    cl.setdb('test1.db')
    for a in range(2000):
        docclass.sampletrain(cl)
    cl.con.commit()

def train2():
    import docclass as docclass
    cl1=docclass.naivebayes(docclass.getwords)
    cl1.setdb('test2.db')
    for a in range(2000):
        docclass.sampletrain(cl1)
    cl1.con.commit()

def train3():
    import docclass as docclass
    cl2=docclass.fisherclassifier(docclass.getwords)
    cl2.setdb('test3.db')
    for a in range(2000):
        docclass.sampletrain(cl2)
    cl2.con.commit()

def train4():
    import ch6ex7a as nn
    mynet=nn.searchnet('test4.db')
    mynet.maketables()
    for a in range(2000):
        nn.sampletrain(mynet)
    mynet.con.commit()

start_time = time.time()
t = train1()
elapsed_time = time.time() - start_time

pretty = "-------------------------------"
print pretty
print "------docclass.classifier------"
print pretty
print elapsed_time, 'seconds'
print pretty

start_time = time.time()
t = train2()
elapsed_time1 = time.time() - start_time

print pretty
print "------docclass.naivebayes------"
print pretty
print elapsed_time1, 'seconds'
print pretty

start_time = time.time()
t = train3()
elapsed_time2 = time.time() - start_time

print pretty
print "---docclass.fisherclassifier---"
print pretty
print elapsed_time2, 'seconds'
print pretty

start_time = time.time()
t = train4()
elapsed_time3 = time.time() - start_time

print pretty
print "---------nn.searchnet----------"
print pretty
print elapsed_time3, 'seconds'
print pretty

time.sleep(4)

"""
###############################################################################
         @@@@@@@@@@@@@@@@@@@@
         @@ TIMED TRAINING @@
         @@@@@@@@@@@@@@@@@@@@

    ---docclass.classifier
    
         4.00573611259 seconds          -1000 ITERATIONS
         8.84838891029 seconds          -2000    "  "
         17.0053019524 seconds          -4000    "  "
         37.0707201958 seconds          -8000    "  "

    ---docclass.naivebayes
    
         4.21931004524 seconds          -1000 ITERATIONS
         9.03012800217 seconds          -2000    "  "
         17.6259031296 seconds          -4000    "  "
         37.2959821224 seconds          -8000    "  "

    ---docclass.fisherclassifier

         4.55036592484 seconds          -1000 ITERATIONS
         9.37840104103 seconds          -2000    "  "
         17.8124477863 seconds          -4000    "  "
         36.2661380768 seconds          -8000    "  "

    ---nn.searchnet

         47.1835539341 seconds          -1000 ITERATIONS
         97.6254498959 seconds          -2000    "  "
         godzilla.............          -4000    "  "
         .....................          -8000    "  "

###############################################################################

"""
