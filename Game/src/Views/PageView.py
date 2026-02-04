"""
PageView Module

Base class for all page views in the game.
Provides common functionality for window creation, background loading, and rendering.
"""

import pygame
import os
from Utils.Logger import Logger


# === PAGE VIEW BASE CLASS ===

class PageView:
    """
    Base class for all page views.
    Handles window initialization, background image loading, and basic drawing functionality.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name="none", width=800, height=800, RESIZABLE=0, backgroud_image="Game/Assets/welcomePage.png"):
        """
        Initialize the page view with window settings and background image.
        
        Args:
            name: Window title/caption
            width: Window width in pixels
            height: Window height in pixels
            RESIZABLE: Pygame flag for window resizability (0 or pygame.RESIZABLE)
            backgroud_image: Path to background image file
        """
        try:
            Logger.debug("PageView.__init__", "Initializing page view", name=name, width=width, height=height)
            
            # Set window position to center
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except Exception as e:
                Logger.error("PageView.__init__", e)
            
            # Pygame initialization is expected to be done by the caller (e.g., WelcomePageView)
            if not pygame.get_init():
                Logger.error("PageView.__init__", "Pygame not initialized. PageView requires pygame to be initialized before instantiation.")
                raise RuntimeError("Pygame must be initialized before creating PageView")
            
            # Store properties
            self.name = name
            self.width = width
            self.height = height
            # If caller explicitely provided a RESIZABLE flag, use it; otherwise default to pygame.RESIZABLE
            self.resizable = RESIZABLE if RESIZABLE else pygame.RESIZABLE
            self.backgroud_image = backgroud_image

            # Create or reuse display surface
            try:
                existing = pygame.display.get_surface()
                if existing is not None:
                    # Reuse existing display surface and adopt its current size
                    self.screen = existing
                    self.width, self.height = self.screen.get_size()
                    # Make sure window is resizable by setting mode if caller didn't force non-resizable
                    if not RESIZABLE:
                        try:
                            # Recreate window with RESIZABLE flag while preserving size
                            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                            self.resizable = pygame.RESIZABLE
                        except Exception:
                            # If recreate fails (platform restrictions), keep existing surface
                            pass
                    pygame.display.set_caption(self.name)
                    Logger.debug("PageView.__init__", "Reusing existing display surface", size=(self.width, self.height), resizable=self.resizable)
                else:
                    # No existing surface -> create one
                    self.screen = pygame.display.set_mode((self.width, self.height), self.resizable)
                    pygame.display.set_caption(self.name)
                    Logger.debug("PageView.__init__", "Display surface created", size=(self.width, self.height), resizable=self.resizable)
            except Exception as e:
                Logger.error("PageView.__init__", e)
                raise
            
            # Load original background image (store for rescaling)
            try:
                self._original_background = pygame.image.load(self.backgroud_image)
                # Scale to initial window size
                self.background = pygame.transform.scale(self._original_background, (self.width, self.height))
                Logger.debug("PageView.__init__", "Background image loaded", path=backgroud_image)
            except FileNotFoundError as e:
                Logger.error("PageView.__init__", e)
                # Create a default black background if image not found
                self._original_background = None
                self.background = pygame.Surface((self.width, self.height))
                self.background.fill((0, 0, 0))
                Logger.debug("PageView.__init__", "Using default black background")
            except Exception as e:
                Logger.error("PageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("PageView.__init__", e)
            raise

    # === BACKGROUND RESCALING ===
    
    def rescaleBackground(self, new_width, new_height):
        """
        Rescale the background image to match new window dimensions.
        
        Args:
            new_width: New window width in pixels
            new_height: New window height in pixels
        """
        try:
            # Update stored dimensions
            self.width = new_width
            self.height = new_height
            
            # Rescale background if original image exists
            if self._original_background is not None:
                self.background = pygame.transform.scale(self._original_background, (new_width, new_height))
                Logger.debug("PageView.rescaleBackground", "Background rescaled", 
                           width=new_width, height=new_height)
            else:
                # Create new default background if no original image
                self.background = pygame.Surface((new_width, new_height))
                self.background.fill((0, 0, 0))
                Logger.debug("PageView.rescaleBackground", "Default background resized", 
                           width=new_width, height=new_height)
        except Exception as e:
            Logger.error("PageView.rescaleBackground", e)

    # === RENDERING ===
    
    def draw(self):
        """
        Draw the background image to the screen.
        Should be called at the start of each frame's rendering.
        """
        try:
            # If pygame display is not initialized or surface is gone, skip drawing
            if not pygame.get_init() or pygame.display.get_surface() is None:
                return

            # Get current screen size to ensure background matches
            current_width, current_height = self.screen.get_size()
            
            # Rescale if dimensions don't match
            if current_width != self.width or current_height != self.height:
                self.rescaleBackground(current_width, current_height)
            
            # Draw background, scaling to fit if needed
            try:
                self.screen.blit(self.background, (0, 0))
            except Exception as e:
                # If blit fails, try rescaling and blitting again
                Logger.debug("PageView.draw", "Blit failed, rescaling background", error=str(e))
                self.rescaleBackground(current_width, current_height)
                self.screen.blit(self.background, (0, 0))
        except Exception as e:
            Logger.error("PageView.draw", e)

    # === GENERIC GAME LOOP HOOKS ===

    def handle_events(self, events):
        """
        Handle a batch of events for this page.

        Subclasses can override this to implement their own logic.

        Args:
            events: iterable of pygame events

        Returns:
            bool: True to keep running, False to exit the loop.
        """
        # Default: keep running and ignore events
        return True

    def update(self):
        """
        Update page state.

        Called once per frame after event handling.
        """
        # Default: no-op
        return None

    def render(self):
        """
        Render the page content.

        Called once per frame after update.
        """
        # Default: just draw the background
        self.draw()

    def run(self):
        """
        Generic main loop for simple pages.

        Subclasses can either:
          - use this implementation by overriding handle_events/update/render
          - or override run() completely for more complex flows (with return codes).
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("PageView.run", "Generic page loop started", name=self.name)

            while running:
                try:
                    events = pygame.event.get()
                    running = self.handle_events(events)

                    if not running:
                        break

                    self.update()
                    self.render()

                    pygame.display.flip()
                    clock.tick(60)
                except Exception as e:
                    Logger.error("PageView.run", e)
                    # Continue running even if one frame fails
                    continue

            Logger.debug("PageView.run", "Generic page loop ended", name=self.name)
        except Exception as e:
            Logger.error("PageView.run", e)
            raise