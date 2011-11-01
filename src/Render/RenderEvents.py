
from Events.EventBase import EventBase 

#Default Event Data Object
class RenderEventData:
    def __init__(self, eventName, eventData):
        self._EventName = eventName
        self._EventData = eventData

#Default Render Event
class BaseRenderEvent(EventBase):
    def __init__(self, eventData):
        self._EventType = 'RenderEvent'
        self._EventData = eventData
        EventBase.__init__(self._EventType, self._EventData)
    
# Event Data for holding new Entities
class AddEntityData(RenderEventData):
    def __init__(self, entityName, entityMesh):
        self._entityName = entityName
        self._entityMesh = entityMesh
        RenderEventData('AddEntity', self)
            
# Event for adding a new Entity to the scene
class AddEntityEvent(BaseRenderEvent):
    def __init__(self, entityName, entityMesh):
        BaseRenderEvent.__init__( AddEntityData(entityName, entityMesh) )
    