'''
Created on Oct 8, 2011

@author: scottporter
'''
import os

from Render.Texture import Texture
from Logging import Logger

# This class holds all of the Texture objects

_instance = None

def GetTextureManager():
    global _instance
    if _instance is None:
        _instance = TextureManager()
    return _instance

_texture_id = 0

def GetTexId():
	global _texture_id
	
	_texture_id += 1
	return _texture_id

class TextureManager(object):
	
	def __init__(self):
		self._textures = []
	
	def CreateTexture(self, filename):
		
		if os.path.exists(filename):
			name = "Texture_" + str(GetTexId())
			new_tex = Texture(filename, name )
			
			self._textures.append(new_tex)
						
		else:
			Logger.Log("TextureERROR: Texture file %s doesn't exist" % filename)
			name = "Load Fail."
			
		return name
			
	def DeleteTexture(self, name):
		del_tex = None
		for tex in self._textures:
			if tex.name == name:
				del_tex = tex
			break
		del_tex.Delete()
		self._textures.remove(del_tex)
		
	def GetTexture(self, name):
		for tex in self._textures:
			if tex.name == name:
				return tex
	
	def LoadTextures(self):
		for tex in self._textures:
			tex.Load()