""" Chapter 12 Programming Collective Intelligence: Support Vector Machines.

   As the chapter has no exercises in it I have decided to create a practical
   application for each of the Algorithms and Methods described.
   Next up the Support Vector Machine Classifier.
   For this I have created a simple application that reads a dataset,containing
   details for passengers on the Titanic who either died or survived.
   The dataset is represented here by two lists:
      answers - a list of whether a passenger survived or died
      inputs  - a list of lists of passenger attributes *see end for attributes
   The list 'inputs' is scaled to values between 0.0 and 1.0 and an SVM is created
   using this scaled list and answers. The user then inputs data and is classified
   as having possibly died or possibly survived.
   The SVM classifies with an accuracy of 81.1448 %.
   This uses libsvm-2.91 so for later versions rewrite the code yourself :p
   I scaled the data as floats so there is always hope... :)

"""

from svm import *
import os as os
from time import sleep


def did_I_survive():
    global inputs,answers
    
    scaledset=scale_data(inputs)
    param = svm_parameter(kernel_type = RBF, C = 0.25, gamma = 0.5) # optimized using grid.py
    prob = svm_problem(answers, scaledset)
    m = svm_model(prob,param)
    newrow=inputDialogue()
    scaleduser=scale_data([newrow])
    a=scaleduser[0]
    print "a =",a
    res=m.predict(a)
    os.system('clear')
    print "-"*44
    print "I can say with an accuracy of 81.1448 % that...."
    sleep(1)
    
    if res>0.5: 
        print "\nHURRAH. You would have survived the sinking of the Titanic.\n"
    else: 
        print "\nAhem.... if the sharks didn't get you first,\nand you weren't crushed to death in the mad scramble\nto reach the lifeboats, or\nopportunistically murdered by a jealous partner..."
        sleep(8)
        print "...you would have drowned."
    
    print "-"*44


def inputDialogue():
    while True:
        list1=[]
        os.system('clear')
        print "-"*44
        try:
            print "    WOULD I SURVIVE THE TITANIC SINKING?"
            print "        (please enter numbers only)"
            print "-"*44
            print "What class are you?"
            list1.append(int(raw_input('   1:Upper,2:Middle or 3:Lower? > ')))
            print "\nWhat gender are you?"
            list1.append(int(raw_input('   0:Male or 1:Female? > ')))
            print "\nWhat is your age?"
            list1.append(float(raw_input('   > ')))
            print "\nHow many spouses,brother or sisters are travelling with you?"
            list1.append(int(raw_input('   > ')))
            print "\nHow many parents or children are travelling with you?"
            list1.append(int(raw_input('   > ')))
            print "\nWhich port will you be embarking from?"
            list1.append(int(raw_input('   0:Unknown, 1:Cherbourg, 2:Queenstown or 3:Southampton? > ')))
            print "-"*44,"\n"
            return list1
        except:
            print "-"*44,"\n"
            print "Try inputting the data properly"
        print "\n","-"*44
        
        again=str(raw_input('Enter q to QUIT or anything else to try to do it properly>'))
        if again=='q': 
            break


def scale_data(inputs):
    lohi=[(1,3),(0,1),(0,80),(0,8),(0,6),(0,3)] # lo/hi range of passenger values
    scaledrows=[]
    for a in range(len(inputs)):
        scaledrow=[]
        for b in range(len(inputs[a])):
            lo,hi=lohi[b]
            s=(inputs[a][b]-lo)/float(hi-lo)
            
            if s<0: 
                s=0.0                       # if below passenger range set to 0
            elif s>1: 
                s=1.0                     # if above passenger range set to 1
            
            scaledrow.append(s)
        scaledrows.append(scaledrow)
    return scaledrows

answers=[0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]


