""" Chapter 4 Exercise 7: Different training options.

    The neural network is trained with a set of 0s for all the URLs that a user did not click, 
    and a 1 for a URL that she did click. 
    Alter the training function so that it works instead for an application where users get to rate results from 1 to 5.

    In this version of trainquery the user has the option of rating the one selected url.

    Example usage: mynet.trainquery([wWorld,wBank],[uWorldBank,uRiver,uEarth],uWorldBank,3)
"""

    def trainquery(self,wordids,urlids,selectedurl,rating=1):
        ratingvalue = [1.0, 0.8, 0.6, 0.4, 0.2]
        self.generatehiddennode(wordids,urlids)
        self.setupnetwork(wordids,urlids)
        self.feedforward()
        targets=[0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=ratingvalue[int(rating)-1]
        error = self.backPropagate(targets)
        self.updatedatabase()

""" In the next version of trainquery the user has the option of rating all urls. (Unrated URLs are trained with 0)
    (The rated urls and their ratings are passed here as seperate lists but could also be passed as a dictionary)

    Example usage: mynet.trainquery([wWorld,wBank],[uWorldBank,uRiver,uEarth],[uWorldBank,uEarth],[1,4])
"""

    def trainquery(self,wordids,urlids,ratedurls,ratings):
        ratingvalue = [1.0, 0.8, 0.6, 0.4, 0.2]
        self.generatehiddennode(wordids,urlids)
        self.setupnetwork(wordids,urlids)
        self.feedforward()
        targets=[0.0]*len(urlids)
        for selectedurl in range(len(ratedurls)):
            targets[urlids.index(ratedurls[selectedurl])]=ratingvalue[int(ratings[selectedurl])-1]
        error = self.backPropagate(targets)
        self.updatedatabase()
