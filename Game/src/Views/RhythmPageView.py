import pygame
import os
from Models.PlayerModel import PlayerModel
from Controllers.GameState import GameState
from Models.RhythmModel import RhythmModel
from Controllers.RhythmController import RhythmController
from Views.RhythmView import RhythmView
from Views.CaracterView import CaracterView
from Views.PauseMenuView import PauseMenuView
from Views.FinTransitionPageView import FinTransitionPageView
from Utils.Logger import Logger
from Utils.AssetManager import AssetManager
from Controllers.GameSequenceController import GameSequenceController
from Songs.SevenNationArmy import loadSevenNationArmy
from Songs.AnotherOneBitesTheDust import loadAnotherOne

class RhythmPageView:

    def __init__(self, screen, player=None, sequence_controller=None, context="act1"):

        try:
            self.screen = screen
            self.sequence_controller = sequence_controller
            self.context = context  
            
            try:
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                
                try:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
                except:
                    pass
                
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.FULLSCREEN
                )
                
                Logger.debug("RhythmPageView.__init__", "Screen dimensions set", 
                           width=self.screen_width, height=self.screen_height)
            except Exception as e:
                Logger.error("RhythmPageView.__init__", e)
                
                self.screen_width, self.screen_height = screen.get_size()
            
            Logger.debug("RhythmPageView.__init__", "Rhythm page view initialized")
            
            try:
                if player is not None:
                    
                    self.lola = player
                    
                    self.lola.setHealth(100)
                    Logger.debug("RhythmPageView.__init__", "Using provided player", 
                               name=self.lola.getName(), 
                               health=self.lola.getHealth(),
                               drunkenness=self.lola.getDrunkenness())
                else:
                    
                    self.lola = PlayerModel("Lola Coma", 60, 60)
                    self.lola.setHealth(100)
                    self.lola.setDrunkenness(0)
                    Logger.debug("RhythmPageView.__init__", "New player created", 
                               name=self.lola.getName())
            except Exception as e:
                Logger.error("RhythmPageView.__init__", e)
                raise
            
            try:
                
                self.rhythm_model = RhythmModel()
                
                asset_manager = AssetManager()
                try:
                    player_config = asset_manager.loadPlayerConfig()
                    Logger.debug("RhythmPageView.__init__", f"Successfully loaded player_config with {len(player_config.get('actions', {}))} actions")
                except Exception as e:
                    Logger.error("RhythmPageView.__init__", f"Failed to load player_config: {e}")
                    player_config = None
                
                self.character_view = None
                try:
                    self.character_view = CaracterView("Game/Assets/lola.png", baseName="lola", 
                                                       spriteSize=(200, 200), 
                                                       characterConfig=player_config,
                                                       gameMode="rhythm")
                    print(f"[DEBUG] CaracterView created successfully, sprite: {self.character_view.sprite}")
                    Logger.debug("RhythmPageView.__init__", "Character view created for rhythm display")
                except Exception as e:
                    print(f"[ERROR] Failed to create character view: {e}")
                    Logger.error("RhythmPageView.__init__", f"Failed to create character view: {e}")
                
                bg_image = "Game/Assets/barconcert.png" if context == "act1" else "Game/Assets/woodstock.png"
                self.rhythm_view = RhythmView(self.screen_width, self.screen_height, backgroundImagePath=bg_image, characterView=None)
                
                from Models.CaracterModel import CaracterModel
                rhythm_boss = CaracterModel("Final Boss", 80, 80)
                rhythm_boss.setDamage(10)  
                
                song = loadAnotherOne() if self.context == "act2" else loadSevenNationArmy()
                self.rhythm_controller = RhythmController(
                    self.rhythm_model, 
                    self.lola, 
                    self.screen_height, 
                    self.rhythm_view,
                    song,
                    context=self.context
                )
                
                Logger.debug("RhythmPageView.__init__", "Rhythm system initialized", 
                           totalNotes =len(self.rhythm_model.notes))
            except Exception as e:
                Logger.error("RhythmPageView.__init__", e)
                raise
            
            self.countdown_active = True
            self.countdown_timer = 5 * 60  
            self.game_complete = False
            self.last_feedback = ""  

        except Exception as e:
            Logger.error("RhythmPageView.__init__", e)
            raise
    
    def run(self):

        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("RhythmPageView.run", "Rhythm page loop started")
            
            while running:
                try:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("RhythmPageView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.VIDEORESIZE:
                            
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen_width = new_width
                                self.screen_height = new_height
                                
                                self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                                
                                try:
                                    bg_image = "Game/Assets/barconcert.png" if self.context == "act1" else "Game/Assets/woodstock.png"
                                    self.rhythm_view = RhythmView(self.screen_width, self.screen_height, backgroundImagePath=bg_image)
                                except Exception as e:
                                    Logger.error("RhythmPageView.run", e)
                                
                                Logger.debug("RhythmPageView.run", "Window resized", 
                                           width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("RhythmPageView.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_F11:
                                try:
                                    self.toggleFullscreen()
                                except Exception as e:
                                    Logger.error("RhythmPageView.run", e)
                            
                            if self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  
                                if self.sequence_controller.handle_numeric_input(stage_number):
                                    Logger.debug("RhythmPageView.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stageName=self.sequence_controller.get_current_stage_name())
                                    
                                    return f"STAGE_{stage_number}"
                            
                            elif event.key == pygame.K_ESCAPE:
                                
                                if not self.countdown_active:
                                    try:
                                        
                                        if self.rhythm_controller:
                                            self.rhythm_controller.isPaused = True
                                            self.rhythm_controller.pauseAudio()
                                        
                                        pause_menu = PauseMenuView(self.screen)
                                        pause_result = pause_menu.run()

                                        if pause_result == GameState.QUIT.value:
                                            Logger.debug("RhythmPageView.run", "Quit requested from pause menu")
                                            
                                            if self.rhythm_controller:
                                                self.rhythm_controller.stopAllAudio()
                                            return GameState.QUIT.value
                                        elif pause_result == GameState.LOGOUT.value:
                                            Logger.debug("RhythmPageView.run", "Logout requested from pause menu")
                                            
                                            if self.rhythm_controller:
                                                self.rhythm_controller.stopAllAudio()
                                            return GameState.LOGOUT.value
                                        elif pause_result == GameState.MAIN_MENU.value:
                                            Logger.debug("RhythmPageView.run", "Main menu requested from pause menu")
                                            
                                            if self.rhythm_controller:
                                                self.rhythm_controller.stopAllAudio()
                                            return GameState.MAIN_MENU.value
                                        else:  
                                            
                                            if self.rhythm_controller:
                                                self.rhythm_controller.isPaused = False
                                                self.rhythm_controller.resumeAudio()
                                            Logger.debug("RhythmPageView.run", "Resuming from pause menu")
                                    except Exception as e:
                                        Logger.error("RhythmPageView.run", e)
                        
                        elif event.type == pygame.VIDEORESIZE:
                            
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen_width = new_width
                                self.screen_height = new_height
                                
                                try:
                                    try:
                                        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
                                    except Exception as e:
                                        Logger.error("RhythmPageView.run", e)
                                    self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                                except Exception:
                                    
                                    pass
                                
                                try:
                                    bg_image = "Game/Assets/barconcert.png" if self.context == "act1" else "Game/Assets/woodstock.png"
                                    self.rhythm_view = RhythmView(self.screen_width, self.screen_height, backgroundImagePath=bg_image)
                                    
                                    self.rhythm_controller.view = self.rhythm_view
                                    Logger.debug("RhythmPageView.run", "Window resized, rhythm view updated", 
                                               width=new_width, height=new_height)
                                except Exception as e:
                                    Logger.error("RhythmPageView.run", e)
                                    
                            except Exception as e:
                                Logger.error("RhythmPageView.run", e)
                        
                        if not self.countdown_active:
                            try:
                                if self.rhythm_controller:
                                    self.rhythm_controller.handleInput(event)
                                
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    if self.isRhythmComplete():
                                        self.game_complete = True
                                        running = False
                                        Logger.debug("RhythmPageView.run", "Rhythm game completed")
                            except Exception as e:
                                Logger.error("RhythmPageView.run", e)
                    
                    try:
                        if self.rhythm_controller:
                            self.rhythm_controller.update()
                    except Exception as e:
                        Logger.error("RhythmPageView.run", e)
                    
                    try:
                        if self.rhythm_model and self.lola:
                            feedback = getattr(self.rhythm_model, 'feedback', '')
                            
                            if feedback and feedback != self.last_feedback and "MISS" not in feedback:
                                
                                self.lola.setCurrentAction("musique", duration=30)
                            self.last_feedback = feedback
                    except Exception as e:
                        Logger.error("RhythmPageView.run - animation trigger", e)
                    
                    if self.countdown_active:
                        self.countdown_timer -= 1
                        if self.countdown_timer <= 0:
                            self.countdown_active = False
                            Logger.debug("RhythmPageView.run", "Countdown finished, starting rhythm game")
                    else:
                        try:
                            
                            if self.isRhythmComplete() and not self.game_complete:
                                self.game_complete = True
                                running = False
                                Logger.debug("RhythmPageView.run", "Rhythm game completed automatically")
                        except Exception as e:
                            Logger.error("RhythmPageView.run", e)
                    
                    try:
                        if self.countdown_active:
                            self.drawCountdown()
                        else:
                            if self.rhythm_view and self.rhythm_model:
                                self.rhythm_view.draw(self.screen, self.rhythm_model, self.lola)
                                
                                if self.character_view and self.lola:
                                    try:
                                        
                                        original_x = self.lola.getX()
                                        original_y = self.lola.getY()
                                        self.lola.setX(0)
                                        self.lola.setY(0)
                                        
                                        player_x = int(self.screen_width * 0.15)
                                        player_y = self.screen_height // 2
                                        self.character_view.drawCaracter(self.screen, self.lola, offset=(player_x, player_y), isMap=True)
                                        
                                        self.lola.setX(original_x)
                                        self.lola.setY(original_y)
                                    except Exception as e:
                                        Logger.error("RhythmPageView.run - character drawing", e)
                    except Exception as e:
                        Logger.error("RhythmPageView.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("RhythmPageView.run", e)
                    
                    continue
            
            try:
                
                Logger.debug("RhythmPageView.run", "Main loop ended", 
                           gameComplete=self.game_complete,
                           running=running)
                
                if self.game_complete:
                    
                    self.rhythm_controller.end_concert()
                    
                    is_victory = self.rhythm_model.crowd_satisfaction > 0
                    
                    Logger.debug("RhythmPageView.run", "Rhythm game completed", 
                               satisfaction=self.rhythm_model.crowd_satisfaction,
                               isVictory=is_victory,
                               totalNotes=len(self.rhythm_model.notes),
                               activeNotes=len([n for n in self.rhythm_model.notes if n.get("active", False)]))
                    
                    if is_victory:
                        Logger.debug("RhythmPageView.run", "Rhythm sequence won - showing transition")
                        Logger.debug("RhythmPageView.run", "Creating FinTransitionPageView",
                                   screen=self.screen,
                                   screenSize =self.screen.get_size() if self.screen else None)
                        
                        transition = FinTransitionPageView(
                            self.screen,
                            message="Stage Complete!",
                            nextStageName ="Next Chapter",
                            durationSeconds =5
                        )
                        
                        Logger.debug("RhythmPageView.run", "FinTransitionPageView created, calling run()")
                        transition.run()
                        Logger.debug("RhythmPageView.run", "FinTransitionPageView.run() returned")
                        
                        return GameState.COMPLETE.value
                    else:
                        Logger.debug("RhythmPageView.run", "Rhythm sequence lost - showing defeat transition")
                        Logger.debug("RhythmPageView.run", "Creating defeat transition",
                                   screen=self.screen,
                                   screenSize =self.screen.get_size() if self.screen else None)
                        
                        transition = FinTransitionPageView(
                            self.screen,
                            message="Game Over",
                            nextStageName ="Main Menu",
                            durationSeconds =3
                        )
                        
                        Logger.debug("RhythmPageView.run", "Defeat transition created, calling run()")
                        transition.run()
                        Logger.debug("RhythmPageView.run", "Defeat transition.run() returned")
                        
                        return GameState.MAIN_MENU.value
                else:
                    Logger.debug("RhythmPageView.run", "Rhythm sequence cancelled")
                    return GameState.QUIT.value
            except Exception as e:
                Logger.error("RhythmPageView.run", e)
                return GameState.QUIT.value
                
        except Exception as e:
            Logger.error("RhythmPageView.run", e)
            return GameState.QUIT.value
    
    def toggleFullscreen(self):

        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
                
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                Logger.debug("RhythmPageView.toggleFullscreen", "Switched to RESIZABLE mode")
            else:
                
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.FULLSCREEN
                )
                Logger.debug("RhythmPageView.toggleFullscreen", "Switched to FULLSCREEN mode")
            
            bg_image = "Game/Assets/barconcert.png" if self.context == "act1" else "Game/Assets/woodstock.png"
            self.rhythm_view = RhythmView(self.screen_width, self.screen_height, backgroundImagePath=bg_image)
            
        except Exception as e:
            Logger.error("RhythmPageView.toggleFullscreen", e)
    
    def isRhythmComplete(self):

        try:
            if not self.rhythm_model:
                return True
            
            active_notes = [n for n in self.rhythm_model.notes if n.get("active", False)]
            
            if self.rhythm_model.crowd_satisfaction <= 0:
                Logger.debug("RhythmPageView.isRhythmComplete", "Game over - crowd satisfaction too low", 
                           satisfaction=self.rhythm_model.crowd_satisfaction)
                return True
            
            return len(active_notes) == 0
            
        except Exception as e:
            Logger.error("RhythmPageView.isRhythmComplete", e)
            return True
    
    def drawCountdown(self):

        try:
            
            try:
                self.screen.fill((0, 0, 0))
            except Exception as e:
                Logger.error("RhythmPageView.drawCountdown", e)
            
            remaining_seconds = (self.countdown_timer // 60)
            
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
            
            try:
                if countdown_text == "GO!":
                    font_size = int(self.screen_height * 0.105)  
                else:
                    font_size = int(self.screen_height * 0.126)  
                countdown_font = pygame.font.SysFont("Arial", font_size, bold=True)
            except Exception as e:
                Logger.error("RhythmPageView.drawCountdown", e)
                countdown_font = pygame.font.Font(None, 100)
            
            try:
                countdown_surf = countdown_font.render(countdown_text, True, (255, 215, 0))  
                countdown_shadow = countdown_font.render(countdown_text, True, (100, 80, 0))  
                
                countdown_x = (self.screen_width - countdown_surf.get_width()) // 2
                countdown_y = (self.screen_height - countdown_surf.get_height()) // 2
                
                self.screen.blit(countdown_shadow, (countdown_x + 5, countdown_y + 5))
                
                self.screen.blit(countdown_surf, (countdown_x, countdown_y))
            except Exception as e:
                Logger.error("RhythmPageView.drawCountdown", e)
                
        except Exception as e:
            Logger.error("RhythmPageView.drawCountdown", e)
    
    def drawIntro(self):

        try:
            
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0462), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0348))  
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0139))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
                
                title_font = pygame.font.Font(None, 48)
                text_font = pygame.font.Font(None, 36)  
                small_font = pygame.font.Font(None, 14)
            
            try:
                title_text = "FINAL RHYTHM SEQUENCE"
                title_surf = title_font.render(title_text, True, (255, 215, 0))
                title_shadow = title_font.render(title_text, True, (100, 80, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
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
            
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("RhythmPageView.draw_intro", e)
            
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
