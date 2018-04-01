#!/usr/bin/python3

"""
Parent Class for "Button" (CheckButton/RadioButton)
"""

from tkinter import *

from tkinter.filedialog import askopenfilename 
from tkinter.simpledialog import askinteger       

from EvalCmdParent import *

#import table from other config files
dbg=False
class ProdFile(LabelEntBtn):
    # Set Widget option/geograph   
    def CustomizedButton(self):
        self.col=self.col+1
        Button(self, text='browse...',command=lambda: self.var.set(askopenfilename() or self.var.get())).grid(row=self.row,column=2)
        self.col=self.col+1
        Button(self, text='State', command=lambda:self.report()).grid(row=self.row,column=self.col) 

        self.col=self.col+1
        Button(self,text='cmdline', command=lambda:self.showcmd()).grid(row=self.row,column=self.col)
    # assign target-os to vulcan cmdline here
    def report(self):
        print(self.var.get())

    def showcmd(self):
        self.cmdline = self.name+'=' # NULL string 
        cmdunit=' '+self.var.get()
        self.cmdline += cmdunit
        if(dbg):
            print(self.cmdline)
        return (self.cmdline)
        
if __name__ == '__main__': 
    root=Tk()
    ProdFile(root,text='--product',VarType='String',rowNum=0)
    root.mainloop()
