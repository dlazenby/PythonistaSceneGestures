'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Recognizer
		A class to define gestures and determine when 
		they have been recognized
		Tap 
		Multi-Tap 
		Long Press
		Long Press N Drag 
		Swipe
		Pan
		Pinch/Zoom
		Rotation
		
	BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''
from gesture_consts import Consts
from gesture_data import Data
import logging
im_logging = False

class Recognizer(Consts):
	'''
	'''
	def __init__(self, action, priority, **kwargs):
		self.minimum_press_duration = self.maximum_press_duration = self.minimum_number_of_touches = self.maximum_number_of_touches = self.minimum_movement = self.maximum_movement = self.ROI = self.start_ROI = self.direction = self.gesture = self.notify_on = self.number_of_instances = None
		self.callback = action
		self.instances = 0
		
		self.priority = priority
		
		if 'minimum_press_duration' in kwargs:
			self.minimum_press_duration = kwargs.get('minimum_press_duration')
		if 'maximum_press_duration' in kwargs:
			self.maximum_press_duration = kwargs.get('maximum_press_duration')
		if 'minimum_number_of_touches' in kwargs:
			self.minimum_number_of_touches = kwargs.get('minimum_number_of_touches')
		if 'maximum_number_of_touches' in kwargs:
			self.maximum_number_of_touches = kwargs.get('maximum_number_of_touches')
		if 'minimum_movement' in kwargs:
			self.minimum_movement = kwargs.get('minimum_movement')	
		if 'maximum_movement' in kwargs:
			self.maximum_movement = kwargs.get('maximum_movement')
		if 'ROI' in kwargs:
			self.ROI = kwargs.get('ROI')
		if 'start_ROI' in kwargs:
			self.start_ROI = kwargs.get('start_ROI')
		if 'direction' in kwargs:
			self.direction = kwargs.get('direction')
		if 'notify_on' in kwargs:
			self.notify_on = kwargs.get('notify_on')
		if 'number_of_instances' in kwargs:
			self.number_of_instances = kwargs.get('number_of_instances')
		if 'gesture' in kwargs:
			self.gesture = kwargs.get('gesture')
	
																													
	#def is_recognized(self, data):
										
	def is_recognized(self, data):
		'''
		'''
		recognized = True
		attributes = 0
		if self.notify_on is not None:
			if im_logging and (data.state in [self.ENDED, self.BEGAN, self.CHANGED]):
				self.log.debug('Checking Notify_On: %s ,against State: %s', self.notify_on, data.state)
			if (data.state in self.notify_on):
				return False
			
		if self.gesture == self.LONG_PRESS_N_DRAG:
			if im_logging:
				self.log.info('Self.Gesture is LONG_PRESS_N_DRAG, checking duration')
			attributes += 1
			if self.minimum_press_duration is not None:
				recognized &= (data.duration >= self.minimum_press_duration)
			else:
				recognized &= (data.duration >= self.LONG_TOUCH_TIME)
			if im_logging:	
				self.log.info('Looking for long press. Recognized: %s', recognized)
				
		if self.gesture == self.ROTATION:
			if im_logging:
				self.log.info('Self.Gesture is ROTATION, checking rotation amount: %s', data.rotation)
			attributes += 1
			min_rotate = 12.0
			if data.rotation > 0:
				recognized &= (data.rotation >= min_rotate and data.rotation <= (360.0 - min_rotate))
			if im_logging:	
				self.log.info('Looking for rotation amount. Recognized: %s', recognized)
			
		if self.ROI is not None:
			attributes += 1
			recognized &= gesture_data.touch_math.in_region(self.ROI, data.position)
			if im_logging:
				self.log.info('Looking for touch in ROI. Recognized: %s', recognized)
			
		if self.start_ROI is not None:
			attributes += 1
			recognized &= gesture_data.touch_math.in_region(self.start_ROI, data.start_position)
			if im_logging:
				self.log.info('Looking for touch starting in ROI. Recognized: %s', recognized)
			
		if self.number_of_instances is not None:
			attributes += 1
			recognized &= True
		
		if self.maximum_number_of_touches is not None:
			attributes += 1
			recognized &= (data.number_of_touches <= self.maximum_number_of_touches)
			if im_logging:
				self.log.info('Looking at Max Num Touches. Recognized: %s', recognized)
			
		if self.minimum_number_of_touches is not None:
			attributes += 1
			recognized &= (data.number_of_touches >= self.minimum_number_of_touches)	
			if im_logging:
				self.log.info('Looking at Min Num Touches. Recognized: %s', recognized)
			
		if self.maximum_movement is not None:
			attributes += 1
			recognized &= (abs(data.translation) <= self.maximum_movement)	 
			if im_logging:
				self.log.info('Looking Max Movement. Recognized: %s', recognized)
		
		if self.minimum_movement is not None:
			attributes += 1
			recognized &= (abs(data.number_of_touches) >= self.minimum_movement)
			if im_logging:
				self.log.info('Looking Min Movement. Recognized: %s', recognized)	
			
		if self.maximum_press_duration is not None:
			attributes += 1
			recognized &= (data.duration <= self.maximum_press_duration)		
			if im_logging:
				self.log.info('Looking at Max Duration. Recognized: %s', recognized)
			
		if self.minimum_press_duration is not None:
			attributes += 1
			recognized &= (data.duration >= self.minimum_press_duration)		 
			if im_logging:
				self.log.info('Looking at Min Duration. Recognized: %s', recognized)
			
		if self.direction is not None:
			attributes += 1
			recognized &= (data.direction == self.direction)	
			if im_logging:
				self.log.info('Looking at Directions. Recognized: %s', recognized)
		
		if attributes < 1:
			return False
		else:
			if recognized:
				self.instances += 1
			return recognized	 
		
	def run_action(self, data):
		'''
		'''
		self.callback(data)

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>				
