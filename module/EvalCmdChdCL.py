#!/usr/bin/python3
'''
instance of " --product " parameter 
'''

from tkinter import *
from EvalCmdParent import *

#import table from other config files
dbg=False 
class CustomCLEntry(LabelEntBtn):
    # Set Widget option/geograph   
    def CustomizedButton(self):
        self.col=self.col+1
        Button(self, text='State',command=lambda: self.report()).grid(row=self.row,column=self.col) 

        self.col=self.col+1
        Button(self,text='cmdline', command=lambda:self.showcmd()).grid(row=self.row,column=self.col)
        # default set CL to tot
        self.var.set('tot')
    # assign target-os to vulcan cmdline here
    def report(self):
        print(self.var.get())

    def showcmd(self):
        # note : CL followed "-" NOT "="
        self.cmdline = self.name  
        # TODO: add something to check var type ?
        self.cmdline += str(self.var.get())
        if(dbg):
            print(self.cmdline)
        return (self.cmdline)
        
if __name__ == '__main__': 
    root=Tk()
    CustomCLEntry(root,text=' --cl',VarType='Int',rowNum=0)
    root.mainloop()
