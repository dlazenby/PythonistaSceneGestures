'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Consts
		Constants used in gesture handling
	BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''

class Consts():
	'''
	This class contains all of the constant values used in the gesture handler classes
	and derivative classes.  This class must be subclassed or included by any class 
	wishing to interact directly with the gesture handler family of classes
	
	The consts within are unique values used to identify states and unique items within
	the gesture handler family of classes.  Most of the consts consist of a unique printable
	string correspondant of the use of the constant value, with the exception of a few numerical
	constants (LONG_TOUCH_TIME, ADD_REMOVE_TIME, and TAP_MOVEMENT) 
	'''
	IDLE = 'State: Idle'
	ADDING = 'State: Adding'
	BEGAN = 'State: Began'
	CHANGED = 'State: Changed'
	REMOVING = 'State: Removing'
	ENDED = 'State: Ended'
	CANCELLED = 'State: Cancelled'
	HANDLED = 'State: Handled'
	
	NO_GESTURE = 'Gesture: None'
	TAP = 'Gesture: Tap'
	LONG_PRESS = 'Gesture: Long Press'
	LONG_PRESS_N_DRAG = 'Gesture: Long Press N Drag'
	SWIPE = 'Gesture: Swipe'
	PAN = 'Gesture: Pan'
	PINCH = 'Gesture: Pinch'
	ROTATION = 'Gesture: Rotation'
	SCREEN_EDGE_PAN = 'Gesture: Screen Edge Pan'
	
	LEFT = 'Direction: Left'
	RIGHT = 'Direction: Right'
	UP = 'Direction: Up'
	DOWN = 'Direction: Down'
	
	EDGE_RIGHT = 'Edge Right'
	EDGE_LEFT = 'Edge Left'
	EDGE_TOP = 'Edge Top'
	EDGE_BOTTOM = 'Edge Bottom'
	
	LONG_TOUCH_TIME = 0.4 #seconds
	ADD_REMOVE_TIME = 0.075 #seconds
	TAP_MOVEMENT = 10 #pixels
	
	'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Consts
	END
<><><><><><><><><><><><><><><><><><><><><><><><>'''
