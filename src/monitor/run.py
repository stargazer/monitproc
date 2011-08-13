import psutil, sys, os, curses
from psutil.error import AccessDenied


def server_processes():
	""" Returns a list of Process instances, that correspond to apache or wsgi processes.
		
		(`Process` as defined by psutil module)
	"""
	process_iter = psutil.process_iter()
	server_processes = []
	
	for process in process_iter:               
		if process.cmdline:
			if 'wsgi' in process.cmdline[0] or \
				'apache' in process.cmdline[0]:
			
				server_processes.append(process)

	return server_processes



class Presentation():
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

	@classmethod
	def get_process_information(cls,process):
		""" 
			Returns a dictionary with the process information

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
	
		return info
 


	@classmethod
	def get_title(cls):
		output_list = [] # A list of all the fields to display
		
		for _name, title in cls.FIELDS:
			output_list.append(
				cls.TEMPLATE % ({'element': title})
			)
       
		return ''.join(output_list)


	@classmethod
	def get_proc_output_list(cls, proc_info):
		template = '%(value)18s'
		output_list = []
		
		for name, _title in cls.FIELDS:
			value = proc_info[name]
			output = cls.TEMPLATE % ({'element':value})
			output_list.append(output)
		return output_list

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
	
					

def main():
	import time ,curses
	os.system('clear')

	title = Presentation.get_title()
	screen_rows = 30
	screen_cols = 130
	
	try:
		screen = Screen(screen_rows, screen_cols, 0, 0)
		if screen.exists:          
			screen.write(1, 1, title)

			while 1:

				proc_info_list = []
				proc_outputs = [] # List of lists. Every lists has the elements of a certain process, exactly as they will be output on screen.
				processes = server_processes()

				for process in processes:
					proc_info = Presentation.get_process_information(process)
					
					if proc_info:
						proc_output_list = Presentation.get_proc_output_list(proc_info)
						proc_outputs.append(proc_output_list)
								

					line = 3
					for proc_output in proc_outputs:
						# proc_output is a list of all the details of one certain process
						proc_output = ''.join(proc_output)
						screen.write(line, 1, proc_output, refresh=False)
						line += 1
				screen.refresh()
				screen.clear_rest()
				time.sleep(0.5)
	except:
		curses.endwin()
		raise

if __name__ == '__main__':
	main()
		

