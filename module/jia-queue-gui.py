# GUI that displays data produced and queued by worker threads
import subprocess as sub
import _thread, queue, time
dataQueue = queue.Queue()    # infinite size

def producer(out, dataq): #(id):
    for line in iter(out.readline, b''):
        dataq.put(line) 
    out.close()
    #for i in range(3):
    #    time.sleep(0.1)
    #    print('put')
    #    dataQueue.put('[producer id=%d, count=%d]' % (id, i))
    #print('==> Prd %d loop Ends \n',id)

def consumer(root):
    try:
        print('get')
        data = dataQueue.get(block=False)
    except queue.Empty:
        pass
    else:
        root.insert('end', 'consumer got => %s\n' % str(data))
        root.see('end')
    root.after(250, lambda: consumer(root))    # 4 times per sec

def makethreads():
        print('*** Threadstart ! \n')

if __name__ == '__main__':
    # main GUI thread: spawn batch of worker threads on each mouse click
    from tkinter.scrolledtext import ScrolledText
    root = ScrolledText()
    root.pack()

    proc=sub.Popen(['./msgloop.py'], bufsize=1, shell=True, stdout=sub.PIPE)
    #root.bind('<Button-1>', lambda event: _thread.start_new_thread(producer, (proc.stdout,dataQueue )))
    _thread.start_new_thread(producer, (proc.stdout,dataQueue ))
    consumer(root)                       # start queue check loop in main thread
    root.mainloop()                      # pop-up window, enter tk event loop
