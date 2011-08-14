import curses 

class Screen:
	""" Thin layer on top of curses. Creates a window on which the rest 
		of the methods operate.
	"""

	def __init__(self, height, width, y, x):
		try:
			# Initialize the library
			stdscr = curses.initscr()

			# Create subwindow. This is the object on which we will be operating.
			self.w = stdscr.subwin(height, width, y, x)
			self.w.box()
			self.w.refresh()
			self.exists = True

		except:
			self.exists = False			

	def write(self, line, column, text, refresh=True):
		self.w.addstr(line, column, text)
		if refresh:
			self.w.refresh()

	def refresh(self):
		"""
		"""
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
		
