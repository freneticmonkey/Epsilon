'''
Created on May 24, 2012

@author: scottporter
'''
from Events.EventBase import EventBase

class MouseEnterUIEvent(EventBase):
    def __init__(self):
        EventBase.__init__(self, 'MouseEnterUI', True)
        
class MouseExitUIEvent(EventBase):
    def __init__(self):
        EventBase.__init__(self, 'MouseExitUI', True)