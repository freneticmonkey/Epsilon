from itertools import repeat

import pygame

from Core.BaseManager import FrameListenerManager

class Input(FrameListenerManager):
	# Mouse Constants
	MOUSE_LEFT = 0
	MOUSE_MIDDLE = 1
	MOUSE_RIGHT = 2
	
	# Key Constants
	KEY_0 = 48
	KEY_1 = 49
	KEY_2 = 50
	KEY_3 = 51
	KEY_4 = 52
	KEY_5 = 53
	KEY_6 = 54
	KEY_7 = 55
	KEY_8 = 56
	KEY_9 = 57
	
	KEY_A = 97
	KEY_B = 98
	KEY_C = 99
	KEY_D = 100
	KEY_E = 101
	KEY_F = 102
	KEY_G = 103
	KEY_H = 104
	KEY_I = 105
	KEY_J = 106
	KEY_K = 107
	KEY_L = 108
	KEY_M = 109
	KEY_N = 110
	KEY_O = 111
	KEY_P = 112
	KEY_Q = 113
	KEY_R = 114
	KEY_S = 115
	KEY_T = 116
	KEY_U = 117
	KEY_V = 118
	KEY_W = 119
	KEY_X = 120
	KEY_Y = 121
	KEY_Z = 122
	
	KEY_TAB = 9
	KEY_DEL = 10
	KEY_RETURN = 13
	KEY_ESCAPE = 27
	KEY_SPACE = 32
	KEY_HYPHEN = 45
	KEY_FORWARD_SLASH = 47
	KEY_EQUALS = 61
	KEY_BACKSLASH = 92
	KEY_TILDE = 96
	
	KEY_UP = 273
	KEY_DOWN = 274
	KEY_LEFT = 276
	KEY_RIGHT = 275
	
	KEY_CAPS = 301
	KEY_RIGHT_SHIFT = 303
	KEY_LEFT_SHIFT = 304
	KEY_CTRL = 306
	KEY_RIGHT_ALT = 307
	KEY_LEFT_ALT = 308
	KEY_RIGHT_CMD = 309
	KEY_LEFT_CMD = 310
	
	INPUT_HELD = 2
	INPUT_DOWN = 1
	INPUT_RELEASED = 0
	
	def __init__(self):
		FrameListenerManager.__init__(self)
	
	def init(self):
		self._ready = False
		
		self._mouse_x = 0.0
		self._mouse_y = 0.0
		self._mouse_rel_x = 0.0
		self._mouse_rel_y = 0.0
		self._mouse_left_down = False
		self._mouse_right_down = False
		self._mouse_middle_down = False
		
		# The state of the mouse buttons
		self._state_mouse_buttons = {}
		
		# The state of the keyboard keys
		self._state_keys = {}
		
		self._quit_detected = False
		
		self._framework_init()
		
		self._ready = True
		
	def _framework_init(self):
		pass
	
	@classmethod
	def get_key(cls, key):
		returnVal = False
		
		if cls._instance._ready and key in cls._instance._state_keys:
			returnVal = (cls._instance._state_keys[key] > cls.INPUT_RELEASED)
		return returnVal
	
	@classmethod
	def get_key_down(cls, key):
		returnVal = False
		if cls._instance._ready and key in cls._instance._state_keys:
			returnVal = (cls._instance._state_keys[key] == cls.INPUT_DOWN)
		return returnVal

	@classmethod
	def get_key_up(cls, key):
		returnVal = False
		if cls._instance._ready and key in cls._instance._state_keys:
			returnVal = (cls._instance._state_keys[key] == cls.INPUT_RELEASED)
		return returnVal
	
	@classmethod
	def get_button(cls, button):
		return_val = False
		
		if cls._instance._ready and \
		   button in cls._instance._state_mouse_buttons:
			return_val = cls._instance._state_mouse_buttons[button] == cls.INPUT_HELD
		return return_val
	
	@classmethod
	def get_button_down(cls, button):
		return_val = False
		
		if cls._instance._ready and \
		   button in cls._instance._state_mouse_buttons:
			return_val = cls._instance._state_mouse_buttons[button] == cls.INPUT_DOWN
		return return_val

	@classmethod
	def get_button_up(cls, button):
		return_val = False
		
		if cls._instance._ready and \
		   button in cls._instance._state_mouse_buttons:
			return_val = cls._instance._state_mouse_buttons[button] == cls.INPUT_RELEASED
		return return_val
	
	@classmethod
	def set_mouse_pos(cls, pos_x, pos_y):
		cls._instance._mouse_x = pos_x
		cls._instance._mouse_y = pos_y
		
		cls._instance._set_mouse_pos(pos_x, pos_y)
	
	@classmethod
	def get_mouse_move(cls):
		return cls._instance._mouse_x, cls._instance._mouse_y
	
	@classmethod
	def get_mouse_move_relative(cls):
		return cls._instance._mouse_rel_x, cls._instance._mouse_rel_y 
	
	@classmethod
	def get_mouse_left(cls):
		return cls.MOUSE_LEFT in cls.get_instance()._state_mouse_buttons
	
	@classmethod
	def get_mouse_right(cls):
		return cls.MOUSE_RIGHT in cls.get_instance()._state_mouse_buttons
	
	@classmethod
	def get_mouse_middle(cls):
		return cls.MOUSE_MIDDLE in cls.get_instance()._state_mouse_buttons
	
	@classmethod
	def get_quit_detected(cls):
		return cls._instance._quit_detected
	
	def on_frame_start(self):
		pass
	
	def _process_input_state(self, button, state):
		
		input_states = {}
		
		if button <= self.MOUSE_MIDDLE:
			input_states = self._state_mouse_buttons
		else:
			input_states = self._state_keys
		
		# If the button is pressed 
		if state == self.INPUT_DOWN:
			# If the button is pressed and not yet marked as down and not held
			if not button in input_states:
				input_states[button] = self.INPUT_DOWN
				
			# If the button has been down for more than one frame
			elif button in input_states and \
			     input_states[button] == self.INPUT_DOWN:
				input_states[button] = self.INPUT_HELD
			
		# If the button is not pressed
		elif state == self.INPUT_RELEASED:
			
			# If the button has been either down or held
			if button in input_states and \
			   not input_states[button] == self.INPUT_RELEASED:
				input_states[button] = self.INPUT_RELEASED
				
			# If the button is indicating that it has been released, remove
			# it from the button state dictionary
			if button in input_states and \
			   input_states[button] == self.INPUT_RELEASED:
				input_states.pop(button)
	
	# Methods over-ridden in inheriting classes
	def _process_input(self):
		pass
	
	def _set_mouse_pos(self, mouse_x, mouse_y):
		pass
	
	@classmethod
	def set_lock_mouse(cls, exclusive):
		cls._instance.set_exclusive_mouse(exclusive)
	
