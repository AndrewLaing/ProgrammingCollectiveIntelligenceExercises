""" Chapter 9 Exercise 4: Hierarchy of interests.

    "Design a simple hierarchy of interests, along with a data structure to represent it.
    Alter the matchcount function to use the hierarchy to give partial points for matches."

    I implemented a scoring system based upon the activeness levels of the interests.
    A higher score means that people share the same activity levels.
    * see end for more methods of personality based scoring of interests
"""

def matchcount(interest1,interest2):
    activeness_scale = {'fashion': 0.3,'art': 0.4, 'scrabble': 0.2, 'skiing': 1.0, 'shopping': 0.6, 
                        'camping': 0.7, 'dancing': 0.8, 'tv': 0.0, 'travel': 0.7, 'cooking': 0.3,
                        'writing': 0.1, 'reading': 0.1, 'knitting': 0.1, 'photography': 0.4, 'football': 1.0, 
                        'running': 1.0, 'soccer': 1.0, 'animals': 0.9, 'opera': 0.2, 'computers': 0.0,
                        'movies': 0.3, 'snowboarding': 1.0}
    l1=interest1.split(':')
    l2=interest2.split(':')
    x, y = 0, 0
    
    for v in l1:
        if v in activeness_scale: 
            x+=activeness_scale[v]
        else: 
            x+=0.5
    
    for v in l2:
        if v in activeness_scale: 
            y+=activeness_scale[v]
        else: 
            y+=0.5
    
    x1 = float(x)/len(l1)
    y1 = float(y)/len(l2)
    
    if x1>y1: 
        return 1-float(x1-y1)
    elif y1>x1: 
        return 1-float(y1-x1)
    else: 
        return 1

"""
Here are some ideas for personality-based scoring of interests influenced by the Hexaco personality inventory.

Unconventionality scale
Altruism (versus Antagonism) scale
Creativity scale
Inquisitiveness scale
Aesthetic Appreciation scale
Prudence scale
Perfectionism scale
Diligence scale
Organization scale
Patience scale
Flexibility scale
Gentleness scale
Forgivingness scale
Liveliness scale
Social Boldness scale
Social Self-Esteem scale
Sincerity scale 
Fairness scale 
Greed Avoidance scale 
Modesty scale 
Fearfulness scale 
Anxiety scale 
Dependence scale 
Sentimentality scale

"""
