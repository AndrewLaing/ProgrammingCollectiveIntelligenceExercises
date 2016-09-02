""" Chapter 10 Exercise 5(a): Alternative display methods.(cont)

    Now a trading-volume chart with important dates shown.
    Enter two stock market tickers. First we find some features, then we plot features
    one at a time on graph of trading volumes for the two stocks.
    
    To do - rename variables
"""

import nmf
import urllib2 as urllib2
from numpy import *
import Gnuplot, Gnuplot.funcutils

def volume_chart(tickers,allporder):
    count=0
    coordic={}
    for t in tickers:
        # Open the URL
        print 't=',t
        rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?'+\
                             's=%s&d=11&e=26&f=2006&g=d&a=3&b=12&c=2005' %t +\
                             '&ignore=.csv').readlines()
        # get coords
        dates={}
        coords=[]
        this=[]
        this=[(r.split(',')) for r in rows if r.strip()!='']
        this.reverse()
        
        for a in range(len(this)-1):
            dates[this[a][0]]=a
            coord=(a,int(this[a][5]))
            coords.append(coord)
        coordic[count]=coords
        count+=1
    
    print dates
    
    for feats in range(len(allporder)):
        g = Gnuplot.Gnuplot(debug=1)
        tittlies='Stock Volume Chart Feature %s' % feats
        g.title(tittlies)
        g('set data style lines')
        g('set grid lt 0 lw 0.5 lc rgb "#ff0000"')
        g('set format y "%f"')
        # g('set arrow from 278,0 to 278,16000000 nohead')
        g('set ylabel "TRADING VOLUME" 2,0')
        labelstocks = 'set xlabel "DATELINE from 03-12-05       %s-Red  %s-Green" 2,0' % (tickers[0], tickers[1])
        g(labelstocks)
        addy=0
        
        for feat in allporder[feats]:
            addy+=1
            print feat
            # labelfeat = 'set arrow from %d,0 to %d,16000000 nohead' % (dates[feat[1]],dates[feat[1]])
            labelfeat = 'set label "X %s" at %d,2000000*%d textcolor rgb "#000000"' % (feat[1], dates[feat[1]], addy)
            g(labelfeat)
        
        plot1 = Gnuplot.PlotItems.Data(coordic[0], with_="lines 1", title=None) # 1=red 2=green 3=blue 4=pink...
        plot2 = Gnuplot.PlotItems.Data(coordic[1], with_="lines 2", title=None) # 1=red 2=green 3=blue 4=pink...
        g.plot(plot1,plot2)
        t=raw_input('Press enter to continue')


def stock_volumes(tickers):
    shortest=300
    prices={}
    dates=None
    allporder=[]
    allols=[]
    
    for t in tickers:
        # Open the URL
        print 't=',t
        rows=urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?'+\
                             's=%s&d=11&e=26&f=2006&g=d&a=3&b=12&c=2005' %t +\
                             '&ignore=.csv').readlines()
        # Extract the volume field from every line
        prices[t]=[float(r.split(',')[5]) for r in rows[1:] if r.strip()!='']
        
        if len(prices[t])<shortest: 
            shortest=len(prices[t])
        
        if not dates:
            dates=[r.split(',')[0] for r in rows[1:] if r.strip()!='']
    
    l1=[[prices[tickers[i]][j] 
      for i in range(len(tickers))]
       for j in range(shortest)]
    
    w,h = nmf.factorize(matrix(l1),pc=5)

    # Loop over all the features
    for i in range(shape(h)[0]):
        print "Feature %d" %i
        
        # Get the top stocks for this feature
        ol=[(h[i,j],tickers[j]) for j in range(shape(h)[1])]
        ol.sort()
        ol.reverse()
        
        for j in range(len(tickers)):
            print ol[j]
        
        allols.append(ol)
        print
        
        # Show the top dates for this feature
        porder=[(w[d,i],d) for d in range(300)]
        porder.sort()
        porder.reverse()
        f = [(p[0],dates[p[1]]) for p in porder[0:3]]
        print f
        allporder.append(f) 
        print
    
    frog=raw_input('press <ENTER> to continue')
    return allporder

def main():
    tickers=[]
    first=str(raw_input('Enter first ticker >'))
    tickers.append(first)
    second=str(raw_input('Enter first ticker >'))
    tickers.append(second)
    allporder = stock_volumes(tickers)
    volume_chart(tickers, allporder)

if __name__ == "__main__":
    main()
    
