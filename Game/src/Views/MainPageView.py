"""
MainPageView Module

Handles the main game view displaying the map, player, and boss.
Manages the main game loop and rendering.
"""

import pygame
from Models.CaracterModel import CaracterModel
from Controllers.PlayerController import PlayerController
from Views.CaracterView import CaracterView
from Views.MapView import MapView
from Views.PageView import PageView
from Models.BottleModel import BottleModel
from Models.PlayerModel import PlayerModel
from Models.BossModel import BossModel
from Models.MapModel import MapModel
from Models.TileModel import TileModel
from Utils.Logger import Logger


# === MAIN PAGE VIEW CLASS ===

class MainPageView(PageView):
    """
    Main game view displaying the map, player character, and boss.
    Handles the main game loop and all game rendering.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name, width=800, height=800, RESIZABLE=0, background_image="Game/Assets/welcomePage.png"):
        """
        Initialize the main page view with game entities.
        
        Args:
            name: Window title
            width: Window width in pixels
            height: Window height in pixels
            RESIZABLE: Pygame flag for window resizability
            background_image: Path to background image file
        """
        try:
            super().__init__(name, width, height, RESIZABLE, background_image)
            Logger.debug("MainPageView.__init__", "Main page view initialized", name=name)

            # === GAME ENTITIES INITIALIZATION ===
            
            try:
                # Create player
                self.johnny = PlayerModel("Johnny Fuzz", 60, 60)
                Logger.debug("MainPageView.__init__", "Player created", name=self.johnny.getName())
            except Exception as e:
                Logger.error("MainPageView.__init__", e)
                raise
            
            try:
                # Create boss
                self.gros_bill = BossModel("Gros Bill", 80, 80)
                Logger.debug("MainPageView.__init__", "Boss created", name=self.gros_bill.getName())
            except Exception as e:
                Logger.error("MainPageView.__init__", e)
                raise
            
            # Create bottles
            try:
                self.beer = BottleModel("Beer", 10, 2, 5)
                self.vodka = BottleModel("Vodka", 35, 8, 20)
                self.champagne = BottleModel("Champagne", 20, 4, 8)
                Logger.debug("MainPageView.__init__", "Bottles created")
            except Exception as e:
                Logger.error("MainPageView.__init__", e)
                raise
            
            # Create tile types and map
            try:
                tile_kinds = [
                    TileModel("road", "Game/Assets/road3_carre.png", False),
                    TileModel("road2", "Game/Assets/road3_carre.png", False)
                ]
                self.map = MapModel("Game/Assets/maps/map.map", tile_kinds, 106)
                Logger.debug("MainPageView.__init__", "Map created")
            except Exception as e:
                Logger.error("MainPageView.__init__", e)
                raise

            # Set player's selected bottle
            try:
                self.johnny.setSelectedBottle(self.beer)
                Logger.debug("MainPageView.__init__", "Player bottle selected")
            except Exception as e:
                Logger.error("MainPageView.__init__", e)

            # Create controller
            try:
                self.controller = PlayerController(self.screen, self.johnny)
                Logger.debug("MainPageView.__init__", "Player controller created")
            except Exception as e:
                Logger.error("MainPageView.__init__", e)
                raise

            # Create views
            try:
                self.player_view = CaracterView("Game/Assets/guitare.png")
                self.boss_view = CaracterView("Game/Assets/boss.png")
                Logger.debug("MainPageView.__init__", "Character views created")
            except Exception as e:
                Logger.error("MainPageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("MainPageView.__init__", e)
            raise

    # === MAIN LOOP ===
    
    def run(self):
        """
        Main game loop for the main page view.
        Handles events, updates game state, and renders all game elements.
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("MainPageView.run", "Main game loop started")

            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            Logger.debug("MainPageView.run", "QUIT event received")
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen = pygame.display.set_mode((new_width, new_height), self.resizable)
                                self.rescaleBackground(new_width, new_height)
                                Logger.debug("MainPageView.run", "Window resized", 
                                          width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("MainPageView.run", e)
                        else:
                            try:
                                self.controller.handleInput(event)
                            except Exception as e:
                                Logger.error("MainPageView.run", e)
                    
                    # === RENDERING ===
                    
                    try:
                        self.draw()
                        # Create and draw map view
                        map_view = MapView(self.map)
                        map_view.draw(self.screen)
                        self.player_view.drawCaracter(self.screen, self.johnny)
                        self.boss_view.drawCaracter(self.screen, self.gros_bill)
                    except Exception as e:
                        Logger.error("MainPageView.run", e)
                        # Continue running even if rendering fails

                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("MainPageView.run", e)
                    # Continue running even if one frame fails
                    continue

            Logger.debug("MainPageView.run", "Main game loop ended")
            pygame.quit()
            
        except Exception as e:
            Logger.error("MainPageView.run", e)
            pygame.quit()
            raise


