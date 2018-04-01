#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    Checkbutton for os/gpu selection
"""

from tkinter import *
#from osTable import oslist
#from quitter import Quitter

#TODO : make picks be able to parse "list array: *picklist"
pickOS = ['u16','win7','unknown']
OSname = "target OS"
DictOS= {
        OSname:pickOS,
        }

pickGPU = ['v40','t100','no']
GPUname = "target GPU"

DictGPU= {
        GPUname:pickGPU,
        }

class TargetItem(Frame):
    # must declare outside of any method 
    row=0 
    col=0 
    def __init__(self, parent=None, text='NULL',picks={},rowNum=0,colNum=0):
        Frame.__init__(self, parent)#=None)
        # TODO: 2 ways to get key from dict contains only one pair
        self.name = next(iter(picks))
        # self.name = list(picks.keys())[0] 
        print('***** ')
        print(self.name)
        print(' *****')

        self.grid()
        self.row=rowNum
        self.col=colNum

        print('iter key:',self.name)
        print()
        Label(self, text=self.name).grid(row=self.row, column=self.col)

        self.SetOptions(picks[self.name])
        #for valTarget in picks[self.name]:
        #    var= StringVar()
        #    self.col=self.col+1
        #    Checkbutton(self,
        #                text=valTarget,
        #                variable=var, onvalue=valTarget, offvalue='').grid(row=self.row, column=self.col)
        #    self.vars.append(var)

        self.col=self.col+1
        Button(self,text='Get '+ self.name, command=lambda :self.getval()).grid(row=self.row,column=self.col)

        # TODO: adjust row somewhere outside 
        #self.row=self.row+1
        # needs set col back to 0 , start of the row 
        #self.col=0

    def SetOptions(self,OptList):
        self.vars=[] 
        for valTarget in OptList:
            var= StringVar()
            self.col=self.col+1
            Checkbutton(self,
                        text=valTarget,
                        variable=var, onvalue=valTarget, offvalue='').grid(row=self.row, column=self.col)
            self.vars.append(var)

    def getval(self):
        for var in self.vars:
            print(var.get(), end=' ')   # current toggle settings: 1 or 0
        print()
    
    #def tools(self):
    #    self.col=self.col+1
    #    Button(self,text='Get '+ self.name, command=lambda :self.getval()).grid(row=self.row,column=self.col)

if __name__ == '__main__': 
    root=Tk()
    # Items for Checkbutton 
    TargetItem(root,picks=DictOS,rowNum=0)
    TargetItem(root,picks=DictGPU,rowNum=1)

    #TargetItem(root,text='target GPU >>',picks=pickGPU,rowNum=1)
    root.mainloop()
