'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Touch Math - Free Functions 
		These take Dict:TouchPlus and/or Point objects 
		and return metrics about the collections
	BEGIN
<><><><><><><><><><><><><><><><><><><><><><><><>'''
import scene
import numpy as np
from touch_plus import TouchPlus
from gesture_consts import Consts

def angle_between(v0, v1):
	'''
	Takes two 2D vectors (x, y) (preferably scene.Point object??) and returns the angle between the two vectors using numpy's arccos.  Also, using numpy's det (determinant) the function will decide the general direction of the vector to return the result in terms of 0 - 2*pi
	'''
	# Returns the angle in radians between vectors 'v0' and 'v1'::
	v0_u = v0 / np.linalg.norm(v0)
	v1_u = v1 / np.linalg.norm(v1)
	ang = np.arccos(np.clip(np.dot(v0_u, v1_u), -1.0, 1.0))
	det = np.linalg.det(np.array([v0, v1]))
	if det < 0:
		ans = ang
	else:
		ans = (2*np.pi) - ang
	if ans == (2*np.pi):
		ans = 0.0
	return ans
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
	
def area(touches):
	'''
	Takes a dictionary of touches and returns the smallest area which bounds all of the touches

	The touches should be TouchPlus objects but if not, they must abide by the following rules
		
	Touches must have the attributes:
		touch.start_position	: x, y location of the touch when it began (preferably a scene.Point object)
		touch.position				: x, y location of the touch now / when it ended (preferably a scene.Point object)
		touch.touch_id				: a unique ID for the touch
	
	Both position attribues are expected to have two attributes:
		position.x	: the x component of the touch position
		position.y	: the y component of the touch position
				
	This function returns a list of 2 areas, each area is a scene.Rect object:
		result[0] is  the area which contains all touch start_positions
		result[1] is the area which contains all touch positions
	'''
	min_x0 = min_y0 = min_x1 = min_y1 = 50000
	max_x0 = max_y0 = max_x1 = max_y1 = 0
	for touch in touches.values():
		min_x0 = min(min_x0, touch.start_position.x)
		min_y0 = min(min_y0, touch.start_position.y)
		max_x0 = max(max_x0, touch.start_position.x)
		max_y0 = max(max_y0, touch.start_position.y)
		min_x1 = min(min_x1, touch.position.x)
		min_y1 = min(min_y1, touch.position.y)
		max_x1 = max(max_x1, touch.position.x)
		max_y1 = max(max_y1, touch.position.y)
	area0 = scene.Rect(min_x0, min_y0, (max_x0-min_x0),(max_y0-min_y0))
	area1 = scene.Rect(min_x1, min_y1, (max_x1-min_x1),(max_y1-min_y1))
	return [area0, area1]
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

def centroid(touches):
	'''
	Takes a dictionary of touches and returns the centroid of all touch positions
	
	The touches should be TouchPlus objects but if not, they must abide by the following rules
	
	Touches must have the attributes:
		touch.start_position	: x, y location of the touch when it began (preferably a scene.Point object)
		touch.position				: x, y location of the touch now / when it ended (preferably a scene.Point object)
		touch.touch_id				: a unique ID for the touch
	
	Both position attribues are expected to have two attributes:
		position.x	: the x component of the touch position
		position.y	: the y component of the touch position

	This function returns a list of 2 centroids, each centroid is a scene.Point object:
		result[0] is the centroid which was derived from touch start_positions
		result[1] is the centroid which was derived from touch positions
	'''
	cent0 = cent1 = scene.Point(0,0)
	if len(touches) > 0:
		for touch in touches.values():
			cent0 += touch.start_position
			cent1 += touch.position
		n = len(touches)
		cent0 /= n
		cent1 /= n
	#x_cent0 = y_cent0 = x_cent1 = y_cent1 = 0
	#for touch in touches.values():
	#	x_cent0 += touch.start_position.x
	#	y_cent0 += touch.start_position.y
	#	x_cent1 += touch.position.x
	#	y_cent1 += touch.position.y
	#if len(touches) > 0:
	#	n = len(touches)
	#	x_cent0 /= n
	#	y_cent0 /= n
	#	x_cent1 /= n
	#	y_cent1 /= n
	#cent0 = scene.Point(x_cent0, y_cent0)
	#cent1 = scene.Point(x_cent1, y_cent1)
	return [cent0, cent1]
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
	
def direction(point0, point1):
	'''
	This function takes two scene.Point objects and returns a gesture_consts value for the direction from the first point to the second (Left, Right, Up, Down)
	'''
	const = Consts()
	diff = point1 - point0
	if diff.x == 0:
		diff.x = 0.0001
	gradient = diff.y / diff.x
	if diff.x > 0 and diff.y > 0 and gradient > 1:
		return const.UP
	elif diff.x > 0 and diff.y > 0 and gradient < 1:
		return const.RIGHT
	elif diff.x > 0 and diff.y < 0 and gradient < 1:
		return const.RIGHT
	elif diff.x > 0 and diff.y < 0 and gradient > 1:
		return const.DOWN
	elif diff.x < 0 and diff.y < 0 and gradient > 1:
		return const.DOWN
	elif diff.x < 0 and diff.y < 0 and gradient < 1:
		return const.LEFT
	elif diff.x < 0 and diff.y > 0 and gradient < 1:
		return const.LEFT
	elif diff.x < 0 and diff.y > 0 and gradient > 1:
		return const.UP
	else:
		return None
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
		
def duration(touches):
	'''
	Takes a dictionary of touches and returns the longest duration of all touches
	
	Touches must have the method:
		touch.duration()
		This method is expected to return the duration (as a positive float of seconds) of the touch
	'''
	t = 0
	#Get the longest duration touch from each collection
	for touch in touches.values():
		t = max(t, touch.duration())
	return t
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
		
def in_region(region, location):
	'''
	Takes a region, and determines if a location is within that region returning True if the location falls within the region
	
	region (preferably a scene.Rect object)
	location (preferably a scene.Point object)
	'''
	return region.contains_point(location)
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
					
def rotation(touches):
	'''
	Takes a dictionary of touches and returns the rotation of the touch start_positions to their (current) positions
	
	The touches should be TouchPlus objects but if not, they must abide by the following rules
	
	Touches must have the attributes:
		touch.start_position	: x, y location of the touch when it began (preferably a scene.Point object)
		touch.position				: x, y location of the touch now / when it ended (preferably a scene.Point object)
		touch.touch_id				: a unique ID for the touch
	
	Both position attribues are expected to have two attributes:
		position.x	: the x component of the touch position
		position.y	: the y component of the touch position
		
	This function returns a list of 2 centroids, each centroid is a scene.Point object:
		result[0] is  the centroid which was derived from touch start_positions
		result[1] is the centroid which was derived from touch positions
	
	'''
	if len(touches) <= 1:
		return 0
	cent0, cent1 = centroid(touches)
	gr_dist = []
	for touch in touches.values():
		#Find the touch which is the farthest from the centroid at the start, that will be our reference touch for rotation tracking 
		gr_dist.append([abs(touch.start_position - cent0), touch.touch_id])
		gr_dist.sort()
		gr_dist.reverse()
	v0 = (touches[gr_dist[0][1]].start_position - cent0)
	v1 = (touches[gr_dist[0][1]].position - cent1)
	return np.rad2deg(angle_between(v0,v1))
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
	
def scale(touches, by_area=False):
	'''
	Takes a dictionary of touches and returns the scale of the touch cluster from the start_positions to their (current) positions.  Has an optional argument by_area, which if True will change the method being used to calculate the scale from using the two farthest points, to using the entire area of the cluster at the beginning and comparing it to the area at the end.
	
	The touches should be TouchPlus objects but if not, they must abide by the following rules
	
	Touches must have the attributes:
		touch.start_position	: x, y location of the touch when it began (preferably a scene.Point object)
		touch.position				: x, y location of the touch now / when it ended (preferably a scene.Point object)
	
	Both position attribues are expected to have two attributes:
		position.x	: the x component of the touch position
		position.y	: the y component of the touch position
		
	This function returns a float value representing the scale (comparison of size) of the touches in the beginning to the size at their current position / ending position.  The value will be 1.0 if the size did not change.  Teh value will be less than 1.0 if the touch grouping closed in / shrunk and will be greater than 1.0 if the touch cluster got farther apart / grew
	'''
	if len(touches) <= 1:
		return 1.0
	size0 = size1 = 0
	if by_area:
		area0, area1 = area(touches)
		size0 = area0.width * area0.height
		size1 = area1.width * area1.height
	else:
		t_list = list(touches.values())
		size0 = abs(t_list[1].start_position - t_list[0].start_position)
		size1 = abs(t_list[1].position - t_list[0].position)
	if size0 == 0 or size1 == 0:
		return 0
	else:
		return (size1 / size0)
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
	
def translation(touches):
	'''
	Takes a dictionary of touches and returns the translation of the centroids of the touch cluster from the start_positions to the (current) positions
	
	The touches should be TouchPlus objects but if not, they must abide by the following rules
	
	Touches must have the attributes:
		touch.start_position	: x, y location of the touch when it began (preferably a scene.Point object)
		touch.position				: x, y location of the touch now / when it ended (preferably a scene.Point object)
		touch.touch_id				: a unique ID for the touch
	
	Both position attribues are expected to have two attributes:
		position.x	: the x component of the touch position
		position.y	: the y component of the touch position
		
	This function returns a scene.Point object representing the x, y translation of the centroids of the touches from start to current location	
	'''
	cent0, cent1 = centroid(touches)
	return (cent1 - cent0)
	#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
	
'''<><><><><><><><><><><><><><><><><><><><><><><><>
	Free Functions END
<><><><><><><><><><><><><><><><><><><><><><><><>'''	
