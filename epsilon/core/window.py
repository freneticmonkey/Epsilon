from epsilon.frameworks.frameworkmanager import FrameworkManager

class Window(object):
	def __init__(self):
		self._width = 800
		self._height = 600
		self._title = "Epsilon Engine"
		
		self._framework = FrameworkManager.framework()
	
	def __del__(self):
		self.shutdown()
	
	@property
	def width(self):
		return self._width
	
	@property
	def height(self):
		return self._height
	
	def init(self, width=None, height=None, title=None):
		if not width is None:
			self._width = width
			
		if not height is None:
			self._height = height
			
		if not title is None:
			self._title = title
		
		# Kick off initialisation of the Window
		self._framework.initialise_display(self._width, self._height, self._title)
		
	def shutdown(self):
		pass
	
	def draw(self):
		pass
		