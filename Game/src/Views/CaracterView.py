"""
CaracterView Module

Handles the visual representation of characters (player, enemies, bosses).
Manages character sprite loading, positioning, rendering, and animations.
"""

import pygame
from Utils.Logger import Logger
from Models.PlayerModel import PlayerModel


# === CHARACTER VIEW CLASS ===

class CaracterView:
    """
    View class for rendering characters on the screen.
    Handles sprite loading, character positioning, status display, and action animations.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, image_path, scale=(50, 50), animation_sprites=None, flip_vertical=False):
        """
        Initialize the character view with a sprite image.
        
        Args:
            image_path: Path to the character sprite image file (default sprite)
            scale: Tuple (width, height) for sprite scaling. Default is (50, 50)
            animation_sprites: Dict of {animation_state: image_path} for action-specific sprites
            flip_vertical: Whether to flip the sprite vertically (for bosses facing left)
        """
        try:
            self.scale = scale
            self.base_image_path = image_path
            self.animation_sprites = animation_sprites or {}  # Store animation sprite paths
            self.flip_vertical = flip_vertical
            
            # Load and scale character sprite
            try:
                original_image = pygame.image.load(image_path).convert_alpha()
                if flip_vertical:
                    original_image = pygame.transform.flip(original_image, True, False)  # Horizontal flip
                self.sprite = pygame.transform.scale(original_image, scale)
                self.original_sprite = self.sprite.copy()  # Keep original for animations
                Logger.debug("CaracterView.__init__", "Character image loaded", image_path=image_path, scale=scale, flip_vertical=flip_vertical)
            except FileNotFoundError as e:
                Logger.error("CaracterView.__init__", e)
                # Create a default magenta sprite if image not found
                self.sprite = pygame.Surface(scale)
                self.sprite.fill((255, 0, 255))
                self.original_sprite = self.sprite.copy()
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
            
            # === ANIMATION STATE ===
            self.animation_state = None  # None, "attack", "dodge", "hit", "drink"
            self.animation_timer = 0  # Frame counter for animation
            self.animation_duration = 10  # Frames per animation
                
        except Exception as e:
            Logger.error("CaracterView.__init__", e)
            raise
    
    # === ANIMATION CONTROL ===
    
    def setAnimation(self, state):
        """
        Set the character's animation state.
        
        Args:
            state: Animation state ("attack", "dodge", "hit", "drink", or None)
        """
        try:
            self.animation_state = state
            self.animation_timer = 0
            Logger.debug("CaracterView.setAnimation", f"Animation state set to {state}")
        except Exception as e:
            Logger.error("CaracterView.setAnimation", e)
    
    def _loadAnimationSprite(self, state):
        """Load sprite for a specific animation state."""
        try:
            if state in self.animation_sprites:
                sprite_path = self.animation_sprites[state]
                try:
                    original_image = pygame.image.load(sprite_path).convert_alpha()
                    if self.flip_vertical:
                        original_image = pygame.transform.flip(original_image, True, False)  # Horizontal flip
                    return pygame.transform.scale(original_image, self.scale)
                except FileNotFoundError:
                    # Silently fallback to original sprite if animation sprite not found
                    Logger.debug("CaracterView._loadAnimationSprite", f"Animation sprite not found, using default", sprite_path=sprite_path)
                    return self.original_sprite.copy()
            return self.original_sprite.copy()
        except Exception as e:
            Logger.error("CaracterView._loadAnimationSprite", e)
            return self.original_sprite.copy()
    
    def updateAnimation(self):
        """Update animation timer and reset when complete."""
        try:
            if self.animation_state is not None:
                self.animation_timer += 1
                if self.animation_timer >= self.animation_duration:
                    self.animation_state = None
                    self.animation_timer = 0
                    self.sprite = self.original_sprite.copy()
        except Exception as e:
            Logger.error("CaracterView.updateAnimation", e)
    
    def _applyAnimationEffect(self):
        """Apply visual effects based on current animation state."""
        try:
            if self.animation_state is None:
                self.sprite = self.original_sprite.copy()
                return
            
            # Load animation-specific sprite if available
            base_sprite = self._loadAnimationSprite(self.animation_state)
            
            # Calculate progress (0.0 to 1.0)
            progress = self.animation_timer / self.animation_duration
            
            if self.animation_state == "attack":
                # Attack: Enlarge and shift forward for 6 frames, then shrink back
                if progress < 0.6:
                    # Expand phase: grow up to 20% larger
                    scale_factor = 1.0 + (0.2 * (progress / 0.6))
                    new_size = (
                        int(base_sprite.get_width() * scale_factor),
                        int(base_sprite.get_height() * scale_factor)
                    )
                    self.sprite = pygame.transform.scale(base_sprite, new_size)
                else:
                    # Shrink back phase
                    remaining_progress = (progress - 0.6) / 0.4
                    scale_factor = 1.0 + (0.2 * (1.0 - remaining_progress))
                    new_size = (
                        int(base_sprite.get_width() * scale_factor),
                        int(base_sprite.get_height() * scale_factor)
                    )
                    self.sprite = pygame.transform.scale(base_sprite, new_size)
            
            elif self.animation_state == "dodge":
                # Dodge: Quick side movement and transparency
                # Make sprite semi-transparent
                self.sprite = base_sprite.copy()
                self.sprite.set_alpha(200)
            
            elif self.animation_state == "hit":
                # Hit: Shake + red tint
                self.sprite = base_sprite.copy()
                # Apply red color overlay
                red_overlay = pygame.Surface(self.sprite.get_size())
                red_overlay.fill((255, 100, 100))
                red_overlay.set_alpha(100)
                self.sprite.blit(red_overlay, (0, 0))
            
            elif self.animation_state == "drink":
                # Drink: Use drinking sprite with subtle opacity change
                self.sprite = base_sprite.copy()
                # Subtle shimmer effect
                shimmer = int(50 * abs(0.5 - progress))
                shimmer_overlay = pygame.Surface(self.sprite.get_size())
                shimmer_overlay.fill((200, 255, 200))
                shimmer_overlay.set_alpha(shimmer)
                self.sprite.blit(shimmer_overlay, (0, 0))
        
        except Exception as e:
            Logger.error("CaracterView._apply_animation_effect", e)

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
            # Update animation
            self.updateAnimation()
            self._applyAnimationEffect()
            
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
