'''
Created on Oct 8, 2011

@author: scottporter
'''
import os

from Render.Texture import Texture
from Logging import Logger

# This class holds all of the Texture objects

from Core.BaseManager import BaseSingleton

class TextureManager(BaseSingleton):
	_texture_id = 0
	
	def __init__(self):
		self._textures = []
		
	def _get_texture_id(self):
		self._texture_id += 1
		return self._texture_id
	
	def create_texture(self, filename):
		if os.path.exists(filename):
			name = "Texture_" + str(self._get_texture_id())
			new_tex = Texture(filename, name )
			
			self._textures.append(new_tex)
		else:
			Logger.Log("TextureERROR: Texture file %s doesn't exist" % filename)
			name = "Load Fail."
		
		return name
			
	def delete_texture(self, name):
		del_tex = None
		for tex in self._textures:
			if tex.name == name:
				del_tex = tex
			break
		del_tex.Delete()
		self._textures.remove(del_tex)
		
	def get_texture(self, name):
		for tex in self._textures:
			if tex.name == name:
				return tex
	
	def load_textures(self):
		for tex in self._textures:
			tex.Load()