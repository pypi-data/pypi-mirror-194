import matplotlib.pyplot as p
import numpy as np

def pie(list,colors=None,labels=None,font=None,title=None):
    list=np.array(list)
    p.rcParams['font.sans-serif']=[font]
    if colors==None:
        p.pie(list,labels)
        p.title(title)
        p.show()
    else:
        p.pie(a,colers=colers,labels=labels)
        p.title(title)
        p.show()

def plot(txtpath,font=None,labels=None,title=None):
    a=np.loadtxt(txtpath)
    p.rcParams['font.sans-serif']=[font]
    p.plot(a)
    p.legend(labels)
    p.title(title)
    p.show()

def bar(xnum,ynum,width=0.5,font=None,xlabel=None,ylabel=None,title=None):
    p.rcParams['font.sans-serif']=[font]
    p.bar(xnum,ynum,width=width)
    p.xlabel(xlabel)
    p.ylabel(ylabel)
    p.title(title)
    p.show()
