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
dataQueue = queue.Queue() 

from ThreadCmd import *

# scrolledText
from TextEditor import *


"""""""""""""""""""""""""""""""""""""""""""""""""""""
             All Button configuration List  
""""""""""""""""""""""""""""""""""""""""""""""""""""" 

"""""""""""""""""""""""""""""""""
Option menu : 
    - select configuartion files
""""""""""""""""""""""""""""""""" 
pickProd= {'v7.1 cuda9.2 r396 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r92_r396.vlcp',
            'v7.1 cuda9.1 r390 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r91_r390.vlcp',
            'v7.1 cuda9.0 r384 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r90_r384.vlcp',
            'v7.1 cuda8.0 r375 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r80_r375.vlcp',
            # TODO : v7.1 weekly
            'cudnn cuda_a':'//sw/gpgpu/MachineLearning/cudnn/eris/cudnn_gpgpu_cuda_a.vlcp'}
              
configname = '--product=' # must be a "=" blank follow as delimiter
DictCfg = {
            configname:pickProd,
        }
""""""""""""""""""""""""""" 
single select Options : 
    -target-arch 
""""""""""""""""""""""""""" 
pickArch = ['x86_64','ppc64le']
Archname = " --target-arch " # must be a " " blank follow as delimiter
DictArch= {
            Archname:pickArch,
        }

""""""""""""""""""""""""""" 
multi-select Options : 
    -OS
    -GPU
""""""""""""""""""""""""""" 
pickOS = ['Ubuntu16_04','RHEL7_3','Windows10','Ubuntu14_04','Windows2012R2','Windows7','Mac10_13']
OSname = " --target-os " # must be a " " blank follow as delimiter
DictOS= {
            OSname:pickOS,
        }

pickGPU = ['gv100sxm2','gv100titan','v100','p4','gp102titanX','p40',
            'gp100sxm2','m4','m60','m40','gtx750ti','k80m','k40c','k5000']
GPUname = " --target-gpu " # must be a " " blank follow as delimiter
DictGPU= {
            GPUname:pickGPU,
        }

# multi-select OS/GPU 
pickTests= ['conv_sample','cudnn_layer_tests','cudnn_level_tests_L3',
            'cudnn_samples_mnist_tests','cudnn_samples_rnn_tests','cudnn_tests_MT']
Testname = " --testsuite " # must be a " " blank follow as delimiter
DictTest= {
            Testname:pickTests,
        }

"""""""""""""""""""""""""""""""""""""""""""""""""""""
             Gloable function/param  
""""""""""""""""""""""""""""""""""""""""""""""""""""" 

""" 
Regression manual submit cmdline  
""" 
#TODO: better data structure ?

cmdElement = []
#vulCmd ='vulcan -v --eris --db --user jiag --dry-run '
vulCmd ='vulcan -v --eris --db --user jiag '
cmdline = ''
shCmdline ='./msgloop.py'

#Get CL number
def showCL(num):
    print("CL num is :",num.get())

#Get CL number
def showfile(cfgFile):
    print("Filepath:",cfgFile.get())

# run all CLs cmdline , replace "tot" to CL num
def RUNAllCLs(cmdline,CLList):
    for data in CLList:
        print('===>Full cmd : ',cmdline.replace('tot',data))
        ThreadCmd(MyText=TextEditor(), cmdline=cmdline.replace('tot',data))
    

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

def producer(dataq):
    global shCmdline
    proc = sub.Popen(shCmdline,bufsize=1, shell=True,stdout=sub.PIPE)
    #for line in iter(out.readline, b''):
    for line in proc.stdout:
        dataq.put(line) 
    #out.close()
    proc.stdout.close()
def consumer(TextWin):
    try:
        print('... > ')
        data = dataQueue.get(block=False)
    except queue.Empty:
        pass
    else:
        TextWin.insert('end', '%s\n' % str(data))
        TextWin.see('end')
    TextWin.after(500, lambda: consumer(TextWin))
# thread - deamon consumer - auto exit
def threadconsumer(TextWin):
    while True:
        try:
            print('... > ')
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            TextWin.insert('end', '%s\n' % str(data))
            TextWin.see('end')

def runcmd():
    #global shCmdline
    # TODO: shell must be true ! to exec cmd
    TextWin = ScrolledText(Toplevel())
    TextWin.grid()
    #proc = sub.Popen(shCmdline,bufsize=1, shell=True,stdout=sub.PIPE)
    print('==> Cmdline:',shCmdline)
    #SimpleEditor(parent=Toplevel(),file=output.decode())
    #_thread.start_new_thread(producer, (proc.stdout,dataQueue))

    #threading.Thread(target=producer, args=(proc.stdout,dataQueue)).start()
    threading.Thread(target=producer, args=(dataQueue,)).start()

    Textthread=threading.Thread(target=consumer, args=(TextWin,))
    #Textthread.daemon=True
    Textthread.start()
    #consumer(TextWin)

