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
    Handles sprite loading, character positioning, and rendering with status information.
    Supports different images based on character action.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, image_path, base_name="", sprite_size=None):
        """
        Initialize the character view with a sprite image.
        
        Args:
            image_path: Path to the character sprite image file
            base_name: Base name for action-based images (e.g., "lola" for lolaquiboit.png)
            sprite_size: Tuple (width, height) for sprite size. Default is (200, 200) for combat, (64, 64) for map
        """
        try:
            self.base_image_path = image_path
            self.base_name = base_name  # For Lola: "lola", for enemies: "agent", "manager", etc.
            self.sprite_size = sprite_size or (200, 200)  # Default size for combat
            self.sprite = None
            self.action_sprites = {}  # Cache for action-based sprites
            
            # Load base sprite
            self._loadSprite(image_path)
            
            # Initialize fonts for text rendering
            try:
                self.font = pygame.font.SysFont(None, 36)
                self.small_font = pygame.font.SysFont(None, 18)  # For map view
                Logger.debug("CaracterView.__init__", "Fonts initialized")
            except Exception as e:
                Logger.error("CaracterView.__init__", e)
                # Use default font if SysFont fails
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 18)
                
        except Exception as e:
            Logger.error("CaracterView.__init__", e)
            raise

    def _loadSprite(self, image_path):
        """Load a sprite from the given path"""
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            # Use sprite_size for scaling
            self.sprite = pygame.transform.scale(original_image, self.sprite_size)
            Logger.debug("CaracterView._loadSprite", "Character image loaded", image_path=image_path, size=self.sprite_size)
        except FileNotFoundError as e:
            Logger.error("CaracterView._loadSprite", f"Image not found: {image_path}")
            # Create a default magenta sprite if image not found
            self.sprite = pygame.Surface(self.sprite_size)
            self.sprite.fill((255, 0, 255))
            Logger.debug("CaracterView._loadSprite", "Using default character sprite")
        except Exception as e:
            Logger.error("CaracterView._loadSprite", e)

    def _getActionImagePath(self, base_name, action):
        """
        Get the image path for a specific action.
        
        Args:
            base_name: Base character name (lola, agent, manager, motard)
            action: Action type (idle, attacking, drinking, dodging)
        
        Returns:
            Path to the action image, or None if not found
        """
        action_map = {
            # Lola
            "lola": {
                "idle": "Game/Assets/lola.png",
                "drinking": "Game/Assets/lolaquiboit (1).png",
                "attacking": "Game/Assets/lolaquilancesabasse (1).png",
                "dodging": "Game/Assets/lolaquisebaisse (2).png"
            },
            # Agent de Sécurité
            "agent": {
                "idle": "Game/Assets/Agentdesecurité.png",
                "attacking": "Game/Assets/agentdesecuritquitape (1).png",
                "dodging": "Game/Assets/agentdesecuritequisebaisse (1).png"
            },
            # Manager Corrompu
            "manager": {
                "idle": "Game/Assets/ManagerCorrompu.png",
                "attacking": "Game/Assets/managerquitape (1).png",
                "dodging": "Game/Assets/managercorrompuquisebaisse (1).png"
            },
            # Motard
            "motard": {
                "idle": "Game/Assets/chefdesmotards.png",
                "attacking": "Game/Assets/motardquidonnedescoupsdepieds (1).png",
                "dodging": "Game/Assets/motardquisebaisse (1).png"
            }
        }
        
        if base_name in action_map and action in action_map[base_name]:
            return action_map[base_name][action]
        return None

    def updateCharacterSprite(self, character):
        """
        Update the displayed sprite based on the character's current action.
        
        Args:
            character: CaracterModel instance
        """
        if not self.base_name:
            return  # No base name set, can't update actions
        
        action = character.getCurrentAction()
        cache_key = f"{self.base_name}_{action}"
        
        # Check if we already have this sprite cached
        if cache_key in self.action_sprites:
            self.sprite = self.action_sprites[cache_key]
            return
        
        # Load the action-specific image
        action_path = self._getActionImagePath(self.base_name, action)
        if action_path:
            try:
                original_image = pygame.image.load(action_path).convert_alpha()
                sprite = pygame.transform.scale(original_image, self.sprite_size)
                self.action_sprites[cache_key] = sprite  # Cache it
                self.sprite = sprite
                Logger.debug("CaracterView.updateCharacterSprite", 
                           f"Sprite updated for action: {action}", base_name=self.base_name)
            except Exception as e:
                Logger.error("CaracterView.updateCharacterSprite", e)
        else:
            # Fallback to base sprite if action image not found
            self.sprite = self._loadSpriteForPath(self.base_image_path)

    def _loadSpriteForPath(self, path):
        """Load and scale a sprite from path, return it without storing"""
        try:
            original_image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(original_image, self.sprite_size)
        except Exception as e:
            Logger.error("CaracterView._loadSpriteForPath", e)
            sprite = pygame.Surface(self.sprite_size)
            sprite.fill((255, 0, 255))
            return sprite

    # === RENDERING ===
    
    def drawCaracter(self, screen, caracter, offset=(0, 0), is_map=False):
        """
        Draw the character sprite and status information to the screen.

        Args:
            screen: Pygame surface to draw on
            caracter: Character model instance (PlayerModel, BossModel, etc.)
            offset: Tuple (offset_x, offset_y) applied to world coordinates for screen rendering
            is_map: Whether this is drawing on the map (affects text size and positioning)
        """
        try:
            # Update sprite based on current action
            if self.base_name:
                self.updateCharacterSprite(caracter)
                caracter.updateActionTimer()
            
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

            # Draw character name above sprite (smaller font for map)
            if is_map:
                try:
                    name = caracter.getName()
                    name_surface = self.small_font.render(name, True, (255, 255, 255))
                    name_x = draw_x + sprite_w // 2 - name_surface.get_width() // 2
                    name_y = draw_y - name_surface.get_height() - 5
                    screen.blit(name_surface, (name_x, name_y))
                except Exception as e:
                    Logger.error("CaracterView.drawCaracter", e)
            else:  # Only draw name below sprite in combat
                try:
                    name = caracter.getName()
                    name_surface = self.font.render(name, True, (255, 255, 255))
                    name_x = draw_x + sprite_w // 2 - name_surface.get_width() // 2
                    name_y = draw_y + sprite_h + 10
                    screen.blit(name_surface, (name_x, name_y))
                except Exception as e:
                    Logger.error("CaracterView.drawCaracter", e)

            # Draw player-specific information (alcohol level)
            if isinstance(caracter, PlayerModel):
                try:
                    alcohol = caracter.getDrunkenness()
                    text_content = f"Alcohol: {alcohol}%"
                    
                    if is_map:
                        # Green text with black background, same horizontal position as level
                        text_surface = self.font.render(text_content, True, (0, 255, 0))
                        text_x = 20  # Same as level
                        text_y = screen.get_height() - 90  # Below level
                        
                        # Draw black rectangle background
                        bg_rect = pygame.Rect(text_x - 5, text_y - 5, text_surface.get_width() + 10, text_surface.get_height() + 10)
                        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                    else:
                        # Green text with black background for combat
                        text_surface = self.font.render(text_content, True, (0, 255, 0))
                        text_x = 10
                        text_y = 10
                        
                        # Draw black rectangle background
                        bg_rect = pygame.Rect(text_x - 5, text_y - 5, text_surface.get_width() + 10, text_surface.get_height() + 10)
                        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                    
                    screen.blit(text_surface, (text_x, text_y))
                    Logger.debug("CaracterView.drawCaracter", "Player alcohol level displayed", 
                               alcohol=alcohol, is_map=is_map)
                except Exception as e:
                    Logger.error("CaracterView.drawCaracter", e)

        except Exception as e:
            Logger.error("CaracterView.drawCaracter", e)
