'''
Created on Oct 8, 2011

@author: scottporter
'''
import os

from epsilon.render.texture import Texture
from epsilon.logging.logger import Logger
from epsilon.core.basemanager import BaseSingleton

# This class holds all of the Texture objects


class TextureManager(BaseSingleton):
	
	def __init__(self):
		self._textures = []
	
	def add_texture(self, texture_obj):
		if isinstance(texture_obj, Texture):
			self._textures.append(texture_obj)
			Logger.Log("TextureManager: Added Texture: %s" % texture_obj.name)
		else:
			Logger.Log("TextureManager: Not a texture: %s" % texture_obj.__class__.__name__)
	
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
			
	def get_texture_by_name(self, name):
		match_tex = None
		for tex in self._textures:
			if tex.name == name:
				match_tex = tex
				break
		return match_tex
	
	def get_texture_by_filename(self, filename):
		match_tex = None
		for tex in self._textures:
			if tex.filename == filename:
				match_tex = tex
				break
		return match_tex
			
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