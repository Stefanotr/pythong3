"""
ActView Module

Generic Act view for handling Act 1 & 2 with configurable boss and story parameters.
Manages the combat sequence with flexible setup based on act_config.
Supports optional rhythm phase for Act 2.
"""

import pygame
import os
from Models.CaracterModel import CaracterModel
from Models.BossModel import BossModel
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
from Controllers.GameState import GameState


# === ACT VIEW CLASS (Generic) ===

class ActView:
    """
    Generic view class for handling Act 1 & 2 with configurable parameters.
    Manages intro sequence, combat against a boss, and optional rhythm mini-game phase.
    Supports both Act 1 (combat only) and Act 2 (combat + rhythm phase).
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, player=None, sequence_controller=None, act_config=None):
        """
        Initialize Act view with screen and game entities.
        
        Args:
            screen: Pygame surface for rendering (will be resized to full screen)
            player: Optional PlayerModel instance to preserve state
            sequence_controller: Optional GameSequenceController for stage navigation
            act_config: Dict with act parameters:
                - title: Act title (e.g., "ACT I : THE DRY THROAT")
                - act_num: Act number for logging
                - location: Location name (e.g., "The Dry Throat")
                - story_lines: List of story text lines
                - boss_name: Boss name
                - boss_asset: Boss asset path
                - boss_base: Boss base sprite name
                - boss_health: Boss starting health
                - boss_damage: Boss damage value
                - boss_accuracy: Boss accuracy (0-1)
                - guitar_factory_method: Method name to create guitar (e.g., 'createLaPelle')
                - has_rhythm_phase: Boolean, whether to include rhythm phase (default False for Act 1)
        """
        try:
            # Get screen dimensions and create resizable window at full screen size, centered
            screen_info = pygame.display.Info()
            full_width = screen_info.current_w
            full_height = screen_info.current_h
            
            # Set window to center
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except:
                pass
            
            # Create resizable window at full screen size
            self.screen = pygame.display.set_mode((full_width, full_height), pygame.RESIZABLE)
            self.screen_width = full_width
            self.screen_height = full_height
            
            self.sequence_controller = sequence_controller
            
            # Default config if not provided (Act 1)
            if act_config is None:
                act_config = self._get_act1_config()
            self.act_config = act_config
            
            Logger.debug("ActView.__init__", f"Initializing Act {act_config.get('act_num', 1)}", 
                        location=act_config.get('location', 'Unknown'),
                        window_size=f"{full_width}x{full_height}")
            
            # === CREATE JOHNNY (PLAYER) ===
            
            try:
                if player is not None:
                    self.johnny = player
                    self.johnny.setHealth(100)
                    Logger.debug("ActView.__init__", "Using provided player")
                else:
                    self.johnny = PlayerModel("Lola Coma", 60, 60)
                    self.johnny.setHealth(100)
                    self.johnny.setDamage(8)
                    self.johnny.setAccuracy(0.85)
                    self.johnny.setDrunkenness(0)
                    self.johnny.setComaRisk(10)
                    
                    # Create guitar based on act_config
                    guitar_method = act_config.get('guitar_factory_method', 'createLaPelle')
                    try:
                        guitar = getattr(GuitarFactory, guitar_method)()
                    except Exception:
                        guitar = GuitarFactory.createLaPelle()
                    
                    # Add second beer to inventory (first one is added in PlayerModel.__init__)
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.johnny.inventory.add_item(beer)
                    self.johnny.setSelectedBottle(self.johnny.inventory.get_selected_item())
                    Logger.debug("ActView.__init__", "New player created with 2 beers")
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
            # === CREATE BOSS ===
            
            try:
                # Get boss from sequence controller if available, otherwise create new one
                self.boss = None
                if self.sequence_controller:
                    self.boss = self.sequence_controller.get_boss()
                
                # If no boss yet (shouldn't happen), create one based on act_num
                if not self.boss:
                    act_num = act_config.get('act_num', 1)
                    
                    if act_num == 1:
                        # Act 1: Gros Bill
                        gros_bill = BossModel("Gros Bill", 80, 80)
                        gros_bill.setHealth(100)
                        gros_bill.setDamage(12)
                        gros_bill.setAccuracy(0.75)
                        self.boss = gros_bill
                    elif act_num == 2:
                        # Act 2: Chef de la Sécurité
                        chef_securite = BossModel("Chef de la Sécurité", 80, 80)
                        chef_securite.setHealth(500)
                        chef_securite.setDamage(14)
                        chef_securite.setAccuracy(0.80)
                        self.boss = chef_securite
                    else:
                        # Fallback
                        boss_name = act_config.get('boss_name', 'Boss')
                        boss_health = act_config.get('boss_health', 150)
                        boss_damage = act_config.get('boss_damage', 12)
                        boss_accuracy = act_config.get('boss_accuracy', 0.75)
                        self.boss = BossModel(boss_name, 80, 80)
                        self.boss.setHealth(boss_health)
                        self.boss.setDamage(boss_damage)
                        self.boss.setAccuracy(boss_accuracy)
                    
                    if self.sequence_controller:
                        self.sequence_controller.set_boss(self.boss)
                
                # Update boss stats based on player level (scale difficulty)
                try:
                    player_level = self.johnny.getLevel() if self.johnny else 0
                    current_health = self.boss.getHealth()
                    # Add HP progression: +50 HP per level
                    scaled_health = int(current_health + (player_level * 50))
                    self.boss.setHealth(scaled_health)
                    
                    # Also scale damage: +1 damage per level
                    current_damage = self.boss.getDamage()
                    scaled_damage = int(current_damage + (player_level * 1))
                    self.boss.setDamage(scaled_damage)
                except Exception as e:
                    Logger.error("ActView.__init__", "Error scaling boss stats", error=str(e))
                
                Logger.debug("ActView.__init__", f"Boss: {self.boss.getName()}",
                           health=self.boss.getHealth(), damage=self.boss.getDamage())
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
            # === INITIALIZE COMBAT ===
            
            try:
                self.combat_model = CombatModel(self.johnny, self.boss)
                self.combat_controller = CombatController(self.combat_model)
                # Pass appropriate background image based on act
                bg_image = act_config.get('background_image', 'Game/Assets/grosbillfight.png')
                self.combat_view = CombatView(self.screen_width, self.screen_height, background_image_path=bg_image)
                Logger.debug("ActView.__init__", "Combat system initialized")
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
            # === CHARACTER VIEWS ===
            
            try:
                boss_asset = act_config.get('boss_asset', 'Game/Assets/chefdesmotards.png')
                boss_base = act_config.get('boss_base', 'motard')
                
                self.player_view = CaracterView("Game/Assets/lola.png", base_name="lola")
                self.boss_view = CaracterView(boss_asset, base_name=boss_base)
                
                self._position_characters()
                Logger.debug("ActView.__init__", "Character views created")
            except Exception as e:
                Logger.error("ActView.__init__", e)
            
            # === RHYTHM PHASE (for Act 2) ===
            
            self.has_rhythm_phase = act_config.get('has_rhythm_phase', False)
            self.rhythm_model = None
            self.rhythm_controller = None
            self.rhythm_view = None
            
            # === ACT STATE ===
            
            self.act_finished = False
            self.victory = False
            self._combat_started = False
            self.show_intro = True
            self.intro_timer = 180  # 3 seconds at 60fps
            self.phase = "intro"  # "intro", "combat", "rhythm", "finished"
            
            Logger.debug("ActView.__init__", "Act initialized successfully")
            
        except Exception as e:
            Logger.error("ActView.__init__", e)
            raise
    
    
    def _get_act1_config(self):
        """Default configuration for Act 1"""
        return {
            'title': "ACT I : THE DRY THROAT",
            'act_num': 1,
            'location': "The Dry Throat",
            'story_lines': [
                "You are Lola Coma, a rockstar on the decline.",
                "",
                "The bar owner refuses to pay you",
                "until you get rid of the bikers",
                "who are squatting the stage.",
                "",
                "Face Gros Bill, the biker leader,",
                "and prove you're still a legend!"
            ],
            'boss_name': "Gros Bill",
            'boss_asset': "Game/Assets/chefdesmotards.png",
            'boss_base': "motard",
            'boss_health': 100,
            'boss_damage': 12,
            'boss_accuracy': 0.75,
            'guitar_factory_method': 'createLaPelle',
            'has_rhythm_phase': False,
            'background_image': 'Game/Assets/grosbillfight.png'
        }
    
    def _get_act2_config(self):
        """Configuration for Act 2"""
        return {
            'title': "ACTE II : WOOD-STOCK-OPTION",
            'act_num': 2,
            'location': "Wood-Stock-Option Festival",
            'story_lines': [
                "You are backstage at the Wood-Stock-Option Festival,",
                "a prestigious rock event.",
                "",
                "Security is tight, and the chief is not happy",
                "about your presence on stage.",
                "",
                "Defeat the Security Chief to earn",
                "the right to perform!"
            ],
            'boss_name': "Chef de la Sécurité",
            'boss_asset': "Game/Assets/Agentdesecurité.png",
            'boss_base': "agent",
            'boss_health': 500,
            'boss_damage': 14,
            'boss_accuracy': 0.80,
            'guitar_factory_method': 'createGuitareGonflable',
            'has_rhythm_phase': True,
            'background_image': 'Game/Assets/chefsecuritefight.png'
        }
    
    @staticmethod
    def create_act1(screen, player=None, sequence_controller=None):
        """Factory method to create Act 1"""
        return ActView(screen, player, sequence_controller)
    
    @staticmethod
    def create_act2(screen, player=None, sequence_controller=None):
        """Factory method to create Act 2"""
        act2_config = ActView({})._get_act2_config()
        return ActView(screen, player, sequence_controller, act2_config)
    
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main loop for Act.
        Handles events, updates game state, and renders intro/combat/rhythm screens.
        
        Returns:
            str: Result of the act (GameState values or "NEXT" for progression)
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("ActView.run", f"Act {self.act_config.get('act_num')} main loop started")
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("ActView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen_width = new_width
                                self.screen_height = new_height
                                
                                # Recreate display with new dimensions
                                self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                                
                                # Update combat view with new dimensions
                                try:
                                    bg_image = self.act_config.get('background_image', 'Game/Assets/grosbillfight.png')
                                    self.combat_view = CombatView(self.screen_width, self.screen_height, background_image_path=bg_image)
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                                
                                # Reposition characters so they remain centered after resize
                                try:
                                    self._position_characters()
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                                
                                Logger.debug("ActView.run", "Window resized", 
                                           width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("ActView.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                            # === HANDLE F11 FOR FULLSCREEN TOGGLE ===
                            if event.key == pygame.K_F11:
                                try:
                                    self._toggle_fullscreen()
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                            
                            # === HANDLE ESCAPE KEY (GLOBAL) ===
                            elif event.key == pygame.K_ESCAPE:
                                try:
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()
                                    if pause_result == GameState.QUIT.value:
                                        Logger.debug("ActView.run", "Quit requested from pause menu")
                                        return GameState.QUIT.value
                                    elif pause_result == GameState.MAIN_MENU.value:
                                        Logger.debug("ActView.run", "Main menu requested from pause menu")
                                        return GameState.MAIN_MENU.value
                                    Logger.debug("ActView.run", "Resuming from pause menu")
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                            
                            # === HANDLE NUMERIC KEYS (1-8) FOR STAGE NAVIGATION ===
                            elif self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  # Convert to 1-8
                                if self.sequence_controller.handle_numeric_input(stage_number):
                                    Logger.debug("ActView.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stage_name=self.sequence_controller.get_current_stage_name())
                                    return f"STAGE_{stage_number}"
                            
                            # === INTRO SKIP (SPACE) ===
                            elif self.phase == "intro" and event.key == pygame.K_SPACE:
                                self.phase = "combat"
                                self.show_intro = False
                                Logger.debug("ActView.run", "Intro skipped by user")
                            
                            # === COMBAT PHASE (A, P, D, B) OR INVENTORY NAVIGATION (LEFT/RIGHT/UP/DOWN) OR COMPLETION (SPACE) ===
                            elif self.phase == "combat":
                                Logger.debug("ActView.run", "Combat key received", key=pygame.key.name(event.key))
                                
                                # === INVENTORY NAVIGATION (LEFT/RIGHT/UP/DOWN) ===
                                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                                    if hasattr(self.johnny, 'inventory') and self.johnny.inventory:
                                        self.johnny.inventory.select_previous()
                                        Logger.debug("ActView.run", "Inventory previous selected")
                                elif event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                                    if hasattr(self.johnny, 'inventory') and self.johnny.inventory:
                                        self.johnny.inventory.select_next()
                                        Logger.debug("ActView.run", "Inventory next selected")
                                
                                elif not self.combat_model.isCombatFinished():
                                    try:
                                        self.combat_controller.handle_input(event)
                                    except Exception as e:
                                        Logger.error("ActView.run", e)
                                else:
                                    # Combat finished
                                    if event.key == pygame.K_SPACE:
                                        if self.combat_model.getWinner() == "PLAYER":
                                            # Check if we need rhythm phase (Act 2)
                                            if self.has_rhythm_phase:
                                                self._init_rhythm_phase()
                                                Logger.debug("ActView.run", "Combat won, transitioning to rhythm phase")
                                            else:
                                                # Act 1: combat only
                                                running = False
                                                Logger.debug("ActView.run", "Combat won, act completed")
                                        else:
                                            # Player lost
                                            running = False
                                            Logger.debug("ActView.run", "Combat lost")
                            
                            # === RHYTHM PHASE (Act 2 only) ===
                            elif self.phase == "rhythm":
                                Logger.debug("ActView.run", "Rhythm key received", key=pygame.key.name(event.key))
                                try:
                                    if self.rhythm_controller:
                                        self.rhythm_controller.handle_input(event)
                                    
                                    # Check for rhythm phase completion (SPACE to finish)
                                    if event.key == pygame.K_SPACE and self._is_rhythm_complete():
                                        running = False
                                        Logger.debug("ActView.run", "Rhythm phase completed")
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                    
                    # === UPDATE ===
                    
                    if self.phase == "intro":
                        self.intro_timer -= 1
                        if self.intro_timer <= 0:
                            self.phase = "combat"
                            self.show_intro = False
                            Logger.debug("ActView.run", "Intro timer expired, starting combat")
                    
                    elif self.phase == "combat":
                        try:
                            self.combat_controller.update()
                            
                            # Check if combat is finished and player won
                            if self.combat_model.isCombatFinished() and self.combat_model.getWinner() == "PLAYER":
                                if self.has_rhythm_phase:
                                    self._init_rhythm_phase()
                        except Exception as e:
                            Logger.error("ActView.run", e)
                    
                    elif self.phase == "rhythm":
                        try:
                            if self.rhythm_controller:
                                self.rhythm_controller.update()
                            
                            # Check if all notes are completed
                            if self._is_rhythm_complete():
                                pass  # Wait for user to press SPACE
                        except Exception as e:
                            Logger.error("ActView.run", e)
                    
                    # If we've just transitioned into combat, reset sprites once
                    if self.phase == "combat" and not getattr(self, '_combat_started', False):
                        try:
                            try:
                                self.johnny.setCurrentAction('idle', duration=0)
                            except Exception:
                                pass
                            try:
                                self.boss.setCurrentAction('idle', duration=0)
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
                            Logger.error("ActView.run", e)
                        self._combat_started = True
                    
                    # === RENDERING ===
                    
                    try:
                        if self.phase == "intro":
                            self._draw_intro()
                        elif self.phase == "combat":
                            self.combat_view.draw(self.screen, self.combat_model)
                            # Draw static character sprites
                            try:
                                self.player_view.drawCaracter(self.screen, self.johnny)
                                self.boss_view.drawCaracter(self.screen, self.boss)
                            except Exception as e:
                                Logger.error("ActView.run", e)
                            
                            # Draw level display
                            try:
                                self._draw_level_display()
                            except Exception as e:
                                Logger.error("ActView.run", e)
                        elif self.phase == "rhythm":
                            if self.rhythm_view and self.rhythm_model:
                                self.rhythm_view.draw(self.screen, self.rhythm_model, self.johnny)
                    except Exception as e:
                        Logger.error("ActView.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("ActView.run", e)
                    # Continue running even if one frame fails
                    continue
            
            # === DETERMINE RESULT ===
            
            try:
                if self.combat_model.getWinner() == "PLAYER":
                    Logger.debug("ActView.run", f"Act {self.act_config.get('act_num')} completed - VICTORY")
                    # Player stats are only increased after defeating the final boss (Manager Corrompu)
                    # Not after individual acts
                    return "NEXT"  # Proceed to next stage
                else:
                    Logger.debug("ActView.run", f"Act {self.act_config.get('act_num')} completed - DEFEAT")
                    return GameState.MAIN_MENU.value
            except Exception as e:
                Logger.error("ActView.run", e)
                return GameState.GAME_OVER.value
                
        except Exception as e:
            Logger.error("ActView.run", e)
            return GameState.QUIT.value
    
    # === FULLSCREEN TOGGLE ===
    
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
                Logger.debug("ActView._toggle_fullscreen", "Switched to RESIZABLE mode")
            else:
                # Currently resizable, switch to fullscreen
                screen_info = pygame.display.Info()
                self.screen = pygame.display.set_mode(
                    (screen_info.current_w, screen_info.current_h),
                    pygame.FULLSCREEN
                )
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                Logger.debug("ActView._toggle_fullscreen", "Switched to FULLSCREEN mode")
        except Exception as e:
            Logger.error("ActView._toggle_fullscreen", e)
    
    
    # === RHYTHM PHASE INITIALIZATION ===
    
    def _init_rhythm_phase(self):
        """
        Initialize the rhythm mini-game phase (for Act 2).
        Sets up RhythmModel, RhythmController, and RhythmView.
        """
        try:
            Logger.debug("ActView._init_rhythm_phase", "Initializing rhythm phase")
            
            # Create rhythm model
            self.rhythm_model = RhythmModel()
            
            # Create rhythm view with Act 2 background (woodstock)
            self.rhythm_view = RhythmView(self.screen_width, self.screen_height, background_image_path="Game/Assets/woodstock.png")
            
            # Create rhythm controller with boss for attack simulation
            self.rhythm_controller = RhythmController(
                self.rhythm_model, 
                self.johnny, 
                self.screen_height, 
                self.rhythm_view,
                context="act2"  # Rhythm phase is only in Act 2
            )
            
            # Transition to rhythm phase
            self.phase = "rhythm"
            
            Logger.debug("ActView._init_rhythm_phase", "Rhythm phase initialized")
            
        except Exception as e:
            Logger.error("ActView._init_rhythm_phase", e)
            # Fallback: skip rhythm phase
            self.phase = "finished"
    
    def _is_rhythm_complete(self):
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
            Logger.error("ActView._is_rhythm_complete", e)
            return True
    
    # === RENDERING ===
    
    def _draw_intro(self):
        """
        Draw the Act introduction screen.
        Displays story text, title, and instructions.
        Uses configuration from act_config.
        """
        try:
            # Black background
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
            
            # Fonts
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.06), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.025))
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.02))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
                # Use default fonts if SysFont fails
                title_font = pygame.font.Font(None, 72)
                text_font = pygame.font.Font(None, 30)
                small_font = pygame.font.Font(None, 24)
            
            # Title from config
            try:
                title_text = self.act_config.get('title', "ACT")
                title_surf = title_font.render(title_text, True, (255, 215, 0))
                title_shadow = title_font.render(title_text, True, (100, 80, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
            
            # Story lines from config
            try:
                story_lines = self.act_config.get('story_lines', [])
                
                story_y = title_y + 120
                for line in story_lines:
                    if line:
                        try:
                            line_surf = text_font.render(line, True, (220, 220, 220))
                            line_x = self.screen_width // 2 - line_surf.get_width() // 2
                            self.screen.blit(line_surf, (line_x, story_y))
                        except Exception as e:
                            Logger.error("ActView._draw_intro", e)
                            continue
                    story_y += 40
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
            
            # Instructions
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
            
            # Blinking animation
            try:
                if (self.intro_timer // 30) % 2 == 0:
                    skip_text = "(or wait 3 seconds)"
                    skip_surf = small_font.render(skip_text, True, (100, 100, 100))
                    skip_x = self.screen_width // 2 - skip_surf.get_width() // 2
                    self.screen.blit(skip_surf, (skip_x, self.screen_height - 70))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
                
        except Exception as e:
            Logger.error("ActView._draw_intro", e)

    def _position_characters(self):
        """Position characters centered and opposite each other based on current screen size."""
        try:
            center_x = self.screen_width // 2
            offset = int(self.screen_width * 0.15)

            # Place player on left of center and boss on right of center
            try:
                self.johnny.setX(center_x - offset)
                self.johnny.setY(self.screen_height // 2)
            except Exception:
                pass

            try:
                self.boss.setX(center_x + offset)
                self.boss.setY(self.screen_height // 2)
            except Exception:
                pass
        except Exception as e:
            Logger.error("ActView._position_characters", e)
    
    def _draw_level_display(self):
        """
        Draw the level and alcohol display in the bottom left corner (map style).
        Note: Inventory is now drawn by CombatView when in combat phase.
        """
        try:
            import pygame
            
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
            Logger.error("ActView._draw_level_display", e)


# === BACKWARD COMPATIBILITY ALIASES ===
# Act1View is now ActView - these aliases maintain backward compatibility
Act1View = ActView

# For standalone usage that imports Act1View
if __name__ == "__main__":
    """
    Standalone test entry point for Act 1.
    Initializes pygame and runs Act 1 view independently.
    """
    try:
        Logger.debug("ActView.__main__", "Standalone test starting")
        
        try:
            pygame.init()
            Logger.debug("ActView.__main__", "Pygame initialized")
        except Exception as e:
            Logger.error("ActView.__main__", e)
            raise
        
        try:
            screen_info = pygame.display.Info()
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except Exception as e:
                Logger.error("ActView.__main__", e)
            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.RESIZABLE)
            pygame.display.set_caption("Act 1 - The Dry Throat")
            Logger.debug("ActView.__main__", "Display created", 
                       width=screen_info.current_w, height=screen_info.current_h)
        except Exception as e:
            Logger.error("ActView.__main__", e)
            raise
        
        try:
            act1 = ActView.create_act1(screen)
            result = act1.run()
            Logger.debug("ActView.__main__", "Act 1 result", result=result)
        except Exception as e:
            Logger.error("ActView.__main__", e)
            raise
            
    except Exception as e:
        Logger.error("ActView.__main__", e)
    finally:
        try:
            pygame.quit()
        except Exception:
            pass