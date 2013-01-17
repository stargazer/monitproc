import threading, psutil
from time import sleep
 
class Measurement(threading.Thread):
    """ This thread, polls the system, saves the observations on list `self.measurements`.
        This list contains Process instances, as implemented by the `psutil` module.

    """
    INTERVAL = 1.0 

    def __init__(self, measurements, lock):
        """ Creates an instance of a thread, that will poll the system
            and get the measurements.

            @param terminate: Event that will signal the thread to terminate
            @param measurements: List where measurements will be stored
            @param lock: Used to control access to `measurements`
        """       
        self.measurements = measurements
        self.lock = lock

        super(Measurement, self).__init__()
        self.daemon = True
    
    def run(self):
        while 1:
            self.poll_system()
            sleep(self.INTERVAL)

    def poll_system(self):
        """ 
        We gather the ``psutil.Process`` instances corresponding to all
        processes we are interested in. Every ``psutil.Process`` instance,
        contains all kinds of measurements about the process.
        """
        # LOCK
        self.lock.acquire()

        del self.measurements[:]
        for process in psutil.process_iter():               
            if process.cmdline:
                if 'wsgi' in process.cmdline[0] or\
                   'apache' in process.cmdline[0]:
                    # Measurements for the process ``process``
                    measurement = []
                    measurement.append(process.cmdline[0])
                    measurement.append(process.pid)
                    measurement.append(process.get_cpu_percent())
                    measurement.append(process.get_memory_info()[0] / (1024**2))
                    measurement.append(process.get_memory_info()[1] / (1024**2))
                    measurement.append(round(process.get_memory_percent(), 3))
                    measurement.append(process.get_num_threads())
       
                    self.measurements.append(measurement)
        # UNLOCK    
        self.lock.release()


