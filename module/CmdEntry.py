#!/usr/bin/python3
"GUI for vulcan nightly regression task submission"
"""
    refer to formrows.py in PP4E 
"""
from tkinter import *
from tkinter.filedialog import askopenfilename 
from tkinter.simpledialog import askinteger       

if __name__ == '__main__': 
    root=Tk()
    # button to open configure file 
    cfg= StringVar()
    Label(root,text='Config file', relief=RIDGE).grid(row=0,column=0)
    Entry(root,relief=SUNKEN, textvariable=cfg).grid(row=0,column=1)
    Button(root, text='browse...',command=lambda: cfg.set(askopenfilename() or cfg.get())).grid(row=0,column=2)

    #entry to input CL number/interger  
    clNum= IntVar()
    Label(root,text='Change List', relief=RIDGE).grid(row=1,column=0)
    Entry(root,relief=SUNKEN, textvariable=clNum).grid(row=1,column=1)

    root.mainloop()
