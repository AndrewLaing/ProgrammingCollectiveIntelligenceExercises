""" Chapter 9 Exercise 1: Bayesian classifier.

    "Can you think of ways that the Bayesian classifier you built in Chapter 6 could be used on the matchmaker dataset?
    What would be good examples of features?"

    I implemented this with features for smoking?, want-kids? and interest combinations.
"""

import docclass_matchmaker as docclass
import advancedclassify1 as advancedclassify
matchmaker=advancedclassify.loadmatch('matchmaker.csv')
cl=docclass.naivebayes(docclass.get_features1)
cl.setdb('matchmaker.db')


# add train1() to the classifier class in docclass.py
    def train1(self,item,cat):
        features=self.getfeatures(item)
        
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)
        
        # Increment the count for this category
        self.incc(cat)
        self.con.commit()


# add get_features1() to the beginning of docclass.py
def get_features1(item):
    interests1 = item[3].split(':')
    interests2 = item[8].split(':')
    list1=[]
    
    for a in interests1:
        for b in interests2:
            feat = a+' '+b
            list1.append(feat)
    
    smokingornot = 'smoke '+item[1]+' '+item[6]
    list1.append(smokingornot)
    kidsornot = 'kids '+item[1]+' '+item[6]
    list1.append(kidsornot)
   
    return list1



# Train the database
for a in range(len(matchmaker)):
    item = matchmaker[a].data
    cat = str(matchmaker[a].match)
    cl.train1(item,cat)
    
"""
# And it classifies <<<hurrah>>>

>>> cl.classify(['39', 'yes', 'no', 'skiing:knitting:dancing', '220 W 42nd St New York NY', '43', 'no', 'yes', 'soccer:reading:scrabble', '824 3rd Ave New York NY'])
u'0'

>>>cl.classify(['39', 'no', 'yes', 'running:fashion:art:travel', '556 7th Ave New York NY', '39', 'no', 'no', 'knitting:photography', '404 E 14th St New York NY'])
u'1'

"""
