'''
Created on Nov 19, 2011

@author: scottporter
'''
from epsilon.events.listenerbase import ListenerBase
from epsilon.core.basesingleton import BaseSingleton

class FrameEvents:
    events = ["frame_started",
              "frame_ended"
             ]

class FrameListenerManager(BaseSingleton, ListenerBase):
    
    # Register for FrameListener Events
    def __init__(self):
        self._instance = self
        ListenerBase.__init__(self, FrameEvents.events)
        
        self.init()
    
    def init(self):
        pass
    
    # Handle Events
    def _process_event(self, new_event):
        if new_event.name == "frame_started":
            self.on_frame_start()
        elif new_event.name == "frame_ended":
            self.on_frame_end()
    
    def on_frame_start(self):
        pass
    
    def on_frame_end(self):
        pass

class FrameListener(object):
    pass