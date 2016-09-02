""" As I couldn't manage to install matplotlib properly, I decided to implement
a version of probability graph from the PDF page 187 using the Python Imaging Library.
Not as smooth as the matplotlib version but it still provides meaningful data :)

See end for usage
"""

import Image, ImageDraw, ImageOps
from random import randint
import numpredict as numpredict


def draw_graph(list1,jpeg='probability_graph.jpg'):
    # height and width of jpeg
    w,h=0,0
    for a in range(len(list1)):
        if list1[a][0]>w:
            w=list1[a][0]
        
        if list1[a][1]>h:
            h=list1[a][1]
    
    # Draw graph and save image
    img = Image.new('RGB',(w+45, h+45),(255,255,255))
    draw = ImageDraw.Draw(img)
    
    for a in range(len(list1)-1):
        xycoords=(list1[a][0]+20,list1[a][1]+10)
        x1y1coords=(list1[a][0]+20,10)
        draw.line([xycoords,x1y1coords], fill=128)
    
    del draw
    
    img = ImageOps.flip(img)
    draw = ImageDraw.Draw(img)
    
    for a in range(0,h,50):
        if a == 0: 
            b=str(a)
        else: 
            b=str(a/500.0)
        draw.text((0,h-a+28),b, fill=0)
    
    for a in range(0,w,25):
        draw.text((a+18,h+35),str(a), fill=0)
    
    del draw
    
    img.save(jpeg,'JPEG')


def av_probs(data,vec1,highnum,k,weightf,width_a):
    dicus={}
    
    for a in range(0,highnum+1):
        b = numpredict.probguess(data,vec1,a,a+width_a,k,weightf)
        
        for c in range(a,a+width_a):
            if c not in dicus: dicus[c]=[]
            dicus[c].append(b)
    
    high2=0
    
    for prob in dicus:
        if len(dicus[prob])>high2: 
            high2=len(dicus[prob])
    
    for x in dicus:
        a = sum(dicus[x])
        if a == 0: 
            dicus[x] = 0.0
        else:
            b = a/high2     
            dicus[x] = b
    
    list1=[]
    
    for a in dicus:
        b=(a,int(dicus[a]*500))
        list1.append(b)
    
    del dicus
    
    return list1


def main(data,vec1,highnum,k,weightf,width_a,jpeg):
    list1 = av_probs(data,vec1,highnum,k,weightf,width_a)
    draw_graph(list1,jpeg='probability_graph.jpg')




"""
----------------------------------------------------------------------------------------
Notes:
----------------------------------------------------------------------------------------
1: width_a
**********
probguess() uses high, and low.
av_probs() checks the probabilities within the range 0-highnum, width_a is used
           to provide a range to pass to probguess(). All the results for each number
           within the range are added to a list for each number and average probabilities
           are calculated then converted into y coordinates.

2: Usage
********
save as probability_graph.py

import probability_graph as av_probs
import numpredict as numpredict
data=numpredict.wineset3()
av_probs.main(data,[99,20],120,5,numpredict.gaussian,50,'probability_graph.jpg')
----------------------------------------------------------------------------------------
"""
