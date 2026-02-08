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
    
    def __init__(self, image_path, base_name="", sprite_size=None, character_config=None, game_mode="combat"):
        """
        Initialize the character view with a sprite image.
        
        Args:
            image_path: Path to the character sprite image file
            base_name: Base name for action-based images (e.g., "lola" for lolaquiboit.png)
            sprite_size: Tuple (width, height) for sprite size. If None, uses config or default
            character_config: Optional dict with character configuration (sizes, actions, positions)
            game_mode: Game mode for loading correct sprite size from config ('map', 'combat', 'rhythm_combat', etc.)
        """
        try:
            self.base_image_path = image_path
            self.base_name = base_name
            self.character_config = character_config  # Store config for later use
            self.game_mode = game_mode
            
            # Determine sprite size: use passed size, config, or default
            if sprite_size:
                self.sprite_size = sprite_size
            elif character_config and 'sizes' in character_config:
                mode_sizes = character_config['sizes'].get(game_mode, {})
                if mode_sizes:
                    self.sprite_size = (mode_sizes.get('width', 200), mode_sizes.get('height', 200))
                else:
                    self.sprite_size = (200, 200)  # Default
            else:
                self.sprite_size = sprite_size or (200, 200)  # Default size for combat
            
            self.sprite = None
            self.action_sprites = {}  # Cache for action-based sprites
            
            # Animation system
            self.animation_frame = 0  # Compteur pour les animations
            self.animation_speed = 8  # Nombre de frames avant de changer d'image (ajustable)
            
            # Load base sprite
            self._loadSprite(image_path)
            
            # Initialize fonts for text rendering
            try:
                self.font = pygame.font.SysFont(None, 36)
                self.small_font = pygame.font.SysFont(None, 18)  # For map view
                self.big_font = pygame.font.SysFont(None, 32)  # For rhythm/rhythm_combat view
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

    def resetToBaseSprite(self):
        """Reset the character view to the base (idle) sprite and clear action cache."""
        try:
            # Clear cached action sprites so future updates start from base
            self.action_sprites = {}
            # Reload base image into `self.sprite`
            self._loadSprite(self.base_image_path)
            Logger.debug("CaracterView.resetToBaseSprite", "Sprite reset to base image", base=self.base_image_path)
        except Exception as e:
            Logger.error("CaracterView.resetToBaseSprite", e)

    def _getActionImagePath(self, base_name, action):
        """
        Get the image path for a specific action.
        Loads from character config (JSON) first, then falls back to hardcoded defaults.
        
        Args:
            base_name: Base character name (lola, agent, manager, motard)
            action: Action type (idle, attacking, drinking, dodging, moving_left, moving_right)
        
        Returns:
            Path to the action image, or list of paths for animated actions, or None if not found
        """
        # === TRY LOADING FROM CHARACTER CONFIG (JSON) FIRST ===
        if self.character_config and 'actions' in self.character_config:
            actions_config = self.character_config['actions']
            if action in actions_config:
                image_path = actions_config[action]
                Logger.debug("CaracterView._getActionImagePath", 
                            f"Loaded from JSON config: {base_name}.{action} = {image_path}")
                return image_path
            else:
                Logger.debug("CaracterView._getActionImagePath",
                            f"Action '{action}' not found in JSON config for {base_name}")
        else:
            Logger.debug("CaracterView._getActionImagePath",
                        f"No character_config available for {base_name} (config is {'None' if not self.character_config else 'missing actions'})")
        
        # === IF NOT IN CONFIG, TRY LOADING FROM BOSS CONFIG VIA ASSETMANAGER ===
        # (For boss characters, they might have separate boss configs)
        try:
            from Utils.AssetManager import AssetManager
            
            # Check if this is a boss character (agent, manager, motard, etc.)
            if base_name in ["agent", "manager", "motard", "gros_bill"]:
                asset_manager = AssetManager()
                
                # Try to get boss by common name mappings
                boss_names = {
                    "agent": "Security Agent",
                    "manager": "Manager Corrompu",
                    "motard": "Gros Bill",
                    "gros_bill": "Gros Bill"
                }
                
                boss_name = boss_names.get(base_name, base_name)
                try:
                    boss_config = asset_manager.get_boss_by_name(boss_name)
                    if boss_config and 'actions' in boss_config:
                        if action in boss_config['actions']:
                            image_path = boss_config['actions'][action]
                            Logger.debug("CaracterView._getActionImagePath",
                                        f"Loaded from boss config: {boss_name}.{action} = {image_path}")
                            return image_path
                except Exception as e:
                    Logger.debug("CaracterView._getActionImagePath",
                                f"Failed to load from boss config: {e}")
        except ImportError as e:
            Logger.debug("CaracterView._getActionImagePath",
                        f"AssetManager not available: {e}")
        
        # === FALLBACK TO HARDCODED DEFAULTS ===
        action_map = {
            # Lola
            "lola": {
                "idle": "Game/Assets/lola.png",
                "drinking": "Game/Assets/lolaquiboit (1).png",
                "attacking": "Game/Assets/lolaquilancesabasse (1).png",
                "dodging": "Game/Assets/lolaquisebaisse (2).png",
                # Animation de mouvement gauche : 2 frames
                "moving_left": [
                    "Game/Assets/lolacoursgauche.png",
                    "Game/Assets/lolagaucheframe1.png"
                ],
                # Animation de mouvement droite : 2 frames
                "moving_right": [
                    "Game/Assets/lolacoursdroite.png",
                    "Game/Assets/lola.png"
                ],
                # Animation musique : 3 frames
                "musique": [
                    "Game/Assets/lolamusique1.png",
                    "Game/Assets/lolamusique2.png",
                    "Game/Assets/lolamusique3.png"
                ]
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
        Handles both static sprites and animated sprites.
        
        Args:
            character: CaracterModel instance
        """
        if not self.base_name:
            return  # No base name set, can't update actions
        
        action = character.getCurrentAction()
        
        # Get action image path(s)
        action_paths = self._getActionImagePath(self.base_name, action)
        if not action_paths:
            # Fallback to base sprite if action image not found
            self.sprite = self._loadSpriteForPath(self.base_image_path)
            return
        
        # Handle animated actions (list of frames)
        if isinstance(action_paths, list):
            # Animation: select frame based on animation_frame counter
            frame_index = (self.animation_frame // self.animation_speed) % len(action_paths)
            action_path = action_paths[frame_index]
            cache_key = f"{self.base_name}_{action}_{frame_index}"
        else:
            # Static action: single sprite
            action_path = action_paths
            cache_key = f"{self.base_name}_{action}"
        
        # Check if we already have this sprite cached
        if cache_key in self.action_sprites:
            self.sprite = self.action_sprites[cache_key]
            return
        
        # Load the action-specific image
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
            # Update animation frame counter
            self.animation_frame += 1
            
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

            # Draw character name above sprite (different font sizes based on game mode)
            if is_map:
                try:
                    name = caracter.getName()
                    # Use bigger font for rhythm modes, smaller for map
                    name_font = self.big_font if self.game_mode in ["rhythm", "rhythm_combat"] else self.small_font
                    name_surface = name_font.render(name, True, (255, 255, 255))
                    name_x = draw_x + sprite_w // 2 - name_surface.get_width() // 2
                    name_y = draw_y - name_surface.get_height() - 5
                    screen.blit(name_surface, (name_x, name_y))
                except Exception as e:
                    Logger.error("CaracterView.drawCaracter", e)



        except Exception as e:
            Logger.error("CaracterView.drawCaracter", e)
