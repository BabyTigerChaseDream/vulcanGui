#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    Checkbutton for os/gpu selection
"""

from tkinter import *
from DicCmdParent import *

dbg = False

#TODO : make picks be able to parse "list array: *picklist"
pickOS = ['u16','win7','unknown']
OSname = "--target-os"
DictOS= {
        OSname:pickOS,
        }

pickGPU = ['v40','t100','no']
GPUname = "--target-gpu"

DictGPU= {
        GPUname:pickGPU,
        }

class CheckBtn(Buttons):
    def SetOptions(self,OptList):
        self.var= StringVar()
        self.var.set(OptList[0])

        for value in OptList:
            self.col=self.col+1
            Radiobutton(self,
                        text=value,
                        value=value,
                        variable=self.var).grid(row=self.row, column=self.col, sticky=W)            
    # assign target-os to vulcan cmdnline here
    def report(self):
        print(self.var.get(), end=' ')   # current toggle settings: 1 or 0
        print()
    # Class DicChdRadio suports single option only 
    # no need to use "delimiter" 
    def showcmd(self):
        self.cmdline = self.name + self.var.get()  
        if(dbg):
            print(self.cmdline)
        return (self.cmdline)

if __name__ == '__main__': 
    root=Tk()
    # Items for Checkbutton 
    CheckBtn(root,picks=DictOS,rowNum=0)
    CheckBtn(root,picks=DictGPU,rowNum=1)

    root.mainloop()
