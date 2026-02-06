"""
RhythmCombatPageView Module

Handles the rhythm combat boss fight view.
Wraps RhythmCombatController in a game loop structure with event handling.
"""

import pygame
from Controllers.RhythmCombatController import RhythmCombatController
from Views.RhythmCombatView import RhythmCombatView
from Views.FinTransitionPageView import FinTransitionPageView
from Controllers.GameState import GameState
from Controllers.GameSequenceController import GameSequenceController
from Models.RhythmModel import RhythmModel
from Utils.Logger import Logger
from Songs.TheFinalCountdown import load_final_countdown


class RhythmCombatPageView:
    """
    View class for the rhythm combat boss fight.
    Manages the final boss combat with rhythm mechanics.
    """
    
    def __init__(self, screen, player=None, boss=None, sequence_controller=None):
        """
        Initialize the rhythm combat page view.
        
        Args:
            screen: Pygame surface for rendering
            player: PlayerModel instance
            boss: CaracterModel instance for the boss (optional, uses sequence_controller if not provided)
            sequence_controller: Optional GameSequenceController for stage navigation
        """
        try:
            self.sequence_controller = sequence_controller
            self.player = player
            
            # Get boss from parameter or sequence controller
            self.boss = boss
            if not self.boss and self.sequence_controller:
                self.boss = self.sequence_controller.get_boss()
            
            if not self.boss:
                Logger.error("RhythmCombatPageView.__init__", "No boss provided or found in sequence controller")
                raise ValueError("Boss instance is required for rhythm combat")
            
            # === BOSS HEALTH MANAGEMENT ===
            # Scale boss health based on player level, but only once
            if not hasattr(self.boss, '_rhythm_combat_max_health'):
                # First time in rhythm combat - scale health based on player level
                try:
                    player_level = self.player.getLevel() if self.player else 0
                    base_health = 3000
                    # Add HP progression: +50 HP per level (more aggressive for final boss)
                    scaled_health = int(base_health + (player_level * 50))
                    self.boss.setHealth(scaled_health)
                    self.boss._rhythm_combat_max_health = scaled_health
                    
                    # Also scale damage: +1 damage per level
                    base_damage = 15
                    scaled_damage = int(base_damage + (player_level * 1))
                    self.boss.setDamage(scaled_damage)
                    
                    Logger.debug("RhythmCombatPageView.__init__", "Boss initialized for rhythm combat",
                               boss_name=self.boss.getName(), level=player_level, health=scaled_health, damage=scaled_damage)
                except Exception as e:
                    Logger.error("RhythmCombatPageView.__init__", f"Error scaling boss health: {e}")
                    self.boss.setHealth(3000)
                    self.boss.setDamage(15)
                    self.boss._rhythm_combat_max_health = 3000
            else:
                Logger.debug("RhythmCombatPageView.__init__", "Boss already initialized, current health",
                           boss_name=self.boss.getName(), current_health=self.boss.getHealth())
            
            # Store the locked max health for display purposes
            self.boss_max_health = self.boss._rhythm_combat_max_health
            Logger.debug("RhythmCombatPageView.__init__", f"Boss max health stored as {self.boss_max_health}, actual health: {self.boss.getHealth()}")
            
            # === PLAYER HEALTH MANAGEMENT ===
            # Use player's current health as the base max health
            # This will be updated dynamically during gameplay
            self.player_max_health = 100  # Default fallback
            if self.player:
                try:
                    # Use current player health as max (will update if player gains HP from leveling)
                    self.player_max_health = self.player.getHealth()
                    Logger.debug("RhythmCombatPageView.__init__", "Player max health set",
                               max_health=self.player_max_health)
                except Exception as e:
                    Logger.error("RhythmCombatPageView.__init__", "Error setting player max health", error=str(e))
            
            # Get screen dimensions and create resizable window
            try:
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                
                # Set window to center
                try:
                    import os
                    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
                except:
                    pass
                
                # Create resizable window at full screen size
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                
                Logger.debug("RhythmCombatPageView.__init__", "Screen dimensions set", 
                           width=self.screen_width, height=self.screen_height)
            except Exception as e:
                Logger.error("RhythmCombatPageView.__init__", e)
                # Fallback to screen size
                self.screen_width, self.screen_height = screen.get_size()
            
            # Create rhythm model and view
            try:
                self.rhythm_model = RhythmModel()
                self.combat_view = RhythmCombatView(self.screen_width, self.screen_height, self.boss_max_health, self.player_max_health, background_image_path="Game/Assets/managerevade.png")
                Logger.debug("RhythmCombatPageView.__init__", "Rhythm and combat views created")
            except Exception as e:
                Logger.error("RhythmCombatPageView.__init__", e)
                raise
            
            # Create combat controller
            try:
                self.controller = RhythmCombatController(
                    self.rhythm_model,
                    self.player,
                    self.boss,
                    self.screen_height,
                    self.combat_view,
                    load_final_countdown()

                )
                Logger.debug("RhythmCombatPageView.__init__", "Rhythm combat controller created",
                           boss_health=self.boss.getHealth())
            except Exception as e:
                Logger.error("RhythmCombatPageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("RhythmCombatPageView.__init__", e)
            raise
    
    def run(self):
        """
        Main loop for the rhythm combat view.
        Handles events, updates game state, and renders the combat.
        
        Returns:
            str: Result ("COMPLETE" if boss defeated, "QUIT", or GameState value)
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("RhythmCombatPageView.run", "Rhythm combat loop started")
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("RhythmCombatPageView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.KEYDOWN:
                            # === HANDLE F11 FOR FULLSCREEN TOGGLE ===
                            if event.key == pygame.K_F11:
                                try:
                                    self._toggle_fullscreen()
                                except Exception as e:
                                    Logger.error("RhythmCombatPageView.run", e)
                            
                            # === HANDLE NUMERIC KEYS (1-8) FOR STAGE NAVIGATION ===
                            elif self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  # Convert to 1-8
                                if self.sequence_controller.handle_numeric_input(stage_number):
                                    Logger.debug("RhythmCombatPageView.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stage_name=self.sequence_controller.get_current_stage_name())
                                    # Return a special code to indicate stage change
                                    return f"STAGE_{stage_number}"
                        
                        elif event.type == pygame.VIDEORESIZE:
                            self.screen_width = event.w
                            self.screen_height = event.h
                            # Recreate combat view with new dimensions
                            self.combat_view = RhythmCombatView(self.screen_width, self.screen_height, self.boss_max_health, self.player_max_health, background_image_path="Game/Assets/managerevade.png")
                            Logger.debug("RhythmCombatPageView.run", "Window resized", width=self.screen_width, height=self.screen_height)
                        
                        
                        # Pass other events to the controller
                        try:
                            if self.controller:
                                self.controller.handle_input(event)
                        except Exception as e:
                            Logger.error("RhythmCombatPageView.run", e)
                    
                    # === UPDATE ===
                    try:
                        if self.controller:
                            # Update controller state (countdown, notes, etc.)
                            self.controller.update()
                            
                            # Check victory condition
                            if hasattr(self.controller, 'victory') and self.controller.victory:
                                Logger.debug("RhythmCombatPageView.run", "Combat completed - Victory!")
                                running = False
                            
                            # Check game over condition
                            if hasattr(self.controller, 'game_over') and self.controller.game_over:
                                Logger.debug("RhythmCombatPageView.run", "Combat completed - Game Over!")
                                running = False
                    except Exception as e:
                        Logger.error("RhythmCombatPageView.run", e)
                    
                    # === RENDERING ===
                    try:
                        self.screen.fill((0, 0, 0))
                        
                        # === UPDATE CHARACTER ANIMATIONS ===
                        if self.player:
                            self.player.updateActionTimer()
                        if self.boss:
                            self.boss.updateActionTimer()
                        
                        # Get current countdown value
                        countdown_val = 0
                        if hasattr(self.controller, 'waiting_to_start') and self.controller.waiting_to_start:
                            countdown_val = max(1, self.controller.current_countdown_val)
                        
                        # Get note speed if available
                        note_speed = getattr(self.controller, 'note_speed', 0.5)
                        
                        # Draw the combat view
                        if self.combat_view and self.rhythm_model:
                            self.combat_view.draw(
                                self.screen,
                                self.rhythm_model,
                                self.player,
                                self.boss,
                                note_speed,
                                countdown_val
                            )
                        
                        pygame.display.flip()
                    except Exception as e:
                        Logger.error("RhythmCombatPageView.run", e)
                    
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("RhythmCombatPageView.run", e)
                    continue
            
            # === DETERMINE RESULT ===
            try:
                if hasattr(self.controller, 'victory') and self.controller.victory:
                    Logger.debug("RhythmCombatPageView.run", "Rhythm combat completed successfully - showing victory transition")
                    
                    # Calculate and apply victory rewards
                    self.controller.end_combat()
                    
                    # Increment player level and apply stat progression
                    if self.player:
                        current_level = self.player.getLevel()
                        new_level = current_level + 1
                        self.player.setLevel(new_level)
                        
                        # Apply progression: +1 damage and +25 HP per level
                        current_damage = self.player.getDamage()
                        new_damage = current_damage + 1
                        self.player.setDamage(new_damage)
                        
                        current_health = self.player.getHealth()
                        new_health = current_health + 25
                        self.player.setHealth(new_health)
                        
                        Logger.debug("RhythmCombatPageView.run", "Player level incremented and stats increased", 
                                   old_level=current_level, new_level=new_level,
                                   new_damage=new_damage, new_health=new_health)
                        
                        # Check if this is the last stage (stage 8 - RHYTHM_COMBAT)
                        is_last_stage = (self.sequence_controller and 
                                        self.sequence_controller.get_current_stage() == 8)
                        
                        if is_last_stage:
                            # Reset player stats for next playthrough
                            self.player.setHealth(100)
                            self.player.setDrunkenness(0)
                            self.player.setComaRisk(0)
                            Logger.debug("RhythmCombatPageView.run", "Player stats reset for new playthrough", 
                                       health=100, drunkenness=0, coma_risk=0)
                    
                    # Show victory transition screen with 5-second auto-advance
                    transition = FinTransitionPageView(
                        self.screen,
                        message="Stage Complete!",
                        next_stage_name="Continued Adventure",
                        duration_seconds=5
                    )
                    transition.run()
                    
                    # After transition, return to stage 1 (RhythmPageView)
                    return "STAGE_1"
                else:
                    Logger.debug("RhythmCombatPageView.run", "Rhythm combat ended (not victory) - showing defeat transition then returning to main menu")
                    
                    # Stop music when defeated
                    try:
                        if self.controller:
                            if hasattr(self.controller, 'guitar_channel'):
                                self.controller.guitar_channel.stop()
                            if hasattr(self.controller, 'track_backing'):
                                self.controller.track_backing.stop()
                    except Exception as e:
                        Logger.error("RhythmCombatPageView.run - Stop music on defeat", e)
                    
                    # Show defeat transition screen with 3-second auto-advance
                    transition = FinTransitionPageView(
                        self.screen,
                        message="Game Over",
                        next_stage_name="Main Menu",
                        duration_seconds=3
                    )
                    transition.run()
                    
                    # After transition, return to main menu
                    return GameState.MAIN_MENU.value
            except Exception as e:
                Logger.error("RhythmCombatPageView.run", e)
                return GameState.QUIT.value
        except Exception as e:
            Logger.error("RhythmCombatPageView.run", e)
            return GameState.QUIT.value
    
    def _toggle_fullscreen(self):
        """Toggle between fullscreen and resizable window modes."""
        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
                # Currently fullscreen, switch to resizable
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                Logger.debug("RhythmCombatPageView._toggle_fullscreen", "Switched to RESIZABLE mode")
            else:
                # Currently resizable, switch to fullscreen
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.FULLSCREEN
                )
                Logger.debug("RhythmCombatPageView._toggle_fullscreen", "Switched to FULLSCREEN mode")
            
            # Recreate combat view with new dimensions
            self.combat_view = RhythmCombatView(self.screen_width, self.screen_height, self.boss_max_health, self.player_max_health, background_image_path="Game/Assets/managerevade.png")
            
            # Update controller's screen height reference if available
            if self.controller and hasattr(self.controller, 'screen_height'):
                self.controller.screen_height = self.screen_height
                
        except Exception as e:
            Logger.error("RhythmCombatPageView._toggle_fullscreen", e)
