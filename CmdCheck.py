#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    Checkbutton for os/gpu selection
"""

from tkinter import *
#from osTable import oslist
#from quitter import Quitter

#TODO : make picks be able to parse "list array: *picklist"
picklist = ['u16','win7','unknown']
name = "target OS"
#pickGPU = ['v40','t100','no']

class TargetItem(Frame):
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
        for key in picks:
            self.col=self.col+1
            Radiobutton(self,
                        text=key,
                        value=key,
                        variable=self.var).grid(row=self.row, column=self.col)

        self.col=self.col+1
        Button(self,text='State '+text, command=self.report).grid(row=self.row,column=self.col)

    # assign target-os to vulcan cmdnline here
    def report(self):
        print(self.var.get(), end=' ')   # current toggle settings: 1 or 0
        print()

    def tools(self):
        #frm = Frame(self)
        #frm.grid()#pack(side=RIGHT)
        print(self.row)
        Button(self,text='StateOS', command=self.report).grid(row=self.row,column=self.col)
        #Quitter(frm).grid(row=2,column=2)

if __name__ == '__main__': 
    root=Tk()
    # Items for Checkbutton 
    TargetItem(root,text=name,picks=picklist,rowNum=0)

    #TargetItem(root,text='target OS >>',picks=pickOS,rowNum=0)
    #TargetItem(root,text='target GPU >>',picks=pickGPU,rowNum=1)
    root.mainloop()
