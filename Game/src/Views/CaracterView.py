"""
CaracterView Module

Handles the visual representation of characters (player, enemies, bosses).
Manages character sprite loading, positioning, and rendering with status information.
"""

import pygame
from Utils.Logger import Logger
from Models.PlayerModel import PlayerModel


# === CHARACTER VIEW CLASS ===

class CaracterView:
    """
    View class for rendering characters on the screen.
    Handles sprite loading, character positioning, and status display.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, image_path):
        """
        Initialize the character view with a sprite image.
        
        Args:
            image_path: Path to the character sprite image file
        """
        try:
            # Load and scale character sprite
            try:
                original_image = pygame.image.load(image_path).convert_alpha()
                self.sprite = pygame.transform.scale(original_image, (50, 50))
                Logger.debug("CaracterView.__init__", "Character image loaded", image_path=image_path)
            except FileNotFoundError as e:
                Logger.error("CaracterView.__init__", e)
                # Create a default magenta sprite if image not found
                self.sprite = pygame.Surface((50, 50))
                self.sprite.fill((255, 0, 255))
                Logger.debug("CaracterView.__init__", "Using default character sprite")
            except Exception as e:
                Logger.error("CaracterView.__init__", e)
                raise

            # Initialize font for text rendering
            try:
                self.font = pygame.font.SysFont(None, 36)
                Logger.debug("CaracterView.__init__", "Font initialized")
            except Exception as e:
                Logger.error("CaracterView.__init__", e)
                # Use default font if SysFont fails
                self.font = pygame.font.Font(None, 36)
                
        except Exception as e:
            Logger.error("CaracterView.__init__", e)
            raise

    # === RENDERING ===
    
    def drawCaracter(self, screen, caracter, offset=(0, 0)):
        """
        Draw the character sprite and status information to the screen.

        Args:
            screen: Pygame surface to draw on
            caracter: Character model instance (PlayerModel, BossModel, etc.)
            offset: Tuple (offset_x, offset_y) applied to world coordinates for screen rendering
        """
        try:
            # Get character position
            try:
                x = caracter.getX()
                y = caracter.getY()
            except Exception as e:
                Logger.error("CaracterView.drawCaracter", e)
                return

            offset_x, offset_y = offset
            sprite_w, sprite_h = self.sprite.get_size()
            draw_x = int(x + offset_x - sprite_w // 2)
            draw_y = int(y + offset_y - sprite_h // 2)

            # Draw character sprite (centered on character coordinates)
            try:
                screen.blit(self.sprite, (draw_x, draw_y))
            except Exception as e:
                Logger.error("CaracterView.drawCaracter", e)

            # Draw player-specific information (alcohol level)
            if isinstance(caracter, PlayerModel):
                try:
                    alcohol = caracter.getDrunkenness()
                    text_content = f"Alcohol: {alcohol}%"
                    text_surface = self.font.render(text_content, True, (255, 255, 255))
                    screen.blit(text_surface, (10, 10))
                    Logger.debug("CaracterView.drawCaracter", "Player alcohol level displayed", alcohol=alcohol)
                except Exception as e:
                    Logger.error("CaracterView.drawCaracter", e)

        except Exception as e:
            Logger.error("CaracterView.drawCaracter", e)
