#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    Checkbutton for os/gpu selection
"""

from tkinter import *
from tkinter.filedialog import askopenfilename 
from tkinter.simpledialog import askinteger
#from quitter import Quitter
#pickSuite= ['layer','sample','none']
#suitename = 'Suite'
dbg = False
pickProd= {'cudnn':'A','cuda':'B','tensorRT':'C'}
configname = '--product='

DictPick = {
#        suitename:pickSuite,
        configname:pickProd,
        }

class CmdOptmenu(Frame):
    # must declare outside of any method 
    row=0 
    col=0 
    def __init__(self, parent=None, text='NULL',picks={},rowNum=0,colNum=0):
        Frame.__init__(self, parent)#=None)
        self.picks=picks 
        self.name = next(iter(self.picks))
        self.grid()
        #self.tools()
        self.row=rowNum
        self.col=colNum

        # pick up the first self.config in dict
        #self.config=next(iter(self.picks))

        # store configuration file , dict's key part 
        self.var= StringVar()
        # store configuration file , dict's value part 
        self.fval= StringVar()
        # first key in 
        #fkey = next(iter(self.picks[self.config]))
        fkey = next(iter(self.picks[self.name]))
        # method-1
        #self.fval.set(self.picks[self.name][fkey])
        # method-2
        self.fval.set(self.picks[self.name].get(fkey))

        Label(self, text=self.name, relief=RIDGE).grid(row=self.row, column=self.col, sticky=W)

        # pick up the first self.config in dict
        self.var.set(next(iter(self.picks[self.name])))

        self.col=self.col+1
        OptionMenu(self, self.var, *self.picks[self.name].keys(), command=lambda inx=self.var.get() : self.setval(inx)).grid(row=self.row, column=self.col, sticky=W)

        #self.row=self.row+1
        #self.col=colNum

        self.col=self.col+1
        Entry(self, relief=SUNKEN, textvariable=self.fval).grid(row=self.row, column=self.col, sticky=W)

        self.col=self.col+1
        Button(self, text='browse...',command=lambda: self.fval.set(askopenfilename() or self.fval.get())).grid(row=self.row,column=self.col, sticky=W)
        self.col=self.col+1
        Button(self,text=' State ', command=lambda:self.showcmd()).grid(row=self.row,column=self.col, sticky=W)

    # assign target-os to vulcan cmdnline here
    def showcmd(self):
        self.cmdline = self.name + self.fval.get()
        print(self.cmdline)   # current toggle settings: 1 or 0
        #print()
        if(dbg):
            print(self.cmdline)
        return (self.cmdline)

    def setval(self,inx):
        self.fval.set(self.picks[self.name][inx])
        print(self.picks[self.name][inx], end=' ')   # current toggle settings: 1 or 0
        print()

if __name__ == '__main__': 
    root=Tk()
    # Items for Optionmenu 
    CmdOptmenu(root,picks=DictPick,rowNum=0)
    #CmdOptmenua(root,text='test suites >>',picks=picklist,rowNum=0)
    #CmdOptmenua(root,text='test list >>',picks=pickTests,rowNum=1)
    root.mainloop()
