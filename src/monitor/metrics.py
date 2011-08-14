import threading, psutil
 
class Measurement(threading.Thread):
	""" This thread, polls the system, saves the observations on list `self.measurements`.
		This list contains Process instances, as implemented by the `psutil` module.

	"""

	INTERVAL = 1.0 

	def __init__(self, terminate, measurements, lock):
		""" Creates an instance of a thread, that will poll the system
			and get the measurements.

			@param terminate: Event that will signal the thread to terminate
			@param measurements: List where measurements will be stored
			@param lock: Used to control access to `measurements`
		"""
		self.event = threading.Event()
		self.terminate = terminate
		self.measurements = measurements
		self.lock = lock
		super(Measurement, self).__init__()
	
	def run(self):
		while not self.terminate.is_set():
			self.poll_system()
			self.event.wait(Measurement.INTERVAL)

	def poll_system(self):
		""" 
		Modified the contents of self.measurements with Process instances, that 
		belong to apache or wsgi processes.
		"""
		process_iter = psutil.process_iter()

		# LOCK
		self.lock.acquire()

		del self.measurements[:]
		for process in process_iter:               
			if process.cmdline:
				if 'wsgi' in process.cmdline[0] or \
					'apache' in process.cmdline[0]:
					self.measurements.append(process)
		
		# UNLOCK	
		self.lock.release()


