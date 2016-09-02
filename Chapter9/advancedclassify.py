import Gnuplot as Gnuplot
import Gnuplot, Gnuplot.funcutils
from numpy import *
import urllib as urllib
from HTMLParser import HTMLParser
import math as math

class MyHTMLParser(HTMLParser):
    count, head, result = 0, 'active', ''
    
    def handle_starttag(self, tag, attrs):
        if self.head=='passive':
            if tag=='script':
                self.count=0
        if tag=='title': self.count=1
    
    def handle_endtag(self, tag):
        if tag=="head":
            self.count=1
            self.head='passive'
        
        if self.head=='passive':
            if tag=='script':
                self.count=1
        
        if tag=='title': self.count=0
    
    def handle_data(self, data):
        if self.count > 0:
            if data!='':
                self.result = self.result + data

class matchrow:
    def __init__(self,row,allnum=False):
        if allnum:
            self.data=[float(row[i]) for i in range(len(row)-1)]
        else:
            self.data=row[0:len(row)-1]
        
        self.match=int(row[len(row)-1])


def loadmatch(f,allnum=False):
    rows=[]
    
    for line in file(f):
        rows.append(matchrow(line.split(','),allnum))
    
    return rows


def plotagematches(rows):
    xdm,ydm=[r.data[0] for r in rows if r.match==1],\
            [r.data[1] for r in rows if r.match==1]
    xdn,ydn=[r.data[0] for r in rows if r.match==0],\
            [r.data[1] for r in rows if r.match==0]
    listm=[]
    
    for fr in range(len(xdm)):
        dep=(xdm[fr],ydm[fr])
        listm.append(dep)
    
    listn=[]
    
    for fr in range(len(xdn)):
        dep=(xdn[fr],ydn[fr])
        listn.append(dep)
    
    g = Gnuplot.Gnuplot(debug=1)
    plot1 = Gnuplot.PlotItems.Data(listm, with_="points 1", title=None)
    plot2 = Gnuplot.PlotItems.Data(listn, with_="points 3", title=None)  # No title
    g.title('plotage matches')
    g.plot(plot1,plot2)
    wait=raw_input('Press <ENTER> to continue')


def lineartrain(rows):
    averages={}
    counts={}

    for row in rows:
        # Get the class of this point
        cl=row.match

        averages.setdefault(cl,[0.0]*(len(row.data)))
        counts.setdefault(cl,0)

        # Add this point to the averages
        for i in range(len(row.data)):
            averages[cl][i]+=float(row.data[i])

        # Keep track of how many points in each class
        counts[cl]+=1

    # Divide sums by counts to get the averages
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[cl]

    return averages


def dotproduct(v1,v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])


def dpclassify(point,avgs):
    b=(dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
    y=dotproduct(point,avgs[0])-dotproduct(point,avgs[1])+b
    
    if y>0: 
        return 0
    else: 
        return 1


def yesno(v):
    if v=='yes': 
        return 1
    elif v=='no': 
        return -1
    else: 
        return 0 


def matchcount(interest1,interest2):
    l1=interest1.split(':')
    l2=interest2.split(':')
    x=0
    
    for v in l1:
        if v in l2: 
            x+=1
    
    return float(x)         # Do as a float for rescaling purposes 


def get_url(url):
    try:
        conn = urllib.urlopen(url).read()
        parser = MyHTMLParser()
        parser.feed(conn)
        data = parser.result
        data1=data.split('\n')
        
        for a in data1:
            if 'Latitute:' in a: 
                lat=a.split(':')
            elif 'Longitute:' in a: 
                lon=a.split(':')
        
        loc_cachequery = (float(lat[1]),float(lon[1]))
        
        return loc_cachequery
    except: 
        return (None,None)


loc_cache={}

def getlocation(address):
    query1=address.replace(' ','+')
    
    if query1 in loc_cache: 
        return loc_cache[query1]
    
    url="http://www.cs.indiana.edu/cgi-pub/markane/geo.cgi?address="
    url+=query1
    url+="&click=Geocode!"
    loc_cache[query1] = get_url(url)
    
    return loc_cache[query1]


def milesdistance(a1,a2):
    lat1,long1=getlocation(a1)
    lat2,long2=getlocation(a2)
    if lat1==None or lat2==None or long1==None or long2==None:
        print 'Unable to calculate distance between',a1,"and",a2
        return 0
    
    latdif=69.1*(lat2-lat1)
    longdif=53.0*(long2-long1)
    return (latdif**2+longdif**2)**0.5


def loadnumerical():
    oldrows=loadmatch('matchmaker.csv')
    newrows=[]
    
    for row in oldrows:
        d=row.data
        data=[float(d[0]),yesno(d[1]),yesno(d[2]),
              float(d[5]),yesno(d[6]),yesno(d[7]),
              matchcount(d[3],d[8]),
              milesdistance(d[4],d[9]),
              row.match]
        newrows.append(matchrow(data))
    return newrows


def scaledata(rows):
    low=[999999999.0]*len(rows[0].data)
    high=[-999999999.0]*len(rows[0].data)
    
    # Find the lowest and highest values
    for row in rows:
        d=row.data
        for i in range(len(d)):
            if d[i]<low[i]: 
                low[i]=d[i]
            if d[i]>high[i]: 
                high[i]=d[i]

    # Create a function that scales data
    def scaleinput(d):
       return [(d[i]-low[i])/(high[i]-low[i])
            for i in range(len(low))]
  
    # Scale all the data
    newrows=[matchrow(scaleinput(row.data)+[row.match])
             for row in rows]
  
    # Return the new data and the function
    return newrows,scaleinput


def veclength(v):
    return sum([p**2 for p in v]) 


def rbf(v1,v2,gamma=20):
    dv=[v1[i]-v2[i] for i in range(len(v1))]
    l=veclength(dv)
    return math.e**(-gamma*l)


def nlclassify(point,rows,offset,gamma=10):
    sum0=0.0
    sum1=0.0
    count0=0
    count1=0

    for row in rows:
        if row.match==0:
            sum0+=rbf(point,row.data,gamma)
            count0+=1
        else:
            sum1+=rbf(point,row.data,gamma)
            count1+=1
    
    y=(1.0/count0)*sum0-(1.0/count1)*sum1+offset

    if y>0: 
        return 0
    else: 
        return 1


def getoffset(rows,gamma=10):
    l0=[]
    l1=[]
    for row in rows:
        if row.match==0: 
            l0.append(row.data)
        else: 
            l1.append(row.data)
    
    sum0=sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
    sum1=sum(sum([rbf(v1,v2,gamma) for v1 in l1]) for v2 in l1)

    return (1.0/(len(l1)**2))*sum1-(1.0/(len(l0)**2))*sum0
    
