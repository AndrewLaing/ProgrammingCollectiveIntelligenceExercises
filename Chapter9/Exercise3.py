""" Chapter 9 Exercise 3: Choosing the best kernel parameters.

    "Write a function that loops over different values for gamma and determines what the best value for a given dataset is."

    Gamma is the radius of RBF.
    I wrote the function then learned how to use the LIBSVM included grid.py to optimize C and gamma. *see end of file
"""

import svm
from svm import *
import advancedclassify1 as advancedclassify
numericalset=advancedclassify.loadnumerical()
scaledset,scalef=advancedclassify.scaledata(numericalset) # libsvm needs scaled data

def optimize_gamma(scaledset):
    answers,inputs=[r.match for r in scaledset],[r.data for r in scaledset]
    cval = 0
    low = 9999
    
    for count in range(1,301,1):
        valg = count/100.0
        prob = svm_problem(answers, inputs)
        param = svm_parameter(kernel_type = RBF, shrinking = 0, gamma = valg)
        list1=[]
        
        for a in range(10):
            guesses = cross_validation(prob, param, 10)
            b=sum([abs(answers[i]-guesses[i]) for i in range(len(guesses))])
            list1.append(b)
        
        total, count = 0, 0
        
        for a in list1:
            count+=1
            total+=a
        
        av =float(total)/count
        
        if av<low:
            low = av
            gval = valg
    
    print "Cost =",av
    return gval

optimize_gamma(scaledset)

# Use the optimized gamma to train with
answers,inputs=[r.match for r in scaledset],[r.data for r in scaledset]
param = svm_parameter(kernel_type = RBF, gamma = 2.4)
prob = svm_problem(answers, inputs)
m = svm_model(prob,param)

newrow=[28.0,-1,-1,26.0,-1,1,2,0.8] # Man doesnt want kids woman does (??Gender stereotyping??)
m.predict(scalef(newrow))
newrow=[28.0,-1,1,26.0,-1,1,2,0.8]  # Both want children
m.predict(scalef(newrow))


"""
--------------------------------------------------------------------------------------------------------
Using grid.py
--------------------------------------------------------------------------------------------------------
First the data needs to be saved in the correct format, (easy enough to write a program to do this :3 .)

    0 1:0.65625 2:1 3:0 4:0.78125 5:0 6:1 7:0.0 8:0.0570524628059 
    1 1:0.15625 2:0 3:0 4:0.375 5:0 6:0 7:0.0 8:0.419948934927 .....

The first number is .match and the rest is indexed .data 

    python grid.py -log2c -4,4,1 -log2g -3,0,1 -v 20 -m 300 answers_inputs_for_grid.txt

If -log2c, -log2g, or -v is not specified, default values are used. *run python grid.py for usage



What are gamma and C?
*********************
Gamma is the radius of RBF.
-------------------------------------------------------------------------------
C is the penalty parameter of the C-SVC model engine. If left empty, its default is 1.
C is a trade-off between training error and the flatness of the solution.

 " The larger C is the less the final training error will be. But if you increase C too much you risk losing 
   the generalization properties of the classifier, because it will try to fit as best as possible all 
   the training points (including the possible errors of your dataset). 
   In addition a large C, usually increases the time needed for training. "

 " If C is small, then the classifier is flat (meaning that its derivatives are small - close to zero, 
   at least for the gaussian rbf kernel this is substantiated theoretically). 
   You have to find a C that keeps the training error small, but also generalizes well 
   (i.e., it doesn't have large fluctuations). There are several methods to find the best possible C automatically, 
   but you must keep in mind that this depends on the application you are interested in. "

C = infinity will allow no misclassification

Pantelis Bouboulis 
National and Kapodistrian University of Athens 

https://www.researchgate.net/post/In_support_vector_machinesSVM_how_we_adjust_the_parameter_C_why_we_use_this_parameter


"""
