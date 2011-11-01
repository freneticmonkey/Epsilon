
from Events.EventBase import *
from Events.ListenerBase import *

#Event Constants
# As the number of events increases using hashes instead of 
# strings might be faster? - In which case make this a dict
class CoreEvents:
	events = ['CoreEvent',
			  'Quit'
			 ]

class CoreListener(ListenerBase):

    def __init__(self, quitFlag):
        self._quitFlag = quitFlag
        
        ListenerBase.__init__(self, CoreEvents.events)
        
    def _processEvent(self, event):
        if event.name == 'Quit':
            self._quitFlag = event.data
                    
    @property
    def quitting(self):
    	return self._quitFlag
        
class CoreEvent(EventBase):
    def __init__(self, eventData):
        EventBase.__init__(self, eventData)

class CoreFlagData():
    def __init__(self, flagName, flag):
        self._EventType = flagName
        self._EventData = flag        
        
class CoreFlagEvent(CoreEvent):
    def __init__(self, flagName, flag):
        CoreEvent.__init__(self, CoreFlagData(flagName, flag) )