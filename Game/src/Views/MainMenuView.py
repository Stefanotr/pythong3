import pygame
import math

class MainMenuView:
    """
    Menu principal du jeu Six-String Hangover
    """
    def __init__(self, screen):
        self.screen = screen
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        # Fonts
        self.title_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.1), bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.04))
        self.menu_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035), bold=True)
        self.small_font = pygame.font.SysFont("Arial", int(self.screen_height * 0.02))
        
        # Couleurs
        self.gold = (255, 215, 0)
        self.white = (255, 255, 255)
        self.red = (255, 50, 50)
        self.green = (50, 255, 50)
        
        # Options du menu
        self.menu_options = [
            "NOUVELLE PARTIE",
            "CREDITS",
            "QUITTER"
        ]
        self.selected_option = 0
        
        # Animation
        self.time = 0
        
        # Charger background si disponible
        self.background = None
        try:
            bg = pygame.image.load("Game/Assets/stage.png").convert()
            self.background = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
            
            # Overlay sombre
            self.overlay = pygame.Surface((self.screen_width, self.screen_height))
            self.overlay.fill((0, 0, 0))
            self.overlay.set_alpha(150)
        except:
            self.background = None
    
    def run(self):
        """Boucle principale du menu"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.KEYDOWN:
                    # Navigation
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    
                    # Sélection
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected_option == 0:  # Nouvelle partie
                            return "START_GAME"
                        elif self.selected_option == 1:  # Crédits
                            self.show_credits()
                        elif self.selected_option == 2:  # Quitter
                            return "QUIT"
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        return "QUIT"
    
    def draw(self):
        """Dessiner le menu"""
        self.time += 1
        
        # Fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.overlay, (0, 0))
        else:
            # Dégradé animé
            for y in range(self.screen_height):
                ratio = y / self.screen_height
                r = int(20 + math.sin(self.time * 0.01 + ratio * 2) * 15)
                g = int(10 + math.sin(self.time * 0.015 + ratio * 1.5) * 10)
                b = int(30 + math.sin(self.time * 0.008 + ratio) * 20)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))
        
        # Titre principal
        title_y = self.screen_height // 5
        
        title_text = "SIX-STRING"
        title_surf = self.title_font.render(title_text, True, self.gold)
        title_shadow = self.title_font.render(title_text, True, (100, 80, 0))
        
        title_x = self.screen_width // 2 - title_surf.get_width() // 2
        self.screen.blit(title_shadow, (title_x + 5, title_y + 5))
        self.screen.blit(title_surf, (title_x, title_y))
        
        # Sous-titre
        subtitle_text = "HANGOVER"
        subtitle_surf = self.title_font.render(subtitle_text, True, self.red)
        subtitle_shadow = self.title_font.render(subtitle_text, True, (80, 0, 0))
        
        subtitle_x = self.screen_width // 2 - subtitle_surf.get_width() // 2
        subtitle_y = title_y + title_surf.get_height() + 10
        self.screen.blit(subtitle_shadow, (subtitle_x + 5, subtitle_y + 5))
        self.screen.blit(subtitle_surf, (subtitle_x, subtitle_y))
        
        # Tagline
        tagline = "🎸 La tournée de la déchéance 🍺"
        tagline_surf = self.subtitle_font.render(tagline, True, self.white)
        tagline_x = self.screen_width // 2 - tagline_surf.get_width() // 2
        self.screen.blit(tagline_surf, (tagline_x, subtitle_y + subtitle_surf.get_height() + 30))
        
        # Options du menu
        menu_start_y = self.screen_height // 2 + 50
        
        for i, option in enumerate(self.menu_options):
            is_selected = (i == self.selected_option)
            
            # Couleur et taille selon sélection
            if is_selected:
                color = self.gold
                # Animation de pulsation
                scale = 1 + math.sin(self.time * 0.1) * 0.05
                font = pygame.font.SysFont("Arial", int(self.screen_height * 0.035 * scale), bold=True)
            else:
                color = self.white
                font = self.menu_font
            
            # Texte
            option_surf = font.render(option, True, color)
            option_x = self.screen_width // 2 - option_surf.get_width() // 2
            option_y = menu_start_y + i * 80
            
            # Ombre
            shadow_surf = font.render(option, True, (0, 0, 0))
            self.screen.blit(shadow_surf, (option_x + 3, option_y + 3))
            
            # Texte principal
            self.screen.blit(option_surf, (option_x, option_y))
            
            # Flèche de sélection
            if is_selected:
                arrow_left = "►"
                arrow_right = "◄"
                arrow_surf_left = self.menu_font.render(arrow_left, True, self.gold)
                arrow_surf_right = self.menu_font.render(arrow_right, True, self.gold)
                
                # Animation de mouvement
                arrow_offset = int(math.sin(self.time * 0.15) * 10)
                
                self.screen.blit(arrow_surf_left, 
                               (option_x - 60 - arrow_offset, option_y))
                self.screen.blit(arrow_surf_right, 
                               (option_x + option_surf.get_width() + 40 + arrow_offset, option_y))
        
        # Instructions
        instruction = "↑↓ Naviguer | ENTRÉE Sélectionner"
        inst_surf = self.small_font.render(instruction, True, (150, 150, 150))
        inst_x = self.screen_width // 2 - inst_surf.get_width() // 2
        self.screen.blit(inst_surf, (inst_x, self.screen_height - 80))
    
    def show_credits(self):
        """Afficher les crédits"""
        showing_credits = True
        clock = pygame.time.Clock()
        
        while showing_credits:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    showing_credits = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        showing_credits = False
            
            # Fond noir
            self.screen.fill((10, 10, 15))
            
            # Titre
            title_text = "🎸 CRÉDITS 🎸"
            title_surf = self.title_font.render(title_text, True, self.gold)
            title_x = self.screen_width // 2 - title_surf.get_width() // 2
            self.screen.blit(title_surf, (title_x, 100))
            
            # Crédits
            credits_lines = [
                "",
                "SIX-STRING HANGOVER",
                "",
                "Un jeu créé pour la Piscine Python",
                "",
                "Développement : Ton Nom",
                "Gameplay : Alcool & Guitares",
                "Musique : Dans ta tête",
                "",
                "Merci d'avoir joué !",
                "",
                "",
                "Appuie sur ESPACE ou ÉCHAP pour revenir"
            ]
            
            credit_y = 250
            for line in credits_lines:
                if line:
                    line_surf = self.subtitle_font.render(line, True, self.white)
                    line_x = self.screen_width // 2 - line_surf.get_width() // 2
                    self.screen.blit(line_surf, (line_x, credit_y))
                credit_y += 50
            
            pygame.display.flip()
            clock.tick(60)


# === TEST STANDALONE ===
if __name__ == "__main__":
    pygame.init()
    
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    pygame.display.set_caption("Six-String Hangover - Menu")
    
    menu = MainMenuView(screen)
    result = menu.run()
    
    print(f"Résultat du menu : {result}")
    
    pygame.quit()