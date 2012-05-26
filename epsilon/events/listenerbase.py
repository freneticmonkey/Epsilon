from epsilon.logging import Logger
from epsilon.events.eventmanager import EventManager

class ListenerBase(object):
    def __init__(self, event_types):
        #The events that the listener will listen to
        self._event_types = event_types
        
        #Event List 
        self._events = []
        
        self._register()
        
    @property
    def listener_name(self):
    	return self.__class__
    	
    @property
    def event_types(self):
    	return self._event_types
 
    def _register(self):
        EventManager.get_instance().add_listener(self)
        
    #These should only be called by the EventCore Object
    #
    
    #Adds event(s) to the Listener.
    def notify(self, event):
        if isinstance(event, object):
            self._events.append(event)
        elif isinstance(event, list):
            self._events.extend(event)
        else:
            Logger.Log("WARNING: Trying to add invalid event(s): " + event.__class__)
        
        self._check_events()
    #
    ###############################
    
    def _check_events(self):
        for new_event in self._events:
            if new_event.name in self.event_types:
                self._process_event(new_event)
        # Clear events after checking
        self._events = []
        
    # This is called when the event list has been updated,
    # this will be overridden in inheriting classes
    def _process_event(self, new_event):
        pass