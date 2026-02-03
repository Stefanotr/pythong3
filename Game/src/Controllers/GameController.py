import pygame
from MainMenuView import MainMenuView
from Act1View import Act1View
from Utils.Logger import Logger

class GameController:
    """
    Contrôleur principal qui gère le flux du jeu
    (Menu → Acte 1 → Acte 2 → Acte 3)
    """
    def __init__(self):
        pygame.init()
        
        # Configuration de l'écran
        screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
        pygame.display.set_caption("Six-String Hangover")
        
        # État du jeu
        self.current_state = "MENU"  # MENU, ACT1, ACT2, ACT3, GAME_OVER, QUIT
        
        Logger.debug("GameController.__init__", "Game initialized")
    
    def run(self):
        """Boucle principale du jeu"""
        running = True
        
        while running:
            Logger.debug("GameController.run", f"Current state: {self.current_state}")
            
            # === MENU PRINCIPAL ===
            if self.current_state == "MENU":
                menu = MainMenuView(self.screen)
                result = menu.run()
                
                if result == "START_GAME":
                    self.current_state = "ACT1"
                elif result == "QUIT":
                    running = False
            
            # === ACTE 1 : LE GOSIER SEC ===
            elif self.current_state == "ACT1":
                act1 = Act1View(self.screen)
                result = act1.run()
                
                if result == "ACT2":
                    # TODO : Implémenter l'Acte 2
                    Logger.debug("GameController.run", "Act 1 completed - Moving to Act 2")
                    self.show_transition("ACTE 2", "WOOD-STOCK-OPTION")
                    # Pour l'instant, retourner au menu
                    self.current_state = "MENU"
                elif result == "GAME_OVER":
                    self.current_state = "GAME_OVER"
                elif result == "QUIT":
                    running = False
            
            # === GAME OVER ===
            elif self.current_state == "GAME_OVER":
                game_over_result = self.show_game_over()
                if game_over_result == "RETRY":
                    self.current_state = "ACT1"  # Recommencer l'acte
                elif game_over_result == "MENU":
                    self.current_state = "MENU"
                else:
                    running = False
            
            # === QUITTER ===
            elif self.current_state == "QUIT":
                running = False
        
        Logger.debug("GameController.run", "Game ended")
        pygame.quit()
    
    def show_transition(self, act_name, location_name):
        """Afficher un écran de transition entre les actes"""
        clock = pygame.time.Clock()
        timer = 180  # 3 secondes
        
        font_title = pygame.font.SysFont("Arial", 80, bold=True)
        font_subtitle = pygame.font.SysFont("Arial", 40)
        font_small = pygame.font.SysFont("Arial", 25)
        
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
    
    def show_game_over(self):
        """Afficher l'écran de game over"""
        clock = pygame.time.Clock()
        
        font_title = pygame.font.SysFont("Arial", 100, bold=True)
        font_option = pygame.font.SysFont("Arial", 40, bold=True)
        font_small = pygame.font.SysFont("Arial", 25)
        
        options = ["RÉESSAYER", "MENU PRINCIPAL", "QUITTER"]
        selected = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if selected == 0:
                            return "RETRY"
                        elif selected == 1:
                            return "MENU"
                        else:
                            return "QUIT"
            
            # Fond noir avec effet
            self.screen.fill((20, 0, 0))
            
            screen_info = pygame.display.Info()
            screen_width = screen_info.current_w
            screen_height = screen_info.current_h
            
            # Titre GAME OVER
            title_text = "💀 GAME OVER 💀"
            title_surf = font_title.render(title_text, True, (255, 50, 50))
            title_shadow = font_title.render(title_text, True, (100, 0, 0))
            
            title_x = screen_width // 2 - title_surf.get_width() // 2
            title_y = screen_height // 3
            
            self.screen.blit(title_shadow, (title_x + 5, title_y + 5))
            self.screen.blit(title_surf, (title_x, title_y))
            
            # Message
            message = "Tu t'es fait défoncer comme une guitare cheap..."
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
            inst_text = "↑↓ Naviguer | ENTRÉE Sélectionner"
            inst_surf = font_small.render(inst_text, True, (150, 150, 150))
            inst_x = screen_width // 2 - inst_surf.get_width() // 2
            self.screen.blit(inst_surf, (inst_x, screen_height - 80))
            
            pygame.display.flip()
            clock.tick(60)


# === POINT D'ENTRÉE ===
if __name__ == "__main__":
    game = GameController()
    game.run()