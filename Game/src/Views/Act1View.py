

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
from Songs.SevenNationArmy import load_seven_nation_army
from Songs.AnotherOneBitesTheDust import load_another_one
from Songs.TheFinalCountdown import load_final_countdown



class ActView:
   
   
    
    def __init__(self, screen, player=None, sequence_controller=None, act_config=None):
        
        
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
                act_config = self._get_act1_config()
            self.act_config = act_config
            
            Logger.debug("ActView.__init__", f"Initializing Act {act_config.get('act_num', 1)}", 
                        location=act_config.get('location', 'Unknown'),
                        window_size=f"{full_width}x{full_height}")
            
           
           
            
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
                    
                   
                    guitar_method = act_config.get('guitar_factory_method', 'createLaPelle')
                    try:
                        guitar = getattr(GuitarFactory, guitar_method)()
                    except Exception:
                        guitar = GuitarFactory.createLaPelle()
                    
                   
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.johnny.inventory.add_item(beer)
                    self.johnny.setSelectedBottle(self.johnny.inventory.get_selected_item())
                    Logger.debug("ActView.__init__", "New player created with 2 beers")
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
           
           
            
            try:
               
                self.asset_manager = AssetManager("Game")
                
               
               
                self.boss = None
                self.boss_config = None  
                if self.sequence_controller:
                    self.boss = self.sequence_controller.get_boss()
                
                
                

                if not self.boss:
                    act_num = act_config.get('act_num', 1)
                    
                    try:
                        
                        boss_config = self.asset_manager.get_boss_by_act(act_num)
                        if boss_config:
                            self.boss = BossModel.from_config(boss_config, 80, 80)

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
                            

                            self.boss_config = self.asset_manager.get_boss_by_name("Gros Bill")

                        elif act_num == 2:
                           
                            chef_securite = BossModel("Chef de la Sécurité", 80, 80)
                            chef_securite.setHealth(500)
                            chef_securite.setDamage(14)
                            chef_securite.setAccuracy(0.80)
                            self.boss = chef_securite
                           
                            self.boss_config = self.asset_manager.get_boss_by_name("Chef de la Sécurité")


                        else:
                            
                            boss_name = act_config.get('boss_name', 'Boss')
                            boss_health = act_config.get('boss_health', 150)
                            boss_damage = act_config.get('boss_damage', 12)
                            boss_accuracy = act_config.get('boss_accuracy', 0.75)
                            self.boss = BossModel(boss_name, 80, 80)
                            self.boss.setHealth(boss_health)
                            self.boss.setDamage(boss_damage)
                            self.boss.setAccuracy(boss_accuracy)
                            
                            self.boss_config = self.asset_manager.get_boss_by_name(boss_name)
                    
                    if self.sequence_controller:
                        self.sequence_controller.set_boss(self.boss)
                
               
                self.boss_name = self.boss.getName() if self.boss else None
                
                
                try:
                    player_level = self.johnny.getLevel() if self.johnny else 0
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
                self.combat_model = CombatModel(self.johnny, self.boss)
                self.combat_controller = CombatController(self.combat_model)
                
              
                bg_image = 'Game/Assets/grosbillfight.png'  
                if hasattr(self, 'boss_config') and self.boss_config:
                    boss_backgrounds = self.boss_config.get('backgrounds', {})
                    bg_image = boss_backgrounds.get('combat', 'Game/Assets/grosbillfight.png')
                
                self.combat_view = CombatView(self.screen_width, self.screen_height, background_image_path=bg_image)
                Logger.debug("ActView.__init__", "Combat system initialized", background=bg_image)
            except Exception as e:
                Logger.error("ActView.__init__", e)
                raise
            
           
           
            
            try:
                boss_asset = act_config.get('boss_asset', 'Game/Assets/chefdesmotards.png')
                boss_base = act_config.get('boss_base', 'motard')
                
               
                try:
                    player_config = self.asset_manager.load_player_config()
                    Logger.debug("ActView.__init__", f"Successfully loaded player_config with {len(player_config.get('actions', {}))} actions")
                except Exception as e:
                    Logger.error("ActView.__init__", f"Failed to load player_config: {e}")
                    player_config = None
                
                try:
                    boss_config = self.asset_manager.get_boss_by_name(self.boss_name) if self.boss_name else None
                    if boss_config:
                        Logger.debug("ActView.__init__", f"Successfully loaded boss_config for {self.boss_name}")
                except Exception as e:
                    Logger.error("ActView.__init__", f"Failed to load boss_config: {e}")
                    boss_config = None
                
                self.player_view = CaracterView("Game/Assets/lola.png", base_name="lola", 
                                               character_config=player_config, game_mode="combat")
                self.boss_view = CaracterView(boss_asset, base_name=boss_base,
                                             character_config=boss_config, game_mode="combat")
                
                self._position_characters()
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
            self.intro_timer = 180  
            self.phase = "intro" 
            
            Logger.debug("ActView.__init__", "Act initialized successfully")
            
        except Exception as e:
            Logger.error("ActView.__init__", e)
            raise
    
    


    def _get_act1_config(self):
     

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
    
   


    def create_act1(screen, player=None, sequence_controller=None):
        
        return ActView(screen, player, sequence_controller)
    

    def create_act2(screen, player=None, sequence_controller=None):
       
        act2_config = ActView({})._get_act2_config()
        return ActView(screen, player, sequence_controller, act2_config)
    


    

    
    def run(self):
      

        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("ActView.run", f"Act {self.act_config.get('act_num')} main loop started")
            
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
                                    bg_image = self.act_config.get('background_image', 'Game/Assets/grosbillfight.png')
                                    self.combat_view = CombatView(self.screen_width, self.screen_height, background_image_path=bg_image)
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                                
                               
                                try:
                                    self._position_characters()
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                                
                                Logger.debug("ActView.run", "Window resized", 
                                           width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("ActView.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                          


                            if event.key == pygame.K_F11:
                                try:
                                    self._toggle_fullscreen()
                                except Exception as e:


                                    Logger.error("ActView.run", e)
                            
                            
                            elif event.key == pygame.K_ESCAPE:
                                try:
                                 
                                    if self.combat_controller and hasattr(self.combat_controller, 'is_paused'):
                                        self.combat_controller.is_paused = True
                                        if hasattr(self.combat_controller, 'pause_audio'):


                                            self.combat_controller.pause_audio()
                                    if self.rhythm_controller and hasattr(self.rhythm_controller, 'is_paused'):
                                        self.rhythm_controller.is_paused = True
                                        if hasattr(self.rhythm_controller, 'pause_audio'):
                                            self.rhythm_controller.pause_audio()
                                    
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()
                                    
                                    if pause_result == GameState.QUIT.value:
                                        Logger.debug("ActView.run", "Quit requested from pause menu")
                                      
                                      

                                        if self.combat_controller and hasattr(self.combat_controller, 'stop_all_audio'):
                                            self.combat_controller.stop_all_audio()
                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'stop_all_audio'):
                                            self.rhythm_controller.stop_all_audio()


                                        return GameState.QUIT.value
                                    elif pause_result == GameState.LOGOUT.value:
                                        Logger.debug("ActView.run", "Logout requested from pause menu")
                                        # Stop all audio before logout
                                        if self.combat_controller and hasattr(self.combat_controller, 'stop_all_audio'):
                                            self.combat_controller.stop_all_audio()
                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'stop_all_audio'):
                                            self.rhythm_controller.stop_all_audio()

                                        return GameState.LOGOUT.value
                                    elif pause_result == GameState.MAIN_MENU.value:
                                        Logger.debug("ActView.run", "Main menu requested from pause menu")
                                        # Stop all audio before returning to main menu
                                        if self.combat_controller and hasattr(self.combat_controller, 'stop_all_audio'):
                                            self.combat_controller.stop_all_audio()

                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'stop_all_audio'):
                                            self.rhythm_controller.stop_all_audio()
                                        return GameState.MAIN_MENU.value
                                    
                                    else:  # CONTINUE or anything else
                                        # Resume all audio and notes when continuing
                                        if self.combat_controller and hasattr(self.combat_controller, 'is_paused'):
                                            self.combat_controller.is_paused = False
                                            if hasattr(self.combat_controller, 'resume_audio'):
                                                self.combat_controller.resume_audio()

                                        if self.rhythm_controller and hasattr(self.rhythm_controller, 'is_paused'):
                                            self.rhythm_controller.is_paused = False
                                            if hasattr(self.rhythm_controller, 'resume_audio'):

                                                self.rhythm_controller.resume_audio()
                                        Logger.debug("ActView.run", "Resuming from pause menu")
                                except Exception as e:
                                    Logger.error("ActView.run", e)
                            
                           
                            elif self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  
                                if self.sequence_controller.handle_numeric_input(stage_number):

                                    Logger.debug("ActView.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stage_name=self.sequence_controller.get_current_stage_name())
                                    return f"STAGE_{stage_number}"
                            
                          
                          

                            elif self.phase == "intro" and event.key == pygame.K_SPACE:
                                self.phase = "combat"
                                self.show_intro = False
                                Logger.debug("ActView.run", "Intro skipped by user")
                            
                           
                            elif self.phase == "combat":
                                Logger.debug("ActView.run", "Combat key received", key=pygame.key.name(event.key))
                                
                               
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
                                   
                                   
                                    if event.key == pygame.K_SPACE:
                                        if self.combat_model.getWinner() == "PLAYER":
                                           
                                           
                                            if self.has_rhythm_phase:
                                                self._init_rhythm_phase()
                                                Logger.debug("ActView.run", "Combat won, transitioning to rhythm phase")
                                            else:
                                              
                                                running = False
                                                Logger.debug("ActView.run", "Combat won, act completed")
                                        else:
                                          
                                            running = False
                                            Logger.debug("ActView.run", "Combat lost")
                            
                          
                          
                            elif self.phase == "rhythm":
                                Logger.debug("ActView.run", "Rhythm key received", key=pygame.key.name(event.key))
                                try:
                                    if self.rhythm_controller:
                                        self.rhythm_controller.handle_input(event)
                                    
                                   
                                   
                                    if event.key == pygame.K_SPACE and self._is_rhythm_complete():
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
                                    self._init_rhythm_phase()
                        except Exception as e:
                            Logger.error("ActView.run", e)
                    
                    elif self.phase == "rhythm":
                        try:
                            if self.rhythm_controller:
                                self.rhythm_controller.update()
                            
                         
                         
                            if self._is_rhythm_complete():
                                pass  
                            


                        except Exception as e:
                            Logger.error("ActView.run", e)
                    
                   
                   


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
                    
                  
                  

                    
                    try:
                        if self.phase == "intro":
                            self._draw_intro()
                        elif self.phase == "combat":
                            self.combat_view.draw(self.screen, self.combat_model)
                           
                           
                            try:
                                self.player_view.drawCaracter(self.screen, self.johnny)
                                self.boss_view.drawCaracter(self.screen, self.boss)
                            except Exception as e:
                                Logger.error("ActView.run", e)
                            
                            
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
                  
                    continue
            
            
            try:
                if self.combat_model.getWinner() == "PLAYER":
                    Logger.debug("ActView.run", f"Act {self.act_config.get('act_num')} completed - VICTORY")
                    
                    
                    return "NEXT"  
                
                else:
                    Logger.debug("ActView.run", f"Act {self.act_config.get('act_num')} completed - DEFEAT")
                    return GameState.MAIN_MENU.value
            except Exception as e:
                Logger.error("ActView.run", e)
                return GameState.GAME_OVER.value
                
        except Exception as e:
            Logger.error("ActView.run", e)
            return GameState.QUIT.value
    
  
    
    def _toggle_fullscreen(self):
   

        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
              
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                Logger.debug("ActView._toggle_fullscreen", "Switched to RESIZABLE mode")
            else:
              
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
    
    

    def _init_rhythm_phase(self):
   
   

        try:
            Logger.debug("ActView._init_rhythm_phase", "Initializing rhythm phase")
            
       
            self.rhythm_model = RhythmModel()
            
            
            self.rhythm_view = RhythmView(self.screen_width, self.screen_height, background_image_path="Game/Assets/woodstock.png")
            
            
            self.rhythm_controller = RhythmController(
                self.rhythm_model, 
                self.johnny, 
                self.screen_height, 
                self.rhythm_view,
                load_another_one(),
                context="act2" 
            )
            
            # Transition to rhythm phase
            self.phase = "rhythm"
            
            Logger.debug("ActView._init_rhythm_phase", "Rhythm phase initialized")
            
        except Exception as e:
            Logger.error("ActView._init_rhythm_phase", e)
            # Fallback: skip rhythm phase
            self.phase = "finished"




    
    def _is_rhythm_complete(self):
       
       
        try:
            if not self.rhythm_model:
                return True
            
           
            active_notes = [n for n in self.rhythm_model.getNotes() if n.get("active", False)]
            
          
            if self.johnny.getHealth() <= 0:
                return True
            
            
            return len(active_notes) == 0
            
        except Exception as e:
            Logger.error("ActView._is_rhythm_complete", e)
            return True
    
   
   





    
    def _draw_intro(self):
        
        try:
           
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
            
            
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0462), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0348))
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.0139))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)

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
                Logger.error("ActView._draw_intro", e)
            
          



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
            
            
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2


                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("ActView._draw_intro", e)
            
          
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
       
        try:
            center_x = self.screen_width // 2
            offset = int(self.screen_width * 0.15)

            
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
       
        try:
            import pygame
            
            font = pygame.font.Font(None, 36)
            
          
            level = self.johnny.getLevel() if hasattr(self.johnny, 'getLevel') else 1
            level_text = font.render(f"LEVEL {level}", True, (0, 255, 0))
            
           
            text_x = 20
            text_y = self.screen_height - 50

            bg_rect = pygame.Rect(text_x - 5, text_y - 5, level_text.get_width() + 10, level_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
            self.screen.blit(level_text, (text_x, text_y))
            
            alcohol = self.johnny.getDrunkenness() if hasattr(self.johnny, 'getDrunkenness') else 0
            alcohol_text = font.render(f"Alcohol: {alcohol}%", True, (0, 255, 0))
            
            
            alcohol_x = 20
            alcohol_y = self.screen_height - 90
            bg_rect_alcohol = pygame.Rect(alcohol_x - 5, alcohol_y - 5, alcohol_text.get_width() + 10, alcohol_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect_alcohol)
            self.screen.blit(alcohol_text, (alcohol_x, alcohol_y))
            
        except Exception as e:
            Logger.error("ActView._draw_level_display", e)



Act1View = ActView