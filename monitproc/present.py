import threading
from time import sleep

class Presentation(threading.Thread):
    """ 
    This class is responsible to manipulate the ``curses`` window, and present the 
    measurements, using the ``measurements`` list that is populated by the other
    thread.                     

    http://code.google.com/p/psutil/wiki/Documentation

    """
    HEADERS = (
        ('Command line',   '%(element)18s'),
        ('pid',            '%(element)10s'),
        ('ppid',           '%(element)10s'),
        ('user',           '%(element)15s'),
        ('CPU %',          '%(element)10s'),
        ('RSS Mem(MB)',    '%(element)13s'),
        ('Virt Mem(MB)',   '%(element)15s'),
        ('Memory %',       '%(element)10s'),
        ('Num Threads',    '%(element)13s'),
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

        # The first few lines will contain system stats
        from psutil import swap_memory, virtual_memory, cpu_percent
        cpu = 'CPU\t-\tUtilization: %.2f' % cpu_percent()
        content.append((1, cpu))

        mem = 'MEMORY\t-\tTotal: %dMB\tUsed: %d%%' % (
            virtual_memory()[0] / (1024**2), virtual_memory()[2]                            
        )
        content.append((2, mem))
        swap = 'SWAP\t-\tTotal: %dMB\tUsed: %d%%' % ( 
            swap_memory()[0] / (1024**2), swap_memory()[3]
        )
        content.append((3, swap))
                               
        title = self.get_header_line()
        content.append((5, title))

        # LOCK
        self.lock.acquire()

        row = 7
        for proc_measurements in self.measurements:
            # Retrieve process measurements as a formatted string
            output_line = self.get_proc_info_line(proc_measurements)
            
            content.append((row, output_line))
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
            template % ({'element': header}) for header, template in self.HEADERS 
        ]

        return ''.join(header_list)

    def get_proc_info_line(self, proc_measurements):
        """ 
        @param proc_measurement: Tuple that contains the measurements for
        one single process. Every number in the tuple, corresponds to a
        metric indicated by the corresponding entry in ``self.HEADERS``. 

        Returns a formatted string with the measurements, that will
        correspong to one line of output.
        """
        return ''.join(
            self.HEADERS[i][1] % ({'element': value}) for i, value in enumerate(proc_measurements)
        )

