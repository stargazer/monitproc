import threading
from screen import Screen
from psutil.error import AccessDenied

class Presentation(threading.Thread):
	""" This class is responsible to create an ncurses window, and present the 
		measurements, using the `measurements` list that is populated by the other
		thread.

	"""
	SCREEN_ROWS = 30
	SCREEN_COLS = 130

	FIELDS = (
		# (name, title)
		( 'cmdline', 'Command line' ) ,
		('pid', 'PID' ),
		('cpu_percent', 'CPU Percent' ),
		('memory_info_rss', 'Memory Usage'),
		('memory_info_vms', 'VM Size'),
		('memory_percent', 'Memory Percent' ),
		('num_threads', 'Num Threads' ),
	)

	# How the elements will be displayed		
	TEMPLATE = '%(element)18s'

	def __init__(self, terminate, measurements, lock):
		self.event = threading.Event()
		self.terminate = terminate
		self.measurements = measurements
		self.lock = lock
		super(Presentation, self).__init__()
		

	def run(self): 
		# create a virtual screen
		s = Screen(Presentation.SCREEN_ROWS, Presentation.SCREEN_COLS, 0, 0)

		while not self.terminate.is_set():
			if s.exists:
				# create contents of screen
				content = self.create_content()
        	    # Returns a list of tuples
				# (row, string_to_write)
			
				for row, string in content:
					s.write(row, 1, string, refresh=False)
				s.refresh()
				s.clear_rest()
			self.event.wait(1)
		
		if s.exists:		
			s.kill()

 
	def create_content(self):
		""" Returns a list of tuples of (row, string), 
			which represents the row, and the string to be written
			in the `curses` screen.
		"""
		outputs = []

		title = Presentation.get_title()
   		outputs.append((1, title))

		row = 3

		# LOCK
		self.lock.acquire()

		for process in self.measurements:
			# Retrieve process information
			proc_info = Presentation.get_process_information(process)
			if proc_info:
				outputs.append((row, proc_info))
				row += 1

		# UNLOCK
		self.lock.release()
		return outputs
			
 
	@classmethod
	def get_title(cls):
		output_list = [] # A list of all the fields to display
		for _name, title in cls.FIELDS:
			output_list.append(
				cls.TEMPLATE % ({'element': title})
			)
				       
		return ''.join(output_list)

	@classmethod
	def get_process_information(cls,process):
			""" 
			Analyzes the `process` received. Retrieves all its information, and returns
			a string with the process information, which will eventually represent
			a line of output.
			
			@param process: psutil.Process instance
			"""
	 		# In the meantime, the process might have died. That's why we wrap this in
			# try-catch block
			try:
				info = {
					'pid': process.pid,
					'cmdline': 'N/A',
					'cpu_times': process.get_cpu_times(),
					'cpu_percent': process.get_cpu_percent(),
					'memory_info_rss': process.get_memory_info().rss / (1024 ** 2),
					'memory_info_vms': process.get_memory_info().vms / (1024 ** 2),
					'memory_percent': round(process.get_memory_percent(), 3),
					#'num_connections': 'N/A',
					'num_threads': process.get_num_threads(),
				}
			except:
				return None
																																																															    	
			try:
				info['cmdline'] =  process.cmdline[0]	
			except IndexError:
				pass

			try:
				info['num_connections'] = process.get_connections()
			except AccessDenied:
			 	pass

			output_list = []
			# Make a list out of the dictionary
			for name, _title in cls.FIELDS:
				value = info[name]
				output = cls.TEMPLATE % ({'element':value})
				output_list.append(output)

			return ''.join(output_list)

                        
