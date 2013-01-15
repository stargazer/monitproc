import threading
from time import sleep
from psutil.error import AccessDenied

class Presentation(threading.Thread):
    """ 
    This class is responsible to manipulate the ``curses`` window, and present the 
    measurements, using the ``measurements`` list that is populated by the other
    thread.                     

    http://code.google.com/p/psutil/wiki/Documentation

    """
    HEADERS = (
        'Process',
        'Pid',
        'CPU Percent',
        'RSS Memory',
        'VM Size (MBs)',
        'Memory Percent',
        'Num Threads',
    )

    # The column headers and data will be displayed using this template. 
    TEMPLATE = '%(element)18s'

    # The screen will be updated every...
    INTERVAL = 0.5

    def __init__(self, measurements, lock, screen):
        self.measurements = measurements
        self.lock = lock
        self.screen = screen
        
        super(Presentation, self).__init__()
        self.daemon = True
        
    def run(self):
        while 1:
            # create contents of screen
            # Returns a list of tuples (row, string_to_write)
            content = self.create_content()
        
            for row, string in content:
                self.screen.write(row, 1, string, refresh=False)
            self.screen.refresh()
            self.screen.clear_rest()
            sleep(self.INTERVAL)
        
    def create_content(self):
        """       
        Returns the content of the screen for this cycle.

        Returns a list of tuples of (row, string), which represents the row and
        string that should be written on the corresponding row of the
        ``curses`` screen.
        """
        content = []

        title = self.get_header_line()
        content.append((1, title))

        # LOCK
        self.lock.acquire()

        row = 3
        for process in self.measurements:
            # Retrieve process measurements as a formatted string
            proc_info = self.get_proc_info_line(process)
            
            if proc_info:
                content.append((row, proc_info))
                row += 1

        # UNLOCK
        self.lock.release()
        return content
            
    def get_header_line(self):
        """
        Returns the title line for the ``curses`` screen, which contains 
        the headers of the columns.
        """
        header_list = [
            self.TEMPLATE % ({'element': header}) for header in self.HEADERS]
        return ''.join(header_list)

    def get_proc_info_line(self, process):
            """ 
            @param process: psutil.Process instance

            Analyzes the ``process`` instance received. Retrieves all its information, and returns
            a string with the process information, which will eventually represent
            a line of output.
            """
            # In the meantime, the process might have died. That's we wrap the
            # accessing of the ``psutil.Process`` instance in a try/catch
            # block.
            measurements = []
            try:
                measurements.append(process.cmdline[0])
                measurements.append(process.pid)
                measurements.append(process.get_cpu_percent())
                measurements.append(process.get_memory_info().rss / (1024**24))
                measurements.append(process.get_memory_info().vms / (1024**24))
                measurements.append(round(process.get_memory_percent(), 3))
                measurements.append(process.get_num_threads())
            except Exception, e:
                #TODO: What exceptions happen here?
                # Investigate whether if the process has died, I cant access
                # its measurementsrmation anymore.
                return None

            return ''.join(self.TEMPLATE % ({'element': value}) for value in measurements)

