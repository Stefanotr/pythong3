import pygame
import os
from Utils.Logger import Logger

class PageView:
    def __init__(self, name="none", width=800, height=800, resizable=0, background_image="Game/Assets/welcomePage.png"):
        try:
            Logger.debug("PageView.__init__", "Initializing page view", name=name, width=width, height=height)
            
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except Exception as e:
                Logger.error("PageView.__init__", e)
            
            if not pygame.get_init():
                Logger.error("PageView.__init__", "Pygame not initialized. PageView requires pygame to be initialized before instantiation.")
                raise RuntimeError("Pygame must be initialized before creating PageView")
            
            self.name = name
            self.width = width
            self.height = height
            self.resizable = resizable if resizable else pygame.RESIZABLE
            self.background_image = background_image
            self._original_background = None

            try:
                existing = pygame.display.get_surface()
                if existing is not None:
                    self.screen = existing
                    self.width, self.height = self.screen.get_size()
                    if not resizable:
                        try:
                            self.setWindowSize(self.width, self.height, pygame.RESIZABLE)
                            self.resizable = pygame.RESIZABLE
                        except Exception:
                            pass
                    pygame.display.set_caption(self.name)
                    Logger.debug("PageView.__init__", "Reusing existing display surface", size=(self.width, self.height), resizable=self.resizable)
                else:
                    self.setWindowSize(self.width, self.height, self.resizable)
                    Logger.debug("PageView.__init__", "Display surface created", size=(self.width, self.height), resizable=self.resizable)
            except Exception as e:
                Logger.error("PageView.__init__", e)
                raise
            
            try:
                if self.background_image and isinstance(self.background_image, str) and os.path.exists(self.background_image):
                    try:
                        self._original_background = pygame.image.load(self.background_image)
                        self.background = pygame.transform.scale(self._original_background, (self.width, self.height))
                        Logger.debug("PageView.__init__", "Background image loaded", path=self.background_image)
                    except Exception as e:
                        Logger.error("PageView.__init__", e)
                        self._original_background = None
                        self.background = pygame.Surface((self.width, self.height))
                        self.background.fill((0, 0, 0))
                        Logger.debug("PageView.__init__", "Using default black background due to load failure")
                else:
                    self._original_background = None
                    self.background = pygame.Surface((self.width, self.height))
                    self.background.fill((0, 0, 0))
                    Logger.debug("PageView.__init__", "Using default black background (no image provided or file missing)", path=self.background_image)
            except Exception as e:
                Logger.error("PageView.__init__", e)
                self._original_background = None
                self.background = pygame.Surface((self.width, self.height))
                self.background.fill((0, 0, 0))
                
        except Exception as e:
            Logger.error("PageView.__init__", e)
            raise

    def rescaleBackground(self, new_width, new_height):
        try:
            self.width = new_width
            self.height = new_height
            
            if self._original_background is not None:
                self.background = pygame.transform.scale(self._original_background, (new_width, new_height))
                Logger.debug("PageView.rescaleBackground", "Background rescaled", 
                           width=new_width, height=new_height)
            else:
                self.background = pygame.Surface((new_width, new_height))
                self.background.fill((0, 0, 0))
                Logger.debug("PageView.rescaleBackground", "Default background resized", 
                           width=new_width, height=new_height)
        except Exception as e:
            Logger.error("PageView.rescaleBackground", e)

    def setWindowSize(self, new_width, new_height, flags=None):
        try:
            try:
                import os
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except Exception as e:
                Logger.error("PageView.setWindowSize", e)

            try:
                used_flags = flags if flags is not None else self.resizable
                screen = pygame.display.set_mode((new_width, new_height), used_flags)
                self.screen = screen
                self.width, self.height = self.screen.get_size()
                pygame.display.set_caption(self.name)

                try:
                    self.rescaleBackground(self.width, self.height)
                except Exception as e:
                    Logger.error("PageView.setWindowSize", e)

                Logger.debug("PageView.setWindowSize", "Window mode set", width=self.width, height=self.height, flags=used_flags)
            except Exception as e:
                Logger.error("PageView.setWindowSize", e)
                raise
        except Exception as e:
            Logger.error("PageView.setWindowSize", e)
            raise

    def draw(self):
        try:
            if not pygame.get_init() or pygame.display.get_surface() is None:
                return

            current_width, current_height = self.screen.get_size()
            
            if current_width != self.width or current_height != self.height:
                self.rescaleBackground(current_width, current_height)
            
            try:
                self.screen.blit(self.background, (0, 0))
            except Exception as e:
                Logger.debug("PageView.draw", "Blit failed, rescaling background", error=str(e))
                self.rescaleBackground(current_width, current_height)
                self.screen.blit(self.background, (0, 0))
        except Exception as e:
            Logger.error("PageView.draw", e)

    def handleEvents(self, events):
        return True

    def update(self):
        return None

    def render(self):
        self.draw()

    def run(self):
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("PageView.run", "Generic page loop started", name=self.name)

            while running:
                try:
                    events = pygame.event.get()
                    running = self.handleEvents(events)

                    if not running:
                        break

                    self.update()
                    self.render()

                    pygame.display.flip()
                    clock.tick(60)
                except Exception as e:
                    Logger.error("PageView.run", e)
                    continue

            Logger.debug("PageView.run", "Generic page loop ended", name=self.name)
        except Exception as e:
            Logger.error("PageView.run", e)
            raise