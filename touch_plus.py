'''<><><><><><><><><><><><><><><><><><><><><><><><>
	TouchPlus 
		This defines an augmented touch object that includes
		its own simple tracking algorithms, a sprite representation,
		and gesture area calculations
	BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''

import scene 
import console
from colorsys import hsv_to_rgb
from random import random

class TouchPlus():
	'''
	A class for touches on the screen which has some added functionality beyond that of the built-in touch class in the scene module (such as simple touch tracking, and visualization of the touch on-screen)
	
	Positional Args:
		parent : a scene.Scene object in which to draw the touch as a sprite representation
	
	kwargs:
		'position' 		: The scene.Point representation of the touch's position
		'start_time' 	: The timestamp when the touch started, obtained from scene.t
		'visible' 		: A True or False value for whether to represent the touch as a sprite (show it on screen)
		'touch_id' 		: The touch_id value (unique ID) for the touch object (best obtained from the scene.touch.touch_id)
		
	Attributes:
		start_position 	: The starting position of the touch as a scene.Point
		last_position		: The previous position of the touch as a scene.Point
		location				: Another accessor for the touch position
		sprite					: The graphical representation object to be shown on the scene.Scene
		area						: A scene.Rect representation of the area that the touch has covered from start to finish
	
	'''
	def __init__(self, parent=None, **kwargs):
		if not isinstance(parent, scene.Scene):
			#raise TypeError('parent must be a Scene object!')
			self.visible = False
			self.parent_scene = None	
		else:
			self.parent_scene = parent
		# Extra kwargs handling
		if 'position' in kwargs:
			self.start_position = kwargs.get('position')
		else:
			self.start_position = scene.Point(0,0)
		if 'start_time' in kwargs:
			self.start_time = kwargs.get('start_time')
		else:
			self.start_time = 0
		if 'visible' in kwargs:
			self.visible = kwargs.get('visible')
		else:
			self.visible = False
		if 'touch_id' in kwargs:
			self.touch_id = kwargs.get('touch_id')
		else:
			self.touch_id = None
		
		# Other
		self.A = scene.Action
		self.last_position = self.position = self.start_position
		self.location = self.position
		self.last_time = self.time = self.start_time
		self.gesture_area = None
		self.sprite = None
		self.area = scene.Rect(self.start_position.x, self.start_position.y, 1, 1)
		if self.visible:
			self.show()
		else:
			self.hide()
	
	def duration(self, time=0):
		'''
		A function to update / track the touch duration
		
		Given a non-zero time (best obtained from scene.t) this will store the new time and return the delta from when the touch started until now
		
		If no arg is passed, the function will return the time from when the touch started to the last updated time
		'''
		if time > 0:
			self.last_time = self.time
			self.time = time
		return self.time - self.start_time
		
	def hide(self):
		'''
		Removes any representation of the touch from the screen and disables visibility of the touch
		'''
		self.remove_highlight()
		if self.sprite is not None:
			self.sprite.remove_from_parent()
			del self.sprite
		self.sprite = None
		self.visble = False
		
	def highlight(self):
		'''
		Generates a highlighted area on-screen from where the touch began to where the touch currently resides
		
		When called, if the gesture_area has not been established, it will generate one
		
		If the gesture_area has been established, it updates the attributes of the gesture_area to reflect the touch's current position
		'''
		start = self.start_position
		stop = self.position
		new = False
		if self.gesture_area is None:
			self.gesture_area = scene.SpriteNode(color='#4db9ff', alpha=0.2)
			new = True
		self.gesture_area.position=((start + stop) / 2)
		delta = stop - start
		self.gesture_area.size=(abs(delta.x), abs(delta.y))
		if self.visible and new:
			self.parent_scene.add_child(self.gesture_area)
		# <><><><><><><><><><><><><><><><><><><><><><><><>
		
	def remove_highlight(self):
		'''
		Removes the highlighted area representation from the screen
		'''
		if self.gesture_area is not None:
			self.gesture_area.remove_from_parent()
			del self.gesture_area
		self.gesture_area = None
		# <><><><><><><><><><><><><><><><><><><><><><><><>
		
	def show(self, parent=None):
		'''
		Enables visual representation of the touch on the screen, but only if a parent_scene is present to display the touch on.
		
		If an arg is passed, it assumed to be a parent scene (scene.Scene) object and will update the parent_scene object
		
		If the parent_scene object is valid the function will attempt to draw a sprite on the scene object
		
		If no parent scene object exists, the function will not draw anything and visibility will remain off
		'''
		if parent is not None:
			if self.parent_scene is not None and self.sprite is not None:
				self.sprite.remove_from_parent() #Remove from the current parent
			self.parent_scene = parent #Assign a new parent for this touch
		if self.parent_scene is not None:
			self.visible = True #The touch has a parent, therefore it can be shown
			if self.sprite is None:
				self.sprite = scene.SpriteNode(
					texture='shp:wavering', 
					position=self.position, 
					color=hsv_to_rgb(random(), 1, 1)) #Give the touch a visible representation 
			self.parent_scene.add_child(self.sprite) #Add the representation to the parent scene 
		else:
			self.visble = False #If no parent scene, then there cannot be a sprite shown
			self.sprite = None
	
	def update(self, pos, time=0):
		'''
		A function to update the touch's position and (optionally) time
		
		This function also handles the recalculation of certain tracking attributes such as:
			last_position
			position
			area
			
		The function also takes care of the movement of the sprite representing the touch to its newest location on screen
		'''
		self.duration(time)
		self.last_position = self.position
		self.position = pos
		self.location = self.position
		wh = self.position - self.start_position
		self.area = scene.Rect(self.start_position.x, 
		self.start_position.y, 
		wh.x, wh.y)
		if self.sprite is not None:
			self.sprite.run_action(self.A.move_to(pos.x, pos.y, 0.01))
			
'''<><><><><><><><><><><><><><><><><><><><><><><><>
	touch_plus.py file END
<><><><><><><><><><><><><><><><><><><><><><><><>'''
