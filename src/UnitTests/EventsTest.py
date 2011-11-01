from Events.EventCore import *
from Events.EventBase import *
from Events.ListenerBase import *

class TestListener(ListenerBase):
    def __init__(self):
        self._EventType = 'TestEvent'
        ListenerBase.__init__(self, self._EventType)
        
    def _processEvent(self, new_event):
        print 'Received Event. Inside Test Listener'
        print 'new event is: ' + new_event._EventType
        
class TestEvent(EventBase):
    def __init__(self):
        self._EventType = 'TestEvent'
        EventBase.__init__(self, self._EventType, None)
        print 'Created Event: ' + self._EventType
        
class ATestListener(ListenerBase):
    def __init__(self):
        self._EventType = 'AnotherTestEvent'
        ListenerBase.__init__(self, self._EventType)
        
    def _processEvent(self, new_event):
        print 'Received Event. Inside Another Test Listener'
        print 'new event is: ' + new_event._EventType
        
class ATestEvent(EventBase):
    def __init__(self):
        self._EventType = 'AnotherTestEvent'
        EventBase.__init__(self, self._EventType, None)
        print 'Created Event: ' + self._EventType  
        
class EventsTest:
    def __init__(self):
        
        #Create an EventCore Object
        self._eventCore = EventCore()
        
        #Create Listeners
        self._testListener = TestListener()
        self._aTestListener = ATestListener()
                
        # Attaching Listeners
        # Add an TestListener Object
#        self._eventsCore._addListener(self._testListener)
        
        # Add different Listener Object
#        self._eventsCore._addListener(self._anTestListener)
        
        # Creating Events
        # Add a TestEvent Object
        te = TestEvent()
        te.Send()
#        self._eventsCore._newEvent(TestEvent())
        
        # Add a different Event Object
        ate = ATestEvent()
        ate.Send()
#        self._eventsCore._newEvent(ATestEvent())        
        
        # Processing Events within listeners
        # Process Listener for Test events
#        self._testListener._processEvent()
        
        # ProcessListener for the other events
#        self._anTestListener._processEvent()
        

EventsTest()
    
    
        