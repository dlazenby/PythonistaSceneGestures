import console
import scene 
import time as T
import touch_math
from colorsys import hsv_to_rgb
from gesture_consts import Consts
from gesture_data import Data
from gesture_recognizer import Recognizer
from timer import Timer
from touch_plus import TouchPlus
from random import random
from datetime import date

import logging
im_logging = True

#if im_logging:
	# set up logging to file - see previous section for more details
#	LOG_FILENAME = 'gh_log_{0}.txt'.format(date.today())
#	logging.basicConfig(level=logging.DEBUG,
#											format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
#											filename=LOG_FILENAME,
#											filemode='a')

class GestureHandler(Consts):
	'''
	'''
	def __init__(self, parent, **kwargs):
		self.parent_scene = parent
		if not isinstance(parent, scene.Scene):
			raise TypeError('parent must be a Scene object!')
		if 'visible' in kwargs:
			self.visible = kwargs.get('visible')
		else:
			self.visible = True #False
		self.timer = Timer()
		self.recognizers = []
		self.reset()
		#Debugging
		if self.visible:
			self.setup_messages()

	def reset(self):
		'''
		'''
		self.touches = {}
		self.num_touches = 0
		self.timer.reset()
		self.state = self.IDLE
	# <><><><><><><><><><><><><><><><><><><><><><><><>

	def add_touch(self, touch):
		'''
		REQUIRED - EXTERNAL HOOK
		* Call this function in scene.Scene.touch_began to add touches to the tracking system
		
		Args:
			touch	: A touch object produced by scene.Scene in touch_began
		'''
		#Get the current timestamp
		time = T.time()
		#Add a new touch object to the collection
		self.touches[touch.touch_id] = TouchPlus(self.parent_scene,
		position=(touch.location), 
		color=hsv_to_rgb(random(), 1, 1), 
		start_time=time,
		touch_id = touch.touch_id,
		visible = self.visible)
		# <><><><><><><><><><><><><><><><><><><><><><><><>
		#Handle the gesture state change - The first touch indicates a tap gesture
		new_state = None

		self.timer.update_time('add_touch')
		if (len(self.touches) == 1):
			new_state = self.BEGAN 
		else: 
			if (self.timer.duration() > self.ADD_REMOVE_TIME):
				new_state = self.CANCELLED 
			else:
				new_state = self.ADDING
	
		self.num_touches = len(self.touches)
		self.change_state(new_state)
	# <><><><><><><><><><><><><><><><><><><><><><><><>

	def move_touch(self, touch):
		'''
		REQUIRED - EXTERNAL HOOK
		* Call this function in scene.Scene.touch_moved to change touches in the tracking system
		
		Args:
			touch	: A touch object referenced by scene.Scene in touch_began
		'''
		#Get the current timestamp
		time = T.time()
		#Update the touch with the move
		if touch.touch_id in self.touches:
			self.touches[touch.touch_id].update(touch.location, time)
			self.change_state(self.CHANGED)
	# <><><><><><><><><><><><><><><><><><><><><><><><

	def update_touches(self, touches):
		'''
		OPTIONAL - EXTERNAL HOOK
		* Call this function in scene.Scene.update to change touches in the tracking system
		* NOTE: Calling this may impact update rate on the system, be cautious
		
		Args:
			touches	: The library of touch objects referenced by scene.Scene.touches
		'''
		#Get the current timestamp
		time = T.time()
		#Update the touch collection
		updated = False
		for touch_key in touches.keys():
			if touch_key in self.touches:
				updated = True
				self.touches[touch_key].update(touches[touch_key].location, time)
		if updated:
			self.change_state(self.CHANGED)
	# <><><><><><><><><><><><><><><><><><><><><><><><>

	def remove_touch(self, touch):
		'''
		REQUIRED - EXTERNAL HOOK
		* Call this function in scene.Scene.touch_ended to remove touches from the tracking system
		
		Args:
			touch	: A touch object referenced by scene.Scene in touch_ended
		'''
		#Get the current timestamp
		time = T.time()
		#Handle the gesture state change - The last touch indicates a gesture is complete
		new_state=None

		self.timer.update_time('remove_touch')
		if (self.num_touches <= 1):
			new_state = self.ENDED
		else:
			if (self.timer.duration() > self.ADD_REMOVE_TIME):
				new_state = self.CANCELLED
			else:
				new_state = self.REMOVING

		#Remove a touch object from the collection
		if touch.touch_id in self.touches:  
			self.touches[touch.touch_id].hide()
			self.num_touches -= 1

		self.change_state(new_state)
	# <><><><><><><><><><><><><><><><><><><><><><><><>

	def change_state(self, new_state=None):
		'''
		'''
		#The main state machine for detecting and handling gestures, this is where all the smarts (should) happen.
		if new_state is None:
			new_state = self.IDLE
		# .........................................
		clean_on_exit = False
		data = Data(self.touches, new_state)
			
		#Things to do specific to each state
		if new_state == self.BEGAN:
			pass
		elif new_state == self.ADDING:
			pass
		elif new_state == self.CHANGED:
			pass
		elif new_state == self.REMOVING:
			pass
		elif new_state == self.ENDED:			
			clean_on_exit = True
		elif new_state == self.CANCELLED:
			clean_on_exit = True
		
		#Loop through all recognizers and check if the gesture is a match
		recognized = False
		recognized = self.check_recognizers(data)
		if data.gesture is None:
			gest = 'None'
		else:
			gest = data.gesture
			
		#Live state info printing string
		strings = ['{0} -> {1}'.format(self.state,new_state), 'Touches: {0} (Num={1})'.format(len(self.touches), self.num_touches)]
		if len(self.touches) > 0:
			strings.append('Duration={0:.2f}, Translation={1}'.format(data.duration,data.translation))
			strings.append('Rotation={0:.4f}, Scale={1:.4f}'.format(data.rotation,data.scale))
		else:
			strings.append('Duration=None, Translation=None'.format(data.duration,data.translation))
			strings.append('Rotation=None, Scale=None'.format(data.rotation,data.scale))	
		strings.append('Recognized: {0}, Gesture: {1} '.format(recognized, gest))
		
		self.state = new_state
		if self.visible:
			self.print_messages(strings)
		if clean_on_exit:
			self.cleanup()
	#<><><><><><><><><><><><><><><><><><><><><><><><>

	def cleanup(self):
		'''
		'''
		#Cleanup any touch tracking objects on screen, highlights, and call the reset function for all other relevant resetting
		for touch in self.touches.values():
			touch.hide()
			#del touch
		self.touches.clear()
		if self.visible:
			self.print_messages([self.state, 'Touches: {0} (Num={1})'.format(len(self.touches), self.num_touches)])
		self.reset()
	#<><><><><><><><><><><><><><><><><><><><><><><><>
	
	def add_recognizer(self, recog):
		'''
		'''
		self.recognizers.append(recog)
		self.recognizers.sort(key=lambda x: x.priority, reverse=True)
	#<><><><><><><><><><><><><><><><><><><><><><><><>
			
	def check_recognizers(self, gesture_data):
		'''
		'''
		recognized = False
		if len(self.touches) > 0:
			for recog in self.recognizers:
				if recog.is_recognized(gesture_data):
					gesture_data.set_gesture(recog.gesture)
					recog.run_action(gesture_data)
					recognized = True
					#Comment out to run through all recognizers
					break
					# If the new_state indicates that the gesture was cancelled or handled, reset everything and wait for something meaningful to happen		
		return recognized
 	#<><><><><><><><><><><><><><><><><><><><><><><><> 
 	
	def clear_recognizers(self):
		'''
		'''
		self.recognizers.clear()	
	#<><><><><><><><><><><><><><><><><><><><><><><><>

	def setup_messages(self):
		'''
		'''
		#For testing purposes, replaces console HUD with labels on screen. print using the print_messages() function
		w, h = scene.get_screen_size()
		self.labels = []
		for i in range(8):
			d = 15 + (15 * i)
			self.labels.append(scene.LabelNode('', font=('Helvetica',12) ,position=(w/2, (h-d))))
		for lbl in self.labels:
			self.parent_scene.add_child(lbl)
	#<><><><><><><><><><><><><><><><><><><><><><><><>
	def print_messages(self, strings=[]):
		'''
		'''
		#Replacement for Console.hud_alert, to allow for more formatting of the print area 
		if len(self.labels) > 0:
			for lbl in self.labels:
				lbl.text = ''
			i = 0
			for txt in strings:
				self.labels[i].text = txt
				i += 1
	#<><><><><><><><><><><><><><><><><><><><><><><><>

	def hide(self):
		'''
		'''
		self.visible = False    
	# <><><><><><><><><><><><><><><><><><><><><><><><>

	def show(self):
		'''
		'''
		self.visible = True
	# <><><><><><><><><><><><><><><><><><><><><><><><>

	def register_tap(self, callback, priority = 0, number_of_touches_required = None):
		''' Call `callback` when a tap gesture is recognized.
	
		Additional parameters:
	
		* `number_of_touches_required` - Set if more than one finger is required for the gesture to be recognized.
		'''
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=None, 
		maximum_press_duration=self.LONG_TOUCH_TIME, 
		minimum_number_of_touches=number_of_touches_required, 
		maximum_number_of_touches=number_of_touches_required, 
		minimum_movement=None, 
		maximum_movement=self.TAP_MOVEMENT, 
		direction=None, 
		gesture=self.TAP, 
		notify_on=[self.ENDED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
		
	def register_long_press(self, callback, priority = 0, number_of_touches_required = None, minimum_press_duration = None, allowable_movement = None):
		''' Call `callback` when a long press gesture is recognized. Note that this is a continuous gesture; you might want to check for `data.state == Gestures.CHANGED` or `ENDED` to get the desired results.
	
		Additional parameters:
	
		* `number_of_touches_required` - Set if more than one finger is required for the gesture to be recognized.
		* `minimum_press_duration` - Set to change the default 0.5 second recognition treshold.
		* `allowable_movement` - Set to change the default 10 point maximum distance allowed for the gesture to be recognized.
		'''
		if minimum_press_duration is None:
			minimum_press_duration=self.LONG_TOUCH_TIME
		if allowable_movement is None:
			allowable_movement=self.TAP_MOVEMENT
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=minimum_press_duration, 
		maximum_press_duration=None, 
		minimum_number_of_touches=number_of_touches_required, 
		maximum_number_of_touches=number_of_touches_required, 
		minimum_movement=None, 
		maximum_movement=allowable_movement, 
		direction=None, 
		gesture=self.LONG_PRESS, 
		notify_on=[self.ENDED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
		
	def register_long_press_n_drag(self, callback, priority = 0, number_of_touches_required = None, minimum_press_duration = None, allowable_movement = None):
		''' Call `callback` when a long press gesture is recognized. Note that this is a continuous gesture; you might want to check for `data.state == Gestures.CHANGED` or `ENDED` to get the desired results.
	
		Additional parameters:
	
		* `number_of_touches_required` - Set if more than one finger is required for the gesture to be recognized.
		* `minimum_press_duration` - Set to change the default 0.5 second recognition treshold.
		* `allowable_movement` - Set to change the default 10 point maximum distance allowed for the gesture to be recognized.
		'''
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=minimum_press_duration, 
		maximum_press_duration=None, 
		minimum_number_of_touches=number_of_touches_required, 
		maximum_number_of_touches=number_of_touches_required, 
		minimum_movement=None, 
		maximum_movement=None, 
		direction=None, 
		gesture=self.LONG_PRESS_N_DRAG, 
		notify_on=[self.CHANGED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
	
	def register_pan(self, callback, priority = 0, minimum_number_of_touches = None, maximum_number_of_touches = None):
		''' Call `callback` when a pan gesture is recognized. This is a continuous gesture.
	
		Additional parameters:
	
		* `minimum_number_of_touches` - Set to control the gesture recognition.
		* `maximum_number_of_touches` - Set to control the gesture recognition.
	
		Handler `action` receives the following gesture-specific attributes in the `data` argument:
	
		* `translation` - Translation from the starting point of the gesture as a `ui.Point` with `x` and `y` attributes.
		* `velocity` - Current velocity of the pan gesture as points per second (a `ui.Point` with `x` and `y` attributes).
		'''
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=None, 
		maximum_press_duration=None, 
		minimum_number_of_touches=minimum_number_of_touches, 
		maximum_number_of_touches=maximum_number_of_touches, 
		minimum_movement=None, 
		maximum_movement=None, 
		direction=None, 
		gesture=self.PAN, 
		notify_on=[self.CHANGED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
	
	#def register_screen_edge_pan(self, callback, priority = 0, edges):
	#	''' Call `callback` when a pan gesture starting from the edge is recogized. This is a continuous gesture.
	#
	#	`edges` must be set to one of `Gestures.EDGE_NONE/EDGE_TOP/EDGE_LEFT/EDGE_BOTTOM/EDGE_RIGHT/EDGE_ALL`. If you #want to recognize pans from different edges, you have to set up separate recognizers with separate calls to this #method.
	#
	#	Handler `action` receives the same gesture-specific attributes in the `data` argument as pan gestures, see #`add_pan`.
	#	'''
	#	recog = Recognizer(callback, 
	# priority,
	# minimum_press_duration=None, 
	#	maximum_press_duration=None, 
	# minimum_number_of_touches=None, 
	# maximum_number_of_touches=None, 
	#	minimum_movement=None, 
	#	maximum_movement=None, 
	#	direction=None, 
	#	gesture=None, 
	#	notify_on=[self.ENDED])
		
	#	self.recognizers.append(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
	
	def register_pinch(self, callback, priority = 0):
		''' Call `callback` when a pinch gesture is recognized. This is a continuous gesture.
	
		Handler `action` receives the following gesture-specific attributes in the `data` argument:
	
		* `scale` - Relative to the distance of the fingers as opposed to when the touch first started.
		* `velocity_t` - Current velocity of the pinch gesture as scale per second.
		'''
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=None, 
		maximum_press_duration=None, 
		minimum_number_of_touches=None, 
		maximum_number_of_touches=None, 
		minimum_movement=None, 
		maximum_movement=None, 
		direction=None, 
		gesture=self.PINCH, 
		notify_on=[self.CHANGED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
	
	def register_rotation(self, callback, priority = 0):
		''' Call `callback` when a rotation gesture is recognized. This is a continuous gesture.
	
		Handler `action` receives the following gesture-specific attributes in the `data` argument:
		
		* `rotation` - Rotation in radians, relative to the position of the fingers when the touch first started.
		* `velocity_r` - Current velocity of the rotation gesture as radians per second.
		'''
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=None, 
		maximum_press_duration=None, 
		minimum_number_of_touches=None, 
		maximum_number_of_touches=None, 
		minimum_movement=None, 
		maximum_movement=None, 
		direction=None, 
		gesture=self.ROTATION, 
		notify_on=[self.CHANGED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
	
	def register_swipe(self, callback, priority = 0, direction = None, number_of_touches_required = None):
		''' Call `callback` when a swipe gesture is recognized
	
		Additional parameters:
	
		* `direction` - Direction of the swipe to be recognized. Either one of `Gestures.RIGHT/LEFT/UP/DOWN`.
		* `number_of_touches_required` - Set if you need to change the minimum number of touches required.
	
		If swipes to multiple directions are to be recognized, the handler does not receive any indication of the direction of the swipe. Add multiple recognizers if you need to differentiate between different directions. '''
		recog = Recognizer(callback, 
		priority,
		minimum_press_duration=None, 
		maximum_press_duration=self.LONG_TOUCH_TIME, 
		minimum_number_of_touches=number_of_touches_required, 
		maximum_number_of_touches=number_of_touches_required, 
		minimum_movement=None, 
		maximum_movement=None, 
		direction=direction, 
		gesture=self.SWIPE, 
		notify_on=[self.ENDED])
		
		self.add_recognizer(recog)
		#<><><><><><><><><><><><><><><><><><><><><><><><>
		
'''<><><><><><><><><><><><><><><><><><><><><><><><>
	gesture_handler.py file END
<><><><><><><><><><><><><><><><><><><><><><><><>'''



'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Test Code. Example usage
<><><><><><><><><><><><><><><><><><><><><><><><>'''
#<><><><><><><><><><><><><><><><><><><><><><><><><><>                           
#This example is the update - object based Scene
class ExampleScene (scene.Scene):
	def general_handler(self, data):
		console.hud_alert('{0} ({1} fingers) Handled!'.format(data.gesture, data.number_of_touches), duration=0.25)
	def setup(self):
#		if im_logging:
#			logging.info('  ')
#			logging.info('<><><><><> APPLICATION STARTED <><><><><> ')
#			logging.info('  ')
		self.background_color = '#000000'
		self.gesture = GestureHandler(self)
		self.gesture.register_tap(self.general_handler, 0)
		self.gesture.register_tap(self.general_handler, 1, 2)
		self.gesture.register_tap(self.general_handler, 5, 3)
		self.gesture.register_pan(self.general_handler, 3, 2, 2)
		self.gesture.register_pinch(self.general_handler, 6)
		self.gesture.register_swipe(self.general_handler, 7)
		self.gesture.register_rotation(self.general_handler, 8)
		self.gesture.register_long_press(self.general_handler, 9)
		self.gesture.register_long_press_n_drag(self.general_handler, 10)

	def update(self):
		self.gesture.update_touches(self.touches)
		pass

	def touch_began(self, touch):
		self.gesture.add_touch(touch)

	def touch_moved(self, touch):
		self.gesture.move_touch(touch)

	def touch_ended(self, touch):
		self.gesture.remove_touch(touch)

scene.run(ExampleScene(), show_fps=True)

logging.shutdown()
#<><><><><><><><><><><><><><><><><><><><><><><><><><>
