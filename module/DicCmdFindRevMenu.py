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
components = ['cudnn','[cudnn',']cudnn']
name = ' --revision-range '
RevDict = {
    name:components
}

class DicCmdFindRevMenu(Frame):
    # must declare outside of any method 
    row=0 
    col=0 
    def __init__(self, parent=None, text='NULL',picks={},rowNum=0,colNum=0):
        Frame.__init__(self, parent)
        self.picks=picks 
        self.name = next(iter(self.picks))
        self.grid()
        #self.tools()
        self.row=rowNum
        self.col=colNum

        # store configuration file , dict's key part 
        self.component= StringVar()
        self.range= StringVar()

        Label(self, text=self.name, relief=RIDGE).grid(row=self.row, column=self.col, sticky=W)

        # pick up the first self.config in dict
        self.component.set(self.picks[self.name][0])

        self.col=self.col+1
        Entry(self, relief=SUNKEN, textvariable=self.range).grid(row=self.row, column=self.col, sticky=W)

        self.col=self.col+1
        OptionMenu(self, self.component, *self.picks[self.name]).grid(row=self.row, column=self.col, sticky=W)

        self.col=self.col+1
        Button(self,text=' State ', command=lambda:self.showcmd()).grid(row=self.row,column=self.col, sticky=W)

    # assign target-os to vulcan cmdnline here
    def showcmd(self):
        self.cmdline = self.name + self.range.get() + self.component.get()
        print(self.cmdline)   # current toggle settings: 1 or 0
        #print()
        if(dbg):
            print(self.cmdline)
        return (self.cmdline)

if __name__ == '__main__': 
#TODO : not tested yet 
    root=Tk()
    # Items for Optionmenu 
    CmdOptmenu(root,picks=DictPick,rowNum=0)
    #CmdOptmenua(root,text='test suites >>',picks=picklist,rowNum=0)
    #CmdOptmenua(root,text='test list >>',picks=pickTests,rowNum=1)
    root.mainloop()
