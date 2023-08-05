try:
    import numpy as np
    import matplotlib as mt
except ImportError:
    print("Please install numpy and matplotlib.")
except ModuleNotFoundError:
    print("Please install numpy and matplotlib.")

'''
THE FIRST ONE IS ABOUT TXT WRITE AND READ.
'''
class txt():
    def __init__(self,path,ways="w+"):
        if ways==("r" or "r+"):
            try:
                a=open(path,ways)
            except:
                raise FileNotFoundError(f"Can not found txt",path)
        elif ways==("a" or "a+"):
            print("This will delete the words in the txt.")
        a=open(path,ways)
        a.close()
        
    def __new__(self):
        pass
    
    def write_oneline(self,txt):
        with open(path,"w+") as f:
            f.write(txt)
            f.close

    def read_oneline(self):
        with open(path,"w+") as f:
            txt=f.readline()
            f.close()
            return txt

    def read_all_notlist(self):
        with open(path,"w+") as f:
            txt=f.read()
            f.close()
            return txt

    def read_all_inlist(self):
        with open(path,"w+") as f:
            txt=f.readlines()
            f.close()
            return txt

def numbers_in_txt(path,stop,start=0,step=1,numbertipe='%.3f'):
    if stop<start:
        def unrange(stop,start,step):
            list=[]
            while stop>=start:
                stop-=step
                list.append(stop)
            list.remove(-1)
            return list
        a=unrange(stop,start,step)
        np.savetxt(path,a,fmt=numbertipe,delimiter='/n')
    elif stop>start:
        a=range(stop,start,step)
        np.savetxt(path,a,fmt=numbertipe,delimiter='/n')
    else:
        print("Stop can not be the same as start.")
