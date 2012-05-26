
#from Events.EventBase import EventBase 
#
##Default Event Data Object
#class RenderEventData:
#    def __init__(self, eventName, eventData):
#        self._EventName = eventName
#        self._EventData = eventData
#
##Default Render Event
#class BaseRenderEvent(EventBase):
#    def __init__(self, eventData):
#        self._EventType = 'RenderEvent'
#        self._EventData = eventData
#        EventBase.__init__(self._EventType, self._EventData)
#    
## Event Data for holding new Entities
#class AddEntityData(RenderEventData):
#    def __init__(self, entityName, entityMesh):
#        self._entityName = entityName
#        self._entityMesh = entityMesh
#        RenderEventData('AddEntity', self)
#            
## Event for adding a new Entity to the scene
#class AddEntityEvent(BaseRenderEvent):
#    def __init__(self, entityName, entityMesh):
#        BaseRenderEvent.__init__( AddEntityData(entityName, entityMesh) )
    
from Events.ListenerBase import ListenerBase
from Events.EventBase import EventBase

class ToggleWireFrameEvent(EventBase):
    def __init__(self, state):
        EventBase.__init__(self, 'ToggleWireframe', state)
        
class ToggleGridEvent(EventBase):
    def __init__(self, state):
        EventBase.__init__(self, 'ToggleGrid', state)

class RenderListener(ListenerBase):
    event_types = ['ToggleWireframe','ToggleGrid']
    def __init__(self, renderer):
        ListenerBase.__init__(self, event_types=self.event_types)
        self._renderer = renderer
        
    def _process_event(self, new_event):
        if not self._renderer is None:
            if new_event.name == 'ToggleWireframe':
                self._renderer.wireframe = new_event.data
                
            if new_event.name == 'ToggleGrid':
                self._renderer.grid = new_event.data
    