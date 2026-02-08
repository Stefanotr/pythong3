"""
CombatView Module

Handles the visual representation of turn-based combat interface.
Manages rendering of combat UI, health bars, status effects, and combat log.
"""

import pygame
import math
from Utils.Logger import Logger
from Views.InventoryView import InventoryView


# === COMBAT VIEW CLASS ===

class CombatView:
    """
    View class for rendering turn-based combat interface.
    Displays fighter information, health bars, status effects, action menu, and combat log.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen_width, screen_height, background_image_path="Game/Assets/grosbillfight.png"):
        """
        Initialize the combat view with screen dimensions.
        
        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
            background_image_path: Path to background image (default: grosbillfight.png)
        """
        try:
            self.screen_width = screen_width
            self.screen_height = screen_height
            Logger.debug("CombatView.__init__", "Initializing combat view", 
                        width=screen_width, height=screen_height)
            
            # === FONTS INITIALIZATION ===
            
            try:
                # Fonts for fullscreen (10% increase)
                self.title_font = pygame.font.SysFont("Arial", max(20, int(screen_height * 0.0254)), bold=True)
                self.font = pygame.font.SysFont("Arial", max(15, int(screen_height * 0.0153)), bold=True)
                self.small_font = pygame.font.SysFont("Arial", max(12, int(screen_height * 0.0141)))
                self.log_font = pygame.font.SysFont("Courier New", max(13, int(screen_height * 0.0128)))
                Logger.debug("CombatView.__init__", "Fonts initialized")
            except Exception as e:
                Logger.error("CombatView.__init__", e)
                # Use default fonts if SysFont fails
                self.title_font = pygame.font.Font(None, 40)
                self.font = pygame.font.Font(None, 20)
                self.small_font = pygame.font.Font(None, 18)
                self.log_font = pygame.font.Font(None, 16)
            
            # === COLORS ===
            
            self.bg_color = (20, 15, 30)
            self.panel_color = (40, 30, 50)
            self.text_color = (255, 255, 255)
            self.player_color = (50, 255, 50)
            self.enemy_color = (255, 50, 50)
            self.gold_color = (255, 215, 0)
            
            # === ANIMATION ===
            
            self.time = 0
            self.shake_offset = 0
            self.flash_alpha = 0
            
            # === BACKGROUND IMAGE ===
            
            self.background_image = None
            try:
                bg_img = pygame.image.load(background_image_path).convert()
                self.background_image = pygame.transform.scale(bg_img, (screen_width, screen_height))
                Logger.debug("CombatView.__init__", "Background image loaded", path=background_image_path)
            except FileNotFoundError:
                Logger.debug("CombatView.__init__", "Background image not found, using gradient", path=background_image_path)
            except Exception as e:
                Logger.error("CombatView.__init__", e)
                Logger.debug("CombatView.__init__", "Using gradient background")
            
            # === INVENTORY VIEW ===
            
            try:
                self.inventory_view = InventoryView(screen_width, screen_height)
                Logger.debug("CombatView.__init__", "Inventory view initialized")
            except Exception as e:
                Logger.error("CombatView.__init__", e)
                self.inventory_view = None
            
            Logger.debug("CombatView.__init__", "Combat view initialization completed")
            
        except Exception as e:
            Logger.error("CombatView.__init__", e)
            raise
        
    # === MAIN RENDERING ===
    
    def draw(self, screen, combat_model):
        """
        Main draw method for the combat view.
        Renders all combat UI elements including background, fighters, menus, and effects.
        
        Args:
            screen: Pygame surface to draw on
            combat_model: CombatModel instance containing combat state
        """
        try:
            self.time += 1
            
            # Draw background gradient
            try:
                self.drawBackground(screen)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw combat title
            try:
                self.drawTitle(screen, combat_model)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw fighter information
            try:
                self.drawFightersInfo(screen, combat_model)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw combat log
            try:
                self.drawCombatLog(screen, combat_model)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw action menu (if player's turn)
            try:
                if combat_model.isPlayerTurn() and not combat_model.isCombatFinished():
                    self.drawActionMenu(screen, combat_model)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw combat end screen
            try:
                if combat_model.isCombatFinished():
                    self.drawCombatEnd(screen, combat_model)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw turn indicator
            try:
                self.drawTurnIndicator(screen, combat_model)
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw visual effects
            try:
                if self.flash_alpha > 0:
                    self.drawFlash(screen)
                    self.flash_alpha -= 10
            except Exception as e:
                Logger.error("CombatView.draw", e)
            
            # Draw inventory (if player has one) - above alcohol position on left
            try:
                # Get player from combat_model
                player = None
                if hasattr(combat_model, 'getPlayer'):
                    player = combat_model.getPlayer()
                elif hasattr(combat_model, '_player'):
                    player = combat_model._player
                
                if player and hasattr(player, 'inventory') and self.inventory_view:
                    # Position: left side, above where alcohol would be displayed
                    inv_x = 115  # Left side, centered in box
                    inv_y = self.screen_height - 200 # Much higher above alcohol display
                    self.inventory_view.draw_inventory_display(screen, player.inventory, inv_x, inv_y)
            except Exception as e:
                Logger.error("CombatView.draw - inventory", e)
                
        except Exception as e:
            Logger.error("CombatView.draw", e)
    
    # === RENDERING METHODS ===
    
    def drawBackground(self, screen):
        """
        Draw background (either image or gradient).
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            if self.background_image:
                screen.blit(self.background_image, (0, 0))
            else:
                # Fallback to gradient if no image
                for y in range(self.screen_height):
                    try:
                        ratio = y / self.screen_height
                        r = int(20 + math.sin(self.time * 0.01 + ratio * 2) * 10)
                        g = int(15 + math.cos(self.time * 0.015 + ratio * 1.5) * 8)
                        b = int(30 + math.sin(self.time * 0.008 + ratio) * 15)
                        pygame.draw.line(screen, (r, g, b), (0, y), (self.screen_width, y))
                    except Exception as e:
                        Logger.error("CombatView.drawBackground", e)
                        continue
        except Exception as e:
            Logger.error("CombatView.drawBackground", e)
    
    def drawTitle(self, screen, combat_model):
        """Draw the combat title"""
        title_text = "COMBAT"
        title_surf = self.title_font.render(title_text, True, self.gold_color)
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        
        title_x = self.screen_width // 2 - title_surf.get_width() // 2
        title_y = 10  # Moved up to avoid overlap with turn indicator
        
        screen.blit(title_shadow, (title_x + 3, title_y + 3))
        screen.blit(title_surf, (title_x, title_y))
        
        # Turn
        turn_text = f"Turn {combat_model.getTurn()}"
        turn_surf = self.font.render(turn_text, True, (200, 200, 200))
        screen.blit(turn_surf, (self.screen_width // 2 - turn_surf.get_width() // 2, title_y + title_surf.get_height() + 5))
    
    def drawFightersInfo(self, screen, combat_model):
        """Draw fighter information panels"""
        player = combat_model.getPlayer()
        enemy = combat_model.getEnemy()
        # Try to position panels relative to character sprite positions so
        # characters appear centered and facing each other in the middle.
        try:
            player_x_center = int(player.getX())
            player_y_center = int(player.getY())
        except Exception:
            player_x_center = self.screen_width // 3
            player_y_center = 120

        try:
            enemy_x_center = int(enemy.getX())
            enemy_y_center = int(enemy.getY())
        except Exception:
            enemy_x_center = int(self.screen_width * 2 / 3)
            enemy_y_center = 120

        # Place panels above the sprites (clamped to screen)
        panel_width = 320  # Reduced from 460
        panel_height = 220  # Reduced from 300
        padding = 16  # Reduced from 24

        player_x = max(padding, min(player_x_center - panel_width // 2, self.screen_width - panel_width - padding))
        player_y = max(padding, player_y_center - panel_height - 40)

        panel_x = player_x - 20
        panel_y = player_y - 20

        # Panel joueur
        self.drawPanel(screen, panel_x, panel_y, panel_width, panel_height, self.player_color)

        # Prepare content positions and center the block vertically in the panel
        name_h = self.title_font.get_height()
        hp_h = 20  # Reduced from 30
        drunk_h = 18  # Reduced from 25
        stats_h = self.small_font.get_height()
        effects_h = 15  # Reduced from 20
        spacing = 6  # Reduced from 10

        content_height = name_h + spacing + hp_h + spacing + drunk_h + spacing + stats_h + spacing + effects_h
        start_y = panel_y + (panel_height - content_height) // 2

        # Name (left aligned inside panel)
        name_surf = self.title_font.render(player.getName(), True, self.player_color)
        screen.blit(name_surf, (panel_x + 16, start_y))

        # HP
        hp_y = start_y + name_h + spacing
        player_max = combat_model.getPlayerMaxHealth() if hasattr(combat_model, 'getPlayerMaxHealth') else 100
        self.drawHealthBar(screen, panel_x + 16, hp_y, panel_width - 32, hp_h, player.getHealth(), player_max, "HP", self.player_color)

        # Drunkenness
        drunk_y = hp_y + hp_h + spacing
        drunk = player.getDrunkenness()
        drunk_color = (255, 100, 255) if drunk > 60 else (100, 200, 255)
        self.drawProgressBar(screen, panel_x + 16, drunk_y, panel_width - 32, drunk_h, drunk, 100, f"Drunkenness: {drunk}%", drunk_color)

        # Stats
        stats_y = drunk_y + drunk_h + spacing
        stats_text = f"Damage: {player.getDamage()} | Accuracy: {int(player.getAccuracy() * 100)}%"
        stats_surf = self.small_font.render(stats_text, True, (200, 200, 200))
        screen.blit(stats_surf, (panel_x + 16, stats_y))

        # Status effects (placed under stats)
        self.drawStatusEffects(screen, panel_x + 16, stats_y + stats_h + spacing, combat_model, is_player=True)
        
        # === ENEMY (RIGHT) ===
        enemy_x = max(padding, min(enemy_x_center - panel_width // 2, self.screen_width - panel_width - padding))
        enemy_y = max(padding, enemy_y_center - panel_height - 40)

        enemy_panel_x = enemy_x - 20
        enemy_panel_y = enemy_y - 20

        # Panel ennemi
        self.drawPanel(screen, enemy_panel_x, enemy_panel_y, panel_width, panel_height, self.enemy_color)

        # Center enemy content block vertically
        name_h = self.title_font.get_height()
        hp_h = 20  # Reduced from 30
        drunk_h = 0  # enemy may not show drunkenness here
        stats_h = self.small_font.get_height()
        effects_h = 15  # Reduced from 20
        spacing = 6  # Reduced from 10

        content_height = name_h + spacing + hp_h + spacing + stats_h + spacing + effects_h
        start_y = enemy_panel_y + (panel_height - content_height) // 2

        # Name (right aligned inside panel)
        enemy_name_surf = self.title_font.render(enemy.getName(), True, self.enemy_color)
        screen.blit(enemy_name_surf, (enemy_panel_x + panel_width - enemy_name_surf.get_width() - 16, start_y))

        # HP
        enemy_hp_y = start_y + name_h + spacing
        enemy_max = combat_model.getEnemyMaxHealth() if hasattr(combat_model, 'getEnemyMaxHealth') else 100
        self.drawHealthBar(screen, enemy_panel_x + 16, enemy_hp_y, panel_width - 32, hp_h, enemy.getHealth(), enemy_max, "HP", self.enemy_color)

        # Stats
        enemy_stats_y = enemy_hp_y + hp_h + spacing
        enemy_stats_text = f"Damage: {enemy.getDamage()} | Accuracy: {int(enemy.getAccuracy() * 100)}%"
        enemy_stats_surf = self.small_font.render(enemy_stats_text, True, (200, 200, 200))
        screen.blit(enemy_stats_surf, (enemy_panel_x + 16, enemy_stats_y))

        # Status effects
        self.drawStatusEffects(screen, enemy_panel_x + 16, enemy_stats_y + stats_h + spacing, combat_model, is_player=False)
    
    def drawHealthBar(self, screen, x, y, width, height, current, maximum, label, color):
        """Dessiner une barre de vie"""
        ratio = current / maximum if maximum > 0 else 0
        
        # Fond
        pygame.draw.rect(screen, (20, 20, 20), (x, y, width, height), border_radius=8)
        
        # Remplissage
        filled_width = int(width * ratio)
        pygame.draw.rect(screen, color, (x, y, filled_width, height), border_radius=8)
        
        # Bordure
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2, border_radius=8)
        
        # Texte
        hp_text = f"{label}: {current}/{maximum}"
        text_surf = self.font.render(hp_text, True, (255, 255, 255))
        text_x = x + width // 2 - text_surf.get_width() // 2
        text_y = y + height // 2 - text_surf.get_height() // 2
        screen.blit(text_surf, (text_x, text_y))
    
    def drawProgressBar(self, screen, x, y, width, height, current, maximum, label, color):
        """Dessiner une barre de progression"""
        ratio = current / maximum if maximum > 0 else 0
        
        # Fond
        pygame.draw.rect(screen, (20, 20, 20), (x, y, width, height), border_radius=6)
        
        # Remplissage
        filled_width = int(width * ratio)
        pygame.draw.rect(screen, color, (x, y, filled_width, height), border_radius=6)
        
        # Bordure
        pygame.draw.rect(screen, (80, 80, 80), (x, y, width, height), 2, border_radius=6)
        
        # Texte
        text_surf = self.small_font.render(label, True, (255, 255, 255))
        text_x = x + width // 2 - text_surf.get_width() // 2
        text_y = y + height // 2 - text_surf.get_height() // 2
        screen.blit(text_surf, (text_x, text_y))
    
    def drawStatusEffects(self, screen, x, y, combat_model, is_player):
        """Dessiner les effets de statut actifs"""
        status_effects = []
        
        if is_player:
            if combat_model.getPlayerStatus("paralyzed") > 0:
                status_effects.append(f"Paralyzed ({combat_model.getPlayerStatus('paralyzed')})")
            if combat_model.getPlayerStatus("bleeding") > 0:
                status_effects.append(f"Bleeding ({combat_model.getPlayerStatus('bleeding')})")
            if combat_model.getPlayerStatus("stunned") > 0:
                status_effects.append(f"Stunned ({combat_model.getPlayerStatus('stunned')})")
        else:
            if combat_model.getEnemyStatus("paralyzed") > 0:
                status_effects.append(f"Paralyzed ({combat_model.getEnemyStatus('paralyzed')})")
            if combat_model.getEnemyStatus("bleeding") > 0:
                status_effects.append(f"Bleeding ({combat_model.getEnemyStatus('bleeding')})")
            if combat_model.getEnemyStatus("stunned") > 0:
                status_effects.append(f"Stunned ({combat_model.getEnemyStatus('stunned')})")
            if combat_model.getEnemyStatus("disgusted") > 0:
                status_effects.append(f"Disgusted ({combat_model.getEnemyStatus('disgusted')})")
        
        for i, effect in enumerate(status_effects):
            effect_surf = self.small_font.render(effect, True, (255, 200, 0))
            screen.blit(effect_surf, (x, y + i * 25))
    
    def drawCombatLog(self, screen, combat_model):
        """
        Draw the combat log with text wrapping.
        Messages stay within the rectangle boundaries.
        """
        # Position log at bottom, centered
        log_width = 650  # Reduced from 900
        log_x = self.screen_width // 2 - log_width // 2
        log_y = self.screen_height - 140  # Reduced from 190
        log_height = 120  # Reduced from 170
        
        # Draw panel background and border
        self.drawPanel(screen, log_x, log_y, log_width, log_height, (100, 150, 100))
        
        # Title
        title_surf = self.font.render("Battle Log", True, (150, 255, 150))
        screen.blit(title_surf, (log_x + 15, log_y + 8))
        
        # Messages with text wrapping, rendered into the log area using clipping
        messages = combat_model.getCombatLog() or []
        max_width = log_width - 40  # Leave padding on sides
        line_height = 15  # Reduced from 20
        max_lines = 4  # Reduced from 5

        # Build list of lines (wrapped) from recent messages
        wrapped_all = []
        for message in messages[-10:]:
            try:
                wrapped = self._wrap_text(message, max_width)
                wrapped_all.extend(wrapped)
            except Exception as e:
                Logger.error("CombatView.drawCombatLog.wrap", e)

        # Keep only the last `max_lines` lines
        display_lines = wrapped_all[-max_lines:]

        # Clip drawing to the log inner rect
        inner_rect = pygame.Rect(log_x + 20, log_y + 45, max_width, log_height - 60)
        prev_clip = screen.get_clip()
        screen.set_clip(inner_rect)

        # Draw from bottom up
        start_y = log_y + log_height - 25
        for line in reversed(display_lines):
            try:
                low = line.lower()
                if "coma" in low or "defeat" in low or "knocked" in low or "collapsed" in low:
                    text_color = (255, 100, 100)
                elif "victory" in low or "defeated" in low or "won" in low:
                    text_color = (100, 255, 100)
                elif "miss" in low or "failed" in low:
                    text_color = (200, 100, 100)
                else:
                    text_color = (220, 220, 220)

                msg_surf = self.log_font.render(line, True, text_color)
                screen.blit(msg_surf, (inner_rect.x, start_y - msg_surf.get_height()))
                start_y -= line_height
            except Exception as e:
                Logger.error("CombatView.drawCombatLog.render", e)

        # Restore previous clip
        screen.set_clip(prev_clip)
    
    def _wrap_text(self, text, max_width):
        """
        Wrap text to fit within max_width.
        Returns list of wrapped lines.
        """
        try:
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                test_surf = self.log_font.render(test_line, True, (255, 255, 255))
                
                if test_surf.get_width() <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            return lines
        except Exception as e:
            Logger.error("CombatView._wrap_text", e)
            return [text]  # Return original text if wrapping fails
    
    def drawActionMenu(self, screen, combat_model):
        """
        Draw the action menu with better alignment and visual hierarchy.
        """
        # Position menu on right side, fairly close to center but not overlapping main UI
        menu_width = 300  # Reduced from 380
        menu_x = max(40, self.screen_width - menu_width - 10)
        menu_y = self.screen_height - 410  # Adjusted to fit reduced height
        menu_height = 260  # Reduced from 320
        
        # Panel with player color accent
        self.drawPanel(screen, menu_x, menu_y, menu_width, menu_height, (100, 255, 100))
        
        # Title
        title_surf = self.font.render("ACTIONS", True, (150, 255, 150))
        screen.blit(title_surf, (menu_x + 20, menu_y + 10))
        
        # Divider line
        pygame.draw.line(screen, (100, 200, 100), 
                        (menu_x + 15, menu_y + 38), 
                        (menu_x + menu_width - 15, menu_y + 38), 3)
        
        # Actions with better spacing and color-coded keys
        actions = [
            ("A", "Simple Attack", "Strike with your guitar", (150, 255, 100)),
            ("P", "Power Chord", "Powerful burst (-10 HP)", (255, 180, 100)),
            ("D", "Dégueulando", "Paralyze (requires >=60% drunk)", (200, 100, 255)),
            ("B", "Drink", "Restore & boost stats", (100, 200, 255))
        ]
        
        action_y = menu_y + 50
        for key, name, desc, key_color in actions:
            # Key with custom color
            key_surf = self.font.render(f"[{key}]", True, key_color)
            screen.blit(key_surf, (menu_x + 15, action_y))
            
            # Name
            name_surf = self.small_font.render(name, True, (255, 255, 255))
            screen.blit(name_surf, (menu_x + 45, action_y))
            
            # Description
            desc_surf = self.log_font.render(desc, True, (200, 200, 200))
            screen.blit(desc_surf, (menu_x + 45, action_y + 18))
            
            # Divider between actions
            pygame.draw.line(screen, (80, 150, 80), 
                            (menu_x + 15, action_y + 42), 
                            (menu_x + menu_width - 15, action_y + 42), 1)
            
            action_y += 55  # Reduced spacing from 70
        
        # Hint text below the action menu frame
        if combat_model.isPlayerTurn():
            hint_surf = self.font.render("Press KEY to act", True, (150, 200, 150))
            hint_x = menu_x + menu_width // 2 - hint_surf.get_width() // 2
            screen.blit(hint_surf, (hint_x, menu_y + menu_height + 15))
    
    def drawTurnIndicator(self, screen, combat_model):
        """Draw the turn indicator"""
        if combat_model.isCombatFinished():
            return
        
        if combat_model.isPlayerTurn():
            text = "YOUR TURN"
            color = self.player_color
        else:
            text = "ENEMY TURN"
            color = self.enemy_color
        
        # Animation de pulsation
        scale = 1 + math.sin(self.time * 0.1) * 0.1
        
        indicator_surf = self.title_font.render(text, True, color)
        scaled_width = int(indicator_surf.get_width() * scale)
        scaled_height = int(indicator_surf.get_height() * scale)
        indicator_surf = pygame.transform.scale(indicator_surf, (scaled_width, scaled_height))
        
        indicator_x = self.screen_width // 2 - scaled_width // 2
        indicator_y = 150  # Positioned at top to avoid overlap
        
        # Ombre
        shadow_surf = self.title_font.render(text, True, (0, 0, 0))
        shadow_surf = pygame.transform.scale(shadow_surf, (scaled_width, scaled_height))
        screen.blit(shadow_surf, (indicator_x + 3, indicator_y + 3))
        
        screen.blit(indicator_surf, (indicator_x, indicator_y))
    
    def drawCombatEnd(self, screen, combat_model):
        """
        Draw the combat end screen.
        Displays victory or defeat message based on combat result.
        
        Args:
            screen: Pygame surface to draw on
            combat_model: CombatModel instance containing combat state
        """
        try:
            # Semi-transparent overlay
            try:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
            except Exception as e:
                Logger.error("CombatView.drawCombatEnd", e)
            
            # Victory/defeat message
            try:
                if combat_model.getWinner() == "PLAYER":
                    message = "VICTOIRE !"
                    color = self.player_color
                    sub_message = f"You defeated {combat_model.getEnemy().getName()}!"
                else:
                    message = "DÉFAITE"
                    color = self.enemy_color
                    sub_message = f"{combat_model.getEnemy().getName()} knocked you out!"
            except Exception as e:
                Logger.error("CombatView.drawCombatEnd", e)
                message = "COMBAT ENDED"
                color = (255, 255, 255)
                sub_message = ""
            
            # Main message
            try:
                msg_surf = self.title_font.render(message, True, color)
                msg_shadow = self.title_font.render(message, True, (0, 0, 0))
                
                msg_x = self.screen_width // 2 - msg_surf.get_width() // 2
                msg_y = self.screen_height // 2 - 100
                
                screen.blit(msg_shadow, (msg_x + 4, msg_y + 4))
                screen.blit(msg_surf, (msg_x, msg_y))
            except Exception as e:
                Logger.error("CombatView.drawCombatEnd", e)
            
            # Sub-message
            try:
                if sub_message:
                    sub_surf = self.font.render(sub_message, True, (255, 255, 255))
                    sub_x = self.screen_width // 2 - sub_surf.get_width() // 2
                    screen.blit(sub_surf, (sub_x, msg_y + 80))
            except Exception as e:
                Logger.error("CombatView.drawCombatEnd", e)
            
            # Instructions
            try:
                instruction = "Press SPACE to continue"
                inst_surf = self.small_font.render(instruction, True, (200, 200, 200))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                screen.blit(inst_surf, (inst_x, msg_y + 150))
            except Exception as e:
                Logger.error("CombatView.drawCombatEnd", e)
                
        except Exception as e:
            Logger.error("CombatView.drawCombatEnd", e)
    
    def drawPanel(self, screen, x, y, width, height, accent_color):
        """
        Draw a panel with border.
        
        Args:
            screen: Pygame surface to draw on
            x: X position of panel
            y: Y position of panel
            width: Panel width
            height: Panel height
            accent_color: Border accent color
        """
        try:
            # Background
            pygame.draw.rect(screen, self.panel_color, (x, y, width, height), border_radius=12)
            
            # Border
            pygame.draw.rect(screen, accent_color, (x, y, width, height), 3, border_radius=12)
        except Exception as e:
            Logger.error("CombatView.drawPanel", e)
    
    def drawFlash(self, screen):
        """
        Draw a white flash effect.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            flash_surf = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, self.flash_alpha))
            screen.blit(flash_surf, (0, 0))
        except Exception as e:
            Logger.error("CombatView.drawFlash", e)
    
    def triggerFlash(self):
        """
        Trigger a flash effect.
        Sets flash alpha to maximum value.
        """
        try:
            self.flash_alpha = 100
            Logger.debug("CombatView.triggerFlash", "Flash effect triggered")
        except Exception as e:
            Logger.error("CombatView.triggerFlash", e)