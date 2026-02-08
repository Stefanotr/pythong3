import pygame
from Controllers.RhythmCombatController import RhythmCombatController
from Views.RhythmCombatView import RhythmCombatView
from Views.FinTransitionPageView import FinTransitionPageView
from Controllers.GameState import GameState
from Controllers.GameSequenceController import GameSequenceController
from Models.RhythmModel import RhythmModel
from Utils.Logger import Logger
from Utils.AssetManager import AssetManager
from Songs.TheFinalCountdown import loadFinalCountdown

class RhythmCombatPageView:

    def __init__(self, screen, player=None, boss=None, sequence_controller =None):

        try:
            self.sequence_controller = sequence_controller
            self.player = player
            
            self.boss = boss
            if not self.boss and self.sequence_controller:
                self.boss = self.sequence_controller.getBoss()
            
            if not self.boss:
                Logger.error("RhythmCombatPageView.__init__", "No boss provided or found in sequence controller")
                raise ValueError("Boss instance is required for rhythm combat")
            
            if not hasattr(self.boss, '_rhythm_combat_max_health'):
                
                try:
                    player_level = self.player.getLevel() if self.player else 0
                    base_health = 3000
                    
                    scaled_health = int(base_health + (player_level * 50))
                    self.boss.setHealth(scaled_health)
                    self.boss._rhythm_combat_max_health = scaled_health
                    
                    base_damage = 15
                    scaled_damage = int(base_damage + (player_level * 1))
                    self.boss.setDamage(scaled_damage)
                    
                    Logger.debug("RhythmCombatPageView.__init__", "Boss initialized for rhythm combat",
                               boss_name =self.boss.getName(), level=player_level, health=scaled_health, damage=scaled_damage)
                except Exception as e:
                    Logger.error("RhythmCombatPageView.__init__", f"Error scaling boss health: {e}")
                    self.boss.setHealth(3000)
                    self.boss.setDamage(15)
                    self.boss._rhythm_combat_max_health = 3000
            else:
                Logger.debug("RhythmCombatPageView.__init__", "Boss already initialized, current health",
                           boss_name =self.boss.getName(), current_health =self.boss.getHealth())
            
            self.boss_max_health = self.boss._rhythm_combat_max_health
            Logger.debug("RhythmCombatPageView.__init__", f"Boss max health stored as {self.boss_max_health}, actual health: {self.boss.getHealth()}")
            
            self.player_max_health = 100  
            if self.player:
                try:
                    
                    self.player_max_health = self.player.getHealth()
                    Logger.debug("RhythmCombatPageView.__init__", "Player max health set",
                               max_health =self.player_max_health)
                except Exception as e:
                    Logger.error("RhythmCombatPageView.__init__", "Error setting player max health", error=str(e))
            
            try:
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                
                try:
                    import os
                    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
                except:
                    pass
                
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.FULLSCREEN
                )
                
                Logger.debug("RhythmCombatPageView.__init__", "Screen dimensions set", 
                           width=self.screen_width, height=self.screen_height)
            except Exception as e:
                Logger.error("RhythmCombatPageView.__init__", e)
                
                self.screen_width, self.screen_height = screen.get_size()
            
            try:
                
                asset_manager = AssetManager("Game")
                boss_config = asset_manager.getBossByBame(self.boss.getName())
                
                bg_image = "Game/Assets/managerevade.png"  
                if boss_config:
                    boss_backgrounds = boss_config.get('backgrounds', {})
                    bg_image = boss_backgrounds.get('rhythmCombat', "Game/Assets/managerevade.png")
                
                self.bg_image = bg_image
                
                self.rhythm_model = RhythmModel()
                self.combat_view = RhythmCombatView(self.screen_width, self.screen_height, self.boss_max_health, self.player_max_health, backgroundImagePath =bg_image)
                Logger.debug("RhythmCombatPageView.__init__", "Rhythm and combat views created", background=bg_image)
            except Exception as e:
                Logger.error("RhythmCombatPageView.__init__", e)
                raise
            
            try:
                self.controller = RhythmCombatController(
                    self.rhythm_model,
                    self.player,
                    self.boss,
                    self.screen_height,
                    self.combat_view,
                    loadFinalCountdown()

                )
                Logger.debug("RhythmCombatPageView.__init__", "Rhythm combat controller created",
                           boss_health =self.boss.getHealth())
            except Exception as e:
                Logger.error("RhythmCombatPageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("RhythmCombatPageView.__init__", e)
            raise
    
    def run(self):

        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("RhythmCombatPageView.run", "Rhythm combat loop started")
            
            while running:
                try:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("RhythmCombatPageView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_F11:
                                try:
                                    self.toggleFullscreen()
                                except Exception as e:
                                    Logger.error("RhythmCombatPageView.run", e)
                            
                            elif self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1
                                if self.sequence_controller.handleNumericInput(stage_number):
                                    Logger.debug("RhythmCombatPageView.run", "Navigation to stage requested",
                                               stage=stage_number,
                                               stage_name =self.sequence_controller.getCurrentStageName())
                                    
                                    return f"STAGE_{stage_number}"
                        
                        elif event.type == pygame.VIDEORESIZE:
                            self.screen_width = event.w
                            self.screen_height = event.h
                            
                            self.combat_view = RhythmCombatView(self.screen_width, self.screen_height, self.boss_max_health, self.player_max_health, backgroundImagePath =self.bg_image)
                            Logger.debug("RhythmCombatPageView.run", "Window resized", width=self.screen_width, height=self.screen_height)
                        
                        try:
                            if self.controller:
                                self.controller.handleInput(event)
                        except Exception as e:
                            Logger.error("RhythmCombatPageView.run", e)
                    
                    try:
                        if self.controller:
                            
                            self.controller.update()
                            
                            if hasattr(self.controller, 'victory') and self.controller.victory:
                                Logger.debug("RhythmCombatPageView.run", "Combat completed - Victory!")
                                running = False
                            
                            if hasattr(self.controller, 'gameOver') and self.controller.game_over:
                                Logger.debug("RhythmCombatPageView.run", "Combat completed - Game Over!")
                                running = False
                    except Exception as e:
                        Logger.error("RhythmCombatPageView.run", e)
                    
                    try:
                        self.screen.fill((0, 0, 0))
                        
                        if self.player:
                            self.player.updateActionTimer()
                        if self.boss:
                            self.boss.updateActionTimer()
                        
                        count_down_val = 0
                        if hasattr(self.controller, 'waitingToStart') and self.controller.waiting_to_start:
                            count_down_val = max(1, self.controller.current_count_down_val)
                        
                        note_speed = getattr(self.controller, 'note_speed', 0.5)
                        
                        if self.combat_view and self.rhythm_model:
                            self.combat_view.draw(
                                self.screen,
                                self.rhythm_model,
                                self.player,
                                self.boss,
                                note_speed,
                                count_down_val
                            )
                        
                        pygame.display.flip()
                    except Exception as e:
                        Logger.error("RhythmCombatPageView.run", e)
                    
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("RhythmCombatPageView.run", e)
                    continue
            
            try:
                if hasattr(self.controller, 'victory') and self.controller.victory:
                    Logger.debug("RhythmCombatPageView.run", "Rhythm combat completed successfully - showing victory transition")
                    
                    self.controller.endCombat()
                    
                    if self.player:
                        current_level = self.player.getLevel()
                        new_level = current_level + 1
                        self.player.setLevel(new_level)
                        
                        current_damage = self.player.getDamage()
                        new_damage = current_damage + 1
                        self.player.setDamage(new_damage)
                        
                        current_health = self.player.getHealth()
                        new_health = current_health + 25
                        self.player.setHealth(new_health)
                        
                        Logger.debug("RhythmCombatPageView.run", "Player level incremented and stats increased", 
                                   old_level =current_level, new_level =new_level,
                                   new_damage =new_damage, new_health =new_health)
                        
                        is_last_stage = (self.sequence_controller and 
                                        self.sequence_controller.getCurrentStage() == 8)
                        
                        if is_last_stage:
                            
                            self.player.setHealth(100)
                            self.player.setDrunkenness(0)
                            self.player.setComaRisk(0)
                            Logger.debug("RhythmCombatPageView.run", "Player stats reset for new playthrough", 
                                       health=100, drunkenness=0, comaRisk =0)
                    
                    transition = FinTransitionPageView(
                        self.screen,
                        message="Stage Complete!",
                        next_stage_name ="Continued Adventure",
                        duration_seconds =5
                    )
                    transition.run()
                    
                    return "STAGE_1"
                else:
                    Logger.debug("RhythmCombatPageView.run", "Rhythm combat ended (not victory) - showing defeat transition then returning to main menu")
                    
                    try:
                        if self.controller:
                            if hasattr(self.controller, 'guitarChannel'):
                                self.controller.guitar_channel.stop()
                            if hasattr(self.controller, 'trackBacking'):
                                self.controller.track_backing.stop()
                    except Exception as e:
                        Logger.error("RhythmCombatPageView.run - Stop music on defeat", e)
                    
                    transition = FinTransitionPageView(
                        self.screen,
                        message="Game Over",
                        next_stage_name ="Main Menu",
                        duration_seconds =3
                    )
                    transition.run()
                    
                    return GameState.MAIN_MENU.value
            except Exception as e:
                Logger.error("RhythmCombatPageView.run", e)
                return GameState.QUIT.value
        except Exception as e:
            Logger.error("RhythmCombatPageView.run", e)
            return GameState.QUIT.value
    
    def toggleFullscreen(self):

        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
                
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                Logger.debug("RhythmCombatPageView.toggleFullscreen", "Switched to RESIZABLE mode")
            else:
                
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.FULLSCREEN
                )
                Logger.debug("RhythmCombatPageView.toggleFullscreen", "Switched to FULLSCREEN mode")
            
            self.combat_view = RhythmCombatView(self.screen_width, self.screen_height, self.boss_max_health, self.player_max_health, backgroundImagePath =self.bg_image)
            
            if self.controller and hasattr(self.controller, 'screen_height'):
                self.controller.screen_height = self.screen_height
                
        except Exception as e:
            Logger.error("RhythmCombatPageView.toggleFullscreen", e)
