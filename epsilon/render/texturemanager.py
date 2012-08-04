'''
Created on Oct 8, 2011

@author: scottporter
'''
import os

from epsilon.render.texture import Texture
from epsilon.logging import Logger
from epsilon.core.basemanager import BaseSingleton

# This class holds all of the Texture objects


class TextureManager(BaseSingleton):
	
	def __init__(self):
		self._textures = []
	
	def add_texture(self, texture_obj):
		if isinstance(texture_obj, Texture):
			self._textures.append(texture_obj)
	
#	def create_texture(self, filename):
#		if os.path.exists(filename):
#			self._textures.append(Texture(filename))
#		else:
#			Logger.Log("TextureERROR: Texture file %s doesn't exist" % filename)
#			name = "Load Fail."
#		
#		return name

	@property
	def textures(self):
		return self._textures
			
	def delete_texture(self, name):
		del_tex = None
		for tex in self._textures:
			if tex.name == name:
				del_tex = tex
			break
		del_tex.unload()
		self._textures.remove(del_tex)
		
	def get_texture(self, name):
		for tex in self._textures:
			if tex.name == name:
				return tex
	
	def load_textures(self):
		for tex in self._textures:
			tex.load()