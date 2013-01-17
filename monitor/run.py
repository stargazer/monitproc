import psutil, sys, os
from psutil.error import AccessDenied
from screen import Screen 
import threading
import time
from metrics import Measurement
from present import Presentation
import signal
import curses

def main():
    """ 
    This is the main entry of the program. We do the following:
     * Create the screen for displaying the data
     * Create the 2 daemon threads that handle 2 tasks:
        * Making the measurements
        * Writing the measurements on the screen
     * Handle the termination which either happens if one of the threads
       terminates, or if Ctrl-C is pressed

    """
    # List where the latest measurements will be kept
    measurements = []
    # Used to lock access to ``measurements`` list        
    lock = threading.Lock()

    try:
        # create a virtual screen
        s = Screen()
    except curses.error:     
        print 'ERROR: Terminal size not large enough'
        exit()

    workers = (
        Measurement(measurements, lock),
        Presentation(measurements, lock, s),
    )
    for worker in workers:
        worker.start()      
                                          
    try:
        while threading.active_count() == 3:
            time.sleep(0.1)        
    except KeyboardInterrupt:
        pass

    # Gracefully destroy the screen
    s.kill()

if __name__ == '__main__':
    main()
