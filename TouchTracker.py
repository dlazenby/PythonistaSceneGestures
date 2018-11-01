import scene
import console
from touch_plus import TouchPlus
from colorsys import hsv_to_rgb
from random import random

'''<><><><><><><><><><><><><><><><><><><><><><><><>
	touch_tracker.py file BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''
class TouchTracker():
	def __init__(self, parent, **kwargs):
		self.parentScene = parent
		if not isinstance(parent, scene.Scene):
			raise TypeError('parent must be a Scene object!')
		self.A = scene.Action
		if 'visible' in kwargs:
			self.visible = kwargs.get('visible')
		else:
			self.visible = True #False
		self.touches = {}
		self.touch_keys = []
		
	def add_touch(self, touch, time=0):
		self.touches[touch.touch_id] = TouchPlus(self.parentScene,
			position=(touch.location), 
			color=hsv_to_rgb(random(), 1, 1), 
			startTime=time,
			touch_id = touch.touch_id,
			visible = self.visible)
		self.touch_keys.append(touch.touch_id) 
		console.hud_alert('{0} touches'.format(len(self.touches), duration=0.25))
		
	def move_touch(self, touch, time=0):
		if touch.touch_id in self.touches:
			self.touches[touch.touch_id].update(touch.location, time)
				
	def update_touches(self, touches, time=0):
		for touch_key in touches.keys():
			if touch_key in self.touches:
				self.touches[touch_key].update(touches[touch_key].location, time)
		
	def remove_touch(self, touch, time=0):
		if touch.touch_id in self.touches:
			self.touches[touch.touch_id].hide()
			del self.touches[touch.touch_id]
			self.touch_keys.remove(touch.touch_id)

'''<><><><><><><><><><><><><><><><><><><><><><><><>
	touch_tracker.py file END
<><><><><><><><><><><><><><><><><><><><><><><><>'''

'''<><><><><><><><><><><><><><><><><><><><><><><><>
	test code:
<><><><><><><><><><><><><><><><><><><><><><><><>'''
# Variation of the 'Basic Scene' template that shows every
# touch in a different (random) color that stays the same
# for the duration of the touch.

#import scene
#from gesture_handler import GestureHandler
#from touch_tracker import TouchTracker

#<><><><><><><><><><><><><><><><><><><><><><><><><><>							
#This example is the update - object based Scene
class ExampleScene (scene.Scene):
	def setup(self):
		self.background_color = '#000000'
		self.gesture = TouchTracker(self)

	def update(self):
		self.gesture.update_touches(self.touches, self.t)
	
	def touch_began(self, touch):
		self.gesture.add_touch(touch, self.t)
	
	def touch_moved(self, touch):
		self.gesture.move_touch(touch, self.t)

	def touch_ended(self, touch):
		self.gesture.remove_touch(touch, self.t)
		
scene.run(ExampleScene(), show_fps=True)
#<><><><><><><><><><><><><><><><><><><><><><><><><><>
