from screen import Screen 
from metrics import Measurement
from present import Presentation

from optparse import OptionParser

import signal
import curses
import threading
import time

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
    # Utility's usage and command line arguments
    usage = "usage: %prog arg1 arg2 ...argn"
    description=\
    "Monitoring utility. "\
    "Outputs a list of processes indicated by ``arg1``, ``arg2``, ...,"\
    "``argn`` and the system resources that they occupy."
    parser = OptionParser(usage=usage, description=description)
    (options, args) = parser.parse_args()

    # List where the latest measurements will be kept
    measurements = []
    # Used to lock access to ``measurements`` list        
    lock = threading.Lock()

    try:
        # create a virtual screen
        s = Screen()
    except curses.error:     
        print 'ERROR: Please maximize the terminal'
        exit()

    workers = (
        Measurement(measurements, lock, args),
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
