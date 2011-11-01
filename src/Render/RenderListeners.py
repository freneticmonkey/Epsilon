from Events.ListenerBase import * 
from Logging import LoggerCore 

class RenderListener(ListenerBase):
    def __init__(self, renderOps):
        self._renderOps = renderOps
        self._EventType = 'RenderEvent'
        ListenerBase.__init__(self, self._EventType)
        
    def _processEvents(self):
        LoggerCore()._print('RenderListener. Received Render Event(s).')
        
        length = len(self._Events)
        
        #Debug print Events. 
        if length > 0:
            LoggerCore()._print('New Render Listener event is: ' + self._Events[length-1]._EventType)
            
        # Process Render events here - triggering relevant RenderCore Functions
        for newEvent in self._Events:
            #Process Event contents 
            if newEvent._eventType == 'RenderEvent':
            
                # All RenderEvents' data contains another eventType breakdown within the eventData
                eventData = newEvent._eventData
            
                if eventData._eventType == 'AddEntity':
                    entName = eventData._entityName
                    entMesh = eventData._entityMesh                    
                    self._renderOps.addEntity(entName, entMesh)
                    
                #Process Other RenderEvents here
                