"""
GameController Module

Main game controller managing the overall game flow.
Handles state transitions between menu, acts, game over, and quit states.
"""

import pygame
from Views.WelcomePageView import WelcomPageView
from Views.Act1View import Act1View
from Utils.Logger import Logger
from Controllers.GameState import GameState


# === GAME CONTROLLER CLASS ===

class GameController:
    """
    Main game controller managing the overall game flow.
    Handles state transitions: Menu → Act 1 → Act 2 → Act 3 → Game Over.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self):
        """
        Initialize the game controller.
        Sets up pygame, display, and initial game state.
        """
        try:
            # Ensure pygame is initialized (WelcomePageView should initialize in normal app flow)
            try:
                if not pygame.get_init():
                    pygame.init()
                    Logger.debug("GameController.__init__", "Pygame initialized by GameController (standalone mode)")
                else:
                    Logger.debug("GameController.__init__", "Pygame already initialized, reusing")
            except Exception as e:
                Logger.error("GameController.__init__", e)
                raise

            # Screen configuration: reuse existing display if present, else create one
            try:
                screen_surface = pygame.display.get_surface()
                if screen_surface is None:
                    screen_info = pygame.display.Info()
                    try:
                        import os
                        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
                    except Exception:
                        pass
                    self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
                    Logger.debug("GameController.__init__", "Display created", width=screen_info.current_w, height=screen_info.current_h)
                else:
                    self.screen = screen_surface
                    Logger.debug("GameController.__init__", "Reusing existing display surface", size=self.screen.get_size())
                pygame.display.set_caption("Six-String Hangover")
            except Exception as e:
                Logger.error("GameController.__init__", e)
                raise
            
            # Game state
            self.current_state = GameState.MAIN_MENU.value  # MAIN_MENU, ACT1, ACT2, RHYTHM, GAME_OVER, QUIT
            
            Logger.debug("GameController.__init__", "Game controller initialized")
            
        except Exception as e:
            Logger.error("GameController.__init__", e)
            raise
    
    # === MAIN GAME LOOP ===
    
    def run(self):
        """
        Main game loop managing state transitions.
        Handles menu, acts, game over, and quit states.
        """
        try:
            running = True
            Logger.debug("GameController.run", "Game loop started")
            
            while running:
                try:
                    Logger.debug("GameController.run", f"Current state: {self.current_state}")
                    
                    # === MAIN MENU ===
                    if self.current_state == GameState.MAIN_MENU.value:
                        try:
                            # Instantiate the welcome/main menu view using current display size and resizable flag
                            screen_info = pygame.display.Info()
                            menu = WelcomPageView("Six-String Hangover", width=screen_info.current_w, height=screen_info.current_h, RESIZABLE=pygame.RESIZABLE)
                            result = menu.run()
                            
                            if result == GameState.START_GAME.value:
                                self.current_state = GameState.ACT1.value
                                Logger.debug("GameController.run", "Transitioning to Act 1")
                            elif result == GameState.QUIT.value:
                                running = False
                                Logger.debug("GameController.run", "Quit requested from menu")
                        except Exception as e:
                            Logger.error("GameController.run", e)
                            running = False
                    
                    # === ACT 1: LE GOSIER SEC ===
                    elif self.current_state == GameState.ACT1.value:
                        try:
                            act1 = Act1View(self.screen)
                            result = act1.run()
                            
                            if result == GameState.ACT2.value:
                                # TODO: Implement Act 2
                                Logger.debug("GameController.run", "Act 1 completed - Moving to Act 2")
                                self.showTransition("ACTE 2", "WOOD-STOCK-OPTION")
                                # For now, return to menu
                                self.current_state = GameState.MAIN_MENU.value
                            elif result == GameState.GAME_OVER.value:
                                self.current_state = GameState.GAME_OVER.value
                                Logger.debug("GameController.run", "Game over state")
                            elif result == GameState.QUIT.value:
                                running = False
                                Logger.debug("GameController.run", "Quit requested from Act 1")
                        except Exception as e:
                            Logger.error("GameController.run", e)
                            self.current_state = GameState.GAME_OVER.value
                    
                    # === GAME OVER ===
                    elif self.current_state == GameState.GAME_OVER.value:
                        try:
                            game_over_result = self.showGameOver()
                            if game_over_result == "RETRY":
                                self.current_state = GameState.ACT1.value  # Restart the act
                                Logger.debug("GameController.run", "Retry selected")
                            elif game_over_result == "MENU":
                                self.current_state = GameState.MAIN_MENU.value
                                Logger.debug("GameController.run", "Return to menu selected")
                            else:
                                running = False
                                Logger.debug("GameController.run", "Quit from game over")
                        except Exception as e:
                            Logger.error("GameController.run", e)
                            running = False
                    
                    # === QUIT ===
                    elif self.current_state == GameState.QUIT.value:
                        running = False
                        Logger.debug("GameController.run", "Quit state")
                    
                except Exception as e:
                    Logger.error("GameController.run", e)
                    # Continue running even if one iteration fails
                    continue
            
            Logger.debug("GameController.run", "Game loop ended")
            
        except Exception as e:
            Logger.error("GameController.run", e)
        finally:
            try:
                pygame.quit()
            except Exception:
                pass
    
    # === TRANSITION SCREENS ===
    
    def showTransition(self, act_name, location_name):
        """
        Display a transition screen between acts.
        
        Args:
            act_name: Name of the act (e.g., "ACTE 2")
            location_name: Name of the location (e.g., "WOOD-STOCK-OPTION")
        """
        try:
            clock = pygame.time.Clock()
            timer = 180  # 3 seconds at 60fps
            
            try:
                font_title = pygame.font.SysFont("Arial", 80, bold=True)
                font_subtitle = pygame.font.SysFont("Arial", 40)
                font_small = pygame.font.SysFont("Arial", 25)
            except Exception as e:
                Logger.error("GameController.showTransition", e)
                font_title = pygame.font.Font(None, 80)
                font_subtitle = pygame.font.Font(None, 40)
                font_small = pygame.font.Font(None, 25)
        
            while timer > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return
                
                # Fond noir
                self.screen.fill((10, 10, 15))
                
                screen_info = pygame.display.Info()
                screen_width = screen_info.current_w
                screen_height = screen_info.current_h
                
                # Titre
                title_text = f"🎸 {act_name} 🎸"
                title_surf = font_title.render(title_text, True, (255, 215, 0))
                title_x = screen_width // 2 - title_surf.get_width() // 2
                self.screen.blit(title_surf, (title_x, screen_height // 2 - 100))
                
                # Sous-titre
                subtitle_text = location_name
                subtitle_surf = font_subtitle.render(subtitle_text, True, (255, 255, 255))
                subtitle_x = screen_width // 2 - subtitle_surf.get_width() // 2
                self.screen.blit(subtitle_surf, (subtitle_x, screen_height // 2))
                
                # Instructions
                skip_text = "Appuie sur ESPACE pour passer"
                skip_surf = font_small.render(skip_text, True, (150, 150, 150))
                skip_x = screen_width // 2 - skip_surf.get_width() // 2
                self.screen.blit(skip_surf, (skip_x, screen_height - 100))
                
                pygame.display.flip()
                clock.tick(60)
                timer -= 1
        
        except Exception as e:
            Logger.error("GameController.showTransition", e)
            return

        """
        Display the game over screen with retry/menu/quit options.
        
        Returns:
            str: User selection ("RETRY", "MENU", or "QUIT")
        """
        try:
            clock = pygame.time.Clock()
            
            try:
                font_title = pygame.font.SysFont("Arial", 100, bold=True)
                font_option = pygame.font.SysFont("Arial", 40, bold=True)
                font_small = pygame.font.SysFont("Arial", 25)
            except Exception as e:
                Logger.error("GameController.showGameOver", e)
                font_title = pygame.font.Font(None, 100)
                font_option = pygame.font.Font(None, 40)
                font_small = pygame.font.Font(None, 25)
        
            options = ["RÉESSAYER", "MENU PRINCIPAL", "QUITTER"]
            selected = 0
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return GameState.QUIT.value
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected = (selected - 1) % len(options)
                        elif event.key == pygame.K_DOWN:
                            selected = (selected + 1) % len(options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if selected == 0:
                                return "RETRY"
                            elif selected == 1:
                                return GameState.MAIN_MENU.value
                            else:
                                return GameState.QUIT.value
                
                # Fond noir avec effet
                self.screen.fill((20, 0, 0))
                
                screen_info = pygame.display.Info()
                screen_width = screen_info.current_w
                screen_height = screen_info.current_h
                
                # GAME OVER Title
                title_text = "💀 GAME OVER 💀"
                title_surf = font_title.render(title_text, True, (255, 50, 50))
                title_shadow = font_title.render(title_text, True, (100, 0, 0))
                
                title_x = screen_width // 2 - title_surf.get_width() // 2
                title_y = screen_height // 3
                
                self.screen.blit(title_shadow, (title_x + 5, title_y + 5))
                self.screen.blit(title_surf, (title_x, title_y))
                
                # Message
                message = "You got wrecked like a cheap guitar..."
                msg_surf = font_small.render(message, True, (200, 200, 200))
                msg_x = screen_width // 2 - msg_surf.get_width() // 2
                self.screen.blit(msg_surf, (msg_x, title_y + 120))
                
                # Options
                option_y = screen_height // 2 + 50
                
                for i, option in enumerate(options):
                    is_selected = (i == selected)
                    color = (255, 215, 0) if is_selected else (255, 255, 255)
                    
                    option_surf = font_option.render(option, True, color)
                    option_x = screen_width // 2 - option_surf.get_width() // 2
                    
                    self.screen.blit(option_surf, (option_x, option_y + i * 70))
                    
                    if is_selected:
                        arrow = "►"
                        arrow_surf = font_option.render(arrow, True, (255, 215, 0))
                        self.screen.blit(arrow_surf, (option_x - 50, option_y + i * 70))
                
                # Instructions
                inst_text = "↑↓ Navigate | ENTER Select"
                inst_surf = font_small.render(inst_text, True, (150, 150, 150))
                inst_x = screen_width // 2 - inst_surf.get_width() // 2
                self.screen.blit(inst_surf, (inst_x, screen_height - 80))
                
                pygame.display.flip()
                clock.tick(60)

        except Exception as e:
            Logger.error("GameController.showGameOver", e)
            return GameState.QUIT.value


# === ENTRY POINT ===
if __name__ == "__main__":
    game = GameController()
    game.run()