import curses 

class Screen:
    """ 
    Thin layer on top of curses which creates a window on which we will be
    displaying the measurements.
    """
    ROWS = 35
    COLUMNS = 130 
    X = 0
    Y = 0

    def __init__(self):
        try:
            # Initialize the library
            stdscr = curses.initscr()
            
            # Create subwindow. This is the object on which we will be operating.
            self.w = stdscr.subwin(self.ROWS, self.COLUMNS, self.Y, self.X)
            self.w.box()
            self.w.refresh()
        except:
            self.kill()
            raise

    def write(self, line, column, text, refresh=True):
        try:
            self.w.addstr(line, column, text)
        except curses.error:
            pass
        if refresh:
            self.w.refresh()

    def refresh(self):
        self.w.refresh()

    def clear_rest(self):
        """ When the process number decreases, the lines that belong to them might
            not be deleted, but instead stay present at the window.
            Here, we remove everything that comes after the cursor, and re-draw 
            the window.
        """
        self.w.clrtobot()
        self.w.redrawwin()
        self.w.box()
        self.w.refresh()          

    def kill(self):
        curses.endwin()
        