"""""""""""""""""""""""""""""""""""""""""""""""""""""
             TK GUI start   
""""""""""""""""""""""""""""""""""""""""""""""""""""" 
# TODO Jia:
# define a class / init it with diff cmdline - other routine stays the same 
# queuetest-gui-class.py

""""""""""""""""""""
"   main() start   "
""""""""""""""""""""

root = Tk() # make explicit root first
root.title('vulcan cmd GUI')
startRow = 1
#TextWin = ScrolledText(Toplevel())
#TextWin.grid()
# vlcp config file
startRow += 1
cmdElement.append(CmdOptmenu(root,picks=DictCfg,rowNum=startRow))

# single-select :
startRow += 1
cmdElement.append(MBtn(root,picks=DictGPU,rowNum=startRow))

startRow += 1
cmdElement.append(CheckBtn(root,picks=DictArch,rowNum=startRow))

# multi-select :
startRow += 1
cmdElement.append(MBtn(root,picks=DictOS,rowNum=startRow))

startRow += 1
cmdElement.append(MBtn(root,sep=' ',picks=DictTest,rowNum=startRow))

#CL Entry 
startRow += 1
cmdElement.append(CustomCLEntry(root,text=' --target-revision=cl-',VarType='String',rowNum=startRow))

# tag 
startRow += 1
cmdElement.append(CustomTagEntry(root,text=' --tags ',VarType='String',delimiter=' ',rowNum=startRow))

# Note: TODO has to press "showcmd" then "runcmd" - doesn't make sense
# show full cmdline 
startRow += 1
Button(root,text='FullCmd', command=lambda key=cmdElement:showcmd(key)).grid(row=startRow)

startRow += 1
Button(root,text='Run', command=lambda :ThreadCmd(MyText=TextEditor(), cmdline=cmdline)).grid(row=startRow)

"""""""""""""""""""""""""""
   Add for Find-revisions 
"""""""""""""""""""""""""""
"""
        Find revision cmdline  
"""
FindCmd ='vulcan --find-revisions '
findrevcmdline = ''
"""""""""""""""""""""""""""""""""
Option menu : 
    - find-rev's configuartion files
""""""""""""""""""""""""""""""""" 
FindRevProd= {'v7.1 cuda9.2 r396 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r92_r396.vlcp',
              'v7.1 cuda9.1 r390 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r91_r390.vlcp',
              'v7.1 cuda9.0 r384 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r90_r384.vlcp',
              'v7.1 cuda8.0 r375 ':'//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r80_r375.vlcp',
              # TODO : v7.1 weekly
              'cudnn cuda_a':'//sw/gpgpu/MachineLearning/cudnn/eris/cudnn_gpgpu_cuda_a.vlcp'}
findrevname = '--product=' # must be a "=" blank follow as delimiter
FindRevCfg = {
            findrevname:FindRevProd,
        }

# blank below in the "components" is a must
components = [' cudnn ',' ]cudnn ',' ]=cudnn ',' cudnn_test ',' ]cudnn_test ',' ]=cudnn_tests ']
name = ' --revision-range '
RevDict = {
    name:components
}

def findrevcmd(Element):
    global FindCmd,findrevcmdline
    findrevcmdline = FindCmd
    for ele in Element:
        findrevcmdline += ele.showcmd()
    print('=== ',findrevcmdline,' ===')
    return findrevcmdline

FindrevElement = []

# find-revision config file
startRow += 1
FindRevOptmenu=CmdOptmenu(root,picks=FindRevCfg,rowNum=startRow)
FindrevElement.append(FindRevOptmenu)

#CL Entry 
startRow += 1
FindrevElement.append(DicCmdFindRevMenu(root,picks=RevDict,rowNum=startRow))


# show full cmdline 
startRow += 1
Button(root,text='FindRevCmd', command=lambda key=FindrevElement:findrevcmd(key)).grid(row=startRow)

startRow += 1
CLList = []
Button(root,text='Run-FindRev', command=lambda :ThreadCmd(MyText=TextEditor(), cmdline=findrevcmdline,OutData=CLList)).grid(row=startRow)


def showCL(cmdline,CLList):
    for data in CLList:
        print('===>Full cmd : ',cmdline.replace('tot',data))

startRow += 1
Button(root,text='list-triage', command=lambda :showCL(cmdline, CLList)).grid(row=startRow)

startRow += 1
Button(root,text='RUN-ALL-CLs', command=lambda :RUNAllCLs(cmdline, CLList)).grid(row=startRow)

root.mainloop()

