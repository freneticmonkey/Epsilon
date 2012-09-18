from epsilon.core.basesingleton import BaseSingleton

class RenderSettings(BaseSingleton):

	@classmethod
	def get_setting(cls, name):
		return cls.get_instance()._get_setting(name)

	@classmethod
	def set_setting(cls, name, value):
		cls.get_instance()._set_setting(name, value)

	def __init__(self):
		self._settings = {}

	@property
	def settings(self):
		return self._settings

	def _get_setting(self, name):
		ret_val = None
		if name in self._settings:
			ret_val = self._settings[name]

		return ret_val

	def _set_setting(self, name, value):
		self._settings[name] = value