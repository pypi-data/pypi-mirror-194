#from .txt import (txt,numbers_in_txt)
from .version import get_version

if get_version()=='1.1.1':
    pass
else:
    print("Please improve this model in to 1.1.1.")
    pass

__all__=['txt','plot']

def letter(sth='y'):
    if sth!='n':
        a="""A LETTER FROM AUTHOR TO USERS
Dear Users:
  Welcome to use this model.I am the author Sky Vega Yang.
I make this model for making writing and reading txt easily.
This model will improve at least once a season.So please always
check the version of this model.If you find some wrrons in this
model,you can write an e-mail to me.My e-mail is xjgis@126.com.
                                                   SKY VEGA YANG"""
        b="If you want to close this letter try letter('n')"
        print(a)
        print(b)
        pass
    else:
        pass

