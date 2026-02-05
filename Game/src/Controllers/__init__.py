"""
Controllers package

Defines shared base classes for controllers.
"""

from Utils.Logger import Logger


class BaseController:
    """
    Base controller providing a unified interface for input handling.

    Subclasses can override:
      - handleEvents(self, events): frame-based processing of a list of events
      - handleInput(self, event): reaction to a single input event
    """

    def handleEvents(self, events):
        """
        Handle a batch of events for this frame.

        Args:
            events: iterable of pygame events
        """
        try:
            # Default implementation: delegate to handleInput for each event
            for event in events:
                try:
                    self.handleInput(event)
                except Exception as e:
                    Logger.error("BaseController.handleEvents", e)
        except Exception as e:
            Logger.error("BaseController.handleEvents", e)

    def handleInput(self, event):
        """
        Handle a single input event.

        Subclasses should override this to react to specific events.
        """
        # Default: no-op
        return None

    # Backward compatible aliases
    def handle_events(self, events):
        """Legacy alias."""
        return self.handleEvents(events)
    
    def handle_input(self, event):
        """Legacy alias."""
        return self.handleInput(event)


