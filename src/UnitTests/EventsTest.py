import time

from Events.EventManager import EventManager
from Events.EventBase import EventBase
from Events.ListenerBase import ListenerBase

class TestListener(ListenerBase):
    event_types = ['TestEvent']
    def __init__(self): 
        ListenerBase.__init__(self, self.event_types)
        self._rec_events = 0
        
    def _process_event(self, new_event):
        self._rec_events += 1
#        print 'Received Event. Inside Test Listener'
#        print 'new event is: ' + new_event._event_type
        
class TestEvent(EventBase):
    _event_type = 'TestEvent'
    def __init__(self): 
        EventBase.__init__(self, self._event_type, None)
#        print 'Created Event: ' + self._event_type
        
class ATestListener(ListenerBase):
    event_types = ['AnotherTestEvent']
    def __init__(self): 
        ListenerBase.__init__(self, self.event_types)
        self._rec_events = 0
        
    def _process_event(self, new_event):
        self._rec_events += 1
#        print 'Received Event. Inside Another Test Listener'
#        print 'new event is: ' + new_event._event_type
        
class ATestEvent(EventBase):
    _event_type = 'AnotherTestEvent'
    def __init__(self):
        EventBase.__init__(self, self._event_type, None)
#        print 'Created Event: ' + self._event_type  
        
if __name__ == "__main__":
        
        start_time = time.time()
        
        #Create an EventCore Object
        _event_core = EventManager().get_instance()
        
        #Create Listeners
        _test_listener = TestListener()
        _a_test_listener = ATestListener()
        
        # Creating and sending Events
        
        NUM_EVENTS = 100000
        FREQ_PROCESS = 100
        
        for i in range(0, NUM_EVENTS):
            # Add a TestEvent Object
            te = TestEvent().send()
            
            # Add a different Event Object
            ate = ATestEvent().send()
            
            if i % FREQ_PROCESS == 0:
                _event_core.process_events()
        
        _event_core.process_events()
        
        end_time = time.time()
        print "Listener 1 received: %d, Listener 2 received: %d" % (_test_listener._rec_events, _a_test_listener._rec_events)
        print "Total Time: %f" % (end_time - start_time)
        
        