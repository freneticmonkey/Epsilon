from epsilon.events.listenerbase import ListenerBase
from epsilon.logging.logger import Logger

class RenderListener(ListenerBase):
    def __init__(self, renderOps):
        self._render_ops = renderOps
        self._event_type = 'RenderEvent'
        ListenerBase.__init__(self, self._event_type)
        
    def _process_event(self):
        Logger.Log('RenderListener. Received Render Event(s).')
        
        length = len(self._events)
        
        #Debug print Events. 
        if length > 0:
            Logger.Log('New Render Listener event is: ' + self._events[length-1]._event_type)
            
        # Process Render events here - triggering relevant RenderCore Functions
        for new_event in self._events:
            #Process Event contents 
            if new_event._event_type == 'RenderEvent':
            
                # All RenderEvents' data contains another eventType breakdown within the eventData
                event_data = new_event._event_data
            
                if event_data._event_type == 'AddEntity':
                    entName = event_data._entityName
                    entMesh = event_data._entityMesh                    
                    self._render_ops.addEntity(entName, entMesh)
                    
                #Process Other RenderEvents here
                