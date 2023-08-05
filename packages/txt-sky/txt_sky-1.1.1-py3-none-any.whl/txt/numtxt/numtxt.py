import numpy as np

class save_txt():
    def __init__(self,x,y):
        pass
    def save_zeros(self,path_and_name,times=5):
        try:
            times=int(times)
        except ValueError:
            print("Times must be int.")
        list=np.zeros(times)
        list=np.array(list)
        np.savetxt(path_and_name,list,fmt='%')
        del list
    def save_ones(self,path_and_name,times=5):
        try:
            times=int(times)
        except ValueError:
            print("Times must be int.")
        list=np.ones(times)
        list=np.array(list)
        np.savetxt(path_and_name,list,fmt='%')
        del list
    def save_youwant(self,path_and_name,times=5,num=2):
        try:
            times=int(times)
        except ValueError:
            print("Times must be int.")
        list=[]
        a=0
        while a<5:
            list.append(num)
            a+=1
        list=np.array(list)
        np.savetxt(path_and_name,list,fmt='%')
        del list,a
    def makeForminTxt(self,list,path_and_name,shape,fmt='%.2f',delim='/t'):
        try:
            shape=list(shape)
            if len(shape)==2:
                x=shape[0]
                y=shape[1]
                list=np.shape(x,y)
                np.savetxt(path_and_name,list,fmt=fmt,delimiter=delim)
            else:
                print("shape's must be 2")
        except:
            print("shape must be list")
