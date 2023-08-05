def get_version():
    '''
    import os
    from pathlib import Path
    txt="I:\sky\py11\Lib\site-packages\txtplan\version.mx"
    extension = Path(txt).suffix
    filename=os.path.split(txt)
    fiesion=os.path.splitext(extension)
    newname="version.txt"
    os.rename(txt,newname)
    with open(newname,"r") as r:
        version=r.read()
    txt="I:\sky\py11\Lib\site-packages\txtplan\version.txt"
    extension = Path(txt).suffix
    filename=os.path.split(txt)
    fiesion=os.path.splitext(extension)
    newname="version.mx"
    os.rename(txt,newname)
    return version
    '''
    with open(".version.txt","r") as r:
        version=r.read()
    return version
