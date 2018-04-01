#!/usr/bin/python3

"""
add common edit tools to ScrolledText by inheritance;
composition (embedding) would work just as well here;
this is not robust!--see PyEdit for a feature superset;
"""

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.filedialog   import asksaveasfilename
from tkinter.scrolledtext import ScrolledText

#class TextEditor(Frame):                     # see PyEdit for more
class TextEditor():                     # see PyEdit for more
    def __init__(self, parent=None):
        # TODO: 1226 why This can generate independent window ?
        #frm=Toplevel(Frame.__init__(self, parent))
        frm=Toplevel()
        # TODO : assign title based on cmdline tag 
        frm.title('New Text')
        # TODO , how to make button and Text in a better Layout format ?
        #        grid() param to learn 
        Button(frm, text='Save',  command=self.onSave).grid(row=0,column=0)
        Button(frm, text='Cut',   command=self.onCut).grid(row=0,column=1)
        Button(frm, text='Paste', command=self.onPaste).grid(row=0,column=2)
        Button(frm, text='Find',  command=self.onFind).grid(row=0,column=3)
        self.text = ScrolledText(frm)
        self.text.grid(row=1,columnspan=4)

        #Button(self, text='Save',  command=self.onSave).grid()
        #Button(self, text='Cut',   command=self.onCut).grid()
        #Button(self, text='Paste', command=self.onPaste).grid()
        #Button(self, text='Find',  command=self.onFind).grid()
        #self.text = ScrolledText(self)

    def gettext(self):                                   # returns a string
        return self.text.get('1.0', END+'-1c')           # first through last

    def onSave(self):
        filename = asksaveasfilename()
        #print(filename)
        if filename:
            alltext = self.gettext()                      # first through last
            open(filename, 'w').write(alltext)            # store text in file

    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)         # error if no select
        self.text.delete(SEL_FIRST, SEL_LAST)             # should wrap in try
        self.text.clipboard_clear()
        self.text.clipboard_append(text)

    def onPaste(self):                                    # add clipboard text
        try:
            text = self.text.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass                                          # not to be pasted

    def onFind(self):
        target = askstring('SimpleEditor', 'Search String?')
        if target:
            where = self.text.search(target, INSERT, END)  # from insert cursor
            if where:                                      # returns an index
                print(where)
                pastit = where + ('+%dc' % len(target))    # index past target
               #self.text.tag_remove(SEL, '1.0', END)      # remove selection
                self.text.tag_add(SEL, where, pastit)      # select found target
                self.text.mark_set(INSERT, pastit)         # set insert mark
                self.text.see(INSERT)                      # scroll display
                self.text.focus()                          # select text widget

if __name__ == '__main__':
    root=Tk()
    TextEditor()                    
    root.mainloop()
