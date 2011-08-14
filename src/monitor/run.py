import psutil, sys, os
from psutil.error import AccessDenied
from screen import Screen 
import threading
import time
from metrics import Measurement
from present import Presentation


def main():
	manager = ThreadManager()
	
	try:
		manager.start()		
	except:
		# Setting event `terminate` to True. Now all threads will terminate.
		manager.terminate.set()

class ThreadManager():
	""" Very simple thread management class.

		Creates and starts threads. After starting them, this thread sleeps,
		and only wakes up when it's `terminate` attribute is set. This is set
		by `main()` once an interrupt has been captures.
		Once this happens, this thread awakes, and waits for all other threads
		to terminate.
	"""

	def __init__(self):
		# Event. Signals to threads that they need to terminate
		self.terminate = threading.Event()
		self.measurements = []

		self.threads = (
			Measurement(self.terminate, self.measurements),
			Presentation(self.terminate, self.measurements),
		)
	
	def start(self):
		for thread in self.threads:
			thread.start()      

		def wait():
			# Event. Used to make this thread sleep.
			event = threading.Event()

			# If terminate is not set, sleep.
			# Otherwise, wait for threads to terminate
			while not self.terminate.is_set():
				event.wait(1)
			else:
				for thread in self.threads:
					thread.join()

		wait()

   		


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

	def __init__(self, terminate, measurements):
		self.event = threading.Event()
		self.terminate = terminate
		self.measurements = measurements
		super(Presentation, self).__init__()
		

	def run(self): 
		# create a virtual screen
		s = Screen(Presentation.SCREEN_ROWS, Presentation.SCREEN_COLS, 0, 0)

		while not self.terminate.is_set():
			# create contents of screen
			content = self.create_contents()
			title = Presentation.get_title()
			line = 3

			if s.exists:
				s.write(1, 1, title)
				for lista in content:
					proc_output = ''.join(lista)
					s.write(line, 1, proc_output, refresh = False)
					line = line + 1
				s.refresh()
				s.clear_rest()			
			#
			self.event.wait(1)
		
		if s.exists:		
			s.kill()


	def present(self):
		pass

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
			Analyzes the `process` received, and returns a dictionary with the process information
			
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
	def get_proc_output_list(cls, proc_info):
		template = '%(value)18s'
		output_list = []

		for name, _title in cls.FIELDS:
			value = proc_info[name]
			output = cls.TEMPLATE % ({'element':value})
			output_list.append(output)
		return output_list
																			   

	def create_contents(self):
		proc_info_list = []
		proc_outputs = []

		for process in self.measurements:
			proc_info = Presentation.get_process_information(process)

			if proc_info:
				proc_output_list = Presentation.get_proc_output_list(proc_info)
				proc_outputs.append(proc_output_list)

		return proc_outputs
			

