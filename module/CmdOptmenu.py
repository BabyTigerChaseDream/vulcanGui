#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    Checkbutton for os/gpu selection
"""

from tkinter import *
#from quitter import Quitter
picklist= ['layer','sample','none']
name = 'Test Suite'
#pickTests= ['vlcp','vlct','vlcc']
dbg= False
class Optmenu(Frame):
    # must declare outside of any method 
    row=0 
    col=0 
    def __init__(self, parent=None, text='NULL',picks=[],rowNum=0,colNum=0):
        Frame.__init__(self, parent)#=None)
        self.grid()
        #self.tools()
        self.row=rowNum
        self.col=colNum
        Label(self, text=text).grid(row=self.row, column=self.col)

        self.var= StringVar()
        self.var.set(picks[0])

        #for key in picks:
        self.col=self.col+1
        OptionMenu(self, self.var, *picks).grid(row=self.row, column=self.col)

        self.col=self.col+1
        Button(self,text='State '+text, command=self.report).grid(row=self.row,column=self.col)

    # assign target-os to vulcan cmdline here
    def report(self):
        print(self.var.get(), end=' ')   # current toggle settings: 1 or 0
        print()

    def showcmd(self):
        # note : CL followed "-" NOT "="
        #self.cmdline = self.name+self.delimiter  
        self.cmdline = self.name

        # TODO: add something to check var type ?
        self.cmdline += str(self.var.get())
        if(dbg):
            print(self.cmdline)
        return (self.cmdline)

if __name__ == '__main__': 
    root=Tk()
    # Items for Optionmenu 
    Optmenu(root,text=name,picks=picklist,rowNum=0)
    root.mainloop()
