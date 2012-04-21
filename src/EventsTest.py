from Events.EventManager import EventManager
from Events.EventBase import EventBase
from Events.ListenerBase import ListenerBase

class TestListener(ListenerBase):
    def __init__(self):
        self._EventType = 'TestEvent'
        ListenerBase.__init__(self, self._event_type)
        
    def _process_event(self, new_event):
        print 'Received Event. Inside Test Listener'
        print 'new event is: ' + new_event._event_type
        
class TestEvent(EventBase):
    def __init__(self):
        self._EventType = 'TestEvent'
        EventBase.__init__(self, self._event_type, None)
        print 'Created Event: ' + self._event_type
        
class ATestListener(ListenerBase):
    def __init__(self):
        self._EventType = 'AnotherTestEvent'
        ListenerBase.__init__(self, self._event_type)
        
    def _process_event(self, new_event):
        print 'Received Event. Inside Another Test Listener'
        print 'new event is: ' + new_event._event_type
        
class ATestEvent(EventBase):
    def __init__(self):
        self._EventType = 'AnotherTestEvent'
        EventBase.__init__(self, self._event_type, None)
        print 'Created Event: ' + self._event_type  
        
if __name__ == "__main__":
        
        #Create an EventCore Object
        _event_core = EventManager()
        
        #Create Listeners
        _test_listener = TestListener()
        _a_test_listener = ATestListener()
                
        # Attaching Listeners
        # Add an TestListener Object
#        self._eventsCore._addListener(self._testListener)
        
        # Add different Listener Object
#        self._eventsCore._addListener(self._anTestListener)
        
        # Creating Events
        # Add a TestEvent Object
        te = TestEvent()
        te.send()
#        self._eventsCore._newEvent(TestEvent())
        
        # Add a different Event Object
        ate = ATestEvent()
        ate.send()
#        self._eventsCore._newEvent(ATestEvent())        
        
        # Processing Events within listeners
        # Process Listener for Test events
#        self._testListener._processEvent()
        
        # ProcessListener for the other events
#        self._anTestListener._processEvent()    
        