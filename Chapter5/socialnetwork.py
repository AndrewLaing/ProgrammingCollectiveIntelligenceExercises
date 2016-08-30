import math
from PIL import Image, ImageDraw

people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']
links=[('Augustus', 'Willy'),
       ('Mike', 'Joe'),
       ('Miranda', 'Mike'),
       ('Violet', 'Augustus'),
       ('Miranda', 'Willy'),
       ('Joe', 'Charlie'),
       ('Veruca', 'Augustus'),
       ('Miranda', 'Joe')]


def crosscount(v):
    # Convert the number list t a dictionary of person/ (x,y)
    loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
    total=0

    # Loop through every pair of links
    for i in range(len(links)):
        for j in range(i+1,len(links)):

            # Get the locations
            (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
            (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]

            den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)

            # den=0 if lines are parallel
            if den==0: continue

            # Otherwise ua and ab are a fraction of ithe line where they cross
            ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/float(den)              # Corrected for python 2x
            ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/float(den)              # Corrected for python 2x

            # If the fraction for this total is between 0 and 1 for both lines then they cross each other
            if ua>0 and ua<1 and ub>0 and ub<1:
                total+=1
    print "total=",total
    return total


def drawnetwork(sol):
    jpeg='network_diagram.jpg'
    # Create the image
    img=Image.new('RGB',(400,400),(255,255,255))
    draw=ImageDraw.Draw(img)

    # Create the position dict
    pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(0,len(people))])

    # Draw links
    for (a,b) in links:
        draw.line((pos[a],pos[b]),fill=(255,0,0))

    # draw people
    for n,p in pos.items():
        draw.text(p,n,(0,0,0))
    img.save(jpeg,'JPEG')

domain=[(10,370)]*(len(people)*2)


""" Corrected drawnetwork() to print out result as a jpeg
    Corrected crosscount to allow float division of ua and ub because Python 2x
      defaulted to integer division during "../den"
"""
