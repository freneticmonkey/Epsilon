from itertools import repeat

import pygame

from Core.BaseManager import FrameListenerManager

class Input(FrameListenerManager):
	
	# Mouse Constants
	MOUSE_LEFT = 0
	MOUSE_RIGHT = 2
	MOUSE_MIDDLE = 1
	
	def init(self):
#		self._keys = {}
#		self._keys_down = {}
#		self._keys_held = {}
#		self._keys_up = {}
		self._ready = False
		self._mouse_x = 0.0
		self._mouse_y = 0.0
		self._mouse_left_down = False
		self._mouse_right_down = False
		self._mouse_middle_down = False
		
		self._mouse_buttons = pygame.mouse.get_pressed()
		self._mouse_buttons_down = list(repeat(False, 3))
		self._mouse_buttons_held = list(repeat(False, 3))
		self._mouse_buttons_up = list(repeat(False, 3))
		
		self._keys = pygame.key.get_pressed()
		self._keys_down = list(repeat(False, len(self._keys)))
		self._keys_held = list(repeat(False, len(self._keys)))
		self._keys_up   = list(repeat(False, len(self._keys)))
		
		self._key_events = []
		
		self._quit_detected = False
	
	@classmethod
	def get_key(cls, key):
		returnVal = False
		
		if cls._instance._ready:
			returnVal = cls._instance._keys[key]
			returnVal = (returnVal == 1)
		return returnVal
	
	@classmethod
	def get_key_down(cls, key):
		returnVal = False
		if cls._instance._ready:
			returnVal = cls._instance._keys_down[key]
			returnVal = (returnVal == 1)
		return returnVal

	@classmethod
	def get_key_up(cls, key):
		returnVal = False
		if cls._instance._ready:
			returnVal = cls._instance._keys_up[key]
			returnVal = (returnVal == 1)
		return returnVal
	
	@classmethod
	def get_key_events(cls):
		return cls._instance._key_events
	
	@classmethod
	def get_button(cls, button):
		returnVal = False
		
		if cls._instance._ready:
			returnVal = cls._instance._mouse_buttons_held[button]
			returnVal = (returnVal == 1)
		return returnVal
	
	@classmethod
	def get_button_down(cls, button):
		returnVal = False
		if cls._instance._ready:
			returnVal = cls._instance._mouse_buttons_down[button]
			returnVal = (returnVal == 1)
		return returnVal

	@classmethod
	def get_button_up(cls, button):
		returnVal = False
		if cls._instance._ready:
			returnVal = cls._instance._mouse_buttons_up[button]
			returnVal = (returnVal == 1)
		return returnVal
	
	@classmethod
	def set_mouse_pos(cls, pos_x, pos_y):
		cls._instance._mouse_x = pos_x
		cls._instance._mouse_y = pos_y
	
	@classmethod
	def get_mouse_move(cls):
		return cls._instance._mouse_x, cls._instance._mouse_y
	
	@classmethod
	def get_mouse_left(cls):
		return cls._instance._mouse_buttons_held[cls.MOUSE_LEFT]
	
	@classmethod
	def get_mouse_right(cls):
		return cls._instance._mouse_buttons_held[cls.MOUSE_RIGHT]
	
	@classmethod
	def get_mouse_middle(cls):
		return cls._instance._mouse_buttons_held[cls.MOUSE_MIDDLE]
	
	@classmethod
	def get_quit_detected(cls):
		return cls._instance._quit_detected
	
	def on_frame_start(self):
		self._process_input()
	
	def _process_input(self):

		# Set mouse position
		self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
		
		self._mouse_buttons = pygame.mouse.get_pressed()
		
		for button in range(0, len(self._mouse_buttons)):
			# If the button  is pressed and has been so for more than one frame
			if self._mouse_buttons[button] and \
			   self._mouse_buttons_down[button] and \
			   not self._mouse_buttons_held[button]:
				# Assign the button as held
				self._mouse_buttons_held[button] = True
				# Ensure that it is no longer marked as up
				self._mouse_buttons_down[button] = False
				
			
			# If the button is pressed and not yet marked as down and not held
			if self._mouse_buttons[button] and \
			   not self._mouse_buttons_down[button] and \
			   not self._mouse_buttons_held[button]:
				self._mouse_buttons_down[button] = True
			
			# Else if the button is not pressed and it has been either down or held
			if not self._mouse_buttons[button] and \
			   ( self._mouse_buttons_down[button] or \
			     self._mouse_buttons_held[button] ):
				# Mark the button as up
				self._mouse_buttons_up[button] = True
				# Ensure that it isn't marked as held or down
				self._mouse_buttons_down[button] = False
				self._mouse_buttons_held[button] = False
			
			# If the button has already been registered as up
			# then on the next frame reset it to false 
			elif not self._mouse_buttons[button] and \
			   self._mouse_buttons_up[button]:
				self._mouse_buttons_up[button] = False
		
		# Keyboard
		self._keys = pygame.key.get_pressed()
				
		# Check for Keys pressed this frame
		for key in range(0, len(self._keys)):
