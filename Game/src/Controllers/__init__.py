"""
Controllers package

Defines shared base classes for controllers.
"""

from Utils.Logger import Logger


class BaseController:
    """
    Base controller providing a unified interface for input handling.

    Subclasses can override:
      - handle_events(self, events): frame-based processing of a list of events
      - handle_input(self, event): reaction to a single input event
    """

    def handle_events(self, events):
        """
        Handle a batch of events for this frame.

        Args:
            events: iterable of pygame events
        """
        try:
            # Default implementation: delegate to handle_input for each event
            for event in events:
                try:
                    self.handle_input(event)
                except Exception as e:
                    Logger.error("BaseController.handle_events", e)
        except Exception as e:
            Logger.error("BaseController.handle_events", e)

    def handle_input(self, event):
        """
        Handle a single input event.

        Subclasses should override this to react to specific events.
        """
        # Default: no-op
        return None


