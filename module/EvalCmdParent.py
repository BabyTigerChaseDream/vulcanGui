#!/usr/bin/python3

"""
Parent Class for "Button" (CheckButton/RadioButton)
"""

from tkinter import *
#import table from other config files
dbg=False
class LabelEntBtn(Frame):
    # must declare outside of any method 
    row=0 
    col=0 
    
    """"""""""""""""""""""""""""""""""""""""""""""
       VarType: used to call IntVar()/StringVar()
                call func from a "string name"
       represent a single widget   

    """""""""""""""""""""""""""""""""""""""""""""
    def __init__(self, parent=None, text='Unknown',VarType='NULL',delimiter='NULL',rowNum=0,colNum=0):
        Frame.__init__(self, parent)
        self.name = text 
        self.delimiter=delimiter
        print('Init LableEntBtn:',self.name)
        print()

        self.grid()
        self.row=rowNum
        self.col=colNum

        # below should be "StringVar()" or "IntVar()"
        self.var=eval(VarType+'Var()')

        Label(self, text=self.name, relief=RIDGE).grid(row=self.row, column=self.col)
        self.col=self.col+1
        Entry(self, relief=SUNKEN, textvariable=self.var).grid(row=self.row, column=self.col)
        
        self.CustomizedButton()

    # Set Widget option/geograph   
    def CustomizedButton(self,delimiter):
        raise NotImplementedError

    # assign target-os to vulcan cmdline here
    def report(self):
        raise NotImplementedError

    def showcmd(self):
        raise NotImplementedError

