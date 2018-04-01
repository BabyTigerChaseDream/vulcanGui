#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    Checkbutton for os/gpu selection
"""

from tkinter import *
from DicCmdParent import *
dbg = False
#TODO : make picks be able to parse "list array: *picklist"
pickTests= ['layer','sample','unknown']
Testname = "--tests "
DictTest= {
        Testname:pickTests,
        }

pickSuites = ['mnist','RNN','none']
Suitesname = "--target-suites "

DictSuites= {
        Suitesname:pickSuites,
        }

class MBtn(Buttons):
    def SetOptions(self,OptList):
        self.vars=[]
        for value in OptList:
            #print('--->',value)
            var= StringVar()
            self.col=self.col+1
            Checkbutton(self,
                        text=value,
                        variable=var, onvalue=value, offvalue='').grid(row=self.row, column=self.col, sticky=W)
            self.vars.append(var)

    def report(self):
        # combine for and if 
        # NOTE: when nothing selected , var.get is empty (isspace == False)
        varList = (var for var in self.vars if var.get())
        for var in varList:
            print('*',var.get(),'*',len(var.get()))   # current toggle settings: 1 or 0
        print()

    def showcmd(self):
        # select none empty item
        # without list() , error: TypeError: 'generator' object is not subscriptable
        varList = list(var for var in self.vars if var.get())
        if len(varList) == 0:
            print('Empty varList, must select ONE !')
            return

        self.cmdline,restvars = self.name+varList[0].get(),varList[1:]  
        for var in restvars:
            self.cmdline += self.sep+var.get()
        if(dbg):
            print(self.cmdline)
        return self.cmdline

if __name__ == '__main__': 
    root=Tk()
    # Items for Checkbutton 
    MBtn(root,picks=DictTest,rowNum=0)
    MBtn(root,picks=DictSuites,rowNum=1)

    root.mainloop()
