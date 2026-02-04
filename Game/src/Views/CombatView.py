"""
CombatView Module

Handles the visual representation of turn-based combat interface.
Manages rendering of combat UI, health bars, status effects, and combat log.
"""

import pygame
import math
from Utils.Logger import Logger


# === COMBAT VIEW CLASS ===

class CombatView:
    """
    View class for rendering turn-based combat interface.
    Displays fighter information, health bars, status effects, action menu, and combat log.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize the combat view with screen dimensions.
        
        Args:
            screen_width: Width of the screen in pixels
            screen_height: Height of the screen in pixels
        """
        try:
            self.screen_width = screen_width
            self.screen_height = screen_height
            Logger.debug("CombatView.__init__", "Initializing combat view", 
                        width=screen_width, height=screen_height)
            
            # === FONTS INITIALIZATION ===
            
            try:
                self.title_font = pygame.font.SysFont("Arial", int(screen_height * 0.05), bold=True)
                self.font = pygame.font.SysFont("Arial", int(screen_height * 0.025), bold=True)
                self.small_font = pygame.font.SysFont("Arial", int(screen_height * 0.02))
                self.log_font = pygame.font.SysFont("Courier New", int(screen_height * 0.018))
                Logger.debug("CombatView.__init__", "Fonts initialized")
            except Exception as e:
                Logger.error("CombatView.__init__", e)
                # Use default fonts if SysFont fails
                self.title_font = pygame.font.Font(None, 48)
                self.font = pygame.font.Font(None, 24)
                self.small_font = pygame.font.Font(None, 20)
                self.log_font = pygame.font.Font(None, 18)
            
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
                
        except Exception as e:
            Logger.error("CombatView.draw", e)
    
    # === RENDERING METHODS ===
    
    def drawBackground(self, screen):
        """
        Draw animated gradient background.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
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
        title_text = "⚔️ COMBAT ⚔️"
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
        
        # Position fighters higher to avoid overlap with action menu and combat log
        mid_y = self.screen_height // 2 - 200
        
        # === PLAYER (LEFT) ===
        player_x = 100
        player_y = mid_y
        
        # Panel joueur
        panel_width = 400
        panel_height = 250
        self.drawPanel(screen, player_x - 20, player_y - 20, panel_width, panel_height, self.player_color)
        
        # Nom
        name_surf = self.title_font.render(player.getName(), True, self.player_color)
        screen.blit(name_surf, (player_x, player_y))
        
        # HP
        hp_y = player_y + 50
        self.drawHealthBar(screen, player_x, hp_y, 350, 30, player.getHealth(), 100, "HP", self.player_color)
        
        # Drunkenness
        drunk_y = hp_y + 45  # Reduced spacing
        drunk = player.getDrunkenness()
        drunk_color = (255, 100, 255) if drunk > 60 else (100, 200, 255)
        self.drawProgressBar(screen, player_x, drunk_y, 350, 25, drunk, 100, f"Drunkenness: {drunk}%", drunk_color)
        
        # Stats
        stats_y = drunk_y + 40  # Reduced spacing
        stats_text = f"Damage: {player.getDamage()} | Accuracy: {int(player.getAccuracy() * 100)}%"
        stats_surf = self.small_font.render(stats_text, True, (200, 200, 200))
        screen.blit(stats_surf, (player_x, stats_y))
        
        # Status effects
        self.drawStatusEffects(screen, player_x, stats_y + 25, combat_model, is_player=True)  # Reduced spacing
        
        # === ENEMY (RIGHT) ===
        enemy_x = self.screen_width - panel_width - 100 + 20
        enemy_y = mid_y
        
        # Panel ennemi
        self.drawPanel(screen, enemy_x - 20, enemy_y - 20, panel_width, panel_height, self.enemy_color)
        
        # Nom
        enemy_name_surf = self.title_font.render(enemy.getName(), True, self.enemy_color)
        screen.blit(enemy_name_surf, (enemy_x + panel_width - enemy_name_surf.get_width() - 20, enemy_y))
        
        # HP
        enemy_hp_y = enemy_y + 50
        self.drawHealthBar(screen, enemy_x, enemy_hp_y, 350, 30, enemy.getHealth(), 100, "HP", self.enemy_color)
        
        # Stats
        enemy_stats_y = enemy_hp_y + 45  # Reduced spacing
        enemy_stats_text = f"Damage: {enemy.getDamage()} | Accuracy: {int(enemy.getAccuracy() * 100)}%"
        enemy_stats_surf = self.small_font.render(enemy_stats_text, True, (200, 200, 200))
        screen.blit(enemy_stats_surf, (enemy_x, enemy_stats_y))
        
        # Status effects
        self.drawStatusEffects(screen, enemy_x, enemy_stats_y + 25, combat_model, is_player=False)  # Reduced spacing
    
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
                status_effects.append(f"⚡ Paralyzed ({combat_model.getPlayerStatus('paralyzed')})")
            if combat_model.getPlayerStatus("bleeding") > 0:
                status_effects.append(f"💉 Bleeding ({combat_model.getPlayerStatus('bleeding')})")
            if combat_model.getPlayerStatus("stunned") > 0:
                status_effects.append(f"💫 Stunned ({combat_model.getPlayerStatus('stunned')})")
        else:
            if combat_model.getEnemyStatus("paralyzed") > 0:
                status_effects.append(f"⚡ Paralyzed ({combat_model.getEnemyStatus('paralyzed')})")
            if combat_model.getEnemyStatus("bleeding") > 0:
                status_effects.append(f"💉 Bleeding ({combat_model.getEnemyStatus('bleeding')})")
            if combat_model.getEnemyStatus("stunned") > 0:
                status_effects.append(f"💫 Stunned ({combat_model.getEnemyStatus('stunned')})")
            if combat_model.getEnemyStatus("disgusted") > 0:
                status_effects.append(f"🤮 Disgusted ({combat_model.getEnemyStatus('disgusted')})")
        
        for i, effect in enumerate(status_effects):
            effect_surf = self.small_font.render(effect, True, (255, 200, 0))
            screen.blit(effect_surf, (x, y + i * 25))
    
    def drawCombatLog(self, screen, combat_model):
        """Draw the combat log"""
        # Position log at bottom, but leave space for action menu if visible
        log_x = self.screen_width // 2 - 400
        log_y = self.screen_height - 180  # Moved up to avoid overlap
        log_width = 800
        log_height = 150  # Reduced height
        
        # Panel
        self.drawPanel(screen, log_x, log_y, log_width, log_height, (100, 100, 100))
        
        # Title
        title_surf = self.font.render("📜 Combat Log", True, self.gold_color)
        screen.blit(title_surf, (log_x + 10, log_y + 10))
        
        # Messages
        messages = combat_model.getCombatLog()
        message_y = log_y + 50
        
        for message in messages[-6:]:  # Display the last 6 messages
            msg_surf = self.log_font.render(message, True, (220, 220, 220))
            screen.blit(msg_surf, (log_x + 20, message_y))
            message_y += 25
    
    def drawActionMenu(self, screen, combat_model):
        """Draw the action menu"""
        # Position menu on left side, above combat log
        menu_x = 50
        menu_y = self.screen_height - 500  # Moved up to avoid overlap with log
        menu_width = 350
        menu_height = 300  # Reduced height
        
        # Panel
        self.drawPanel(screen, menu_x, menu_y, menu_width, menu_height, self.player_color)
        
        # Title
        title_surf = self.font.render("🎸 ACTIONS", True, self.gold_color)
        screen.blit(title_surf, (menu_x + 20, menu_y + 10))
        
        # Actions
        actions = [
            ("A", "Simple Attack", "Strike with your guitar"),
            ("P", "Power Chord", "Powerful attack (-10 HP)"),
            ("D", "Dégueulando", "Paralyzes enemy (60% drunkenness)"),
            ("B", "Drink", "Increases your stats")
        ]
        
        action_y = menu_y + 60
        for key, name, desc in actions:
            # Key
            key_surf = self.font.render(f"[{key}]", True, self.gold_color)
            screen.blit(key_surf, (menu_x + 20, action_y))
            
            # Name
            name_surf = self.small_font.render(name, True, (255, 255, 255))
            screen.blit(name_surf, (menu_x + 80, action_y))
            
            # Description
            desc_surf = self.log_font.render(desc, True, (180, 180, 180))
            screen.blit(desc_surf, (menu_x + 80, action_y + 25))
            
            action_y += 60  # Reduced spacing between actions
    
    def drawTurnIndicator(self, screen, combat_model):
        """Draw the turn indicator"""
        if combat_model.isCombatFinished():
            return
        
        if combat_model.isPlayerTurn():
            text = "🎸 YOUR TURN"
            color = self.player_color
        else:
            text = "👊 ENEMY TURN"
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
                    message = "🏆 VICTOIRE ! 🏆"
                    color = self.player_color
                    sub_message = f"You defeated {combat_model.getEnemy().getName()}!"
                else:
                    message = "💀 DÉFAITE 💀"
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