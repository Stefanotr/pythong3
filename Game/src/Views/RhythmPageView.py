"""
RhythmPageView Module

Handles the final rhythm sequence view.
Uses existing RhythmModel, RhythmController, and RhythmView classes.
"""

import pygame
from Models.PlayerModel import PlayerModel
from Models.RhythmModel import RhythmModel
from Controllers.RhythmController import RhythmController
from Views.RhythmView import RhythmView
from Views.PauseMenuView import PauseMenuView
from Utils.Logger import Logger


# === RHYTHM PAGE VIEW CLASS ===

class RhythmPageView:
    """
    View class for the final rhythm sequence.
    Wraps existing rhythm classes in a game loop structure.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, player=None):
        """
        Initialize the rhythm page view.
        
        Args:
            screen: Pygame surface for rendering
            player: Optional PlayerModel instance to preserve state (if None, creates new)
        """
        try:
            self.screen = screen
            
            # Get screen dimensions
            try:
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                Logger.debug("RhythmPageView.__init__", "Screen dimensions retrieved", 
                           width=self.screen_width, height=self.screen_height)
            except Exception as e:
                Logger.error("RhythmPageView.__init__", e)
                # Fallback to screen size
                self.screen_width, self.screen_height = screen.get_size()
            
            Logger.debug("RhythmPageView.__init__", "Rhythm page view initialized")
            
            # === PLAYER INITIALIZATION ===
            
            try:
                if player is not None:
                    # Use provided player to preserve state (drunkenness, etc.)
                    self.johnny = player
                    # Ensure health is full for rhythm game (but keep drunkenness)
                    self.johnny.setHealth(100)
                    Logger.debug("RhythmPageView.__init__", "Using provided player", 
                               name=self.johnny.getName(), 
                               health=self.johnny.getHealth(),
                               drunkenness=self.johnny.getDrunkenness())
                else:
                    # Create new player if none provided
                    self.johnny = PlayerModel("Johnny Fuzz", 60, 60)
                    self.johnny.setHealth(100)
                    self.johnny.setDrunkenness(0)
                    Logger.debug("RhythmPageView.__init__", "New player created", 
                               name=self.johnny.getName())
            except Exception as e:
                Logger.error("RhythmPageView.__init__", e)
                raise
            
            # === RHYTHM SYSTEM INITIALIZATION ===
            
            try:
                # Create rhythm model
                self.rhythm_model = RhythmModel()
                
                # Create rhythm view
                self.rhythm_view = RhythmView(self.screen_width, self.screen_height)
                
                # Create a boss for attack simulation on missed notes
                from Models.CaracterModel import CaracterModel
                rhythm_boss = CaracterModel("Final Boss", 80, 80)
                rhythm_boss.setDamage(10)  # Stronger boss for final sequence
                
                # Create rhythm controller with boss
                self.rhythm_controller = RhythmController(
                    self.rhythm_model, 
                    self.johnny, 
                    self.screen_height, 
                    self.rhythm_view,
                    rhythm_boss  # Pass boss for attack simulation
                )
                
                Logger.debug("RhythmPageView.__init__", "Rhythm system initialized", 
                           total_notes=len(self.rhythm_model.getNotes()))
            except Exception as e:
                Logger.error("RhythmPageView.__init__", e)
                raise
            
            # === COUNTDOWN STATE ===
            
            self.countdown_active = True
            self.countdown_timer = 5 * 60  # 5 seconds at 60fps
            self.game_complete = False
            
        except Exception as e:
            Logger.error("RhythmPageView.__init__", e)
            raise
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main loop for the rhythm page view.
        Handles events, updates game state, and renders rhythm game.
        
        Returns:
            str: Result ("COMPLETE" or "QUIT")
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("RhythmPageView.run", "Rhythm page loop started")
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("RhythmPageView.run", "QUIT event received")
                            return "QUIT"
                        
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            # Open pause menu (only if countdown is finished)
                            if not self.countdown_active:
                                try:
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()

                                    if pause_result == "quit":
                                        Logger.debug("RhythmPageView.run", "Quit requested from pause menu")
                                        return "QUIT"
                                    elif pause_result == "main_menu":
                                        Logger.debug("RhythmPageView.run", "Main menu requested from pause menu")
                                        return "MAIN_MENU"

                                    # If "continue" or anything else, just resume the game loop
                                    Logger.debug("RhythmPageView.run", "Resuming from pause menu")
                                except Exception as e:
                                    Logger.error("RhythmPageView.run", e)
                        
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen_width = new_width
                                self.screen_height = new_height
                                
                                # Update screen if it's a resizable window
                                try:
                                    self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                                except Exception:
                                    # Screen might not be resizable, just update dimensions
                                    pass
                                
                                # Recreate rhythm view with new dimensions
                                try:
                                    self.rhythm_view = RhythmView(self.screen_width, self.screen_height)
                                    # Update controller with new view
                                    self.rhythm_controller.view = self.rhythm_view
                                    Logger.debug("RhythmPageView.run", "Window resized, rhythm view updated", 
                                               width=new_width, height=new_height)
                                except Exception as e:
                                    Logger.error("RhythmPageView.run", e)
                                    
                            except Exception as e:
                                Logger.error("RhythmPageView.run", e)
                        
                        # Countdown events (no skipping allowed)
                        # Rhythm game events
                        if not self.countdown_active:
                            try:
                                if self.rhythm_controller:
                                    self.rhythm_controller.handleInput(event)
                                
                                # Check for completion (SPACE to finish)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    if self.isRhythmComplete():
                                        self.game_complete = True
                                        running = False
                                        Logger.debug("RhythmPageView.run", "Rhythm game completed")
                            except Exception as e:
                                Logger.error("RhythmPageView.run", e)
                    
                    # === UPDATE ===
                    
                    if self.countdown_active:
                        self.countdown_timer -= 1
                        if self.countdown_timer <= 0:
                            self.countdown_active = False
                            Logger.debug("RhythmPageView.run", "Countdown finished, starting rhythm game")
                    else:
                        try:
                            if self.rhythm_controller:
                                self.rhythm_controller.update()
                            
                            # Check if rhythm is complete
                            if self.isRhythmComplete() and not self.game_complete:
                                self.game_complete = True
                                Logger.debug("RhythmPageView.run", "Rhythm game completed automatically")
                        except Exception as e:
                            Logger.error("RhythmPageView.run", e)
                    
                    # === RENDERING ===
                    
                    try:
                        if self.countdown_active:
                            self.drawCountdown()
                        else:
                            if self.rhythm_view and self.rhythm_model:
                                self.rhythm_view.draw(self.screen, self.rhythm_model, self.johnny)
                    except Exception as e:
                        Logger.error("RhythmPageView.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("RhythmPageView.run", e)
                    # Continue running even if one frame fails
                    continue
            
            # === DETERMINE RESULT ===
            
            try:
                if self.game_complete:
                    Logger.debug("RhythmPageView.run", "Final rhythm sequence completed")
                    return "COMPLETE"
                else:
                    Logger.debug("RhythmPageView.run", "Rhythm sequence ended")
                    return "QUIT"
            except Exception as e:
                Logger.error("RhythmPageView.run", e)
                return "QUIT"
                
        except Exception as e:
            Logger.error("RhythmPageView.run", e)
            return "QUIT"
    
    # === RHYTHM COMPLETION CHECK ===
    
    def isRhythmComplete(self):
        """
        Check if the rhythm game is complete.
        
        Returns:
            bool: True if all notes are completed or player health is too low
        """
        try:
            if not self.rhythm_model:
                return True
            
            # Check if all notes are inactive (completed or missed)
            active_notes = [n for n in self.rhythm_model.getNotes() if n.get("active", False)]
            
            # Also check if player is dead
            if self.johnny.getHealth() <= 0:
                return True
            
            # Complete if no active notes remain
            return len(active_notes) == 0
            
        except Exception as e:
            Logger.error("RhythmPageView.isRhythmComplete", e)
            return True
    
    # === RENDERING ===
    
    def drawCountdown(self):
        """
        Draw the 5-second countdown before starting the rhythm game.
        Displays large numbers: 5, 4, 3, 2, 1, GO!
        """
        try:
            # Black background
            try:
                self.screen.fill((0, 0, 0))
            except Exception as e:
                Logger.error("RhythmPageView.drawCountdown", e)
            
            # Calculate remaining seconds (countdown from 5 to 0)
            remaining_seconds = (self.countdown_timer // 60)
            
            # Determine countdown text
            if remaining_seconds >= 5:
                countdown_text = "5"
            elif remaining_seconds >= 4:
                countdown_text = "4"
            elif remaining_seconds >= 3:
                countdown_text = "3"
            elif remaining_seconds >= 2:
                countdown_text = "2"
            elif remaining_seconds >= 1:
                countdown_text = "1"
            else:
                countdown_text = "GO!"
            
            # Font setup
            try:
                if countdown_text == "GO!":
                    font_size = int(self.screen_height * 0.15)  # Larger for GO!
                else:
                    font_size = int(self.screen_height * 0.2)  # Very large numbers
                countdown_font = pygame.font.SysFont("Arial", font_size, bold=True)
            except Exception as e:
                Logger.error("RhythmPageView.drawCountdown", e)
                countdown_font = pygame.font.Font(None, 150)
            
            # Render countdown text
            try:
                countdown_surf = countdown_font.render(countdown_text, True, (255, 215, 0))  # Gold color
                countdown_shadow = countdown_font.render(countdown_text, True, (100, 80, 0))  # Dark shadow
                
                # Center on screen
                countdown_x = (self.screen_width - countdown_surf.get_width()) // 2
                countdown_y = (self.screen_height - countdown_surf.get_height()) // 2
                
                # Draw shadow first
                self.screen.blit(countdown_shadow, (countdown_x + 5, countdown_y + 5))
                # Draw text
                self.screen.blit(countdown_surf, (countdown_x, countdown_y))
            except Exception as e:
                Logger.error("RhythmPageView.drawCountdown", e)
                
        except Exception as e:
            Logger.error("RhythmPageView.drawCountdown", e)
    
    def drawIntro(self):
        """
        Draw the final rhythm sequence introduction screen.
        Displays story text, title, and instructions.
        (DEPRECATED - replaced by countdown)
        """
        try:
            # Black background
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
            # Fonts
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.06), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.025))
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.02))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
                # Use default fonts if SysFont fails
                title_font = pygame.font.Font(None, 72)
                text_font = pygame.font.Font(None, 30)
                small_font = pygame.font.Font(None, 24)
            
            # Title
            try:
                title_text = "🎸 FINAL RHYTHM SEQUENCE 🎵"
                title_surf = title_font.render(title_text, True, (255, 215, 0))
                title_shadow = title_font.render(title_text, True, (100, 80, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
            # Story
            try:
                story_lines = [
                    "This is it! The final performance!",
                    "",
                    "Show the world you're still a legend!",
                    "Hit the notes with perfect timing!",
                    "",
                    "Use keys C, V, B, N to hit notes",
                    "on the four guitar strings.",
                    "",
                    "Miss too many and the audience",
                    "will throw soda cans at you!"
                ]
                
                story_y = title_y + 120
                for line in story_lines:
                    if line:
                        try:
                            line_surf = text_font.render(line, True, (220, 220, 220))
                            line_x = self.screen_width // 2 - line_surf.get_width() // 2
                            self.screen.blit(line_surf, (line_x, story_y))
                        except Exception as e:
                            Logger.error("RhythmPageView.draw_intro", e)
                            continue
                    story_y += 35
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
            # Instructions
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
            # Blinking animation
            try:
                if (self.intro_timer // 30) % 2 == 0:
                    skip_text = "(or wait 3 seconds)"
                    skip_surf = small_font.render(skip_text, True, (100, 100, 100))
                    skip_x = self.screen_width // 2 - skip_surf.get_width() // 2
                    self.screen.blit(skip_surf, (skip_x, self.screen_height - 70))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
                
        except Exception as e:
            Logger.error("RhythmPageView.draw_intro", e)