#		# Set mouse position
#		self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
#		
#		mouse_buttons = pygame.mouse.get_pressed()
#		
#		for button in range(0, len(mouse_buttons)):
#			
#			state = mouse_buttons[button]
#			
#			self._process_input_state(button, state)
#			
##			# If the button is pressed and has been so for more than one frame
##			if self._mouse_buttons[button] and \
##			   self._mouse_buttons_down[button] and \
##			   not self._mouse_buttons_held[button]:
##				# Assign the button as held
##				self._mouse_buttons_held[button] = True
##				# Ensure that it is no longer marked as up
##				self._mouse_buttons_down[button] = False
##					
##			# If the button is pressed and not yet marked as down and not held
##			if self._mouse_buttons[button] and \
##			   not self._mouse_buttons_down[button] and \
##			   not self._mouse_buttons_held[button]:
##				self._mouse_buttons_down[button] = True
##			
##			# Else if the button is not pressed and it has been either down or held
##			if not self._mouse_buttons[button] and \
##			   ( self._mouse_buttons_down[button] or \
##			     self._mouse_buttons_held[button] ):
##				# Mark the button as up
##				self._mouse_buttons_up[button] = True
##				# Ensure that it isn't marked as held or down
##				self._mouse_buttons_down[button] = False
##				self._mouse_buttons_held[button] = False
##			
##			# If the button has already been registered as up
##			# then on the next frame reset it to false 
##			elif not self._mouse_buttons[button] and \
##			   self._mouse_buttons_up[button]:
##				self._mouse_buttons_up[button] = False
#		
#		# Keyboard
#		keys = pygame.key.get_pressed()
#				
#		# Check for Keys pressed this frame
#		for key in range(0, len(keys)):
#			
#			state = keys[key]
#			
#			self._process_input_state(key, state)
#			
#			
##		for key in self._keys.keys():
##			
##			# If the key is pressed and has been so for more than one frame
##			if self._keys[key] and \
##			   self._keys_down[key] and \
##			   not self._keys_held[key]:
##				# Assign the key as held
##				self._keys_held[key] = True
##				# Ensure that it is no longer marked as up
##				self._keys_down[key] = False
##				
##			
##			# If the key is pressed and not yet marked as down and not held
##			if self._keys[key] and \
##			   not self._keys_down[key] and \
##			   not self._keys_held[key]:
##				self._keys_down[key] = True
##			
##			# Else if the key is not pressed and it has been either down or held
##			if not self._keys[key] and \
##			   ( self._keys_down[key] or \
##			     self._keys_held[key] ):
##				# Mark the key as up
##				self._keys_up[key] = True
##				# Ensure that it isn't marked as held or down
##				self._keys_down[key] = False
##				self._keys_held[key] = False
##			
##			# If the key has already been registered as up
##			# then on the next frame reset it to false 
##			elif not self._keys[key] and \
##			   self._keys_up[key]:
##				self._keys_up[key] = False
#		
#		self._ready = True
#		
#		# Clear on each frame
#		self._key_events = []		
#		for event in pygame.event.get():
#			if event.type == pygame.KEYDOWN:
#				self._key_events.append(event)
#			elif event.type == pygame.KEYUP:
#				self._key_events.append(event)
#			elif event.type == pygame.QUIT:
#				self._quit_detected = True
#		
#		# Remove all other events from the pygame eventlist
#		pygame.event.clear()
		
	
	
	
