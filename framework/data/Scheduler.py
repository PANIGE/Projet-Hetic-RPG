from os import kill
import  time
import threading 
import ctypes 
import time 
from framework.data.ErrorHandler import raiseError
import sys

class Scheduler:
    def __init__(self):
        self.threads = []
        self.joins = []

    def AddNow(self, function, **kwargs):
        self.AddDelayed(0, function, **kwargs)

    def AddDelayed(self, wait, function, **kwargs):
        t = pThread(target=self.__DelayedAsync__, args=(wait, function), kwargs=kwargs, killable=kwargs.get("killable", True))
        t.daemon = True
        self.threads.append(t)
        t.start()

    def __DelayedAsync__(self, wait, function, **kwargs):
        try:
            
            time.sleep(wait/1000)
            kwargs.pop("killable", None)
            function(**kwargs)
        except Exception as e:
            raiseError(e)


    def killThreads(self):
        for t in self.threads:
            t.abort()


class pThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.killable = kwargs.pop("killable", True)
        
        threading.Thread.__init__(self, *args, **kwargs)
        
    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def abort(self):
        if not self.killable:
            return
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')