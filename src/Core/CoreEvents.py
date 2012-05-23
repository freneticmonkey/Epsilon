
from Events.EventBase import EventBase
from Events.ListenerBase import ListenerBase

from Frameworks.FrameworkManager import FrameworkManager

#Event Constants
# As the number of events increases using hashes instead of 
# strings might be faster? - In which case make this a dict
class CoreEvents:
    events = ['CoreEvent',
			  'Quit'
			 ]

class CoreListener(ListenerBase):

    def __init__(self, quit_flag):
        self._quit_flag = quit_flag
        
        ListenerBase.__init__(self, CoreEvents.events)
        
    def _process_event(self, event):
        if event.name == 'Quit':
            #self._quit_flag = event.data
            
            # Send the Quit event to the FrameworkManager
            if event.data:
                FrameworkManager.get_instance().stop()
                    
#    @property
#    def quitting(self):
#        return self._quit_flag
        
class CoreEvent(EventBase):
    def __init__(self, event_data):
        EventBase.__init__(self, event_data)

class CoreFlagData():
    def __init__(self, flag_name, flag):
        self._event_type = flag_name
        self._event_data = flag        
        
class CoreFlagEvent(CoreEvent):
    def __init__(self, flag_name, flag):
        CoreEvent.__init__(self, CoreFlagData(flag_name, flag) )