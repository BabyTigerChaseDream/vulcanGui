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

class ThreadCmd():
    def __init__(self, log=None ,MyText=None, cmdline='',OutData=[]):
        self.cmdline=cmdline
        # data queue to store instance's data 
        self.dataQueue =queue.Queue()
        #self.text = ScrolledText()              # save widget as state
        self.log = log
        self.text=MyText
        #self.text.grid()
        self.OutData = OutData
    
        #mytag = 'tag:%s' % i
        mytag = 'tag: per GUI pls' 
        #self.threadAction()
        #self.threadChecker(self.text,self.dataQueue)      # start thread check loop

        threading.Thread(target=self.threadAction, args=()).start()
        # if use "while True" must set daemon to True so that main thread end, checker end also 
        CheckerThd = threading.Thread(target=self.threadChecker, args=(self.text,self.dataQueue)).start()
        #CheckerThd.daemon=True
        #CheckerThd.start()

    def threadAction(self):
        proc = sub.Popen(self.cmdline, bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        
        self.dataQueue.put(self.cmdline)
        for line in proc.stdout:
            self.dataQueue.put(line.decode("utf-8")) 
        proc.stdout.clone()

        # TODO How to handle err/out elegantly
        self.dataQueue.put(' ----- Check Error ----- ')
        for err in proc.stderr:
            self.dataQueue.put(err.decode("utf-8")) 
        proc.stderr.close()

        #if proc.poll() is not None:
        #    self.SaveText()

# Use while True --> daemon ?
# works but no GOOD 
#    def threadChecker(self, TextWin, dataQueue, delayMsecs=500):       # 10x/sec, 1/timer
#        while True:
#            try:                                                
#                data = dataQueue.get(block=False)
#            except queue.Empty:
#                pass 
#            else:
#                TextWin.insert('end', '%s\n' % str(data))
#                TextWin.see('end')
#        
#            #TextWin.after(delayMsecs,                                  # reset timer event
#            #    lambda: self.threadChecker(TextWin, dataQueue, delayMsecs)) # back to event loop

# [Rel] Use after- works in parallel form  
    def threadChecker(self, TextWin, dataQueue, delayMsecs=200):       # 10x/sec, 1/timer
        try:                                                
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass 
        else:
            TextWin.text.insert('end', '%s\n' % str(data))
            TextWin.text.see('end')

            print('Raw string' , str(data).endswith('\n'))

            if 'http' in str(data):
                urlAddr=str(data).split()[3]
                print('*****',urlAddr)
                webbrowser.open(urlAddr,new=1)
            elif (str(data).split('\n'))[0].isdigit():
                print('Got it',str(data))
                self.OutData.append(str(data))

        TextWin.text.after(delayMsecs,                                  
            lambda: self.threadChecker(TextWin, dataQueue, delayMsecs)) 

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

