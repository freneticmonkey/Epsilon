import pygame

from pygame import K_0

from Events import EventCore
from Events.EventBase import *

class QuitEvent(EventBase):
	def __init__(self):
		EventBase.__init__(self, 'Quit', True)

_instance = None

def GetInput():
	global _instance
	if not _instance:
		_instance = Input()
	return _instance

def GetKey(key):
	return GetInput().GetKey(key)

def GetKeyDown(key):
	return GetInput().GetKeyDown(key)

def GetKeyUp(key):
	return GetInput().GetKeyUp(key)

def GetMouseMove():
	return GetInput().GetMouseMove()

class Input(object):
	def __init__(self):
		self._keys = {}
		self._keys_down = {}
		self._keys_held = {}
		self._keys_up = {}
		self._ready = False
		self._mouse_x = 0.0
		self._mouse_y = 0.0
		
	def GetKey(self, key):
		returnVal = False
		if self._ready:
			returnVal = self._keys[key]
			returnVal = (returnVal == 1)
		return returnVal
	
	def GetKeyDown(self, key):
		returnVal = False
		if self._ready:
			returnVal = self._keys_down[key]
			returnVal = (returnVal == 1)
		return returnVal

	def GetKeyUp(self, key):
		returnVal = False
		if self._ready:
			returnVal = self._keys_up[key]
			returnVal = (returnVal == 1)
		return returnVal
	
	def GetMouseMove(self):
		return self._mouse_x, self._mouse_y

class InputProcessor(object):

	def __init__(self):
		self._input = GetInput()
		self._input._keys = pygame.key.get_pressed()
		self._input._keys_down = list(False for i in range(len(self._input._keys)))
		self._input._keys_held = list(False for i in range(len(self._input._keys)))
		self._input._keys_up   = list(False for i in range(len(self._input._keys)))
		
		self._initial_mouse_down = True
		
	def _process_input(self):
		eventlist = pygame.event.get()
		
		# Mouse
		left_down = pygame.mouse.get_pressed()[0]
		# If the left mouse button is down
		# Hide the cursor
		pygame.mouse.set_visible(not left_down)
		# Send Mouse Movement events 
		if left_down:
			
			if not self._initial_mouse_down:
				self._input._mouse_x, self._input._mouse_y = pygame.mouse.get_pos()
				self._input._mouse_x -= 400
				self._input._mouse_y -= 300
			else:
				self._initial_mouse_down = False
			pygame.mouse.set_pos(400,300)
		else:
			self._initial_mouse_down = True
		
		# Keyboard
		self._input._keys = pygame.key.get_pressed()
		
		# Check for Keys pressed this frame
		for key in range(0, len(self._input._keys)):
#		for key in self._input._keys.keys():
			
			# If the key is pressed and has been so for more than one frame
			if self._input._keys[key] and \
			   self._input._keys_down[key] and \
			   not self._input._keys_held[key]:
				# Assign the key as held
				self._input._keys_held[key] = True
				# Ensure that it is no longer marked as up
				self._input._keys_down[key] = False
				
			
			# If the key is pressed and not yet marked as down and not held
			if self._input._keys[key] and \
			   not self._input._keys_down[key] and \
			   not self._input._keys_held[key]:
				self._input._keys_down[key] = True
			
			# Else if the key is not pressed and it has been either down or held
			if not self._input._keys[key] and \
			   ( self._input._keys_down[key] or \
			     self._input._keys_held[key] ):
				# Mark the key as up
				self._input._keys_up[key] = True
				# Ensure that it isn't marked as held or down
				self._input._keys_down[key] = False
				self._input._keys_held[key] = False
			
			# If the key has already been registered as up
			# then on the next frame reset it to false 
			elif not self._input._keys[key] and \
			   self._input._keys_up[key]:
				self._input._keys_up[key] = False
			
		# Check for keys released this frame
		
		self._input._ready = True
		
#		print "dumping events: " + str(self._input._keys)
		for event in eventlist:
			if event.type == pygame.QUIT \
				or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				
				# Fire a Quit Event
				QuitEvent().Send()
					