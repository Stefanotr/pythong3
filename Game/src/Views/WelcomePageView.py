"""
WelcomePageView Module

Displays the welcome/main menu page with play and quit buttons.
Handles the transition to the main game view when play button is clicked.
"""

import pygame
from Utils.Logger import Logger
from Controllers.ButtonController import ButtonController
from Controllers.GameState import GameState
from Views.PageView import PageView
from Views.ButtonView import ButtonView
from Views.MapPageView import MapPageView
from Views.Act1View import Act1View
from Views.Act2View import Act2View
from Views.RhythmView import RhythmView
from Views.RhythmCombatView import RhythmCombatView
from Models.RhythmModel import RhythmModel
from Controllers.RhythmController import RhythmController
from Controllers.RhythmCombatController import RhythmCombatController


# === WELCOME PAGE VIEW CLASS ===

class WelcomPageView(PageView):
    """
    Welcome page view displaying the main menu.
    Provides navigation to start the game or quit the application.
    """
    
    def __init__(self, name, width=800, height=800, RESIZABLE=0, background_image="Game/Assets/welcomePage.png"):
        """
        Initialize the welcome page view.
        
        Args:
            name: Window title
            width: Window width in pixels
            height: Window height in pixels
            RESIZABLE: Pygame flag for window resizability
            background_image: Path to background image file
        """
        try:
            # Ensure pygame is initialized once (WelcomePageView is responsible)
            try:
                if not pygame.get_init():
                    pygame.init()
                    Logger.debug("WelcomPageView.__init__", "Pygame initialized by WelcomePageView")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise

            super().__init__(name, width, height, RESIZABLE, background_image)
            Logger.debug("WelcomPageView.__init__", "Welcome page initialized", name=name, width=width, height=height)
            
            # === BUTTON INITIALIZATION ===
            
            self.buttons = []
            self.buttons_controllers = []
            
            # Play button (center-top)
            try:
                self.play_button = ButtonView(
                    image_path='Game/Assets/buttonPlay.png',
                    position=(400, 500),
                )
                self.buttons.append(self.play_button)
                
                play_button_controller = ButtonController(self.play_button, "start_game")
                self.buttons_controllers.append(play_button_controller)
                Logger.debug("WelcomPageView.__init__", "Play button created")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise
            
            # Quit button (bottom)
            try:
                self.quit_button = ButtonView(
                    image_path='Game/Assets/buttonQuit.png',
                    position=(400, 700),
                )
                self.buttons.append(self.quit_button)
                
                quit_button_controller = ButtonController(self.quit_button, "quit_game")
                self.buttons_controllers.append(quit_button_controller)
                Logger.debug("WelcomPageView.__init__", "Quit button created")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("WelcomPageView.__init__", e)
            raise
    # === GENERIC LOOP HOOKS (PageView) ===

    def handle_events(self, events):
        """
        Handle events for the welcome page.
        DEBUG: Keys 1-7 jump to specific game stages for testing.

        Returns:
            bool: True to keep running, False to exit the menu.
        """
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    Logger.debug("WelcomPageView.handle_events", "QUIT event received")
                    return False

                if event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    try:
                        new_width = event.w
                        new_height = event.h
                        self.set_window_size(new_width, new_height, self.resizable)
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Window resized",
                            width=new_width,
                            height=new_height,
                        )
                    except Exception as e:
                        Logger.error("WelcomPageView.handle_events", e)
                    # Continue running after resize
                    continue

                # DEBUG: Number keys 1-8 to jump to game stages for testing
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_8:
                        stage_num = event.key - pygame.K_1 + 1
                        Logger.debug("WelcomPageView.handle_events", f"DEBUG: Jump to stage {stage_num} requested via keyboard")
                        # Stage mapping:
                        # 1: Rhythm Final, 2: Map Act1, 3: Act1, 4: Map Act2, 5: Act2, 6: Rhythm Classic, 7: Map Act3, 8: Rhythm Combat
                        try:
                            result = self._startGameFlow(debug_stage=stage_num)
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Returned from game flow, showing menu again",
                                result=result,
                            )
                            if result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView.handle_events", "Quit requested during game flow, exiting menu")
                                return False
                        except Exception as e:
                            Logger.error("WelcomPageView.handle_events", e)
                        continue

                # Delegate clicks/inputs to button controllers
                for button_controller in self.buttons_controllers:
                    action = button_controller.handleEvents(event)
                    if action == GameState.START_GAME.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Start game action received, starting game flow",
                        )
                        try:
                            result = self._startGameFlow()
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Returned from game flow, showing menu again",
                                result=result,
                            )
                            if result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView.handle_events", "Quit requested during game flow, exiting menu")
                                return False
                        except Exception as e:
                            Logger.error("WelcomPageView.handle_events", e)
                    elif action == GameState.QUIT.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Quit game action received",
                        )
                        return False

            return True
        except Exception as e:
            Logger.error("WelcomPageView.handle_events", e)
            return False

    def update(self):
        """
        Update welcome page state.
        Currently no per-frame state to update.
        """
        return None

    def render(self):
        """
        Render welcome page content.
        """
        try:
            self.draw()
            for button in self.buttons:
                button.draw(self.screen)
        except Exception as e:
            Logger.error("WelcomPageView.render", e)
    
    # === GAME TRANSITION ===
    
    def _startGameFlow(self, debug_stage=None):
        """
        Start the complete game flow: Rhythm Final → Map → Act1 → Map → Act2 → Rhythm Classic → Map → Act3 → Rhythm Combat.
        Manages all transitions between game states.
        
        Args:
            debug_stage: (DEBUG) Optional stage to jump to (1-8) for testing.
                        1: Rhythm Final
                        2: Map (Act 1)
                        3: Act 1
                        4: Map (Act 2)
                        5: Act 2
                        6: Rhythm Classic
                        7: Map (Act 3)
                        8: Rhythm Combat (final boss)
        """
        try:
            Logger.debug("WelcomPageView._startGameFlow", "Starting game flow", debug_stage=debug_stage)
            
            # Save current menu size and attempt to switch to screen resolution for gameplay
            menu_size = None
            menu_resizable = getattr(self, "resizable", pygame.RESIZABLE)
            try:
                screen = self.screen
                menu_size = (screen.get_width(), screen.get_height())
                pygame.display.set_caption("Six-String Hangover")
                Logger.debug("WelcomPageView._startGameFlow", "Menu size saved", width=menu_size[0], height=menu_size[1])
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)

            try:
                screen_info = pygame.display.Info()
                full_size = (screen_info.current_w, screen_info.current_h)
                # If not already fullscreen, switch to fullscreen for gameplay
                try:
                    pre_fullscreen = bool(self.screen.get_flags() & pygame.FULLSCREEN)
                except Exception:
                    pre_fullscreen = False

                if not pre_fullscreen:
                    try:
                        # Switch to exclusive fullscreen mode
                        pygame.display.set_mode(full_size, pygame.FULLSCREEN)
                        screen = pygame.display.get_surface()
                        self.screen = screen
                        Logger.debug("WelcomPageView._startGameFlow", "Switched to FULLSCREEN for gameplay", width=full_size[0], height=full_size[1])
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", e)
                else:
                    Logger.debug("WelcomPageView._startGameFlow", "Already in fullscreen", width=full_size[0], height=full_size[1])
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
            
            # Create player once - will be passed through all views to preserve state
            try:
                from Models.PlayerModel import PlayerModel
                from Models.BottleModel import BottleModel
                from Models.GuitarModel import GuitarFactory
                
                player = PlayerModel("Johnny Fuzz", 60, 60)
                player.setHealth(100)
                player.setDamage(10)
                player.setAccuracy(0.85)
                player.setDrunkenness(0)  # Start at 0, but will persist after this
                player.setComaRisk(10)
                
                # Equip with starting guitar
                la_pelle = GuitarFactory.createLaPelle()
                
                # Give starting bottle
                beer = BottleModel("Beer", 15, 3, 5)
                player.setSelectedBottle(beer)
                
                Logger.debug("WelcomPageView._startGameFlow", "Player created and initialized")
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
                raise
            
            # If debug_stage is set, skip to that stage
            if debug_stage:
                Logger.debug("WelcomPageView._startGameFlow", f"DEBUG: Jumping to stage {debug_stage}")
                # Stage mapping:
                # 1: Rhythm Final (uses RhythmModel like test_rhythm_final)
                # 2: Map Act 1 (current_act = 1)
                # 3: Act 1 (skip map, go straight to act)
                # 4: Map Act 2 (current_act = 2)  
                # 5: Act 2 (skip map, go straight to act)
                # 6: Rhythm Classic (uses RhythmModel, same as Rhythm Final but called "Classique")
                # 7: Map Act 3 (current_act = 3)
                # 8: Rhythm Combat (final boss - directly launch)
                
                if debug_stage == 8:
                    # Direct jump to Rhythm Combat - skip everything else
                    skip_rhythm_final = True
                    skip_to_rhythm_combat = True
                elif debug_stage == 7:
                    current_act = 3
                    skip_map_act3 = False  # Run Map Act 3 normally
                elif debug_stage == 6:
                    # Rhythm Classic - will be run before Map Act 3
                    skip_to_rhythm_classic = True
                elif debug_stage == 5:
                    # Go straight to Act2
                    current_act = 2
                elif debug_stage == 4:
                    # Map Act 2
                    current_act = 2
                elif debug_stage == 3:
                    # Go straight to Act1
                    pass
                elif debug_stage == 2:
                    # Map Act 1 (normal start after Rhythm Final)
                    skip_rhythm_final = True
                elif debug_stage == 1:
                    # Rhythm Final (normal start)
                    pass
            
            # Game flow: Rhythm Final → Map → Act1 → Map → Act2 → Rhythm Classic → Map → Act3 → Rhythm Combat
            current_act = 1
            current_stage = 1  # Track which stage we're on for proper flow
            skip_rhythm_final = False
            skip_to_rhythm_classic = False
            skip_map_act3 = False
            skip_to_rhythm_combat = False
            
            # === STAGE 8: RHYTHM COMBAT (Direct Jump) ===
            if skip_to_rhythm_combat:
                try:
                    Logger.debug("WelcomPageView._startGameFlow", "Starting RHYTHM COMBAT (Direct)")
                    
                    # === CRÉATION DES COMBATTANTS ===
                    # Johnny (Joueur)
                    from Models.CaracterModel import CaracterModel
                    boss = CaracterModel("Le Manager Corrompu", x=0, y=0, type="BOSS")
                    boss.setHealth(100)
                    boss.setDamage(10)
                    
                    # Modèle Rythme
                    rhythm_combat_model = RhythmModel()
                    
                    # Vue spéciale combat
                    rhythm_combat_view = RhythmCombatView(screen.get_width(), screen.get_height())
                    
                    # Contrôleur de combat rhythm
                    rhythm_combat_controller = RhythmCombatController(
                        rhythm_combat_model, 
                        player, 
                        boss, 
                        screen.get_height(), 
                        rhythm_combat_view
                    )
                    print("✅ Contrôleur Combat Rhythm chargé.")
                    print("🎸⚔️ Mode : BOSS COMBAT")
                    print("📜 Règles :")
                    print("   - Bonnes notes → Dégâts au BOSS")
                    print("   - MISS → Dégâts au JOUEUR + Boss récupère HP")
                    print("   - Victoire si Boss K.O.")
                    print("   - Défaite si Joueur K.O. OU Boss survit")

                    # Boucle de Jeu
                    clock = pygame.time.Clock()
                    running = True
                    
                    print("--- DÉBUT DU COMBAT ---")

                    while running:
                        # Gestion des événements
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                Logger.debug("WelcomPageView._startGameFlow", "QUIT from Rhythm Combat")
                                return GameState.QUIT.value
                            
                            rhythm_combat_controller.handle_input(event)

                        # Mise à jour
                        rhythm_combat_controller.update()

                        # Vérification Game Over
                        if rhythm_combat_controller.game_over:
                            print("\n=== FIN DU COMBAT ===")
                            if rhythm_combat_controller.victory:
                                print("🏆 VICTOIRE !")
                            else:
                                print("💀 DÉFAITE !")
                            
                            Logger.debug("WelcomPageView._startGameFlow", "Rhythm Combat finished", victory=rhythm_combat_controller.victory)
                            
                            # Attendre 3 secondes avant de continuer
                            pygame.time.wait(3000)
                            running = False

                        # Dessin
                        screen.fill((0, 0, 0))
                        
                        # Calcul du countdown
                        current_countdown = rhythm_combat_controller.current_countdown_val if rhythm_combat_controller.waiting_to_start else 0
                        
                        # Dessiner la vue de combat
                        rhythm_combat_view.draw(
                            screen, 
                            rhythm_combat_model, 
                            player,
                            boss,
                            rhythm_combat_controller.note_speed, 
                            countdown_val=current_countdown
                        )
                        
                        pygame.display.flip()
                        clock.tick(60)

                    # Game complete
                    if rhythm_combat_controller.victory:
                        Logger.debug("WelcomPageView._startGameFlow", "Game completed successfully - VICTORY!")
                        return
                    else:
                        Logger.debug("WelcomPageView._startGameFlow", "Game completed - DEFEAT")
                        return
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", e)
                    raise
            
            # === STAGE 1: RHYTHM FINAL ===
            if not skip_rhythm_final:
                try:
                    Logger.debug("WelcomPageView._startGameFlow", "Starting RHYTHM FINAL")
                    rhythm_final_model = RhythmModel()
                    rhythm_final_view = RhythmView(screen.get_width(), screen.get_height())
                    rhythm_final_controller = RhythmController(
                        rhythm_final_model,
                        player,
                        screen.get_height(),
                        rhythm_final_view
                    )
                    
                    # Run rhythm final loop
                    clock = pygame.time.Clock()
                    running = True
                    while running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                Logger.debug("WelcomPageView._startGameFlow", "QUIT from Rhythm Final")
                                return GameState.QUIT.value
                            rhythm_final_controller.handleInput(event)
                        
                        rhythm_final_controller.update()
                        
                        # Continue after song finished or auto-continue timeout
                        if rhythm_final_controller.continue_pressed or (rhythm_final_controller.game_over and not rhythm_final_controller.song_finished):
                            Logger.debug("WelcomPageView._startGameFlow", "Rhythm Final completed")
                            running = False
                        
                        screen.fill((0, 0, 0))
                        current_countdown = rhythm_final_controller.current_countdown_val if rhythm_final_controller.waiting_to_start else 0
                        rhythm_final_view.draw(
                            screen,
                            rhythm_final_model,
                            player,
                            rhythm_final_controller.note_speed,
                            countdown_val=current_countdown,
                            boss_model=None,
                            player_model=player,
                            rhythm_controller=rhythm_final_controller
                        )
                        pygame.display.flip()
                        clock.tick(60)
                    
                    if not rhythm_final_controller.game_over:
                        rhythm_final_controller.end_concert()
                    
                    Logger.debug("WelcomPageView._startGameFlow", "Rhythm Final completed successfully")
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", e)
                    raise
            
            while True:
                try:
                    # === RHYTHM CLASSIC (between Act 2 and Act 3) ===
                    if skip_to_rhythm_classic:
                        try:
                            Logger.debug("WelcomPageView._startGameFlow", "Starting RHYTHM CLASSIC")
                            rhythm_classic_model = RhythmModel()
                            rhythm_classic_view = RhythmView(screen.get_width(), screen.get_height())
                            rhythm_classic_controller = RhythmController(
                                rhythm_classic_model,
                                player,
                                screen.get_height(),
                                rhythm_classic_view
                            )
                            
                            # Run rhythm classic loop
                            clock = pygame.time.Clock()
                            running = True
                            while running:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        Logger.debug("WelcomPageView._startGameFlow", "QUIT from Rhythm Classic")
                                        return GameState.QUIT.value
                                    rhythm_classic_controller.handleInput(event)
                                
                                rhythm_classic_controller.update()
                                
                                # Continue after song finished or auto-continue timeout
                                if rhythm_classic_controller.continue_pressed or (rhythm_classic_controller.game_over and not rhythm_classic_controller.song_finished):
                                    Logger.debug("WelcomPageView._startGameFlow", "Rhythm Classic completed")
                                    running = False
                                
                                screen.fill((0, 0, 0))
                                current_countdown = rhythm_classic_controller.current_countdown_val if rhythm_classic_controller.waiting_to_start else 0
                                rhythm_classic_view.draw(
                                    screen,
                                    rhythm_classic_model,
                                    player,
                                    rhythm_classic_controller.note_speed,
                                    countdown_val=current_countdown,
                                    boss_model=None,
                                    player_model=player,
                                    rhythm_controller=rhythm_classic_controller
                                )
                                pygame.display.flip()
                                clock.tick(60)
                            
                            if not rhythm_classic_controller.game_over:
                                rhythm_classic_controller.end_concert()
                            
                            Logger.debug("WelcomPageView._startGameFlow", "Rhythm Classic completed successfully")
                            skip_to_rhythm_classic = False  # Reset flag
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            raise
                    
                    # === MAP PHASE ===
                    # Skip map if debug_stage is 3 (go directly to Act1) or 5 (go directly to Act2)
                    if debug_stage not in [3, 5]:
                        try:
                            map_view = MapPageView(screen, current_act, player)
                            result = map_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Map completed", result=result, current_act=current_act)
                            
                            if result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested from map")
                                return GameState.QUIT.value
                            elif result == GameState.MAIN_MENU.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from map")
                                # Return to main menu (exit game flow)
                                return
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    else:
                        # Skip map - directly to act
                        if current_act == 1:
                            result = GameState.ACT1.value
                        elif current_act == 2:
                            result = GameState.ACT2.value
                        elif current_act == 3:
                            result = GameState.RHYTHM.value
                        Logger.debug("WelcomPageView._startGameFlow", "DEBUG: Skipping map phase, jumping directly to act", current_act=current_act, result=result)
                        debug_stage = None  # Reset after jumping
                        skip_map_act3 = False  # Reset flag
                    
                    # === ACT 1 ===
                    if result == GameState.ACT1.value:
                        try:
                            act1_view = Act1View(screen, player)
                            act1_result = act1_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Act 1 completed", result=act1_result)
                            
                            if act1_result == GameState.MAIN_MENU.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from Act 1")
                                return
                            
                            if act1_result == GameState.GAME_OVER.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Game over")
                                return
                            elif act1_result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                                return GameState.QUIT.value
                            elif act1_result == GameState.MAP.value:
                                # Continue to next map phase
                                current_act = 2
                                continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    # === ACT 2 ===
                    elif result == GameState.ACT2.value:
                        try:
                            act2_view = Act2View(screen, player)
                            act2_result = act2_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Act 2 completed", result=act2_result)
                            
                            if act2_result == GameState.MAIN_MENU.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from Act 2")
                                return
                            
                            if act2_result == GameState.GAME_OVER.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Game over")
                                return
                            elif act2_result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                                return GameState.QUIT.value
                            elif act2_result == GameState.MAP.value:
                                # Continue to Rhythm Classic before final map
                                current_act = 3
                                skip_to_rhythm_classic = True
                                continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    # === RHYTHM COMBAT (Act 3 - Final Boss) ===
                    elif result == GameState.RHYTHM.value:
                        try:
                            # Create boss for final combat
                            from Models.CaracterModel import CaracterModel
                            boss = CaracterModel("Le Manager Corrompu", x=0, y=0, type="BOSS")
                            boss.setHealth(100)
                            boss.setDamage(10)
                            
                            # Create rhythm model for combat
                            rhythm_combat_model = RhythmModel()
                            
                            # Create rhythm combat view and controller
                            rhythm_combat_view = RhythmCombatView(screen.get_width(), screen.get_height())
                            rhythm_combat_controller = RhythmCombatController(
                                rhythm_combat_model,
                                player,
                                boss,
                                screen.get_height(),
                                rhythm_combat_view
                            )
                            
                            # Run rhythm combat loop
                            clock = pygame.time.Clock()
                            running = True
                            while running:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        Logger.debug("WelcomPageView._startGameFlow", "QUIT from Rhythm Combat")
                                        return GameState.QUIT.value
                                    rhythm_combat_controller.handleInput(event)
                                
                                rhythm_combat_controller.update()
                                
                                # Check if combat is finished
                                if rhythm_combat_controller.game_over:
                                    Logger.debug("WelcomPageView._startGameFlow", "Rhythm Combat finished", victory=rhythm_combat_controller.victory)
                                    running = False
                                
                                screen.fill((0, 0, 0))
                                current_countdown = rhythm_combat_controller.current_countdown_val if rhythm_combat_controller.waiting_to_start else 0
                                rhythm_combat_view.draw(
                                    screen,
                                    rhythm_combat_model,
                                    player,
                                    boss,
                                    rhythm_combat_controller.note_speed,
                                    countdown_val=current_countdown
                                )
                                pygame.display.flip()
                                clock.tick(60)
                            
                            # Game complete
                            if rhythm_combat_controller.victory:
                                Logger.debug("WelcomPageView._startGameFlow", "Game completed successfully - VICTORY!")
                                return
                            else:
                                Logger.debug("WelcomPageView._startGameFlow", "Game completed - DEFEAT")
                                return
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    else:
                        # Unknown result, exit
                        Logger.debug("WelcomPageView._startGameFlow", "Unknown result, exiting", result=result)
                        break
                        
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", e)
                    break
            
        except Exception as e:
            Logger.error("WelcomPageView._startGameFlow", e)
            raise
        finally:
            # Restore the menu window size if it was saved
            try:
                if menu_size:
                    try:
                        # Restore menu window centered
                        self.set_window_size(menu_size[0], menu_size[1], menu_resizable if menu_resizable else pygame.RESIZABLE)
                        Logger.debug("WelcomPageView._startGameFlow", "Restored menu window size", width=menu_size[0], height=menu_size[1])
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", e)
            except Exception:
                pass
