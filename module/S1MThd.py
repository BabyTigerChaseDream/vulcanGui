#!/usr/bin/python3
"""
4 demo class components (subframes) on one window;
there are 5 Quitter buttons on this one window too, and each kills entire gui;
GUIs can be reused as frames in container, independent windows, or processes;

# Sample command : 
vulcan -v --eris --trace 3 --product=//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r91_r387.vlcp 
--target-arch x86_64 --target-os Ubuntu16_04,Ubuntu14_04,RHEL7_3 --target-revision=cl-tot --apply-change 23270662 
--build --testsuite cudnn_level_tests_L4 --user jiag --tag bugxxx 
--target-gpu gv100sxm2,k40c,p4,gv100titan,gv100sxm2-dgxs,gp104mxm

"""

# sys lib 
from tkinter import *
from tkinter.filedialog import askopenfilename 
from tkinter.simpledialog import askinteger       

# Self define 
from DicChdMBtn import *
from DicChdRadio import *
from EvalCmdChdProd import *
from EvalCmdChdCL import *
from EvalCmdChdTag import *
from DicCmdOptmenu import *
from DicCmdFindRevMenu import *

import subprocess as sub

# dry-run cmd
#from tkinter.scrolledtext import ScrolledText
import queue, threading #_thread

from ThreadCmd import *

# scrolledText
from TextEditor import *

### TODO 20180121 ###
from threading import Thread, Event
import time
"""""""""""""""""""""""""""""""""""""""""""""""""""""
             All Button configuration List  
""""""""""""""""""""""""""""""""""""""""""""""""""""" 

""""""""""""""""""""""""""" 
single select Options : 
    -target-arch 
""""""""""""""""""""""""""" 
pickArch = ['x86_64','ppc64le']
Archname = " --target-arch " # must be a " " blank follow as delimiter
DictArch= {
            Archname:pickArch,
        }

"""""""""""""""""""""""""""""""""""""""""""""""""""""
             Gloable function/param  
""""""""""""""""""""""""""""""""""""""""""""""""""""" 

""" 
    Regression manual submit cmdline  
""" 
#TODO: better data structure ?

cmdElement = []
vulCmd ='echo vulcan -v --eris --db --user jiag --dry-run '
vulcmdline = './msgloop.py'
shCmdline ='./msgloop.py'


def showcmd(cmdElement):
    global vulCmd, cmdline
    vulCmdline = vulCmd
    for ele in cmdElement:
        vulCmdline +=  ele.showcmd()
    print('=== ',vulCmdline,' ===')
    # vulCmd = ''
    cmdline = vulCmdline
    vulCmdline = ''
    return cmdline 

"""""""""""""""""""""""""""
   Add for Find-revisions 
"""""""""""""""""""""""""""
FindCmd ='echo vulcan --find-revisions '
findrevcmdline = ''
"""""""""""""""""""""""""""""""""
Option menu : 
    - find-rev's configuartion files
""""""""""""""""""""""""""""""""" 
# blank below in the "components" is a must
components = [' cudnn ',' [cudnn ',' ]cudnn ']
name = ' --revision-range '
RevDict = {
    name:components
}

########################################
# Data Structure to share among thread #
########################################

global FindRevQueue 
FindRevQueue = queue.Queue()
global CLQueue 
CLQueue = queue.Queue()

# flags to tell if a threads completed
_sentinel = object()

### Find Rev cmdline ### 
def GetFindRevCmd(RevRange):
    global FindCmd
    cmdline = FindCmd + RevRange.showcmd()
    print('=== ',cmdline,' ===')
    return cmdline

