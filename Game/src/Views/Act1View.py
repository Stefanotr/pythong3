"""
Act1View Module

Handles Act 1: "Le Gosier Sec" (The Dry Throat Bar).
Manages the combat sequence against Gros Bill, including intro screen and combat interface.
"""

import pygame
from Models.CaracterModel import CaracterModel
from Models.PlayerModel import PlayerModel
from Models.BottleModel import BottleModel
from Models.GuitarModel import GuitarFactory
from Models.CombatModel import CombatModel
from Controllers.CombatController import CombatController
from Views.CombatView import CombatView
from Utils.Logger import Logger


# === ACT 1 VIEW CLASS ===

class Act1View:
    """
    View class for Act 1: "Le Gosier Sec" (The Dry Throat Bar).
    Manages the intro sequence, combat against Gros Bill, and act completion.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen):
        """
        Initialize Act 1 view with screen and game entities.
        
        Args:
            screen: Pygame surface for rendering
        """
        try:
            self.screen = screen
            
            # Get screen dimensions
            try:
                screen_info = pygame.display.Info()
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                Logger.debug("Act1View.__init__", "Screen dimensions retrieved", 
                           width=self.screen_width, height=self.screen_height)
            except Exception as e:
                Logger.error("Act1View.__init__", e)
                # Fallback to screen size
                self.screen_width, self.screen_height = screen.get_size()
            
            Logger.debug("Act1View.__init__", "Starting Act 1: Le Gosier Sec")
            
            # === CREATE JOHNNY (PLAYER) ===
            
            try:
                self.johnny = PlayerModel("Johnny Fuzz", 60, 60)
                self.johnny.setHealth(100)
                self.johnny.setDamage(10)
                self.johnny.setAccuracy(0.85)  # 85% accuracy
                self.johnny.setDrunkenness(0)
                self.johnny.setComaRisk(10)
                Logger.debug("Act1View.__init__", "Player created", 
                           name=self.johnny.getName(), 
                           health=self.johnny.getHealth(),
                           damage=self.johnny.getDamage())
            except Exception as e:
                Logger.error("Act1View.__init__", e)
                raise
            
            # Equip Johnny with La Pelle (starting guitar)
            try:
                la_pelle = GuitarFactory.create_la_pelle()
                Logger.debug("Act1View.__init__", f"Johnny equipped with {la_pelle.getName()}")
            except Exception as e:
                Logger.error("Act1View.__init__", e)
            
            # Give a bottle to Johnny
            try:
                beer = BottleModel("Beer", 15, 3, 5)
                self.johnny.setSelectedBottle(beer)
                Logger.debug("Act1View.__init__", "Player bottle selected", bottle=beer.getName())
            except Exception as e:
                Logger.error("Act1View.__init__", e)
            
            # === CREATE GROS BILL (BOSS) ===
            
            try:
                self.gros_bill = CaracterModel("Gros Bill", 80, 80)
                self.gros_bill.setHealth(80)
                self.gros_bill.setDamage(8)
                self.gros_bill.setAccuracy(0.75)  # 75% accuracy
                
                Logger.debug("Act1View.__init__", 
                            f"Boss created: {self.gros_bill.getName()}",
                            boss_hp=self.gros_bill.getHealth(),
                            boss_damage=self.gros_bill.getDamage())
            except Exception as e:
                Logger.error("Act1View.__init__", e)
                raise
            
            # === INITIALIZE COMBAT ===
            
            try:
                self.combat_model = CombatModel(self.johnny, self.gros_bill)
                self.combat_controller = CombatController(self.combat_model)
                self.combat_view = CombatView(self.screen_width, self.screen_height)
                Logger.debug("Act1View.__init__", "Combat system initialized")
            except Exception as e:
                Logger.error("Act1View.__init__", e)
                raise
            
            # === ACT STATE ===
            
            self.act_finished = False
            self.victory = False
            
            # === INTRO ===
            
            self.show_intro = True
            self.intro_timer = 180  # 3 seconds at 60fps
            
            Logger.debug("Act1View.__init__", "Act 1 initialized successfully")
            
        except Exception as e:
            Logger.error("Act1View.__init__", e)
            raise
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main loop for Act 1.
        Handles events, updates game state, and renders intro/combat screens.
        
        Returns:
            str: Result of the act ("ACT2", "GAME_OVER", or "QUIT")
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("Act1View.run", "Act 1 main loop started")
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("Act1View.run", "QUIT event received")
                            return "QUIT"
                        
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
                                
                                # Recreate combat view with new dimensions
                                try:
                                    self.combat_view = CombatView(self.screen_width, self.screen_height)
                                    Logger.debug("Act1View.run", "Window resized, combat view updated", 
                                               width=new_width, height=new_height)
                                except Exception as e:
                                    Logger.error("Act1View.run", e)
                                    
                            except Exception as e:
                                Logger.error("Act1View.run", e)
                        
                        # Intro screen events
                        elif self.show_intro:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                self.show_intro = False
                                Logger.debug("Act1View.run", "Intro skipped by user")
                        
                        # Combat events
                        elif not self.combat_model.isCombatFinished():
                            try:
                                self.combat_controller.handleInput(event)
                            except Exception as e:
                                Logger.error("Act1View.run", e)
                        
                        # Combat end events
                        else:
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                running = False
                                Logger.debug("Act1View.run", "Combat end screen skipped")
                    
                    # === UPDATE ===
                    
                    if self.show_intro:
                        self.intro_timer -= 1
                        if self.intro_timer <= 0:
                            self.show_intro = False
                            Logger.debug("Act1View.run", "Intro timer expired, starting combat")
                    else:
                        try:
                            self.combat_controller.update()
                        except Exception as e:
                            Logger.error("Act1View.run", e)
                    
                    # === RENDERING ===
                    
                    try:
                        if self.show_intro:
                            self.draw_intro()
                        else:
                            self.combat_view.draw(self.screen, self.combat_model)
                    except Exception as e:
                        Logger.error("Act1View.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("Act1View.run", e)
                    # Continue running even if one frame fails
                    continue
            
            # === DETERMINE RESULT ===
            
            try:
                if self.combat_model.getWinner() == "PLAYER":
                    Logger.debug("Act1View.run", "Act 1 completed - VICTORY")
                    return "ACT2"  # Proceed to Act 2
                else:
                    Logger.debug("Act1View.run", "Act 1 completed - DEFEAT")
                    return "GAME_OVER"
            except Exception as e:
                Logger.error("Act1View.run", e)
                return "GAME_OVER"
                
        except Exception as e:
            Logger.error("Act1View.run", e)
            return "QUIT"
    
    # === RENDERING ===
    
    def draw_intro(self):
        """
        Draw the Act 1 introduction screen.
        Displays story text, title, and instructions.
        """
        try:
            # Black background
            try:
                self.screen.fill((10, 10, 15))
            except Exception as e:
                Logger.error("Act1View.draw_intro", e)
            
            # Fonts
            try:
                title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.06), bold=True)
                text_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.025))
                small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.02))
            except Exception as e:
                Logger.error("Act1View.draw_intro", e)
                # Use default fonts if SysFont fails
                title_font = pygame.font.Font(None, 72)
                text_font = pygame.font.Font(None, 30)
                small_font = pygame.font.Font(None, 24)
            
            # Title
            try:
                title_text = "🎸 ACTE I : LE GOSIER SEC 🍺"
                title_surf = title_font.render(title_text, True, (255, 215, 0))
                title_shadow = title_font.render(title_text, True, (100, 80, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("Act1View.draw_intro", e)
            
            # Story
            try:
                story_lines = [
                    "You are Johnny Fuzz, a rockstar on the decline.",
                    "",
                    "The bar owner refuses to pay you",
                    "until you get rid of the bikers",
                    "who are squatting the stage.",
                    "",
                    "Face Gros Bill, the biker leader,",
                    "and prove you're still a legend!"
                ]
                
                story_y = title_y + 120
                for line in story_lines:
                    if line:
                        try:
                            line_surf = text_font.render(line, True, (220, 220, 220))
                            line_x = self.screen_width // 2 - line_surf.get_width() // 2
                            self.screen.blit(line_surf, (line_x, story_y))
                        except Exception as e:
                            Logger.error("Act1View.draw_intro", e)
                            continue
                    story_y += 40
            except Exception as e:
                Logger.error("Act1View.draw_intro", e)
            
            # Instructions
            try:
                instruction = "Press SPACE to start"
                inst_surf = small_font.render(instruction, True, (150, 150, 150))
                inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, self.screen_height - 100))
            except Exception as e:
                Logger.error("Act1View.draw_intro", e)
            
            # Blinking animation
            try:
                if (self.intro_timer // 30) % 2 == 0:
                    skip_text = "(or wait 3 seconds)"
                    skip_surf = small_font.render(skip_text, True, (100, 100, 100))
                    skip_x = self.screen_width // 2 - skip_surf.get_width() // 2
                    self.screen.blit(skip_surf, (skip_x, self.screen_height - 70))
            except Exception as e:
                Logger.error("Act1View.draw_intro", e)
                
        except Exception as e:
            Logger.error("Act1View.draw_intro", e)


# === STANDALONE TEST ===

if __name__ == "__main__":
    """
    Standalone test entry point for Act 1.
    Initializes pygame and runs Act 1 view independently.
    """
    try:
        Logger.debug("Act1View.__main__", "Standalone test starting")
        
        try:
            pygame.init()
            Logger.debug("Act1View.__main__", "Pygame initialized")
        except Exception as e:
            Logger.error("Act1View.__main__", e)
            raise
        
        try:
            screen_info = pygame.display.Info()
            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.RESIZABLE)
            pygame.display.set_caption("Act 1 - Le Gosier Sec")
            Logger.debug("Act1View.__main__", "Display created", 
                       width=screen_info.current_w, height=screen_info.current_h)
        except Exception as e:
            Logger.error("Act1View.__main__", e)
            raise
        
        try:
            act1 = Act1View(screen)
            result = act1.run()
            Logger.debug("Act1View.__main__", "Act 1 result", result=result)
        except Exception as e:
            Logger.error("Act1View.__main__", e)
            raise
            
    except Exception as e:
        Logger.error("Act1View.__main__", e)
    finally:
        try:
            pygame.quit()
        except Exception:
            pass