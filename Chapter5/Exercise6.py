""" Chapter 5 Exercise 6: Line angle penalization.

    Add an additional cost to the network layout algorithm cost function when the angle between 
    two lines attached to the same person is very small. (Hint: you can use the vector cross-product.)

    Here's the basic line angle penalization to add.
"""

def crosscount1(v):
    total = 0
    res = 0
    
    def calculate_angle(centre,line1,line2):
        # Calculate the angles created.
        delta_x = float(line1[0] - centre[0])
        delta_y = float(line1[1] - centre[1])
        answer = atan2(delta_y, delta_x)*180.0/pi

        delta_x = float(line2[0] - centre[0])
        delta_y = float(line2[1] - centre[1])
        answer1 = atan2(delta_y, delta_x)*180.0/pi

        # Get the answer
        if answer > answer1: return answer-answer1
        else: return answer1-answer

    # Convert the number list t a dictionary of person/ (x,y)
    loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
    total=0

    # Loop through every pair of links
    for i in range(len(links)):
        for j in range(i+1,len(links)):

            # Get the locations
            (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
            (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]

            # Find nodes then calculate angle between lines
            if (x1,y1)==(x3,y3): 
                res = calculate_angle((x1,y1),(x2,y2),(x4,y4))                       
            elif (x1,y1)==(x4,y4): 
                res = calculate_angle((x1,y1),(x2,y2),(x3,y3)) 
            elif (x2,y2)==(x3,y3): 
                res = calculate_angle((x2,y2),(x1,y1),(x4,y4)) 
            elif (x2,y2)==(x4,y4): 
                res = calculate_angle((x2,y2),(x1,y1),(x3,y3)) 
            
            # Find the smallest of the two angles between the lines
            if res>180: 
                res1 = 360-res
            else: 
                res1=res
            
            # If the angle is less than 30 add to cost
            if res1<30:
                total+=(1-(res1/30.0))
    
    return total
