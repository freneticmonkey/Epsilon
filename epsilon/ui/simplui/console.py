import pyglet

from dialogue import Dialogue
from label import Label
from layout import VLayout, HLayout
from text_input import TextInput
from folding_box import FoldingBox
from slider import Slider

class Console(Dialogue):
	"""Console Window that contains x lines of text"""
	def __init__(self, title, lines=10, width=750, max_buffer=400, **kwargs):

		Dialogue.__init__(self, title, **kwargs)

		self._line_num = lines
		self._width = width
		self._lines = []

		for i in range(0, self._line_num):
			self._lines.append(Label('',w=self._width))

		# As there isn't a virtical slider currently implemented in simplui
		# I'm just going to use a horizontal one to save time here.
		self._lines.append(Slider(w=self._width,value=1.0,action=self._on_scroll))
		self._lines.append(TextInput(text='>>>',w=self._width))

		#children = [Label('',w=390) for i in range(0, self._lines)]+[TextInput(w=390),]
		
		content = FoldingBox('Output',
							 collapsed=True,
							 content=VLayout(autosizex=True,
						  		  		     hpadding=0,
						  				     children=self._lines)
							)

		self._set_content(content)

		self._max_buffer = max_buffer
		self._console_text = []

		self._is_scrolling = False

	def new_line(self, text):

		if len(self._console_text) > self._max_buffer:
			del self._console_text[0]
		self._console_text.append(text)

		if not self._is_scrolling:
			end_start = 0
			if len(self._console_text) > self._line_num:
				end_start = len(self._console_text) - self._line_num

			self._update_text(end_start)

	def _update_text(self, start_line):
		pt = self._console_text[start_line:]

		if len(pt) > self._line_num:
			pt = self._console_text[start_line:start_line+self._line_num]

		for i in range(0, len(pt)-1):
			self._lines[i].text = pt[i]

	def _on_scroll(self, slider):
		self._is_scrolling = not slider._value == 1.0

		if self._is_scrolling and len(self._console_text) > self._line_num:
			pos = int(len(self._console_text) * slider._value)
			if pos > (self._line_num/2):
				pos -= self._line_num / 2

			if (len(self._console_text) - pos) < self._line_num:
				pos = len(self._console_text) - self._line_num
			
			self._update_text(pos)