inputs=[[3, 0, 22.0, 1, 0, 2], [1, 1, 38.0, 1, 0, 0], [3, 1, 26.0, 0, 0, 2], [1, 1, 35.0, 1, 0, 2], [3, 0, 35.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 0, 54.0, 0, 0, 2], [3, 0, 2.0, 3, 1, 2], [3, 1, 27.0, 0, 2, 2], [2, 1, 14.0, 1, 0, 0], [3, 1, 4.0, 1, 1, 2], [1, 1, 58.0, 0, 0, 2], [3, 0, 20.0, 0, 0, 2], [3, 0, 39.0, 1, 5, 2], [3, 1, 14.0, 0, 0, 2], [2, 1, 55.0, 0, 0, 2], [3, 0, 2.0, 4, 1, 1], [2, 0, 0.0, 0, 0, 2], [3, 1, 31.0, 1, 0, 2], [3, 1, 0.0, 0, 0, 0], [2, 0, 35.0, 0, 0, 2], [2, 0, 34.0, 0, 0, 2], [3, 1, 15.0, 0, 0, 1], [1, 0, 28.0, 0, 0, 2], [3, 1, 8.0, 3, 1, 2], [3, 1, 38.0, 1, 5, 2], [3, 0, 0.0, 0, 0, 0], [1, 0, 19.0, 3, 2, 2], [3, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [1, 0, 40.0, 0, 0, 0], [1, 1, 0.0, 1, 0, 0], [3, 1, 0.0, 0, 0, 1], [2, 0, 66.0, 0, 0, 2], [1, 0, 28.0, 1, 0, 0], [1, 0, 42.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 2], [3, 1, 18.0, 2, 0, 2], [3, 1, 14.0, 1, 0, 0], [3, 1, 40.0, 1, 0, 2], [2, 1, 27.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 0], [2, 1, 3.0, 1, 2, 0], [3, 1, 19.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 1, 0, 1], [3, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 2, 0, 0], [3, 1, 18.0, 1, 0, 2], [3, 0, 7.0, 4, 1, 2], [3, 0, 21.0, 0, 0, 2], [1, 1, 49.0, 1, 0, 0], [2, 1, 29.0, 1, 0, 2], [1, 0, 65.0, 0, 1, 0], [1, 0, 0.0, 0, 0, 2], [2, 1, 21.0, 0, 0, 2], [3, 0, 28.5, 0, 0, 0], [2, 1, 5.0, 1, 2, 2], [3, 0, 11.0, 5, 2, 2], [3, 0, 22.0, 0, 0, 0], [1, 1, 38.0, 0, 0, 0], [1, 0, 45.0, 1, 0, 2], [3, 0, 4.0, 3, 2, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 0.0, 1, 1, 0], [2, 1, 29.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [3, 1, 17.0, 4, 2, 2], [3, 0, 26.0, 2, 0, 2], [2, 0, 32.0, 0, 0, 2], [3, 1, 16.0, 5, 2, 2], [2, 0, 21.0, 0, 0, 2], [3, 0, 26.0, 1, 0, 0], [3, 0, 32.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 0, 0.82999999999999996, 0, 2, 2], [3, 1, 30.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [1, 0, 28.0, 0, 0, 2], [2, 1, 17.0, 0, 0, 2], [3, 1, 33.0, 3, 0, 2], [3, 0, 16.0, 1, 3, 2], [3, 0, 0.0, 0, 0, 2], [1, 1, 23.0, 3, 2, 2], [3, 0, 24.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 2], [3, 0, 20.0, 0, 0, 2], [1, 0, 46.0, 1, 0, 2], [3, 0, 26.0, 1, 2, 2], [3, 0, 59.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 71.0, 0, 0, 0], [1, 0, 23.0, 0, 1, 0], [2, 1, 34.0, 0, 1, 2], [2, 0, 34.0, 1, 0, 2], [3, 1, 28.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 21.0, 0, 1, 2], [3, 0, 33.0, 0, 0, 2], [3, 0, 37.0, 2, 0, 2], [3, 0, 28.0, 0, 0, 2], [3, 1, 21.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 38.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 1], [1, 0, 47.0, 0, 0, 2], [3, 1, 14.5, 1, 0, 0], [3, 0, 22.0, 0, 0, 2], [3, 1, 20.0, 1, 0, 2], [3, 1, 17.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 70.5, 0, 0, 1], [2, 0, 29.0, 1, 0, 2], [1, 0, 24.0, 0, 1, 0], [3, 1, 2.0, 4, 2, 2], [2, 0, 21.0, 2, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 0, 32.5, 1, 0, 0], [2, 1, 32.5, 0, 0, 2], [1, 0, 54.0, 0, 1, 2], [3, 0, 12.0, 1, 0, 0], [3, 0, 0.0, 0, 0, 1], [3, 0, 24.0, 0, 0, 2], [3, 1, 0.0, 1, 1, 0], [3, 0, 45.0, 0, 0, 2], [3, 0, 33.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [3, 1, 47.0, 1, 0, 2], [2, 1, 29.0, 1, 0, 2], [2, 0, 25.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 0], [1, 1, 19.0, 0, 2, 2], [1, 0, 37.0, 1, 0, 2], [3, 0, 16.0, 0, 0, 2], [1, 0, 24.0, 0, 0, 0], [3, 1, 0.0, 0, 2, 0], [3, 1, 22.0, 0, 0, 2], [3, 1, 24.0, 1, 0, 2], [3, 0, 19.0, 0, 0, 1], [2, 0, 18.0, 0, 0, 2], [2, 0, 19.0, 1, 1, 2], [3, 0, 27.0, 0, 0, 2], [3, 1, 9.0, 2, 2, 2], [2, 0, 36.5, 0, 2, 2], [2, 0, 42.0, 0, 0, 2], [2, 0, 51.0, 0, 0, 2], [1, 1, 22.0, 1, 0, 2], [3, 0, 55.5, 0, 0, 2], [3, 0, 40.5, 0, 2, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 51.0, 0, 1, 0], [3, 1, 16.0, 0, 0, 1], [3, 0, 30.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 8, 2, 2], [3, 0, 44.0, 0, 1, 2], [2, 1, 40.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 17.0, 0, 0, 2], [3, 0, 1.0, 4, 1, 2], [3, 0, 9.0, 0, 2, 2], [1, 1, 0.0, 0, 1, 2], [3, 1, 45.0, 1, 4, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 28.0, 0, 0, 2], [1, 0, 61.0, 0, 0, 2], [3, 0, 4.0, 4, 1, 1], [3, 1, 1.0, 1, 1, 2], [3, 0, 21.0, 0, 0, 2], [1, 0, 56.0, 0, 0, 0], [3, 0, 18.0, 1, 1, 2], [3, 0, 0.0, 3, 1, 2], [1, 1, 50.0, 0, 0, 0], [2, 0, 30.0, 0, 0, 2], [3, 0, 36.0, 0, 0, 2], [3, 1, 0.0, 8, 2, 2], [2, 0, 0.0, 0, 0, 0], [3, 0, 9.0, 4, 2, 2], [2, 0, 1.0, 2, 1, 2], [3, 1, 4.0, 0, 2, 2], [1, 0, 0.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 1], [1, 0, 45.0, 0, 0, 2], [3, 0, 40.0, 1, 1, 1], [3, 0, 36.0, 0, 0, 2], [2, 1, 32.0, 0, 0, 2], [2, 0, 19.0, 0, 0, 2], [3, 1, 19.0, 1, 0, 2], [2, 0, 3.0, 1, 1, 2], [1, 1, 44.0, 0, 0, 0], [1, 1, 58.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 1], [3, 0, 42.0, 0, 1, 2], [3, 1, 0.0, 0, 0, 1], [2, 1, 24.0, 0, 0, 2], [3, 0, 28.0, 0, 0, 2], [3, 0, 0.0, 8, 2, 2], [3, 0, 34.0, 0, 0, 2], [3, 0, 45.5, 0, 0, 0], [3, 0, 18.0, 0, 0, 2], [3, 1, 2.0, 0, 1, 2], [3, 0, 32.0, 1, 0, 2], [3, 0, 26.0, 0, 0, 0], [3, 1, 16.0, 0, 0, 1], [1, 0, 40.0, 0, 0, 0], [3, 0, 24.0, 0, 0, 2], [2, 1, 35.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [2, 0, 30.0, 0, 0, 2], [3, 0, 0.0, 1, 0, 1], [1, 1, 31.0, 1, 0, 0], [3, 1, 27.0, 0, 0, 2], [2, 0, 42.0, 1, 0, 2], [1, 1, 32.0, 0, 0, 0], [2, 0, 30.0, 0, 0, 2], [3, 0, 16.0, 0, 0, 2], [2, 0, 27.0, 0, 0, 2], [3, 0, 51.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 38.0, 1, 0, 2], [3, 0, 22.0, 0, 0, 2], [2, 0, 19.0, 0, 0, 2], [3, 0, 20.5, 0, 0, 2], [2, 0, 18.0, 0, 0, 2], [3, 1, 0.0, 3, 1, 2], [1, 1, 35.0, 1, 0, 2], [3, 0, 29.0, 0, 0, 2], [2, 0, 59.0, 0, 0, 2], [3, 1, 5.0, 4, 2, 2], [2, 0, 24.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 2], [2, 0, 44.0, 1, 0, 2], [2, 1, 8.0, 0, 2, 2], [2, 0, 19.0, 0, 0, 2], [2, 0, 33.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 0], [3, 1, 0.0, 1, 0, 1], [2, 0, 29.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 0, 30.0, 0, 0, 0], [1, 0, 44.0, 2, 0, 1], [3, 1, 25.0, 0, 0, 2], [2, 1, 24.0, 0, 2, 2], [1, 0, 37.0, 1, 1, 2], [2, 0, 54.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 29.0, 1, 1, 2], [1, 0, 62.0, 0, 0, 2], [3, 0, 30.0, 1, 0, 2], [3, 1, 41.0, 0, 2, 2], [3, 1, 29.0, 0, 2, 0], [1, 1, 0.0, 0, 0, 0], [1, 1, 30.0, 0, 0, 2], [1, 1, 35.0, 0, 0, 0], [2, 1, 50.0, 0, 1, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 3.0, 4, 2, 2], [1, 0, 52.0, 1, 1, 2], [1, 0, 40.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [2, 0, 36.0, 0, 0, 2], [3, 0, 16.0, 4, 1, 2], [3, 0, 25.0, 1, 0, 2], [1, 1, 58.0, 0, 1, 2], [1, 1, 35.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [2, 1, 41.0, 0, 1, 2], [1, 0, 37.0, 0, 1, 0], [3, 1, 0.0, 0, 0, 1], [1, 1, 63.0, 1, 0, 2], [3, 1, 45.0, 0, 0, 2], [2, 0, 0.0, 0, 0, 2], [3, 0, 7.0, 4, 1, 1], [3, 1, 35.0, 1, 1, 2], [3, 0, 65.0, 0, 0, 1], [3, 0, 28.0, 0, 0, 2], [3, 0, 16.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 33.0, 0, 0, 0], [3, 0, 30.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [2, 0, 42.0, 0, 0, 2], [3, 1, 22.0, 0, 0, 1], [1, 1, 26.0, 0, 0, 2], [1, 1, 19.0, 1, 0, 0], [2, 0, 36.0, 0, 0, 0], [3, 1, 24.0, 0, 0, 2], [3, 0, 24.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 23.5, 0, 0, 0], [1, 1, 2.0, 1, 2, 2], [1, 0, 0.0, 0, 0, 2], [1, 1, 50.0, 0, 1, 0], [3, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 2, 0, 1], [3, 0, 19.0, 0, 0, 2], [2, 1, 0.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [1, 0, 0.92000000000000004, 1, 2, 2], [1, 1, 0.0, 0, 0, 0], [1, 1, 17.0, 1, 0, 0], [2, 0, 30.0, 1, 0, 0], [1, 1, 30.0, 0, 0, 0], [1, 1, 24.0, 0, 0, 0], [1, 1, 18.0, 2, 2, 0], [2, 1, 26.0, 1, 1, 2], [3, 0, 28.0, 0, 0, 2], [2, 0, 43.0, 1, 1, 2], [3, 1, 26.0, 0, 0, 2], [2, 1, 24.0, 1, 0, 2], [2, 0, 54.0, 0, 0, 2], [1, 1, 31.0, 0, 2, 2], [1, 1, 40.0, 1, 1, 0], [3, 0, 22.0, 0, 0, 2], [3, 0, 27.0, 0, 0, 2], [2, 1, 30.0, 0, 0, 1], [2, 1, 22.0, 1, 1, 2], [3, 0, 0.0, 8, 2, 2], [1, 1, 36.0, 0, 0, 0], [3, 0, 61.0, 0, 0, 2], [2, 1, 36.0, 0, 0, 2], [3, 1, 31.0, 1, 1, 2], [1, 1, 16.0, 0, 1, 0], [3, 1, 0.0, 2, 0, 1], [1, 0, 45.5, 0, 0, 2], [1, 0, 38.0, 0, 1, 2], [3, 0, 16.0, 2, 0, 2], [1, 1, 0.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 29.0, 1, 0, 2], [1, 1, 41.0, 0, 0, 0], [3, 0, 45.0, 0, 0, 2], [1, 0, 45.0, 0, 0, 2], [2, 0, 2.0, 1, 1, 2], [1, 1, 24.0, 3, 2, 2], [2, 0, 28.0, 0, 0, 2], [2, 0, 25.0, 0, 0, 2], [2, 0, 36.0, 0, 0, 2], [2, 1, 24.0, 0, 0, 2], [2, 1, 40.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 2], [3, 0, 3.0, 1, 1, 2], [3, 0, 42.0, 0, 0, 2], [3, 0, 23.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 15.0, 1, 1, 0], [3, 0, 25.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 28.0, 0, 0, 2], [1, 1, 22.0, 0, 1, 2], [2, 1, 38.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [3, 1, 0.0, 0, 0, 1], [3, 0, 40.0, 1, 4, 2], [2, 0, 29.0, 1, 0, 0], [3, 1, 45.0, 0, 1, 0], [3, 0, 35.0, 0, 0, 2], [3, 0, 0.0, 1, 0, 1], [3, 0, 30.0, 0, 0, 2], [1, 1, 60.0, 1, 0, 0], [3, 1, 0.0, 0, 0, 0], [3, 1, 0.0, 0, 0, 1], [1, 1, 24.0, 0, 0, 0], [1, 0, 25.0, 1, 0, 0], [3, 0, 18.0, 1, 0, 2], [3, 0, 19.0, 0, 0, 2], [1, 0, 22.0, 0, 0, 0], [3, 1, 3.0, 3, 1, 2], [1, 1, 0.0, 1, 0, 0], [3, 1, 22.0, 0, 0, 2], [1, 0, 27.0, 0, 2, 0], [3, 0, 20.0, 0, 0, 0], [3, 0, 19.0, 0, 0, 2], [1, 1, 42.0, 0, 0, 0], [3, 1, 1.0, 0, 2, 0], [3, 0, 32.0, 0, 0, 2], [1, 1, 35.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 0, 18.0, 0, 0, 2], [3, 0, 1.0, 5, 2, 2], [2, 1, 36.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [2, 1, 17.0, 0, 0, 0], [1, 0, 36.0, 1, 2, 2], [3, 0, 21.0, 0, 0, 2], [3, 0, 28.0, 2, 0, 2], [1, 1, 23.0, 1, 0, 0], [3, 1, 24.0, 0, 2, 2], [3, 0, 22.0, 0, 0, 2], [3, 1, 31.0, 0, 0, 2], [2, 0, 46.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 2], [2, 1, 28.0, 0, 0, 2], [3, 0, 39.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 1, 21.0, 1, 0, 2], [3, 0, 28.0, 1, 0, 2], [3, 1, 20.0, 0, 0, 2], [2, 0, 34.0, 1, 0, 2], [3, 0, 51.0, 0, 0, 2], [2, 0, 3.0, 1, 1, 2], [3, 0, 21.0, 0, 0, 2], [3, 1, 0.0, 3, 1, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 1, 33.0, 1, 0, 1], [2, 0, 0.0, 0, 0, 2], [3, 0, 44.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 2], [2, 1, 34.0, 1, 1, 2], [2, 1, 18.0, 0, 2, 2], [2, 0, 30.0, 0, 0, 2], [3, 1, 10.0, 0, 2, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 1], [3, 0, 29.0, 0, 0, 2], [3, 1, 28.0, 1, 1, 2], [3, 0, 18.0, 1, 1, 2], [3, 0, 0.0, 0, 0, 2], [2, 1, 28.0, 1, 0, 2], [2, 1, 19.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 32.0, 0, 0, 2], [1, 0, 28.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 2], [2, 1, 42.0, 1, 0, 2], [3, 0, 17.0, 0, 0, 2], [1, 0, 50.0, 1, 0, 2], [1, 1, 14.0, 1, 2, 2], [3, 1, 21.0, 2, 2, 2], [2, 1, 24.0, 2, 3, 2], [1, 0, 64.0, 1, 4, 2], [2, 0, 31.0, 0, 0, 2], [2, 1, 45.0, 1, 1, 2], [3, 0, 20.0, 0, 0, 2], [3, 0, 25.0, 1, 0, 2], [2, 1, 28.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 4.0, 0, 2, 2], [2, 1, 13.0, 0, 1, 2], [1, 0, 34.0, 0, 0, 2], [3, 1, 5.0, 2, 1, 0], [1, 0, 52.0, 0, 0, 2], [2, 0, 36.0, 1, 2, 2], [3, 0, 0.0, 1, 0, 2], [1, 0, 30.0, 0, 0, 0], [1, 0, 49.0, 1, 0, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 0], [1, 0, 65.0, 0, 0, 2], [1, 1, 0.0, 1, 0, 2], [2, 1, 50.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 0, 48.0, 0, 0, 2], [3, 0, 34.0, 0, 0, 2], [1, 0, 47.0, 0, 0, 2], [2, 0, 48.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 38.0, 0, 0, 2], [2, 0, 0.0, 0, 0, 2], [1, 0, 56.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 1, 0.75, 2, 1, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 38.0, 0, 0, 2], [2, 1, 33.0, 1, 2, 2], [2, 1, 23.0, 0, 0, 0], [3, 1, 22.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [2, 0, 34.0, 1, 0, 2], [3, 0, 29.0, 1, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 1, 2.0, 0, 1, 2], [3, 0, 9.0, 5, 2, 2], [2, 0, 0.0, 0, 0, 2], [3, 0, 50.0, 0, 0, 2], [3, 1, 63.0, 0, 0, 2], [1, 0, 25.0, 1, 0, 0], [3, 1, 0.0, 3, 1, 2], [1, 1, 35.0, 1, 0, 2], [1, 0, 58.0, 0, 0, 0], [3, 0, 30.0, 0, 0, 2], [3, 0, 9.0, 1, 1, 2], [3, 0, 0.0, 1, 0, 2], [3, 0, 21.0, 0, 0, 2], [1, 0, 55.0, 0, 0, 2], [1, 0, 71.0, 0, 0, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [1, 1, 54.0, 1, 0, 0], [3, 0, 0.0, 0, 0, 2], [1, 1, 25.0, 1, 2, 2], [3, 0, 24.0, 0, 0, 2], [3, 0, 17.0, 0, 0, 2], [3, 1, 21.0, 0, 0, 1], [3, 1, 0.0, 0, 0, 1], [3, 1, 37.0, 0, 0, 2], [1, 1, 16.0, 0, 0, 2], [1, 0, 18.0, 1, 0, 0], [2, 1, 33.0, 0, 2, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 28.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 29.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [1, 0, 36.0, 0, 0, 2], [1, 1, 54.0, 1, 0, 0], [3, 0, 24.0, 0, 0, 2], [1, 0, 47.0, 0, 0, 2], [2, 1, 34.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [2, 1, 36.0, 1, 0, 2], [3, 0, 32.0, 0, 0, 2], [1, 1, 30.0, 0, 0, 2], [3, 0, 22.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [1, 1, 44.0, 0, 1, 0], [3, 0, 0.0, 0, 0, 0], [3, 0, 40.5, 0, 0, 1], [2, 1, 50.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 39.0, 0, 0, 2], [2, 0, 23.0, 2, 1, 2], [2, 1, 2.0, 1, 1, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 17.0, 1, 1, 0], [3, 1, 0.0, 0, 2, 0], [3, 1, 30.0, 0, 0, 2], [2, 1, 7.0, 0, 2, 2], [1, 0, 45.0, 0, 0, 2], [1, 1, 30.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 2], [1, 1, 22.0, 0, 2, 0], [1, 1, 36.0, 0, 2, 2], [3, 1, 9.0, 4, 2, 2], [3, 1, 11.0, 4, 2, 2], [2, 0, 32.0, 1, 0, 2], [1, 0, 50.0, 1, 0, 0], [1, 0, 64.0, 0, 0, 2], [2, 1, 19.0, 1, 0, 2], [2, 0, 0.0, 0, 0, 0], [3, 0, 33.0, 1, 1, 2], [2, 0, 8.0, 1, 1, 2], [1, 0, 17.0, 0, 2, 0], [2, 0, 27.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 22.0, 0, 0, 0], [3, 1, 22.0, 0, 0, 2], [1, 0, 62.0, 0, 0, 2], [1, 1, 48.0, 1, 0, 0], [1, 0, 0.0, 0, 0, 0], [1, 1, 39.0, 1, 1, 2], [3, 1, 36.0, 1, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 40.0, 0, 0, 2], [2, 0, 28.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 2], [3, 0, 24.0, 2, 0, 2], [3, 0, 19.0, 0, 0, 2], [3, 1, 29.0, 0, 4, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 32.0, 0, 0, 2], [2, 0, 62.0, 0, 0, 2], [1, 1, 53.0, 2, 0, 2], [1, 0, 36.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [3, 0, 16.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [2, 1, 34.0, 0, 0, 2], [1, 1, 39.0, 1, 0, 2], [3, 1, 0.0, 1, 0, 0], [3, 0, 32.0, 0, 0, 2], [2, 1, 25.0, 1, 1, 2], [1, 1, 39.0, 1, 1, 0], [2, 0, 54.0, 0, 0, 2], [1, 0, 36.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 0], [1, 1, 18.0, 0, 2, 2], [2, 0, 47.0, 0, 0, 2], [1, 0, 60.0, 1, 1, 0], [3, 0, 22.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 35.0, 0, 0, 2], [1, 1, 52.0, 1, 0, 0], [3, 0, 47.0, 0, 0, 2], [3, 1, 0.0, 0, 2, 1], [2, 0, 37.0, 1, 0, 2], [3, 0, 36.0, 1, 1, 2], [2, 1, 0.0, 0, 0, 2], [3, 0, 49.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [1, 0, 49.0, 1, 0, 0], [2, 1, 24.0, 2, 1, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 0, 44.0, 0, 0, 2], [1, 0, 35.0, 0, 0, 0], [3, 0, 36.0, 1, 0, 2], [3, 0, 30.0, 0, 0, 2], [1, 0, 27.0, 0, 0, 2], [2, 1, 22.0, 1, 2, 0], [1, 1, 40.0, 0, 0, 2], [3, 1, 39.0, 1, 5, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 0.0, 1, 0, 1], [3, 0, 0.0, 0, 0, 1], [3, 0, 35.0, 0, 0, 2], [2, 1, 24.0, 1, 2, 2], [3, 0, 34.0, 1, 1, 2], [3, 1, 26.0, 1, 0, 2], [2, 1, 4.0, 2, 1, 2], [2, 0, 26.0, 0, 0, 2], [3, 0, 27.0, 1, 0, 0], [1, 0, 42.0, 1, 0, 2], [3, 0, 20.0, 1, 1, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 21.0, 0, 0, 2], [1, 0, 61.0, 0, 0, 2], [2, 0, 57.0, 0, 0, 1], [1, 1, 21.0, 0, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 0, 80.0, 0, 0, 2], [3, 0, 51.0, 0, 0, 2], [1, 0, 32.0, 0, 0, 0], [1, 0, 0.0, 0, 0, 2], [3, 1, 9.0, 3, 2, 2], [2, 1, 28.0, 0, 0, 2], [3, 0, 32.0, 0, 0, 2], [2, 0, 31.0, 1, 1, 2], [3, 1, 41.0, 0, 5, 2], [3, 0, 0.0, 1, 0, 2], [3, 0, 20.0, 0, 0, 2], [1, 1, 24.0, 0, 0, 0], [3, 1, 2.0, 3, 2, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 0.75, 2, 1, 0], [1, 0, 48.0, 1, 0, 0], [3, 0, 19.0, 0, 0, 2], [1, 0, 56.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 2], [3, 1, 23.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [2, 1, 18.0, 0, 1, 2], [3, 0, 21.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [3, 1, 18.0, 0, 0, 1], [2, 0, 24.0, 2, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 1, 32.0, 1, 1, 1], [2, 0, 23.0, 0, 0, 2], [1, 0, 58.0, 0, 2, 0], [1, 0, 50.0, 2, 0, 2], [3, 0, 40.0, 0, 0, 0], [1, 0, 47.0, 0, 0, 2], [3, 0, 36.0, 0, 0, 2], [3, 0, 20.0, 1, 0, 2], [2, 0, 32.0, 2, 0, 2], [2, 0, 25.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 43.0, 0, 0, 2], [1, 1, 0.0, 1, 0, 2], [2, 1, 40.0, 1, 1, 2], [1, 0, 31.0, 1, 0, 2], [2, 0, 70.0, 0, 0, 2], [2, 0, 31.0, 0, 0, 2], [2, 0, 0.0, 0, 0, 2], [3, 0, 18.0, 0, 0, 2], [3, 0, 24.5, 0, 0, 2], [3, 1, 18.0, 0, 0, 2], [3, 1, 43.0, 1, 6, 2], [1, 0, 36.0, 0, 1, 0], [3, 1, 0.0, 0, 0, 1], [1, 0, 27.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [3, 0, 14.0, 5, 2, 2], [2, 0, 60.0, 1, 1, 2], [2, 0, 25.0, 1, 2, 0], [3, 0, 14.0, 4, 1, 2], [3, 0, 19.0, 0, 0, 2], [3, 0, 18.0, 0, 0, 2], [1, 1, 15.0, 0, 1, 2], [1, 0, 31.0, 1, 0, 2], [3, 1, 4.0, 0, 1, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 0], [1, 0, 60.0, 0, 0, 2], [2, 0, 52.0, 0, 0, 2], [3, 0, 44.0, 0, 0, 2], [3, 1, 0.0, 0, 0, 1], [1, 0, 49.0, 1, 1, 0], [3, 0, 42.0, 0, 0, 2], [1, 1, 18.0, 1, 0, 0], [1, 0, 35.0, 0, 0, 2], [3, 1, 18.0, 0, 1, 0], [3, 0, 25.0, 0, 0, 1], [3, 0, 26.0, 1, 0, 2], [2, 0, 39.0, 0, 0, 2], [2, 1, 45.0, 0, 0, 2], [1, 0, 42.0, 0, 0, 2], [1, 1, 22.0, 0, 0, 2], [3, 0, 0.0, 1, 1, 0], [1, 1, 24.0, 0, 0, 0], [1, 0, 0.0, 0, 0, 2], [1, 0, 48.0, 1, 0, 2], [3, 0, 29.0, 0, 0, 2], [2, 0, 52.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [1, 1, 38.0, 0, 0, 0], [2, 1, 27.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 33.0, 0, 0, 2], [2, 1, 6.0, 0, 1, 2], [3, 0, 17.0, 1, 0, 2], [2, 0, 34.0, 0, 0, 2], [2, 0, 50.0, 0, 0, 2], [1, 0, 27.0, 1, 0, 2], [3, 0, 20.0, 0, 0, 2], [2, 1, 30.0, 3, 0, 2], [3, 1, 0.0, 0, 0, 1], [2, 0, 25.0, 1, 0, 2], [3, 1, 25.0, 1, 0, 2], [1, 1, 29.0, 0, 0, 2], [3, 0, 11.0, 0, 0, 0], [2, 0, 0.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 2], [2, 0, 23.0, 0, 0, 2], [3, 0, 28.5, 0, 0, 2], [3, 1, 48.0, 1, 3, 2], [1, 0, 35.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [1, 0, 36.0, 1, 0, 2], [1, 1, 21.0, 2, 2, 0], [3, 0, 24.0, 1, 0, 2], [3, 0, 31.0, 0, 0, 2], [1, 0, 70.0, 1, 1, 2], [3, 0, 16.0, 1, 1, 2], [2, 1, 30.0, 0, 0, 2], [1, 0, 19.0, 1, 0, 2], [3, 0, 31.0, 0, 0, 1], [2, 1, 4.0, 1, 1, 2], [3, 0, 6.0, 0, 1, 2], [3, 0, 33.0, 0, 0, 2], [3, 0, 23.0, 0, 0, 2], [2, 1, 48.0, 1, 2, 2], [2, 0, 0.67000000000000004, 1, 1, 2], [3, 0, 28.0, 0, 0, 2], [2, 0, 18.0, 0, 0, 2], [3, 0, 34.0, 0, 0, 2], [1, 1, 33.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 41.0, 0, 0, 2], [3, 0, 20.0, 0, 0, 0], [1, 1, 36.0, 1, 2, 2], [3, 0, 16.0, 0, 0, 2], [1, 1, 51.0, 1, 0, 2], [1, 0, 0.0, 0, 0, 0], [3, 1, 30.5, 0, 0, 1], [3, 0, 0.0, 1, 0, 1], [3, 0, 32.0, 0, 0, 2], [3, 0, 24.0, 0, 0, 2], [3, 0, 48.0, 0, 0, 2], [2, 1, 57.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 0], [2, 1, 54.0, 1, 3, 2], [3, 0, 18.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [3, 1, 5.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 1], [1, 1, 43.0, 0, 1, 2], [3, 1, 13.0, 0, 0, 0], [1, 1, 17.0, 1, 0, 2], [1, 0, 29.0, 0, 0, 2], [3, 0, 0.0, 1, 2, 2], [3, 0, 25.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [3, 1, 18.0, 0, 0, 2], [3, 0, 8.0, 4, 1, 1], [3, 0, 1.0, 1, 2, 2], [1, 0, 46.0, 0, 0, 0], [3, 0, 0.0, 0, 0, 1], [2, 0, 16.0, 0, 0, 2], [3, 1, 0.0, 8, 2, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 25.0, 0, 0, 2], [2, 0, 39.0, 0, 0, 2], [1, 1, 49.0, 0, 0, 2], [3, 1, 31.0, 0, 0, 2], [3, 0, 30.0, 0, 0, 0], [3, 1, 30.0, 1, 1, 2], [2, 0, 34.0, 0, 0, 2], [2, 1, 31.0, 1, 1, 2], [1, 0, 11.0, 1, 2, 2], [3, 0, 0.41999999999999998, 0, 1, 0], [3, 0, 27.0, 0, 0, 2], [3, 0, 31.0, 0, 0, 2], [1, 0, 39.0, 0, 0, 2], [3, 1, 18.0, 0, 0, 2], [2, 0, 39.0, 0, 0, 2], [1, 1, 33.0, 1, 0, 2], [3, 0, 26.0, 0, 0, 2], [3, 0, 39.0, 0, 0, 2], [2, 0, 35.0, 0, 0, 2], [3, 1, 6.0, 4, 2, 2], [3, 0, 30.5, 0, 0, 2], [1, 0, 0.0, 0, 0, 2], [3, 1, 23.0, 0, 0, 2], [2, 0, 31.0, 1, 1, 0], [3, 0, 43.0, 0, 0, 2], [3, 0, 10.0, 3, 2, 2], [1, 1, 52.0, 1, 1, 2], [3, 0, 27.0, 0, 0, 2], [1, 0, 38.0, 0, 0, 2], [3, 1, 27.0, 0, 1, 2], [3, 0, 2.0, 4, 1, 2], [3, 0, 0.0, 0, 0, 1], [3, 0, 0.0, 0, 0, 2], [2, 0, 1.0, 0, 2, 0], [3, 0, 0.0, 0, 0, 1], [1, 1, 62.0, 0, 0, 0], [3, 1, 15.0, 1, 0, 0], [2, 0, 0.82999999999999996, 1, 1, 2], [3, 0, 0.0, 0, 0, 0], [3, 0, 23.0, 0, 0, 2], [3, 0, 18.0, 0, 0, 2], [1, 1, 39.0, 1, 1, 0], [3, 0, 21.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 32.0, 0, 0, 2], [1, 0, 0.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [2, 0, 16.0, 0, 0, 2], [1, 1, 30.0, 0, 0, 0], [3, 0, 34.5, 0, 0, 0], [3, 0, 17.0, 0, 0, 2], [3, 0, 42.0, 0, 0, 2], [3, 0, 0.0, 8, 2, 2], [3, 0, 35.0, 0, 0, 0], [2, 0, 28.0, 0, 1, 2], [1, 1, 0.0, 1, 0, 0], [3, 0, 4.0, 4, 2, 2], [3, 0, 74.0, 0, 0, 2], [3, 1, 9.0, 1, 1, 0], [1, 1, 16.0, 0, 1, 2], [2, 1, 44.0, 1, 0, 2], [3, 1, 18.0, 0, 1, 2], [1, 1, 45.0, 1, 1, 2], [1, 0, 51.0, 0, 0, 2], [3, 1, 24.0, 0, 3, 0], [3, 0, 0.0, 0, 0, 0], [3, 0, 41.0, 2, 0, 2], [2, 0, 21.0, 1, 0, 2], [1, 1, 48.0, 0, 0, 2], [3, 1, 0.0, 8, 2, 2], [2, 0, 24.0, 0, 0, 2], [2, 1, 42.0, 0, 0, 2], [2, 1, 27.0, 1, 0, 0], [1, 0, 31.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [3, 0, 4.0, 1, 1, 2], [3, 0, 26.0, 0, 0, 2], [1, 1, 47.0, 1, 1, 2], [1, 0, 33.0, 0, 0, 2], [3, 0, 47.0, 0, 0, 2], [2, 1, 28.0, 1, 0, 0], [3, 1, 15.0, 0, 0, 0], [3, 0, 20.0, 0, 0, 2], [3, 0, 19.0, 0, 0, 2], [3, 0, 0.0, 0, 0, 2], [1, 1, 56.0, 0, 1, 0], [2, 1, 25.0, 0, 1, 2], [3, 0, 33.0, 0, 0, 2], [3, 1, 22.0, 0, 0, 2], [2, 0, 28.0, 0, 0, 2], [3, 0, 25.0, 0, 0, 2], [3, 1, 39.0, 0, 5, 1], [2, 0, 27.0, 0, 0, 2], [1, 1, 19.0, 0, 0, 2], [3, 1, 0.0, 1, 2, 2], [1, 0, 26.0, 0, 0, 0], [3, 0, 32.0, 0, 0, 1]]

if __name__ == "__main__":
    did_I_survive()

"""
 Passenger attributes
**********************
 pclass      Passenger Class            1 upper/2 middle/3 lower
 sex         Sex                        0 male/1 female
 age         Age                        float
 sibsp       Siblings/Spouses Aboard    float
 parch       Parents/Children Aboard    float
 embarked    Port of Embarkation        (0= Unknown; 1 = Cherbourg; 2 = Queenstown; 3 = Southampton)

"""
