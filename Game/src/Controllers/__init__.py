

from Utils.Logger import Logger


class BaseController:

    def handleEvents(self, events):
        try:
            for event in events:
                try:
                    self.handleInput(event)
                except Exception as e:
                    Logger.error("BaseController.handleEvents", e)
        except Exception as e:
            Logger.error("BaseController.handleEvents", e)

    def handleInput(self, event):
        return None


