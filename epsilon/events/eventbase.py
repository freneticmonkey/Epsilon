from epsilon.events.eventmanager import EventManager


class EventBase:
    def __init__(self, event_type, data):
        self._event_type = event_type
        self._data = data
        self._is_handled = False #Limited future event scoping?
        
    @property
    def name(self):
    	return self._event_type
        
    @property
    def data(self):
    	return self._data
    
    @property
    def event_type(self):
        return self._event_type
    
    @property
    def is_handled(self):
        return self._is_handled
 
    def send(self):
        EventManager.get_instance().fire_event(self)
        
    