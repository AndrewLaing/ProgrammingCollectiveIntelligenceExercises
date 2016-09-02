import Gnuplot as Gnuplot
import Gnuplot, Gnuplot.funcutils
from numpy import *

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
    
