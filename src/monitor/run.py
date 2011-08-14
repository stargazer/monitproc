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
		# Signals to threads that they need to terminate
		self.terminate = threading.Event()
		# Will keep the measurements performed.
		self.measurements = []
		# Used to lock access to `measurements` list		
		self.lock = threading.Lock()

		self.threads = (
			Measurement(self.terminate, self.measurements, self.lock),
			Presentation(self.terminate, self.measurements, self.lock),
		)
	
	def start(self):
		# Kick off threads
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

		# Sleep till `terminate` is set. Then wait for all other
		# threads to finish.
		wait()

   		


