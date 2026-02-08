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
from Utils.AssetManager import AssetManager
from Controllers.GameState import GameState
from Songs.SevenNationArmy import loadSevenNationArmy
from Songs.AnotherOneBitesTheDust import loadAnotherOne
from Songs.TheFinalCountdown import loadFinalCountdown

class ActView:

    def __init__(self, screen, player=None, sequence_controller =None, act_config =None):

        try:
            
            screen_info = pygame.display.Info()
            full_width = screen_info.current_w
            full_height = screen_info.current_h
            
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except:
                pass
            
            self.screen = pygame.display.set_mode((full_width, full_height), pygame.FULLSCREEN)
            self.screen_width = full_width
            self.screen_height = full_height
            
            self.sequence_controller = sequence_controller
            
            if act_config is None:
                act_config = self.getAct1Config()
            self.act_config = act_config
            
            Logger.debug("ActView.__init__", f"Initializing Act {act_config.get('actNum', 1)}", 
                        location=act_config.get('location', 'Unknown'),
                        window_size =f"{full_width}x{full_height}")
            
            try:
                if player is not None:
                    self.lola = player
                    self.lola.setHealth(100)
                    Logger.debug("ActView.__init__", "Using provided player")
                else:
                    self.lola = PlayerModel("Lola Coma", 60, 60)
                    self.lola.setHealth(100)
                    self.lola.setDamage(8)
                    self.lola.setAccuracy(0.85)
                    self.lola.setDrunkenness(0)
                    self.lola.setComaRisk(10)
                    
                    guitar_method = act_config.get('guitarFactoryMethod', 'createLaPelle')
                    try:
                        guitar = getattr(GuitarFactory, guitar_method)()
                    except Exception:
                        guitar = GuitarFactory.createLaPelle()
                    
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.lola.inventory.addItem(beer)
                    self.lola.setSelectedBottle(self.lola.inventory.getSelectedItem())
                    Logger.debug("ActView.__init__", "New player created with 2 beers")
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
            try:
                
                self.asset_manager = AssetManager("Game")
                
                self.boss = None
                self.boss_config = None  
                if self.sequence_controller:
                    self.boss = self.sequence_controller.getBoss()
                
                if not self.boss:
                    act_num = act_config.get('actNum', 1)
                    
                    try:
                        
                        boss_config = self.asset_manager.getBossByAct(act_num)
                        if boss_config:
                            self.boss = BossModel.fromConfig(boss_config, 80, 80)
                            self.boss_config = boss_config  
                            Logger.debug("ActView.__init__", f"Boss loaded from config for Act {act_num}")
                        else:
                            raise ValueError(f"No config found for Act {act_num}")
                    except Exception as e:
                        Logger.warn("ActView.__init__", f"Failed to load boss from config: {e}, using fallback")
                        
                        if act_num == 1:
                            
                            gros_bill = BossModel("Gros Bill", 80, 80)
                            gros_bill.setHealth(100)
                            gros_bill.setDamage(12)
                            gros_bill.setAccuracy(0.75)
                            self.boss = gros_bill
                            
                            self.boss_config = self.asset_manager.getBossByBame("Gros Bill")
                        elif act_num == 2:
                            
                            chef_securite = BossModel("Chef de la Sécurité", 80, 80)
                            chef_securite.setHealth(500)
                            chef_securite.setDamage(14)
                            chef_securite.setAccuracy(0.80)
                            self.boss = chef_securite
                            
                            self.boss_config = self.asset_manager.getBossByBame("Chef de la Sécurité")
                        else:
                            
                            boss_name = act_config.get('boss_name', 'Boss')
                            boss_health = act_config.get('boss_health', 150)
                            boss_damage = act_config.get('boss_dDamage', 12)
                            boss_accuracy = act_config.get('boss_accuracy', 0.75)
                            self.boss = BossModel(boss_name, 80, 80)
                            self.boss.setHealth(boss_health)
                            self.boss.setDamage(boss_damage)
                            self.boss.setAccuracy(boss_accuracy)
                            
                            self.boss_config = self.asset_manager.getBossByBame(boss_name)
                    
                    if self.sequence_controller:
                        self.sequence_controller.setBoss(self.boss)
                
                self.boss_name = self.boss.getName() if self.boss else None
                
                try:
                    player_level = self.lola.getLevel() if self.lola else 0
                    current_health = self.boss.getHealth()
                    
                    scaled_health = int(current_health + (player_level * 50))
                    self.boss.setHealth(scaled_health)
                    
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
            
            try:
                self.combat_model = CombatModel(self.lola, self.boss)
                self.combat_controller = CombatController(self.combat_model)
                
                bg_image = 'Game/Assets/grosbillfight.png'  
                if hasattr(self, 'boss_config') and self.boss_config:
                    boss_backgrounds = self.boss_config.get('backgrounds', {})
                    bg_image = boss_backgrounds.get('combat', 'Game/Assets/grosbillfight.png')
                
                self.combat_view = CombatView(self.screen_width, self.screen_height, backgroundImagePath =bg_image)
                Logger.debug("ActView.__init__", "Combat system initialized", background=bg_image)
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
            try:
                boss_asset = act_config.get('bossAsset', 'Game/Assets/chefdesmotards.png')
                boss_base = act_config.get('bossBase', 'motard')
                
                try:
                    player_config = self.asset_manager.loadPlayerConfig()
                    Logger.debug("ActView.__init__", f"Successfully loaded player_config with {len(player_config.get('actions', {}))} actions")
                except Exception as e:
                    Logger.error("ActView.__init__", f"Failed to load player_config: {e}")
                    player_config = None
                
                try:
                    boss_config = self.asset_manager.getBossByBame(self.boss_name) if self.boss_name else None
                    if boss_config:
                        Logger.debug("ActView.__init__", f"Successfully loaded boss_config for {self.boss_name}")
                except Exception as e:
                    Logger.error("ActView.__init__", f"Failed to load boss_config: {e}")
                    boss_config = None
                
                self.player_view = CaracterView("Game/Assets/lola.png", baseName ="lola", 
                                               character_config =player_config, game_mode ="combat")
                self.boss_view = CaracterView(boss_asset, baseName =boss_base,
                                             character_config =boss_config, game_mode ="combat")
                
                self.positionCharacters()
                Logger.debug("ActView.__init__", "Character views created")
            except Exception as e:
                Logger.error("ActView.__init__", e)
            
            self.has_rhythm_phase = act_config.get('has_rhythm_phase', False)
            self.rhythm_model = None
            self.rhythm_controller = None
            self.rhythm_view = None
            
            self.act_finished = False
            self.victory = False
            self._combat_started = False
            self.show_intro = True
            self.intro_timer = 900  
            self.phase = "intro"  
            
            Logger.debug("ActView.__init__", "Act initialized successfully")
            
        except Exception as e:
            Logger.error("ActView.__init__", e)
            raise
    
    def getAct1Config(self):

        return {
            'title': "ACT I : THE DRY THROAT",
            'actNum': 1,
            'location': "The Dry Throat",
            'storyLines': [
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
            'bossAsset': "Game/Assets/chefdesmotards.png",
            'bossBase': "motard",
            'boss_health': 100,
            'boss_dDamage': 12,
            'boss_accuracy': 0.75,
            'guitarFactoryMethod': 'createLaPelle',
            'has_rhythm_phase': False,
            'backgroundImage': 'Game/Assets/grosbillfight.png'
        }
    
    def getAct2Config(self):

        return {
            'title': "ACTE II : WOOD-STOCK-OPTION",
            'actNum': 2,
            'location': "Wood-Stock-Option Festival",
            'storyLines': [
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
            'bossAsset': "Game/Assets/Agentdesecurité.png",
            'bossBase': "agent",
            'boss_health': 500,
            'boss_dDamage': 14,
            'boss_accuracy': 0.80,
            'guitarFactoryMethod': 'createGuitareGonflable',
            'has_rhythm_phase': True,
            'backgroundImage': 'Game/Assets/chefsecuritefight.png'
        }
    

    def createAct1(screen, player=None, sequence_controller =None):

        return ActView(screen, player, sequence_controller)
    
 
    def createAct2(screen, player=None, sequence_controller =None):

        act2_config = ActView({}).getAct2Config()
        return ActView(screen, player, sequence_controller, act2_config)
    
    def run(self):

        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("ActView.run", f"Act {self.act_config.get('actNum')} main loop started")
            
            while running:
                try:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("ActView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.VIDEORESIZE:
                            
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen_width = new_width
                                self.screen_height = new_height
                                
                                self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                                
                                try:
                                    bg_image = self.act_config.get('backgroundImage', 'Game/Assets/grosbillfight.png')
                                    self.combat_view = CombatView(self.screen_width, self.screen_height, background_image_path =bg_image)
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                                
                                try:
                                    self.positionCharacters()
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                                
                                Logger.debug("ActView.run", "Window resized", 
                                           width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("ActView.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_F11:
                                try:
                                    self.toggleFullscreen()
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                            
                            elif event.key == pygame.K_ESCAPE:
                                try:
                                    
                                    if self.combat_controller and hasattr(self.combat_controller, 'is_paused'):
                                        self.combat_controller.is_paused = True
                                        if hasattr(self.combat_controller, 'pauseAudio'):
                                            self.combat_controller.pauseAudio()
                                    if self.rhythm_controller and hasattr(self.rhythm_controller, 'is_paused'):
                                        self.rhythm_controller.is_paused = True
                                        if hasattr(self.rhythm_controller, 'pauseAudio'):
                                            self.rhythm_controller.pauseAudio()
                                    
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()
                                    
                                    if pause_result == GameState.QUIT.value:
                                        Logger.debug("ActView.run", "Quit requested from pause menu")
                                        
                                        if self.combat_controller and hasattr(self.combat_controller, 'stopAllAudio'):
                                            self.combat_controller.stopAllAudio()
                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'stopAllAudio'):
                                            self.rhythm_controller.stopAllAudio()
                                        return GameState.QUIT.value
                                    elif pause_result == GameState.LOGOUT.value:
                                        Logger.debug("ActView.run", "Logout requested from pause menu")
                                        
                                        if self.combat_controller and hasattr(self.combat_controller, 'stopAllAudio'):
                                            self.combat_controller.stopAllAudio()
                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'stopAllAudio'):
                                            self.rhythm_controller.stopAllAudio()
                                        return GameState.LOGOUT.value
                                    elif pause_result == GameState.MAIN_MENU.value:
                                        Logger.debug("ActView.run", "Main menu requested from pause menu")
                                        
                                        if self.combat_controller and hasattr(self.combat_controller, 'stopAllAudio'):
                                            self.combat_controller.stopAllAudio()
                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'stopAllAudio'):
                                            self.rhythm_controller.stopAllAudio()
                                        return GameState.MAIN_MENU.value
                                    else:  
                                        
                                        if self.combat_controller and hasattr(self.combat_controller, 'is_paused'):
                                            self.combat_controller.is_paused = False
                                            if hasattr(self.combat_controller, 'resumeAudio'):
                                                self.combat_controller.resumeAudio()
                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'is_paused'):
                                            self.rhythm_controller.is_paused = False
                                            if hasattr(self.rhythm_controller, 'resumeAudio'):
                                                self.rhythm_controller.resumeAudio()
                                        Logger.debug("ActView.run", "Resuming from pause menu")
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                            
                            elif self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  
                                if self.sequence_controller.handleNumericInput(stage_number):
                                    Logger.debug("ActView.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stage_name =self.sequence_controller.getCurrentStageName())
                                    return f"STAGE_{stage_number}"
                            
                            elif self.phase == "intro" and event.key == pygame.K_SPACE:
                                self.phase = "combat"
                                self.show_intro = False
                                Logger.debug("ActView.run", "Intro skipped by user")
                            
                            elif self.phase == "combat":
                                Logger.debug("ActView.run", "Combat key received", key=pygame.key.name(event.key))
                                
                                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                                    if hasattr(self.lola, 'inventory') and self.lola.inventory:
                                        self.lola.inventory.selectPrevious()
                                        Logger.debug("ActView.run", "Inventory previous selected")
                                elif event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                                    if hasattr(self.lola, 'inventory') and self.lola.inventory:
                                        self.lola.inventory.selectNext()
                                        Logger.debug("ActView.run", "Inventory next selected")
                                
                                if not self.combat_model.isCombatFinished():
                                    try:
                                        self.combat_controller.handleInput(event)
                                    except Exception as e:
                                        Logger.error("ActView.run", e)
                                else:
                                    
                                    if event.key == pygame.K_SPACE:
                                        if self.combat_model.getWinner() == "PLAYER":
                                            
                                            if self.has_rhythm_phase:
                                                self.initRhythmPhase()
                                                Logger.debug("ActView.run", "Combat won, transitioning to rhythm phase")
                                            else:
                                                Logger.debug("ActView.run", "Combat won, act completed")
                                        else:
                                            
                                            running = False
                                            Logger.debug("ActView.run", "Combat lost")
                            
                            elif self.phase == "rhythm":
                                Logger.debug("ActView.run", "Rhythm key received", key=pygame.key.name(event.key))
                                try:
                                    if self.rhythm_controller:
                                        self.rhythm_controller.handleInput(event)
                                    
                                    if event.key == pygame.K_SPACE and self.isRhythmComplete():
                                        running = False
                                        Logger.debug("ActView.run", "Rhythm phase completed")
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                    
                    if self.phase == "intro":
                        self.intro_timer -= 1
                        if self.intro_timer <= 0:
                            self.phase = "combat"
                            self.show_intro = False
                            Logger.debug("ActView.run", "Intro timer expired, starting combat")
                    
                    elif self.phase == "combat":
                        try:
                            self.combat_controller.update()
                            
                            if self.combat_model.isCombatFinished() and self.combat_model.getWinner() == "PLAYER":
                                if self.has_rhythm_phase:
                                    self.initRhythmPhase()
                        except Exception as e:
                            Logger.error("ActView.run", e)
                    
                    elif self.phase == "rhythm":
                        try:
                            if self.rhythm_controller:
                                self.rhythm_controller.update()
                            
                            if self.isRhythmComplete():
                                pass  
                        except Exception as e:
                            Logger.error("ActView.run", e)
                    
                    if self.phase == "combat" and not getattr(self, '_combat_started', False):
                        try:
                            try:
                                self.lola.setCurrentAction('idle', duration=0)
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
                    
                    try:
                        if self.phase == "intro":
                            self.drawIntro()
                        elif self.phase == "combat":
                            self.combat_view.draw(self.screen, self.combat_model)
                            
                            try:
                                self.player_view.drawCaracter(self.screen, self.lola)
                                self.boss_view.drawCaracter(self.screen, self.boss)
                            except Exception as e:
                                Logger.error("ActView.run", e)
                            
                            try:
                                self.drawLevelDisplay()
                            except Exception as e:
                                Logger.error("ActView.run", e)
                        elif self.phase == "rhythm":
                            if self.rhythm_view and self.rhythm_model:
                                self.rhythm_view.draw(self.screen, self.rhythm_model, self.lola)
                    except Exception as e:
                        Logger.error("ActView.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("ActView.run", e)
                    
                    continue
            
            try:
                if self.combat_model.getWinner() == "PLAYER":
                    Logger.debug("ActView.run", f"Act {self.act_config.get('actNum')} completed - VICTORY")
                    
                    return "NEXT"  
                else:
                    Logger.debug("ActView.run", f"Act {self.act_config.get('actNum')} completed - DEFEAT")
                    return GameState.MAIN_MENU.value
            except Exception as e:
                Logger.error("ActView.run", e)
                return GameState.GAME_OVER.value
                
        except Exception as e:
            Logger.error("ActView.run", e)
            return GameState.QUIT.value
    
    def toggleFullscreen(self):

        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
                
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                Logger.debug("ActView.toggleFullscreen", "Switched to RESIZABLE mode")
            else:
                
                screen_info = pygame.display.Info()
                self.screen = pygame.display.set_mode(
                    (screen_info.current_w, screen_info.current_h),
                    pygame.FULLSCREEN
                )
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                Logger.debug("ActView.toggleFullscreen", "Switched to FULLSCREEN mode")
        except Exception as e:
            Logger.error("ActView.toggleFullscreen", e)
    
    def initRhythmPhase(self):

        try:
            Logger.debug("ActView.initRhythmPhase", "Initializing rhythm phase")
            
            self.rhythm_model = RhythmModel()
            
            self.rhythm_view = RhythmView(self.screen_width, self.screen_height, background_image_path="Game/Assets/woodstock.png")
            
            self.rhythm_controller = RhythmController(
                self.rhythm_model, 
                self.lola, 
                self.screen_height,
                self.rhythm_view,
                loadAnotherOne(),
                context="act2"  
            )
            
            self.phase = "rhythm"
            
            Logger.debug("ActView.initRhythmPhase", "Rhythm phase initialized")
            
        except Exception as e:
            Logger.error("ActView.initRhythmPhase", e)
            
            self.phase = "finished"
    
    def isRhythmComplete(self):

        try:
            if not self.rhythm_model:
                return True
            
            active_notes = [n for n in self.rhythm_model.getNotes() if n.get("active", False)]
            
            if self.lola.getHealth() <= 0:
                return True
            
            return len(active_notes) == 0
            
        except Exception as e:
            Logger.error("ActView.isRhythmComplete", e)
            return True
    
    def drawIntro(self):

        try:
            
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("ActView.drawIntro", e)
            
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0462), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0348))  
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0139))
            except Exception as e:
                Logger.error("ActView.drawIntro", e)
                
                title_font = pygame.font.Font(None, 48)
                text_font = pygame.font.Font(None, 36)  
                small_font = pygame.font.Font(None, 14)
            
            try:
                title_text = self.act_config.get('title', "ACT")
                title_surf = title_font.render(title_text, True, (255, 215, 0))
                title_shadow = title_font.render(title_text, True, (100, 80, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("ActView.drawIntro", e)
            
            try:
                story_lines = self.act_config.get('storyLines', [])
                
                story_y = title_y + 120
                for line in story_lines:
                    if line:
                        try:
                            line_surf = text_font.render(line, True, (220, 220, 220))
                            line_x = self.screen_width // 2 - line_surf.get_width() // 2
                            self.screen.blit(line_surf, (line_x, story_y))
                        except Exception as e:
                            Logger.error("ActView.drawIntro", e)
                            continue
                    story_y += 40
            except Exception as e:
                Logger.error("ActView.drawIntro", e)
            
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("ActView.drawIntro", e)
            
            try:
                if (self.intro_timer // 30) % 2 == 0:
                    skip_text = "(or wait 3 seconds)"
                    skip_surf = small_font.render(skip_text, True, (100, 100, 100))
                    skip_x = self.screen_width // 2 - skip_surf.get_width() // 2
                    self.screen.blit(skip_surf, (skip_x, self.screen_height - 70))
            except Exception as e:
                Logger.error("ActView.drawIntro", e)
                
        except Exception as e:
            Logger.error("ActView.drawIntro", e)

    def positionCharacters(self):

        try:
            center_x = self.screen_width // 2
            offset = int(self.screen_width * 0.15)

            try:
                self.lola.setX(center_x - offset)
                self.lola.setY(self.screen_height // 2)
            except Exception:
                pass

            try:
                self.boss.setX(center_x + offset)
                self.boss.setY(self.screen_height // 2)
            except Exception:
                pass
        except Exception as e:
            Logger.error("ActView.positionCharacters", e)
    
    def drawLevelDisplay(self):

        try:
            import pygame
            
            font = pygame.font.Font(None, 36)
            
            level = self.lola.getLevel() if hasattr(self.lola, 'getLevel') else 1
            level_text = font.render(f"LEVEL {level}", True, (0, 255, 0))
            
            text_x = 20
            text_y = self.screen_height - 50
            bg_rect = pygame.Rect(text_x - 5, text_y - 5, level_text.get_width() + 10, level_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
            self.screen.blit(level_text, (text_x, text_y))
            
            alcohol = self.lola.getDrunkenness() if hasattr(self.lola, 'getDrunkenness') else 0
            alcohol_text = font.render(f"Alcohol: {alcohol}%", True, (0, 255, 0))
            
            alcohol_x = 20
            alcohol_y = self.screen_height - 90
            bg_rect_alcohol = pygame.Rect(alcohol_x - 5, alcohol_y - 5, alcohol_text.get_width() + 10, alcohol_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect_alcohol)
            self.screen.blit(alcohol_text, (alcohol_x, alcohol_y))
            
        except Exception as e:
            Logger.error("ActView.drawLevelDisplay", e)

Act1View = ActView

if __name__ == "__main__":

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