'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Data
		A class to define the gesture attributes 
		this calculates the attributes and can be 
		passed as a single collection of the
		gesture characteristics
	BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''
import touch_math
from gesture_consts import Consts

class Data(Consts):
	'''
	This class contains all of the metadata about the touches and their state, specifically regarding their applicability to being a gesture.
	
	This class must bve created using a dictionary of touches (preferably TouchPlus objects) and will automatically calculate all relevant metadata about the touch collection using the touch_math library
	
	Notably, the gesture attribute will be None by default and must be injected by an outside source before passing a data class on to callback functions
	
	Attributes:
		gesture						: 
		state							: 
		number_of_touches	: 
		duration					: 
		translation				: 
		start_area				: 
		area							:	
		start_position		: 
		position					: 
		direction					: 
		scale							: 
		rotation					: 
		velocity_t				: 
		velocity_r				: 
		
	'''
	def __init__(self, touches, state):
		self.gesture = None
		self.state = state
		self.number_of_touches = len(touches)
		self.duration = self.translation = self.start_area = self.area = self.start_position = self.position =	self.direction = self.scale =	self.rotation = self.velocity_t = self.velocity_r = None
		if self.number_of_touches > 0:
			self.duration = touch_math.duration(touches)
			self.translation = touch_math.translation(touches)
			self.start_area, self.area = touch_math.area(touches)
			self.start_position, self.position = touch_math.centroid(touches)
			self.direction = touch_math.direction(self.start_position, self.position)
			self.scale = touch_math.scale(touches)
			self.rotation = touch_math.rotation(touches)
			if self.duration != 0:
				self.velocity_t = self.translation / self.duration
				self.velocity_r = self.rotation / self.duration
				
	def set_gesture(self, gest):
		self.gesture = gest
