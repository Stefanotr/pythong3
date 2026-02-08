

from Utils.Logger import Logger


class BaseController:
 

    def handle_events(self, events):
    
        try:
            for event in events:
                try:
                    self.handle_input(event)
                except Exception as e:
                    Logger.error("BaseController.handle_events", e)
        except Exception as e:
            Logger.error("BaseController.handle_events", e)

    def handle_input(self, event):
     
        return None


