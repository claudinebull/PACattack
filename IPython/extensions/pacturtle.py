import math
from IPython.core.displaypub import publish_display_data
import sys
import tempfile
from glob import glob
from shutil import rmtree
from IPython.core.displaypub import publish_display_data
from IPython.core.magic import (Magics, magics_class, line_magic,
                                line_cell_magic, needs_local_scope)
from IPython.testing.skipdoctest import skip_doctest
from IPython.core.magic_arguments import (
    argument, magic_arguments, parse_argstring
    )
from IPython.external.simplegeneric import generic
from IPython.utils.py3compat import (str_to_unicode, unicode_to_str, PY3,
                                      unicode_type)
from IPython.utils.text import dedent

class pacturtle:
	display_data = [];
	
	homex = 300 #home of turtle
	homey = 200 #xhome of turtle
	#get start coordinates from home
	starty = homey
	startx = homex
	turtleAngle = 90 #turtle is point up, 90 degrees to the x-axis
	turtleSpeed = 1
	checkPac = 0
	penDrawing = 1
	penSize = 1
	penColor = 'black'
					
	def forward(self, distance):
		"""
        Move the turtle forward relative to the current angle by the parameter distance.
        """
		self.turtleAngle = -self.turtleAngle
		radians = math.radians(self.turtleAngle)
		endx = math.cos(radians)
		endy = math.sin(radians)
		endx = distance * endx
		endy =distance * endy
		endy = endy #y goes down
		endx = self.startx - endx
		endy = self.starty + endy
		
		stringx = str(endx);
		stringy = str(endy);
		command = " line " + stringx + " " + stringy
		display_data = []
		publish_display_data('pacturtle.forward', {'turtle':command})
		
		#set up new startpoints
		self.startx = endx
		self.starty = endy
		self.turtleAngle = -self.turtleAngle
		
	def speed(self, speed):
		"""
		Setter for the speed that the turtle animates.
		"""
		stringspeed = str(speed)
		command = " speed " + stringspeed
		publish_display_data('pacturtle.speed', {'turtle':command})
		self.turtleSpeed = speed
		
	def backward(self, distance):
		"""
    	Move the turtle backward relative to the current angle by the parameter distance.
		"""
		#calculate endpoints
		self.turtleAngle = -self.turtleAngle
		radians = math.radians(self.turtleAngle)
		
		endx = math.cos(radians)
		endy = math.sin(radians)
		
		endx = -distance * endx
		endy = -distance * endy
		endy = endy #y goes down
	
		endx = self.startx - endx
		endy = self.starty + endy
		 
		stringx = str(endx);
		stringy = str(endy);
		command = " backward "+ stringx + " " + stringy
		publish_display_data('pacturtle.backward', {'turtle':command})
		#set up new startpoints
		self.startx = endx
		self.starty = endy
		#reset angle
		self.turtleAngle = -self.turtleAngle
		
	def right(self, angle):
		"""
		Rotate the turtle clockwise by the parameter angle measured in Euler angles.
		""" 
		stringangle = str(angle)
		command = " rotate " + stringangle
		publish_display_data('pacturtle.rotate', {'turtle':command})
		self.turtleAngle = self.turtleAngle + angle
		
	def left(self, angle):
		""" 
    	Rotate the turtle clockwise by the parameter angle measured in Euler angles.
     	"""
		strangle = "-" + str(angle)
		command = " rotate " + strangle
		publish_display_data('pacturtle.rotate', {'turtle':command})
		self.turtleAngle = self.turtleAngle - angle
	
	def penup(self):
		"""
		Change the state of the pen, If the pen is up then the turtle will no longer draw when it moves.
		"""
		strzero = str(0);
		command = " penStatus " + strzero
		publish_display_data('pacturtle.penup', {'turtle':command})
		self.penDrawing = 0
		
	def pendown(self):
		"""
    	Change the state of the pen, If the pen is down then the turtle will not draw when it moves.
    	"""
		strone = str(1)
		command = " penStatus " + strone
		publish_display_data('pacturtle.pendown', {'turtle':command})
		self.penStatus = 1
	
	def pensize(self, size):
		"""
    	Change the size of the line drawn by the turtle to the parameter size
    	"""
		strsize = str(size);
		command = " penSize " + strsize
		publish_display_data('pacturtle.pensize', {'turtle':command})
		penSize = size;
		
	def pencolor(self, color):
		"""
    	Change the color of the line drawn by the turtle to the parameter color.
    	"""
		command = " penColor " + color
		publish_display_data('pacturtle.pencolor', {'turtle':command})
		penColor = color;
		
	def circle(self, radius):
		"""
    	Draws a circle with a radius of the given parameter
    	"""
		for x in range(0, 362):
			self.forward(2*math.pi*radius/360.0)
			self.right(1)
	
	def isdown(self):
		"""
    	Prints to output as a string if the turtle is currently drawing
    	"""
		if self.penDrawing == 1:
			print "True"
		else:
			print "False"

	def goto(self, x, y):
		"""
    	Moves the turtle to the point (x,y) specified by parameters
    	"""
		#dif of x
		difx = self.startx - x
		#dif of y
		dify = self.starty - y
		
		if difx == 0:
			if (dify < 0):
				myAngle = -90
			else:
				myAngle = 90
		elif dify == 0:
			if (difx > 0):
				myAngle = 0
			else:
				myAngle = 180
		else:
			difx = abs(difx)
			dify = abs(dify)
			myAngle = math.degrees(math.atan2(dify,difx))
			# check the four quadrants
			if ((self.starty - y) > 0 and (self.startx - x) < 0):
				myAngle = 180 - myAngle
			elif ((self.starty - y) < 0 and (self.startx - x) < 0):
				myAngle = 180 + myAngle
			elif ((self.starty - y) < 0 and (self.startx - x) > 0):
				myAngle = 360 - myAngle
			else:
				myAngle = myAngle
		self.startx = x
		self.starty = y
		strx = str(x)
		stry = str(y)
		strangle = str(myAngle)
		command = " goTo " + strx + " " + stry + " " + strangle
		publish_display_data('pacturtle.goto', {'turtle':command})
		
	def home(self):
		self.goto(self.homex, self.homey)
