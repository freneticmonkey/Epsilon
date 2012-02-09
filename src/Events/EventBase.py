from Events.EventManager import EventManager


class EventBase:
    def __init__(self, eventType, data):
        self._EventType = eventType
        self._Data = data
        self._isHandled = False #Limited future event scoping?
        
    @property
    def name(self):
    	return self._EventType
        
    @property
    def data(self):
    	return self._Data
    
    @property
    def IsHandled(self):
        return self._isHandled
 
    def Send(self):
        EventManager.get_instance().FireEvent(self)
        
    