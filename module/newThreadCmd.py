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

class newThreadCmd():
    def __init__(self, log=None ,MyText=None, cmdline='', handler='', OutData=None):
        self.cmdline=cmdline
        # data queue to store instance's data 
        self.dataQueue =queue.Queue()
        self.text=MyText
        self.OutData = OutData

        self.handler=eval('self.'+handler+'handler')
        #mytag = 'tag:%s' % i
        mytag = 'tag: per GUI pls' 

        threading.Thread(target=self.threadAction, args=()).start()
        # if use "while True" must set daemon to True so that main thread end, checker end also 
        CheckerThd = threading.Thread(target=self.threadChecker, args=(self.text,self.dataQueue)).start()
    def threadAction(self):
        proc = sub.Popen(self.cmdline, bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        
        self.dataQueue.put(self.cmdline)
        for line in proc.stdout:
            self.dataQueue.put(line.decode("utf-8")) 
        proc.stdout.close()

        # TODO How to handle err/out elegantly
        self.dataQueue.put(' ----- Check Error ----- ')
        for err in proc.stderr:
            self.dataQueue.put(err.decode("utf-8")) 
        proc.stderr.close()

# [Rel] Use after- works in parallel form  
    def threadChecker(self, TextWin, dataQueue, delayMsecs=200):       # 10x/sec, 1/timer
        try:                                                
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass 
        else:
            TextWin.text.insert('end', '%s\n' % str(data))
            TextWin.text.see('end')
            
            self.handler(str(data))
            #print('Raw string' , str(data).endswith('\n'))

            #if 'http' in str(data):
            #    urlAddr=str(data).split()[3]
            #    print('*****',urlAddr)
            #    webbrowser.open(urlAddr,new=1)
            #elif (str(data).split('\n'))[0].isdigit():
            #    print('Got it',str(data))
            #    self.OutData.append(str(data))

        TextWin.text.after(delayMsecs,                                  
            lambda: self.threadChecker(TextWin, dataQueue, delayMsecs)) 

    # handler for string(data)
    def Webhandler(self,stringIn):
        if 'http' in stringIn:
            url = stringIn.split()[3]
            print('*****',urlAddr)
            webbrowser.open(urlAddr,new=1)
        print('Quit Webhandler')    
    
    def CLhandler(self,stringIn):
        if stringIn.split('\n')[0].isdigit():
            print('Got digit',stringIn)
            self.OutData.append(stringIn)

if __name__ == '__main__': 
    MyText = ScrolledText(Toplevel())
    myCmd = newThreadCmd(MyText=MyText, cmdline='./msgloop.py').text.mainloop()

