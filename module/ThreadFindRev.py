#!/usr/bin/python3

# tests thread callback queue, but uses class bound methods for action and callbacks
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog   import *

import threading              # run with GUI blocking
import queue, sys, time
import subprocess as sub
import webbrowser 

# TODO: each ThreadCmd should has it's own "call-back" func to take action to different output 

class ThreadFindRev(ThreadCmd):
    def __init__(self, log=None ,MyText=None, cmdline=''):
        self.cmdline=cmdline
        # data queue to store instance's data 
        self.dataQueue =queue.Queue()
        #self.text = ScrolledText()              # save widget as state
        self.log = log
        self.text=MyText
        #self.text.grid()
    
        #mytag = 'tag:%s' % i
        mytag = 'tag: per GUI pls' 
        #self.threadAction()
        #self.threadChecker(self.text,self.dataQueue)      # start thread check loop

        threading.Thread(target=self.threadAction, args=()).start()
        # if use "while True" must set daemon to True so that main thread end, checker end also 
        CheckerThd = threading.Thread(target=self.threadChecker, args=(self.text,self.dataQueue)).start()
        #CheckerThd.daemon=True
        #CheckerThd.start()

# [Rel] Use after- works in parallel form  
    def threadChecker(self, TextWin, dataQueue, delayMsecs=200):       # 10x/sec, 1/timer
        try:                                                
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass 
        else:
            TextWin.text.insert('end', '%s\n' % str(data))
            TextWin.text.see('end')
            # TODO : needs improve, should be 
            if 'http' in str(data):
                urlAddr=str(data).split()[3]
                print('*****',urlAddr)
                webbrowser.open(urlAddr,new=1)
                
            # Detect if http generated, if so , open in webbrowser 
            #if 'http' in str(data):
            #    for links in str(data).split():
            #     if 'http' in links:
            #        print('Got https')
            #        urlAddr = links
            #        webbrowser.open(urlAddr,new=1)
            #        break

        TextWin.text.after(delayMsecs,                                  # reset timer event
            lambda: self.threadChecker(TextWin, dataQueue, delayMsecs)) # back to event loop

    # TODO SaveText must run after sub completed 
    # TODO Also must wait for threadChecker finish "update" Queue
    #      because text data is from Queue 
    #def SaveText(self):
    #    if self.log:
    #        pass
    #    else:
    #        self.log = asksaveasfilename()

    #    print('Save Text to:',self.log)

    #    open(self.log, 'w').write(self.text.get('1.0', END+'-1c'))
    #    #alltexts = self.text.get('1.0', END+'-1c')
    #    #print('-------------------------------')
    #    #with open(self.log,'w') as fd:
    #    #    for line in alltexts:
    #    #        print(line)
    #    #        fd.write(line)

if __name__ == '__main__': 
    MyText = ScrolledText(Toplevel())
    myCmd = ThreadCmd(MyText=MyText, cmdline='./msgloop.py').text.mainloop()

