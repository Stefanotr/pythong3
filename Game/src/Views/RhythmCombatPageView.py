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
            boss: CaracterModel instance for the boss
            sequence_controller: Optional GameSequenceController for stage navigation
        """
        try:
            self.sequence_controller = sequence_controller
            self.player = player
            self.boss = boss
            
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
                self.combat_view = RhythmCombatView(self.screen_width, self.screen_height)
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
                    self.combat_view
                )
                Logger.debug("RhythmCombatPageView.__init__", "Rhythm combat controller created")
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
                            self.combat_view = RhythmCombatView(self.screen_width, self.screen_height)
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
                    # Increment player level
                    if self.player:
                        current_level = self.player.getLevel()
                        self.player.setLevel(current_level + 1)
                        Logger.debug("RhythmCombatPageView.run", "Player level incremented", 
                                   old_level=current_level, new_level=current_level + 1)
                        
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
            self.combat_view = RhythmCombatView(self.screen_width, self.screen_height)
            
            # Update controller's screen height reference if available
            if self.controller and hasattr(self.controller, 'screen_height'):
                self.controller.screen_height = self.screen_height
                
        except Exception as e:
            Logger.error("RhythmCombatPageView._toggle_fullscreen", e)
