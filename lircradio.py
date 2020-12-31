"""
LIRC interface to receive signals from a infrared remote control.
"""

import threading
import time
import queue
import lirc

  
class LircInterface(threading.Thread):
    """
    This interfaces with the lirc daemon to read IR commands.
 
    When using lirc in blocking mode, sometimes repeated commands get produced
    in the next read of a command so we use a thread here to just wait
    around until a non-empty response is obtained from lirc.
    """
 
    def __init__(self, the_queue):
        threading.Thread.__init__(self)
        print("LircInterface init")
        self.daemon = True
        self.stopped = threading.Event()
        self.the_queue = the_queue
        lirc.init('pyqtradio', blocking=False)
 
    def run(self):
        """Main loop of LIRC interface thread."""
        print("LIRC interface thread started")
        while not self.stopped.isSet():
            try:
                code = lirc.nextcode()  # list; empty if no buttons pressed
            except lirc.NextCodeError:
                print("Error reading next code from LIRC")
                code = None
            # interpret result from python-lirc
            if code:
                code = code[0]
                self.the_queue.put(code)
            else:
                time.sleep(0.2)
        lirc.deinit()
        print('LIRC interface thread stopped')
        
 
class LircHandler(object):
    def __init__(self, the_queue):
        print("LircHander started")
        self.the_queue = the_queue 
        self.callbacks = []
 
 
    def timerCall(self):
        try:
            receivedCommand = self.the_queue.get(block=False)
            print("Lirc command from queue: " + receivedCommand)
            for item in self.callbacks:
                if item.get("command") == receivedCommand:
                    callback = item.get("callback")
                    callback()
        except:
            pass # nothng in queue   
 
    def addCallback(self, command, callback):
        self.callbacks.append({"command":command,"callback":callback})
        print("Added callback for command: " + command)
        
