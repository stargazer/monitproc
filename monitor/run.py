import psutil, sys, os
from psutil.error import AccessDenied
from screen import Screen 
import threading
import time
from metrics import Measurement
from present import Presentation
import signal

def main():
	""" Starts the initial ThreadManager thread, and then goes to sleep,
		waiting for a Ctrl-C signal. Once this is given, signals the
		ThreadManager to exit.

	"""
	# Condition variable that initiates termination.
	terminate_please = threading.Condition()

	# Creates and starts the ThreadManager thread
	manager = ThreadManager(terminate_please)
	manager.start()

	def do_exit(sig, stack):
		# Acquires the `terminate_please` lock, awakes the ThreadManager, 
		# which handles the graceful termination.
		terminate_please.acquire()
		terminate_please.notifyAll()
		terminate_please.release()

	# Registering Ctrl-C to do_exit()
	signal.signal(signal.SIGINT, do_exit)

	# Pause and wait for Ctrl-C
	signal.pause()

class ThreadManager(threading.Thread):
	""" Very simple thread management class.

		Creates and starts threads. After starting them, this thread sleeps,
		and only wakes up when it's `terminate` attribute is set. This is set
		by `main()` once an interrupt has been captures.
		Once this happens, this thread awakes, and waits for all other threads
		to terminate.
	"""

	def __init__(self, terminate_please):
		super(ThreadManager, self).__init__()
		# Signals to threads that they need to terminate
		self.terminate = threading.Event()
		# Will keep the measurements performed.
		self.measurements = []
		# Used to lock access to `measurements` list		
		self.lock = threading.Lock()

		# Condition variable, that will activate termination
		self.terminate_please = terminate_please

		self.workers = (
			Measurement(self.terminate, self.measurements, self.lock),
			Presentation(self.terminate, self.measurements, self.lock),
		)


	def run(self):
		""" Kickstarts worker threads, and then sleeps.
		"""
		for worker in self.workers:
			worker.start()      

		self.sleep()

	def sleep(self):
		# Sleeps until the main thread awakes it.
		self.terminate_please.acquire()
		self.terminate_please.wait()

		# When it awakes, it signals to the other threads to terminate.
		self.terminate_workers()

 	def terminate_workers(self):
		""" Sets the `terminate` event, which signals to the other threads to
		terminate.
		"""
		self.terminate.set()
		for worker in self.workers:
			worker.join()            
   		

if __name__ == '__main__':
    main()
