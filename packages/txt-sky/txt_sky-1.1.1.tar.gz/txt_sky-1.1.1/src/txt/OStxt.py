import os
'''
This model is for making path of txt.
'''
def movetxt(oldpath,newpath):
    if (os.path.exists(oldpath) and os.path.exists(newpath)):
        for a,b in os.path.split(oldpath):
            os.path.join(newpath,b)
        del a,b
        pass
    else:
        raise FileNotFoundError(f"Can not fond",oldpath,newpath)
        pass

def findfile(path,file):
    filelist=[]
    if os.path.exists(path):
        for f in os.listdir(path):
            temp_dir = os.path.join(path, f)
            if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                for a,b in os.path.split(temp_dir):
                    filelist.append(b)
                '''
            elif os.path.isdir(temp_dir):
                get_file_list(temp_dir, file, filelist)
                '''
        return filelist
        del a,b
    else:
        raise FileNotFoundError(f"Can not fond",path)
        pass

def findallfile(path,file):
    filelist=[]
    if os.path.exists(path):
        for f in os.listdir(path):
            temp_dir = os.path.join(path, f)
            if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                for a,b in os.path.split(temp_dir):
                    filelist.append(b)
            elif os.path.isdir(temp_dir):
                get_file_list(temp_dir, file, filelist)
        return filelist
        del a,b
    else:
        raise FileNotFoundError(f"Can not fond",path)
        pass

class path():
    def __init__(self,path):
        if os.path.exists(path):
            pass
        else:
            os.exit()
            raise FileNotFoundError(f"Can not fond",path)
            pass
    def readpath():
        for path,dirs,files in os.walk(path):
            list=[path,dirs,files]
        return list
    def readallfile(file):
        filelist=[]
        for f in os.listdir(path):
            temp_dir = os.path.join(path, f)
            if os.path.isfile(temp_dir) and temp_dir.endswith(file):
                for a,b in os.path.split(temp_dir):
                    filelist.append(b)
            elif os.path.isdir(temp_dir):
                get_file_list(temp_dir, file, filelist)
        return filelist
        del a,b
    def readwjj():
        wjj=[]
        a=os.listdir(path)
        if os.path.isdir(a):
            wjj.append(a)
        else:
            pass
        return a
    def newfile(newpath,file):
        if os.path.exists(newpath):
            os.mkdir(file)
        else:
            raise FileNotFoundError(f"Can not fond",newpath)
            pass
    def delfile(path,file,way='0'):
        if os.path.exists(path):
            if way=='0':
                os.rmdir(file)
                pass
            elif way=='1':
                try:
                    os.removedirs(file)
                except NameError or FileNotFoundError:
                    print("can not found",file)
            else:
                raise ValueError(f"way can only be 0 or 1")
        else:
            raise FileNotFoundError(f"Can not fond",newpath)
            pass
    
