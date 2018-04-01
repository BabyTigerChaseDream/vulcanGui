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
pickProd= {'cudnn cuda9.1 r387 ':'//sw/gpgpu/MachineLearning/cudnn/eris/cudnn_r91_r387.vlcp',
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

pickGPU = ['gv100sxm2','gv100titan','v100','p4','gp102titanX','gp100sxm2','p40',
            'm4','m60','m40','gtx750ti','k80m','k40c','k5000']
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
#TODO: better data structure ?
cmdElement = []
vulCmd ='vulcan -v --eris --db --user jiag '

shCmdline ='./msgloop.py'

#Get CL number
def showCL(num):
    print("CL num is :",num.get())

#Get CL number
def showfile(cfgFile):
    print("Filepath:",cfgFile.get())

def showcmd(cmdElement):
    global vulCmd
    for ele in cmdElement:
        #print('*** ',ele.showcmd(),' ***')
        #print(type(vulCmd),type(ele.showcmd()))
        vulCmd = vulCmd + ele.showcmd()
    print('*** ',vulCmd,' ***')
    return vulCmd

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

# TODO: one runcmd can start one "Text" thread ?
#def runcmd(TextWin):
#def runcmd():
#    global vulCmd
#    #for ele in cmdElement:
#    #    vulCmd += ele.cmdline
#    # TODO: shell must be true ! to exec cmd
#    TextWin = ScrolledText(Toplevel())
#    TextWin.grid()
#    proc = sub.Popen(vulCmd,bufsize=1, shell=True,stdout=sub.PIPE)
#    print('==> Cmdline:',vulCmd)
#    #SimpleEditor(parent=Toplevel(),file=output.decode())
#    _thread.start_new_thread(producer, (proc.stdout,dataQueue))
#    consumer(TextWin)

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
########### main() start ############

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
cmdElement.append(CheckBtn(root,picks=DictArch,rowNum=startRow))

# multi-select :
startRow += 1
cmdElement.append(MBtn(root,picks=DictOS,rowNum=startRow))

startRow += 1
cmdElement.append(MBtn(root,picks=DictGPU,rowNum=startRow))

startRow += 1
cmdElement.append(MBtn(root,picks=DictTest,rowNum=startRow))

#CL CmdOptmenu
startRow += 1
cmdElement.append(CustomCLEntry(root,text=' --target-revision=cl-',VarType='Int',rowNum=startRow))

# tag 
startRow += 1
cmdElement.append(CustomTagEntry(root,text=' --tags ',VarType='String',delimiter=' ',rowNum=startRow))

# Note: TODO has to press "showcmd" then "runcmd" - doesn't make sense
# show full cmdline 
startRow += 1
Button(root,text='FullCmd', command=lambda key=cmdElement:showcmd(key)).grid(row=startRow)

startRow += 1
Button(root,text='Run', command=lambda :ThreadCmd(MyText=TextEditor(), cmdline='./msgloop.py')).grid(row=startRow)

root.mainloop()

