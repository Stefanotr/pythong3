"""
RhythmView Module

Handles the visual representation of the rhythm game mode.
Manages note rendering, particle effects, health bars, and HUD elements.
"""

import pygame
import math
from Utils.Logger import Logger


# === RHYTHM VIEW CLASS ===

class RhythmView:
    """
    View class for rendering the rhythm game interface.
    Displays notes, guitar strings, health bars, score, and visual effects.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize the rhythm view with screen dimensions.
        
        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
        """
        try:
            self.screen_width = screen_width
            self.screen_height = screen_height
            Logger.debug("RhythmView.__init__", "Initializing rhythm view", width=screen_width, height=screen_height)
            
            # === BACKGROUND LOADING ===
            
            self.background_image = None
            self.overlay = None
            
            image_path = "Game/Assets/stage.png"

            try:
                loaded_img = pygame.image.load(image_path).convert()
                self.background_image = pygame.transform.scale(loaded_img, (screen_width, screen_height))
                
                # Semi-transparent black overlay for better visibility
                self.overlay = pygame.Surface((screen_width, screen_height))
                self.overlay.fill((0, 0, 0))
                self.overlay.set_alpha(100)
                
                Logger.debug("RhythmView.__init__", "Background image loaded", path=image_path)
                
            except FileNotFoundError as e:
                Logger.error("RhythmView.__init__", e)
                Logger.debug("RhythmView.__init__", "Background image not found, using gradient mode", path=image_path)
                self.background_image = None
            except Exception as e:
                Logger.error("RhythmView.__init__", e)
                self.background_image = None

            # === FONTS INITIALIZATION ===
            
            try:
                self.font = pygame.font.SysFont("Arial", int(screen_height * 0.025), bold=True)
                self.big_font = pygame.font.SysFont("Arial", int(screen_height * 0.08), bold=True)
                self.combo_font = pygame.font.SysFont("Arial", int(screen_height * 0.05), bold=True)
                self.title_font = pygame.font.SysFont("Arial", int(screen_height * 0.035), bold=True)
                self.score_font = pygame.font.SysFont("Arial", int(screen_height * 0.06), bold=True)
                Logger.debug("RhythmView.__init__", "Fonts initialized")
            except Exception as e:
                Logger.error("RhythmView.__init__", e)
                # Use default fonts if SysFont fails
                self.font = pygame.font.Font(None, 24)
                self.big_font = pygame.font.Font(None, 72)
                self.combo_font = pygame.font.Font(None, 48)
                self.title_font = pygame.font.Font(None, 32)
                self.score_font = pygame.font.Font(None, 54)
            
            # === LANE COLORS AND POSITIONS ===
            
            # Neon colors for the 4 guitar strings
            self.lane_colors = [
                (255, 20, 147),   # Neon pink (C)
                (0, 255, 255),    # Neon cyan (V)
                (50, 255, 50),    # Neon green (B)
                (255, 215, 0)     # Neon gold (N)
            ]
            
            # Calculate string positions
            try:
                guitar_width = screen_width * 0.4
                guitar_start = (screen_width - guitar_width) / 2
                spacing = guitar_width / 5
                
                self.lane_x = [
                    int(guitar_start + spacing),
                    int(guitar_start + spacing * 2),
                    int(guitar_start + spacing * 3),
                    int(guitar_start + spacing * 4)
                ]
                
                self.guitar_start = int(guitar_start)
                self.guitar_width = int(guitar_width)
                Logger.debug("RhythmView.__init__", "Lane positions calculated")
            except Exception as e:
                Logger.error("RhythmView.__init__", e)
                # Default positions if calculation fails
                self.lane_x = [200, 300, 400, 500]
                self.guitar_start = 150
                self.guitar_width = 400
            
            # === PARTICLE SYSTEM ===
            
            self.particles = []
            self.time = 0
            Logger.debug("RhythmView.__init__", "Rhythm view initialization completed")
            
        except Exception as e:
            Logger.error("RhythmView.__init__", e)
            raise

    # === PARTICLE SYSTEM ===
    
    def createParticles(self, x, y, color):
        """
        Create explosion particles for hit effects.
        
        Args:
            x: X position for particle origin
            y: Y position for particle origin
            color: RGB color tuple for particles
        """
        try:
            for _ in range(12):
                try:
                    angle = pygame.math.Vector2(1, 0).rotate((_ * 30))
                    self.particles.append({
                        'x': x,
                        'y': y,
                        'vx': angle.x * 4,
                        'vy': angle.y * 4,
                        'life': 25,
                        'color': color
                    })
                except Exception as e:
                    Logger.error("RhythmView.createParticles", e)
                    continue
        except Exception as e:
            Logger.error("RhythmView.createParticles", e)

    def updateParticles(self):
        """
        Update particle positions and lifetimes.
        Removes particles that have expired.
        """
        try:
            for particle in self.particles[:]:
                try:
                    particle['x'] += particle['vx']
                    particle['y'] += particle['vy']
                    particle['vy'] += 0.3
                    particle['life'] -= 1
                    
                    if particle['life'] <= 0:
                        self.particles.remove(particle)
                except Exception as e:
                    Logger.error("RhythmView.updateParticles", e)
                    # Remove problematic particle
                    try:
                        self.particles.remove(particle)
                    except ValueError:
                        pass
        except Exception as e:
            Logger.error("RhythmView.updateParticles", e)

    # === UTILITY METHODS ===
    
    def clamp(self, value, min_val=0, max_val=255):
        """
        Clamp a value between minimum and maximum.
        
        Args:
            value: Value to clamp
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            int: Clamped value
        """
        try:
            return max(min_val, min(int(value), max_val))
        except Exception as e:
            Logger.error("RhythmView.clamp", e)
            return min_val

    # === RENDERING METHODS ===
    
    def drawHealthBar(self, screen, x, y, width, height, current, maximum, label, color_good, color_bad, is_boss=False):
        """
        Draw a styled health bar with gradient fill.
        
        Args:
            screen: Pygame surface to draw on
            x: X position of health bar
            y: Y position of health bar
            width: Width of health bar
            height: Height of health bar
            current: Current health value
            maximum: Maximum health value
            label: Text label for the health bar
            color_good: RGB color for high health
            color_bad: RGB color for low health
            is_boss: Whether this is a boss health bar (affects label position)
        """
        try:
            ratio = current / maximum if maximum > 0 else 0
        
            # Fond
            pygame.draw.rect(screen, (20, 20, 20), (x - 2, y - 2, width + 4, height + 4), border_radius=8)
            pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height), border_radius=6)
            
            # Fill with gradient
            filled_width = int(width * ratio)
            
            if ratio > 0.5:
                color1, color2 = color_good, (int(color_good[0]*1.2), int(color_good[1]*1.2), int(color_good[2]*0.8))
            else:
                color1, color2 = color_bad, (int(color_bad[0]*0.8), int(color_bad[1]*0.5), int(color_bad[2]*0.5))
            
            for i in range(filled_width):
                r_ratio = i / width if width > 0 else 0
                r = self.clamp(color1[0] + (color2[0] - color1[0]) * r_ratio)
                g = self.clamp(color1[1] + (color2[1] - color1[1]) * r_ratio)
                b = self.clamp(color1[2] + (color2[2] - color1[2]) * r_ratio)
                pygame.draw.line(screen, (r, g, b), (x + i, y + 2), (x + i, y + height - 3))
            
            # Bordure
            pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2, border_radius=6)
            
            # Label
            label_surf = self.font.render(label, True, (255, 255, 255))
            label_shadow = self.font.render(label, True, (0, 0, 0))
            
            if is_boss:
                # Label on the left for boss
                screen.blit(label_shadow, (x - label_surf.get_width() - 12, y + height // 2 - label_surf.get_height() // 2 + 2))
                screen.blit(label_surf, (x - label_surf.get_width() - 10, y + height // 2 - label_surf.get_height() // 2))
            else:
                # Label on top for player
                screen.blit(label_shadow, (x + 2, y - 22))
                screen.blit(label_surf, (x, y - 20))
            
            # HP text
            hp_text = self.font.render(f"{current}/{maximum}", True, (255, 255, 255))
            hp_shadow = self.font.render(f"{current}/{maximum}", True, (0, 0, 0))
            text_x = x + width // 2 - hp_text.get_width() // 2
            text_y = y + height // 2 - hp_text.get_height() // 2
            screen.blit(hp_shadow, (text_x + 1, text_y + 1))
            screen.blit(hp_text, (text_x, text_y))
        except Exception as e:
            Logger.error("RhythmView.drawHealthBar",e)

    def draw(self, screen, rhythm_model, character_model):
        """
        Main draw method for the rhythm view.
        Renders all visual elements including background, notes, particles, and HUD.
        
        Args:
            screen: Pygame surface to draw on
            rhythm_model: RhythmModel instance containing game state
            character_model: Character model instance for health display
        """
        try:
            self.time += 1
            
            # --- A. FOND ---
            if self.background_image:
                screen.blit(self.background_image, (0, 0))
                screen.blit(self.overlay, (0, 0))
            else:
                # Simple gradient without animation
                for y in range(self.screen_height):
                        shade = int(20 + y * 0.02)
                        pygame.draw.line(screen, (shade, shade // 2, shade // 3), (0, y), (self.screen_width, y))
                
                # --- B. MANCHE DE GUITARE (semi-transparent) ---
                guitar_rect = pygame.Rect(self.guitar_start - 15, 0, self.guitar_width + 30, self.screen_height)
                
                # Surface semi-transparente pour le manche
                guitar_surf = pygame.Surface((guitar_rect.width, guitar_rect.height), pygame.SRCALPHA)
                
                # Gradient on the neck
                for i in range(guitar_rect.width):
                    ratio = i / guitar_rect.width
                    alpha = int(120 + ratio * 40)
                    color_val = int(15 + ratio * 10)
                    pygame.draw.line(guitar_surf, (color_val, color_val, color_val + 5, alpha), 
                                (i, 0), (i, guitar_rect.height))
                
                screen.blit(guitar_surf, guitar_rect)
                
                # Bordure subtile
                pygame.draw.rect(screen, (80, 120, 180, 200), guitar_rect, 2, border_radius=10)
                
                # --- C. CORDES ---
                for i, x in enumerate(self.lane_x):
                    color = self.lane_colors[i]
                    
                    # Lueur simple
                    glow_surf = pygame.Surface((10, self.screen_height), pygame.SRCALPHA)
                    for t in range(5, 0, -1):
                        alpha = int(40 * (t / 5))
                        glow_color = (*color, alpha)
                        pygame.draw.line(glow_surf, glow_color, (5, 0), (5, self.screen_height), t)
                    screen.blit(glow_surf, (x - 5, 0))
                    
                    # Corde principale
                    pygame.draw.line(screen, color, (x, 0), (x, self.screen_height), 2)
                    
                    # Cercle de cible
                    hit_line_y = rhythm_model.getHitLineY()
                    pygame.draw.circle(screen, (0, 0, 0), (x, hit_line_y), 32)
                    pygame.draw.circle(screen, color, (x, hit_line_y), 28, 3)
                    pygame.draw.circle(screen, tuple(c // 3 for c in color), (x, hit_line_y), 20, 2)
                
                # --- D. LIGNE DE FRAPPE ---
                hit_line_y = rhythm_model.getHitLineY()
                pygame.draw.line(screen, (255, 255, 255), 
                                (self.guitar_start - 15, hit_line_y), 
                                (self.guitar_start + self.guitar_width + 15, hit_line_y), 3)
            
            # --- E. NOTES ---
            try:
                for note in rhythm_model.getNotes():
                    if note.get("active", False):
                        try:
                            lane_index = rhythm_model.getLanes().index(note["lane"])
                            x_pos = self.lane_x[lane_index]
                            color = self.lane_colors[lane_index]
                            y_pos = int(note["y"])
                            
                            # Light trail effect
                            for offset in range(5):
                                try:
                                    trail_y = y_pos - offset * 12
                                    trail_size = int(26 - offset * 3)
                                    alpha_ratio = 1 - (offset * 0.18)
                                    trail_surf = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                                    trail_color = (*color, int(255 * alpha_ratio))
                                    pygame.draw.circle(trail_surf, trail_color, (trail_size, trail_size), trail_size)
                                    screen.blit(trail_surf, (x_pos - trail_size, trail_y - trail_size))
                                except Exception as e:
                                    Logger.error("RhythmView.draw", e)
                                    continue
                            
                            # Main note circle
                            try:
                                pygame.draw.circle(screen, (255, 255, 255), (x_pos, y_pos), 28)
                                pygame.draw.circle(screen, color, (x_pos, y_pos), 25)
                                pygame.draw.circle(screen, tuple(c // 3 for c in color), (x_pos, y_pos), 15)
                                pygame.draw.circle(screen, (0, 0, 0), (x_pos, y_pos), 8)
                            except Exception as e:
                                Logger.error("RhythmView.draw", e)
                        except (ValueError, KeyError, IndexError) as e:
                            Logger.error("RhythmView.draw", e)
                            continue
            except Exception as e:
                Logger.error("RhythmView.draw", e)
            
                # --- F. PARTICLES ---
                try:
                    for particle in self.particles[:]:
                        try:
                            size = int(particle['life'] / 4)
                            if size > 0:
                                alpha_ratio = particle['life'] / 25
                                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                                particle_color = (*particle['color'], int(255 * alpha_ratio))
                                pygame.draw.circle(particle_surf, particle_color, (size, size), size)
                                screen.blit(particle_surf, (int(particle['x']) - size, int(particle['y']) - size))
                        except Exception as e:
                            Logger.error("RhythmView.draw", e)
                            continue
                    
                    self.updateParticles()
                except Exception as e:
                    Logger.error("RhythmView.draw", e)
            
            # --- G. SIMPLIFIED HUD ---
            hud_height = int(self.screen_height * 0.12)
            
            # Semi-transparent panel
            hud_surf = pygame.Surface((self.screen_width, hud_height), pygame.SRCALPHA)
            pygame.draw.rect(hud_surf, (10, 10, 20, 180), (0, 0, self.screen_width, hud_height))
            screen.blit(hud_surf, (0, 0))
            
            # Border
            pygame.draw.line(screen, (80, 120, 180), (0, hud_height), (self.screen_width, hud_height), 2)
            
            # === LEFT: PLAYER HP ===
            player_hp_width = int(self.screen_width * 0.18)
            self.drawHealthBar(
                screen, 
                20, 
                int(hud_height * 0.4),
                player_hp_width,
                int(hud_height * 0.35),
                character_model.getHealth(),
                100,
                f"♪ {character_model.getName()}",
                (50, 255, 50),
                (255, 50, 50),
                is_boss=False
            )
            
            # === CENTER: SCORE ===
            score_value = f"{rhythm_model.getScore():,}"
            score_text = self.score_font.render(score_value, True, (255, 215, 0))
            score_shadow = self.score_font.render(score_value, True, (100, 80, 0))
            
            score_rect = score_text.get_rect(center=(self.screen_width // 2, hud_height // 2 - 5))
            screen.blit(score_shadow, (score_rect.x + 2, score_rect.y + 2))
            screen.blit(score_text, score_rect)
            
            # Label SCORE
            score_label = self.font.render("SCORE", True, (200, 200, 200))
            screen.blit(score_label, (score_rect.centerx - score_label.get_width() // 2, 8))
            
            # === RIGHT: BOSS HP ===
            boss_hp_width = int(self.screen_width * 0.18)
            boss_hp_x = self.screen_width - boss_hp_width - 20
            
            # Simulate a boss (you can replace with the actual boss model)
            boss_hp_current = 75  # To be replaced with rhythm_model.boss.getHealth()
            boss_hp_max = 100
            
            self.drawHealthBar(
                screen,
                boss_hp_x,
                int(hud_height * 0.4),
                boss_hp_width,
                int(hud_height * 0.35),
                boss_hp_current,
                boss_hp_max,
                "🎸 BOSS",
                (255, 100, 255),
                (255, 50, 50),
                is_boss=True
            )
            
            # === COMBO (en dessous du score) ===
            if rhythm_model.getCombo() > 0:
                combo_value = f"x{rhythm_model.getCombo()} COMBO"
                combo_text = self.combo_font.render(combo_value, True, (255, 100, 255))
                combo_shadow = self.combo_font.render(combo_value, True, (100, 0, 100))
                
                combo_rect = combo_text.get_rect(center=(self.screen_width // 2, hud_height - 18))
                screen.blit(combo_shadow, (combo_rect.x + 1, combo_rect.y + 1))
                screen.blit(combo_text, combo_rect)
            
            # --- H. FEEDBACK CENTRAL ---
            if rhythm_model.getFeedback() and rhythm_model.getFeedbackTimer() > 0:
                feedback = rhythm_model.getFeedback()
                if "PERFECT" in feedback:
                    fb_color = (100, 255, 100)
                    extra = " ⭐"
                elif "EXCELLENT" in feedback:
                    fb_color = (255, 255, 100)
                    extra = " ✨"
                elif "GOOD" in feedback:
                    fb_color = (100, 200, 255)
                    extra = " ♪"
                else:
                    fb_color = (255, 100, 100)
                    extra = ""
                
                fb_text = feedback + extra
                fb_surf = self.big_font.render(fb_text, True, fb_color)
                fb_shadow = self.big_font.render(fb_text, True, (0, 0, 0))
                
                fb_rect = fb_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                screen.blit(fb_shadow, (fb_rect.x + 3, fb_rect.y + 3))
                screen.blit(fb_surf, fb_rect)
            
                # --- I. BOTTOM INSTRUCTIONS ---
                try:
                    key_labels = ["C", "V", "B", "N"]
                    for i, (x, label) in enumerate(zip(self.lane_x, key_labels)):
                        try:
                            key_color = self.lane_colors[i]
                            key_text = self.title_font.render(label, True, key_color)
                            key_shadow = self.title_font.render(label, True, (0, 0, 0))
                            
                            key_rect = key_text.get_rect(centerx=x, bottom=self.screen_height - 15)
                            screen.blit(key_shadow, (key_rect.x + 2, key_rect.y + 2))
                            screen.blit(key_text, key_rect)
                        except Exception as e:
                            Logger.error("RhythmView.draw", e)
                            continue
                except Exception as e:
                    Logger.error("RhythmView.draw", e)
                
        except Exception as e:
            Logger.error("RhythmView.draw", e)