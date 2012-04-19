import pygame

class Window(object):
	def __init__(self):
		self._width = 800
		self._height = 600
		
		# Start PyGame
		pygame.init()
	
	def __del__(self):
		self.Shutdown()
	
	@property
	def width(self):
		return self._width
	
	@property
	def height(self):
		return self._height
	
	def init(self, width, height):
		self._width = width
		self._height = height
		
		# Kick off initialisation of the Window
		self.InitialiseDisplay(width, height)
		
	def shutdown(self):
		if pygame:
			pygame.quit()
		
	# This function will be overwritten by children
	# i.e. Renderer Objects
	def initialise_display(self, width, height):
		pygame.display.set_mode((width,height))
		
	def _flip(self):
		pygame.display.flip()
		
		
		