def RunFindRevCmd(FindRevQueue,CLQueue,cmdline,cmdfinish_evt):
    proc = sub.Popen(cmdline, bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    
    FindRevQueue.put(cmdline)
    for line in proc.stdout:
        FindRevQueue.put(line.decode("utf-8")) 
        if line.decode("utf-8").split('\n')[0].isdigit():
            CLQueue.put(line.decode("utf-8"))
    proc.stdout.close()

    # TODO How to handle err/out elegantly
    FindRevQueue.put(' ----- Check Error ----- ')
    for err in proc.stderr:
        FindRevQueue.put(err.decode("utf-8")) 
    proc.stderr.close()

    # tell if a thread completes
    FindRevQueue.put(_sentinel)
    # communicate among threads
    cmdfinish_evt.set()

# DisWidget must be Text GUI
def ThreadsChecker(DisWidget, dataQueue, delayMsecs=200):
    if dataQueue.empty():
        print(' Empty queue ! ')
        pass 
    else:
        data = dataQueue.get(block=False)
        if data is _sentinel:
            print('Find Rev Checker Done !!!')
            return 
        else:
            print(' Get Data %s ! ' % str(data))
            DisWidget.text.insert('end', '%s\n' % str(data))
            DisWidget.text.see('end')
    DisWidget.text.after(delayMsecs,                                  
        lambda : ThreadsChecker(DisWidget, dataQueue, delayMsecs)) 

### Tests cmdline ### 
def GetTestsCmd(CmdWidgets):
    global vulCmd
    cmdline = vulCmd
    for val in CmdWidgets.values():
        cmdline += val.showcmd()
    print('=== ',cmdline,' ===')
    return cmdline

### Generate cmdline lists
def GenerateCmdList(CLQueue, cmdtemplate):
    # TODO expression here ?
    cmdlist = []
    while True:
        try:
            cmdlist.append(cmdtemplate.replace('tot',CLQueue.get(block=False)))
        except queue.Empty:
            break

    return cmdlist

def RunTestsCmd(TestsOutQueue,cmdline):
    # assign new cmdline for debug 
    cmdline = "./msgloop.py "

    proc = sub.Popen(cmdline, bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    
    TestsOutQueue.put(cmdline)
    for line in proc.stdout:
        print(line)
        TestsOutQueue.put(line.decode("utf-8")) 
        if 'http' in line.decode("utf-8"):
            urlAddr= line.decode("utf-8").split()[3]
            print('*****',urlAddr)
            webbrowser.open(urlAddr,new=1)
            
    proc.stdout.close()

    # TODO How to handle err/out elegantly
    TestsOutQueue.put(' ----- Check Error ----- ')
    for err in proc.stderr:
        TestsOutQueue.put(err.decode("utf-8")) 
    proc.stderr.close()

    # tell if a thread completes
    TestsOutQueue.put(_sentinel)

##### Func main definition #####

def MainCmdline(CmdWidgetDict):
    global CLQueue, FindRevQueue

    # lists of cmd for Find Rev
    vulcmdlists= []
    
    # Shared data structure: Event/Queue 
    findcr_evt_completed = Event()

    # 1. check if needs to find CL first  
    if False: 
        pass
    ### if CmdWidgetDict.get('FindRev'):
    ###    print('In FindRev ****** ')
    ###    RevRange = CmdWidgetDict.get('FindRev')
    ###    findrevcmdline = GetFindRevCmd(RevRange)
    ###    # start Find CL thread 
    ###    Thread(target=RunFindRevCmd, 
    ###            args=(FindRevQueue, CLQueue, findrevcmdline, findcr_evt_completed)).start() 
    ###    # start Checker thread for Find CL
    ###    Thread(target=ThreadsChecker, 
    ###            args=(TextEditor(), FindRevQueue).start()) 
    else:
        # TODO no clear() in queue
        #CLQueue.clear()
        findcr_evt_completed.set()

    # done handler "FindRev" item , remove it, it is not test cmd param 
    ### del CmdWidgetDict['FindRev']

    # 2. start collect test cmd
    vulcmdline = GetTestsCmd(CmdWidgetDict)
    # 3. check if CLQueue empty or not
    # wait till FindRev thread completes
    findcr_evt_completed.wait()
    # TODO: check queue.Empty or     
    #if CLQueue.Empty:
    if queue.Empty:
        print('CL Queue Empty,Run single cmdline')
        vulcmdlists.append(vulcmdline)
    else:
        print('Run multiple cmdline')
        vulcmdlists = GenerateCmdList(CLQueue,vulcmdline)

    # 4. exec cmdlineLists
    for cmdline in vulcmdlists:
        QueuePair=queue.Queue()
        # start Tests thread 
        Thread(target=RunTestsCmd, 
                args=(QueuePair,cmdline)).start()
        time.sleep(5)
        # checker for this cmd
        Thread(target=ThreadsChecker, 
               args=(TextEditor(),QueuePair)).start() 

        
""""""""""""""""""""
"   main() start   "
""""""""""""""""""""

root = Tk() # make explicit root first
root.title('vulcan cmd GUI')
# ALL GUI widget put into here 
WidgetAll={}
startRow = 1
#cmdElement.append(CheckBtn(root,picks=DictArch,rowNum=startRow))
WidgetAll.update({'Arch':CheckBtn(root,picks=DictArch,rowNum=startRow)})

# act as a main thread for cli
Button(root,text='Run', command=lambda : MainCmdline(WidgetAll)).grid(row=startRow)

root.mainloop()

