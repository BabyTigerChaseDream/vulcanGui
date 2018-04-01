#!/usr/bin/python3

"""
Parent Class for "Button" (CheckButton/RadioButton)
"""

from tkinter import *
#import table from other config files
dbg=True
class Buttons(Frame):
    # must declare outside of any method 
    row=0 
    col=0 
    
    """""""""""""""""""""""""""""""""""
       picks{} is a single entry dict 
       represent a single widget   

       child: Radio --> RadioButton
              Check --> CheckButton
    """""""""""""""""""""""""""""""""""
    def __init__(self, parent=None, sep=',', text='Unknown-Button',picks={},rowNum=0,colNum=0):
        Frame.__init__(self, parent)
        # TODO: 2 ways to get key from dict contains only one pair
        self.name = next(iter(picks))
        self.sep = sep
        # self.name = list(picks.keys())[0] 

        print('Init button:',self.name)
        print()

        self.grid()
        self.row=rowNum
        self.col=colNum

        #print('iter key:',self.name)
        #print()
        Label(self, text=self.name, relief=RIDGE).grid(row=self.row, column=self.col)
        
        self.SetOptions(picks[self.name])

        self.col=self.col+1
        Button(self,text='State', command=lambda:self.report()).grid(row=self.row,column=self.col)

        self.col=self.col+1
        Button(self,text='cmdline', command=lambda:self.showcmd()).grid(row=self.row,column=self.col)

    # Set Widget option/geograph   
    def SetOptions(self,OptList):
        raise NotImplementedError

    # assign target-os to vulcan cmdline here
    def report(self):
        raise NotImplementedError

    def showcmd(self):
        raise NotImplementedError