#		for key in self._keys.keys():
			
			# If the key is pressed and has been so for more than one frame
			if self._keys[key] and \
			   self._keys_down[key] and \
			   not self._keys_held[key]:
				# Assign the key as held
				self._keys_held[key] = True
				# Ensure that it is no longer marked as up
				self._keys_down[key] = False
				
			
			# If the key is pressed and not yet marked as down and not held
			if self._keys[key] and \
			   not self._keys_down[key] and \
			   not self._keys_held[key]:
				self._keys_down[key] = True
			
			# Else if the key is not pressed and it has been either down or held
			if not self._keys[key] and \
			   ( self._keys_down[key] or \
			     self._keys_held[key] ):
				# Mark the key as up
				self._keys_up[key] = True
				# Ensure that it isn't marked as held or down
				self._keys_down[key] = False
				self._keys_held[key] = False
			
			# If the key has already been registered as up
			# then on the next frame reset it to false 
			elif not self._keys[key] and \
			   self._keys_up[key]:
				self._keys_up[key] = False
		
		self._ready = True
		
		# Clear on each frame
		self._key_events = []		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self._key_events.append(event)
			elif event.type == pygame.KEYUP:
				self._key_events.append(event)
			elif event.type == pygame.QUIT:
				self._quit_detected = True
		
		# Remove all other events from the pygame eventlist
		pygame.event.clear()
			

#class InputProcessor(object):
#
#	def __init__(self):
#		self._input = GetInput()
#		self._input._keys = pygame.key.get_pressed()
#		self._input._keys_down = list(False for i in range(len(self._input._keys)))
#		self._input._keys_held = list(False for i in range(len(self._input._keys)))
#		self._input._keys_up   = list(False for i in range(len(self._input._keys)))
#		
#		self._initial_mouse_down = True
#		
#	def _process_input(self):
#		eventlist = pygame.event.get()
#		
#		# Mouse
#		left_down = pygame.mouse.get_pressed()[0]
#		# If the left mouse button is down
#		# Hide the cursor
#		pygame.mouse.set_visible(not left_down)
#		# Send Mouse Movement events 
#		if left_down:
#			
#			if not self._initial_mouse_down:
#				self._input._mouse_x, self._input._mouse_y = pygame.mouse.get_pos()
#				self._input._mouse_x -= 400
#				self._input._mouse_y -= 300
#			else:
#				self._initial_mouse_down = False
#			pygame.mouse.set_pos(400,300)
#		else:
#			self._initial_mouse_down = True
#		
#		# Keyboard
#		self._input._keys = pygame.key.get_pressed()
#		
#		# Check for Keys pressed this frame
#		for key in range(0, len(self._input._keys)):
##		for key in self._input._keys.keys():
#			
#			# If the key is pressed and has been so for more than one frame
#			if self._input._keys[key] and \
#			   self._input._keys_down[key] and \
#			   not self._input._keys_held[key]:
#				# Assign the key as held
#				self._input._keys_held[key] = True
#				# Ensure that it is no longer marked as up
#				self._input._keys_down[key] = False
#				
#			
#			# If the key is pressed and not yet marked as down and not held
#			if self._input._keys[key] and \
#			   not self._input._keys_down[key] and \
#			   not self._input._keys_held[key]:
#				self._input._keys_down[key] = True
#			
#			# Else if the key is not pressed and it has been either down or held
#			if not self._input._keys[key] and \
#			   ( self._input._keys_down[key] or \
#			     self._input._keys_held[key] ):
#				# Mark the key as up
#				self._input._keys_up[key] = True
#				# Ensure that it isn't marked as held or down
#				self._input._keys_down[key] = False
#				self._input._keys_held[key] = False
#			
#			# If the key has already been registered as up
#			# then on the next frame reset it to false 
#			elif not self._input._keys[key] and \
#			   self._input._keys_up[key]:
#				self._input._keys_up[key] = False
#			
#		# Check for keys released this frame
#		
#		self._input._ready = True
#		
##		print "dumping events: " + str(self._input._keys)
#		for event in eventlist:
#			if event.type == pygame.QUIT \
#				or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#				
#				# Fire a Quit Event
#				QuitEvent().Send()
					