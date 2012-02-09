from Logging import Logger
from Events.EventManager import EventManager

class ListenerBase(object):
    def __init__(self, eventTypes):
        #The events that the listener will listen to
        self._EventTypes = eventTypes
        
        #Event List 
        self._Events = []
        
        self._Register()
        
    @property
    def listener_name(self):
    	return self.__class__
    	
    @property
    def event_types(self):
    	return self._EventTypes
 
    def _Register(self):
        EventManager.get_instance().AddListener(self)
        
    #These should only be called by the EventCore Object
    #
    
    #Adds event(s) to the Listener.
    def _notify(self, event):
        if isinstance(event, object):
            self._Events.append(event)
        elif isinstance(event, list):
            self._Events.extend(event)
        else:
            Logger.Log("WARNING: Trying to add invalid event(s): " + event.__class__)
        
        self._checkEvents()
    #
    ###############################
    
    def _checkEvents(self):
        for newEvent in self._Events:
            if newEvent.name in self.event_types:
                self._processEvent(newEvent)
        # Clear events after checking
        self._Events = []
        
    # This is called when the event list has been updated,
    # this will be overridden in inheriting classes
    def _processEvent(self, new_event):
        pass