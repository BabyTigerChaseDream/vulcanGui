#!/usr/bin/python3
import sys

from tkinter import *
import subprocess as sub

# use Prog Py4 module
from simpleedit import *

root = Tk()
#text = Text(root)
#text.pack()

# use stdout=sub.PIPE
p1 = sub.Popen(['ps','-aux'],stdout=sub.PIPE,stderr=sub.PIPE)
output, errors = p1.communicate()
#SimpleEditor(parent=root,file=output.decode()).mainloop()
SimpleEditor(parent=Toplevel(),file=output.decode())

#TODO: use stdout
#SimpleEditor(parent=root,file=sys.stdout).mainloop()
#p1 = sub.Popen(['ps','-aux'])#,stdout=sub.PIPE,stderr=sub.PIPE)
#text.insert(END, output)

# use stdout=sub.PIPE
p2 = sub.Popen(['pwd'],stdout=sub.PIPE,stderr=sub.PIPE)
output2, errors2 = p2.communicate()
SimpleEditor(parent=Toplevel(),file=output2.decode())

root.mainloop()
