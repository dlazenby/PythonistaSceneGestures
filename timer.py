'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Timer 
		This establishes a resetable timer object
	BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''
import time as T

class Timer():
	'''
	A timer class which takes a given time, expressed as a positive integer,
	and (optionally) a caller ID (typically a string), and tracks the interval 
	between "tick" calls
	'''
	def __init__(self):
		self.reset()
		
	def update_time(self, caller=None):
		'''
		This function (optionally) takes a caller ID
		
		If the caller ID is provided and is the same as the last caller, the time is 
		processed normally.
		If the caller ID is not the same as the previous caller, the timer resets the 
		internal time tracker with the current passed-in time as the starting point
		
		This function calculates the time delta from the last time this function was called
		'''
		time = T.time()
		if caller != self.last_called_by:
			self.stopwatch = 0
		if self.start_time == 0:
			self.last_time = self.start_time = time
		dt = time - self.last_time
		self.last_time = time
		self.stopwatch += dt

	def duration(self):
		'''
		This function returns the internal timer value, which is equivalent to
		the delta between the first "tick" call and the last "tick" call from the 
		same caller-ID
		'''
		return self.stopwatch
		
	def reset(self):
		'''
		This function resets all of the internal timer values to the initial values
		'''
		self.start_time = 0
		self.last_time = 0
		self.stopwatch = 0
		self.last_called_by = None
		
'''<><><><><><><><><><><><><><><><><><><><><><><><>
	timer.py file END
<><><><><><><><><><><><><><><><><><><><><><><><>'''
