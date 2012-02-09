from Logging import Logger
from Core.BaseSingleton import BaseSingleton

# Event Core
class EventManager( BaseSingleton ):

	def __init__(self):
		## a foo class variable
		# A list of all of the Listeners listening for events
		self._listeners = []
		
		# A list of all events since last time _processEvents was run.
		self._newEvents = []
		
		# The logger
		Logger.Log('Initialised EventCore')
	
	def __del__(self):
		self._shutdown()
	
	def _shutdown(self):
		Logger.Log('EventCore Shutdown')
		
	## Add a Listener Object to the list of listeners
	# @param newListener: The new Listener to add
	def AddListener(self, newListener):
		self._listeners.append(newListener)
		
	## Notify the appropriate listener of their events
	# @param newEvent: sends the newEvent object to all of the appropriate listeners
	def FireEvent(self, newEvent):
		# find any matching listeners
		found = False
		for listener in self._listeners:
			if newEvent.name in listener.event_types:
				#listener._notify(newEvent)
				self._newEvents.append(newEvent)
				found = True
				break
			
		if not found:
			Logger.Log('EventsCore: Event ' + newEvent._EventType + ' has no listeners.') 
		
	## Process all of the events that haven't been processed yet
	def _processEvents(self):
		for newEvent in self._newEvents:
			for listener in self._listeners:
				if newEvent.name in listener.event_types:
					listener._notify(newEvent)
				if newEvent.IsHandled:
					break
		# Delete all events
		self._newEvents = []
		