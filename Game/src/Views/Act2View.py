"""
Act2View Module

Handles Act 2: "Wood-Stock-Option" Festival.
Manages combat against Security Chief and rhythm mini-game phase.
"""

import pygame
import os
from Models.CaracterModel import CaracterModel
from Controllers.GameState import GameState
from Models.PlayerModel import PlayerModel
from Models.BottleModel import BottleModel
from Models.GuitarModel import GuitarFactory
from Models.CombatModel import CombatModel
from Models.RhythmModel import RhythmModel
from Controllers.CombatController import CombatController
from Controllers.GameSequenceController import GameSequenceController
from Controllers.RhythmController import RhythmController
from Views.CombatView import CombatView
from Views.RhythmView import RhythmView
from Views.PauseMenuView import PauseMenuView
from Views.CaracterView import CaracterView
from Utils.Logger import Logger


# === ACT 2 VIEW CLASS ===

class Act2View:
    """
    View class for Act 2: "Wood-Stock-Option" Festival.
    Manages intro sequence, combat against Security Chief, and rhythm mini-game phase.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, player=None, sequence_controller=None):
        """
        Initialize Act 2 view with screen and game entities.
        
        Args:
            screen: Pygame surface for rendering
            player: Optional PlayerModel instance to preserve state (if None, creates new)
            sequence_controller: Optional GameSequenceController for stage navigation
        """
        try:
            self.screen = screen
            self.sequence_controller = sequence_controller
            
            # Get screen dimensions
            try:
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                Logger.debug("Act2View.__init__", "Screen dimensions retrieved", 
                           width=self.screen_width, height=self.screen_height)
            except Exception as e:
                Logger.error("Act2View.__init__", e)
                # Fallback to screen size
                self.screen_width, self.screen_height = screen.get_size()
            
            Logger.debug("Act2View.__init__", "Starting Act 2: Wood-Stock-Option")
            
            # === CREATE JOHNNY (PLAYER) ===
            
            try:
                if player is not None:
                    # Use provided player to preserve state (drunkenness, etc.)
                    self.johnny = player
                    # Ensure health is full for combat (but keep drunkenness)
                    self.johnny.setHealth(100)
                    Logger.debug("Act2View.__init__", "Using provided player", 
                               name=self.johnny.getName(), 
                               health=self.johnny.getHealth(),
                               damage=self.johnny.getDamage(),
                               drunkenness=self.johnny.getDrunkenness())
                else:
                    # Create new player if none provided
                    self.johnny = PlayerModel("Lola Coma", 60, 60)
                    self.johnny.setHealth(100)
                    self.johnny.setDamage(8)
                    self.johnny.setAccuracy(0.85)
                    self.johnny.setDrunkenness(0)
                    self.johnny.setComaRisk(10)
                    
                    # Equip Johnny with Guitare Gonflable (inflatable guitar found on ground)
                    guitare_gonflable = GuitarFactory.createGuitareGonflable()
                    
                    # Give a bottle to Johnny
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.johnny.setSelectedBottle(beer)
                    Logger.debug("Act2View.__init__", "New player created", 
                               name=self.johnny.getName())
            except Exception as e:
                Logger.error("Act2View.__init__", e)
                raise
            
            # === CREATE SECURITY CHIEF (BOSS) ===
            
            try:
                self.security_chief = CaracterModel("Chef de la Sécurité", 80, 80)
                self.security_chief.setHealth(130)
                self.security_chief.setDamage(14)
                self.security_chief.setAccuracy(0.80)  # 80% accuracy
                
                Logger.debug("Act2View.__init__", 
                            f"Boss created: {self.security_chief.getName()}",
                            boss_hp=self.security_chief.getHealth(),
                            boss_damage=self.security_chief.getDamage())
            except Exception as e:
                Logger.error("Act2View.__init__", e)
                raise
            
            # === INITIALIZE COMBAT ===
            
            try:
                self.combat_model = CombatModel(self.johnny, self.security_chief)
                self.combat_controller = CombatController(self.combat_model)
                self.combat_view = CombatView(self.screen_width, self.screen_height)
                Logger.debug("Act2View.__init__", "Combat system initialized")
            except Exception as e:
                Logger.error("Act2View.__init__", e)
                raise
            
            # === CHARACTER VIEWS FOR STATIC DISPLAY ===
            
            try:
                # Create character views for visual display
                # Johnny is Lola with action-based sprites
                self.player_view = CaracterView("Game/Assets/lola.png", base_name="lola")
                # Security Chief (boss)
                self.boss_view = CaracterView("Game/Assets/Agentdesecurité.png", base_name="agent")
                
                # Center characters near the middle of the screen, facing each other
                center_x = self.screen_width // 2
                offset = int(self.screen_width * 0.15)

                self.johnny.setX(center_x - offset)
                self.johnny.setY(self.screen_height // 2)

                self.security_chief.setX(center_x + offset)
                self.security_chief.setY(self.screen_height // 2)
                
                Logger.debug("Act2View.__init__", "Character views created for static display",
                           player_base="lola", boss_base="agent")
            except Exception as e:
                Logger.error("Act2View.__init__", e)
                # Continue even if character views fail

            # Ensure characters are positioned relative to the current screen size
            try:
                self._position_characters()
            except Exception as e:
                Logger.error("Act2View.__init__", e)
            
            # === ACT STATE ===
            
            self.phase = "intro"  # "intro", "combat", "rhythm", "finished"
            self.act_finished = False
            self.victory = False
            # Track whether we've reset sprites when combat starts
            self._combat_started = False
            
            # === INTRO ===
            
            self.show_intro = True
            self.intro_timer = 180  # 3 seconds at 60fps
            
            # === RHYTHM PHASE (initialized after combat victory) ===
            
            self.rhythm_model = None
            self.rhythm_controller = None
            self.rhythm_view = None
            self.rhythm_notes_completed = 0
            self.rhythm_total_notes = 0
            
            Logger.debug("Act2View.__init__", "Act 2 initialized successfully")
            
        except Exception as e:
            Logger.error("Act2View.__init__", e)
            raise
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main loop for Act 2.
        Handles events, updates game state, and renders intro/combat/rhythm screens.
        
        Returns:
            str: Result of the act ("MAP", "GAME_OVER", or "QUIT")
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("Act2View.run", "Act 2 main loop started")
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("Act2View.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen_width = new_width
                                self.screen_height = new_height
                                
                                # Update screen if it's a resizable window
                                try:
                                    
                                        try:
                                         os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
                                        except Exception as e:
                                            Logger.error("Act2View.run", e)
                                        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                                except Exception:
                                    # Screen might not be resizable, just update dimensions
                                    pass
                                
                                # Recreate views with new dimensions
                                try:
                                        if self.rhythm_controller:
                                            self.rhythm_controller.view = self.rhythm_view
                                            Logger.debug("Act2View.run", "Window resized, views updated", 
                                               width=new_width, height=new_height)
                                        # Reposition characters after resize so they stay centered
                                        try:
                                            self._position_characters()
                                        except Exception as e:
                                            Logger.error("Act2View.run", e)
                                except Exception as e:
                                    Logger.error("Act2View.run", e)
                                    
                            except Exception as e:
                                Logger.error("Act2View.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                            # === HANDLE ESCAPE KEY (GLOBAL) ===
                            if event.key == pygame.K_ESCAPE:
                                try:
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()

                                    if pause_result == GameState.QUIT.value:
                                        Logger.debug("Act2View.run", "Quit requested from pause menu")
                                        return GameState.QUIT.value
                                    elif pause_result == GameState.MAIN_MENU.value:
                                        Logger.debug("Act2View.run", "Main menu requested from pause menu")
                                        return GameState.MAIN_MENU.value

                                    Logger.debug("Act2View.run", "Resuming from pause menu")
                                except Exception as e:
                                    Logger.error("Act2View.run", e)
                            
                            # === HANDLE NUMERIC KEYS (1-8) FOR STAGE NAVIGATION ===
                            elif self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  # Convert to 1-8
                                if self.sequence_controller.handle_numeric_input(stage_number):
                                    Logger.debug("Act2View.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stage_name=self.sequence_controller.get_current_stage_name())
                                    return f"STAGE_{stage_number}"
                            
                            # === INTRO SKIP (SPACE) ===
                            elif self.phase == "intro" and event.key == pygame.K_SPACE:
                                self.phase = "combat"
                                self.show_intro = False
                                Logger.debug("Act2View.run", "Intro skipped by user")
                            
                            # === COMBAT PHASE (A, P, D, B) OR COMPLETION (SPACE) ===
                            elif self.phase == "combat":
                                Logger.debug("Act2View.run", "Combat key received", key=pygame.key.name(event.key))
                                
                                if not self.combat_model.isCombatFinished():
                                    try:
                                        self.combat_controller.handle_input(event)
                                    except Exception as e:
                                        Logger.error("Act2View.run", e)
                                else:
                                    # Combat finished
                                    if event.key == pygame.K_SPACE:
                                        if self.combat_model.getWinner() == "PLAYER":
                                            # Transition to rhythm phase
                                            self.initRhythmPhase()
                                            Logger.debug("Act2View.run", "Combat won, transitioning to rhythm phase")
                                        else:
                                            # Player lost, exit
                                            running = False
                                            Logger.debug("Act2View.run", "Combat lost")
                            
                            # === RHYTHM PHASE (depends on RhythmController key handling) ===
                            elif self.phase == "rhythm":
                                Logger.debug("Act2View.run", "Rhythm key received", key=pygame.key.name(event.key))
                                try:
                                    if self.rhythm_controller:
                                        self.rhythm_controller.handle_input(event)
                                    
                                    # Check for rhythm phase completion (SPACE to finish)
                                    if event.key == pygame.K_SPACE:
                                        if self.isRhythmComplete():
                                            self.phase = "finished"
                                            running = False
                                            Logger.debug("Act2View.run", "Rhythm phase completed")
                                except Exception as e:
                                    Logger.error("Act2View.run", e)
                    
                    # === UPDATE ===
                    
                    if self.phase == "intro":
                        self.intro_timer -= 1
                        if self.intro_timer <= 0:
                            self.phase = "combat"
                            self.show_intro = False
                            Logger.debug("Act2View.run", "Intro timer expired, starting combat")
                    
                    elif self.phase == "combat":
                        try:
                            self.combat_controller.update()
                            
                            # Check if combat is finished
                            if self.combat_model.isCombatFinished():
                                if self.combat_model.getWinner() == "PLAYER" and self.phase == "combat":
                                    # Initialize rhythm phase
                                    self.initRhythmPhase()
                        except Exception as e:
                            Logger.error("Act2View.run", e)
                    
                    elif self.phase == "rhythm":
                        try:
                            if self.rhythm_controller:
                                self.rhythm_controller.update()
                            
                            # Check if all notes are completed
                            if self.isRhythmComplete():
                                self.phase = "finished"
                                Logger.debug("Act2View.run", "Rhythm phase completed automatically")
                        except Exception as e:
                            Logger.error("Act2View.run", e)
                    
                    # If we've just transitioned into combat, reset sprites once
                    if self.phase == "combat" and not getattr(self, '_combat_started', False):
                        try:
                            try:
                                # Reset model actions to idle so combat shows base sprites
                                self.johnny.setCurrentAction('idle', duration=0)
                            except Exception:
                                pass
                            try:
                                self.security_chief.setCurrentAction('idle', duration=0)
                            except Exception:
                                pass
                            try:
                                self.player_view.resetToBaseSprite()
                            except Exception:
                                pass
                            try:
                                self.boss_view.resetToBaseSprite()
                            except Exception:
                                pass
                        except Exception as e:
                            Logger.error("Act2View.run", e)
                        self._combat_started = True

                    # === RENDERING ===
                    
                    try:
                        if self.phase == "intro":
                            self.drawIntro()
                        elif self.phase == "combat":
                            self.combat_view.draw(self.screen, self.combat_model)
                            # Draw static character sprites
                            try:
                                self.player_view.drawCaracter(self.screen, self.johnny)
                                self.boss_view.drawCaracter(self.screen, self.security_chief)
                            except Exception as e:
                                Logger.error("Act2View.run", e)
                            
                            # Draw level display
                            try:
                                self._drawLevelDisplay()
                            except Exception as e:
                                Logger.error("Act2View.run", e)
                        elif self.phase == "rhythm":
                            if self.rhythm_view and self.rhythm_model:
                                self.rhythm_view.draw(self.screen, self.rhythm_model, self.johnny)
                    except Exception as e:
                        Logger.error("Act2View.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("Act2View.run", e)
                    # Continue running even if one frame fails
                    continue
            
            # === DETERMINE RESULT ===
            
            try:
                if self.phase == "finished" or (self.phase == "rhythm" and self.isRhythmComplete()):
                    Logger.debug("Act2View.run", "Act 2 completed - VICTORY")
                    return GameState.MAP.value  # Return to map
                elif self.phase == "combat" and self.combat_model.getWinner() != "PLAYER":
                    Logger.debug("Act2View.run", "Act 2 completed - DEFEAT")
                    return GameState.GAME_OVER.value
                else:
                    Logger.debug("Act2View.run", "Act 2 completed - VICTORY")
                    return GameState.MAP.value
            except Exception as e:
                Logger.error("Act2View.run", e)
                return GameState.GAME_OVER.value
                
        except Exception as e:
            Logger.error("Act2View.run", e)
            return GameState.QUIT.value
    
    # === RHYTHM PHASE INITIALIZATION ===
    
    def initRhythmPhase(self):
        """
        Initialize the rhythm mini-game phase.
        Sets up RhythmModel, RhythmController, and RhythmView.
        """
        try:
            Logger.debug("Act2View.initRhythmPhase", "Initializing rhythm phase")
            
            # Create rhythm model
            self.rhythm_model = RhythmModel()
            
            # Create rhythm view
            self.rhythm_view = RhythmView(self.screen_width, self.screen_height)
            
            # Create rhythm controller with boss for attack simulation
            self.rhythm_controller = RhythmController(
                self.rhythm_model, 
                self.johnny, 
                self.screen_height, 
                self.rhythm_view,
                self.security_chief  # Pass boss for attack simulation
            )
            
            # Count total notes
            self.rhythm_total_notes = len([n for n in self.rhythm_model.getNotes() if n.get("active", True)])
            self.rhythm_notes_completed = 0
            
            # Transition to rhythm phase
            self.phase = "rhythm"
            
            Logger.debug("Act2View.initRhythmPhase", "Rhythm phase initialized", 
                        total_notes=self.rhythm_total_notes)
            
        except Exception as e:
            Logger.error("Act2View.initRhythmPhase", e)
            # Fallback: skip rhythm phase
            self.phase = "finished"
    
    # === RHYTHM COMPLETION CHECK ===
    
    def isRhythmComplete(self):
        """
        Check if the rhythm phase is complete.
        
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
            Logger.error("Act2View.isRhythmComplete", e)
            return True
    
    # === RENDERING ===
    
    def drawIntro(self):
        """
        Draw the Act 2 introduction screen.
        Displays story text, title, and instructions.
        """
        try:
            # Black background
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("Act2View.drawIntro", e)
            
            # Fonts
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.06), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.025))
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.02))
            except Exception as e:
                Logger.error("Act2View.drawIntro", e)
                # Use default fonts if SysFont fails
                title_font = pygame.font.Font(None, 72)
                text_font = pygame.font.Font(None, 30)
                small_font = pygame.font.Font(None, 24)
            
            # Title
            try:
                title_text = "ACTE II : WOOD-STOCK-OPTION"
                title_surf = title_font.render(title_text, True, (255, 215, 0))
                title_shadow = title_font.render(title_text, True, (100, 80, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("Act2View.drawIntro", e)
            
            # Story
            try:
                story_lines = [
                    "You finally got a real contract!",
                    "",
                    "But security confiscated your equipment.",
                    "You must infiltrate the backstage",
                    "and face the Security Chief.",
                    "",
                    "Found an inflatable guitar on the ground...",
                    "It'll have to do!",
                    "",
                    "After the fight, prove yourself",
                    "in a rhythm mini-game!"
                ]
                
                story_y = title_y + 120
                for line in story_lines:
                    if line:
                        try:
                            line_surf = text_font.render(line, True, (220, 220, 220))
                            line_x = self.screen_width // 2 - line_surf.get_width() // 2
                            self.screen.blit(line_surf, (line_x, story_y))
                        except Exception as e:
                            Logger.error("Act2View.drawIntro", e)
                            continue
                    story_y += 35
            except Exception as e:
                Logger.error("Act2View.drawIntro", e)
            
            # Instructions
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("Act2View.drawIntro", e)
            
            # Blinking animation
            try:
                if (self.intro_timer // 30) % 2 == 0:
                    skip_text = "(or wait 3 seconds)"
                    skip_surf = small_font.render(skip_text, True, (100, 100, 100))
                    skip_x = self.screen_width // 2 - skip_surf.get_width() // 2
                    self.screen.blit(skip_surf, (skip_x, self.screen_height - 70))
            except Exception as e:
                Logger.error("Act2View.drawIntro", e)
                
        except Exception as e:
            Logger.error("Act2View.drawIntro", e)
    
    def _drawLevelDisplay(self):
        """
        Draw the level and alcohol display in the bottom left corner (map style).
        """
        try:
            font = pygame.font.Font(None, 36)
            
            # Draw Level
            level = self.johnny.getLevel() if hasattr(self.johnny, 'getLevel') else 1
            level_text = font.render(f"LEVEL {level}", True, (0, 255, 0))
            
            # Draw black rectangle background for level
            text_x = 20
            text_y = self.screen_height - 50
            bg_rect = pygame.Rect(text_x - 5, text_y - 5, level_text.get_width() + 10, level_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
            self.screen.blit(level_text, (text_x, text_y))
            
            # Draw Alcohol
            alcohol = self.johnny.getDrunkenness() if hasattr(self.johnny, 'getDrunkenness') else 0
            alcohol_text = font.render(f"Alcohol: {alcohol}%", True, (0, 255, 0))
            
            # Draw black rectangle background for alcohol
            alcohol_x = 20
            alcohol_y = self.screen_height - 90
            bg_rect_alcohol = pygame.Rect(alcohol_x - 5, alcohol_y - 5, alcohol_text.get_width() + 10, alcohol_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect_alcohol)
            self.screen.blit(alcohol_text, (alcohol_x, alcohol_y))
            
        except Exception as e:
            Logger.error("Act2View._drawLevelDisplay", e)

