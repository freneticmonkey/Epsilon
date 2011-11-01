import pygame

class Window(object):
	def __init__(self):
		self._width = 800
		self._height = 600
	
	def __del__(self):
		self.Shutdown()
	
	@property
	def width(self):
		return self._width
	
	@property
	def height(self):
		return self._height
	
	def Init(self, width, height):
		self._width = width
		self._height = height
		
		# Start PyGame
		pygame.init()
		
		# Kick off initialisation of the Window
		self.InitialiseDisplay(width, height)
		
	def Shutdown(self):
		if pygame:
			pygame.quit()
		
	# This function will be overwritten by children
	# i.e. Renderer Objects
	def InitialiseDisplay(self, width, height):
		pygame.display.set_mode((width,height))
		
	def _flip(self):
		pygame.display.flip()
		
		
		