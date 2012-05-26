from epsilon.logging import Logger
from epsilon.core.basesingleton import BaseSingleton

# Event Core
class EventManager( BaseSingleton ):

	def __init__(self):
		## a foo class variable
		# A list of all of the Listeners listening for events
		self._listeners = []
		
		# A list of all events since last time _process_events was run.
		self._new_events = []
		
		# The logger
		Logger.Log('Initialised EventCore')
	
	def __del__(self):
		self._shutdown()
	
	def _shutdown(self):
		Logger.Log('EventCore Shutdown')
		
	## Add a Listener Object to the list of listeners
	# @param newListener: The new Listener to add
	def add_listener(self, new_listener):
		self._listeners.append(new_listener)
		
	## Notify the appropriate listener of their events
	# @param newEvent: sends the newEvent object to all of the appropriate listeners
	def fire_event(self, new_event):
		# find any matching listeners
		found = False
		for listener in self._listeners:
			if new_event.name in listener.event_types:
				#listener._notify(newEvent)
				self._new_events.append(new_event)
				found = True
				break
		
		if not found:
			Logger.Log('EventsCore: Event ' + new_event.event_type + ' has no listeners.') 
		
	## Process all of the events that haven't been processed yet
	def process_events(self):
		for new_event in self._new_events:
			for listener in self._listeners:
				if new_event.name in listener.event_types:
					listener.notify(new_event)
				if new_event.is_handled:
					break
		# Delete all events
		self._new_events = []
		