import pygame
import math

class RhythmCombatView:
    """
    Vue pour le MODE COMBAT RHYTHM
    Affiche le jeu de rythme + les HP du joueur et du boss
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Background
        self.background_image = None
        self.overlay = None
        
        image_path = "Game/Assets/stage.png"
        try:
            loaded_img = pygame.image.load(image_path).convert()
            self.background_image = pygame.transform.scale(loaded_img, (screen_width, screen_height))
            self.overlay = pygame.Surface((screen_width, screen_height))
            self.overlay.fill((0, 0, 0))
            self.overlay.set_alpha(120)
        except FileNotFoundError:
            pass

        # Fonts
        self.font = pygame.font.SysFont("Arial", int(screen_height * 0.025), bold=True)
        self.big_font = pygame.font.SysFont("Arial", int(screen_height * 0.08), bold=True)
        self.combo_font = pygame.font.SysFont("Arial", int(screen_height * 0.05), bold=True)
        self.title_font = pygame.font.SysFont("Arial", int(screen_height * 0.035), bold=True)
        self.huge_font = pygame.font.SysFont("Arial", int(screen_height * 0.3), bold=True)
        
        # Couleurs des lanes
        self.lane_colors = [
            (255, 20, 147),   # Rose (C)
            (0, 255, 255),    # Cyan (V)
            (50, 255, 50),    # Vert (B)
            (255, 215, 0)     # Or (N)
        ]
        
        # Positions des cordes - use 85% of screen width for better fullscreen experience
        guitar_width = screen_width * 0.85
        guitar_start = (screen_width - guitar_width) / 2
        spacing = guitar_width / 5
        
        self.lane_x = [
            int(guitar_start + spacing),
            int(guitar_start + spacing * 2),
            int(guitar_start + spacing * 3),
            int(guitar_start + spacing * 4)
        ]
        
        self.guitar_start = int(guitar_start)
        self.guitar_width = int(guitar_width)
        
        # Particules
        self.particles = []
        self.time = 0

    def create_particles(self, x, y, color):
        for _ in range(12):
            angle = pygame.math.Vector2(1, 0).rotate((_ * 30))
            self.particles.append({
                'x': x, 'y': y,
                'vx': angle.x * 4, 'vy': angle.y * 4,
                'life': 25, 'color': color
            })

    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_health_bar(self, screen, x, y, width, height, current, maximum, label, is_player=True):
        """Barre de vie stylée"""
        ratio = current / maximum if maximum > 0 else 0
        
        # Couleurs
        if is_player:
            color_good = (50, 255, 50)   # Vert pour joueur
            color_bad = (255, 50, 50)
        else:
            color_good = (255, 100, 255)  # Rose pour boss
            color_bad = (255, 50, 50)
        
        # Fond
        pygame.draw.rect(screen, (20, 20, 20), (x - 2, y - 2, width + 4, height + 4), border_radius=8)
        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height), border_radius=6)
        
        # Remplissage
        filled_width = int(width * ratio)
        if ratio > 0.5:
            color = color_good
        else:
            color = color_bad
            
        if filled_width > 0:
            pygame.draw.rect(screen, color, (x, y, filled_width, height), border_radius=6)
        
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2, border_radius=6)
        
        # Label
        label_surf = self.font.render(label, True, (255, 255, 255))
        screen.blit(label_surf, (x, y - 20))
        
        # HP text
        hp_text = self.font.render(f"{int(current)}/{int(maximum)}", True, (255, 255, 255))
        screen.blit(hp_text, (x + width//2 - hp_text.get_width()//2, y + height//2 - hp_text.get_height()//2))

    def draw(self, screen, rhythm_model, player_model, boss_model, note_speed=0.5, countdown_val=0):
        """
        Dessine l'interface du combat rhythm
        """
        self.time += 1
        
        # --- FOND ---
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
            screen.blit(self.overlay, (0, 0))
        else:
            for y in range(self.screen_height):
                shade = int(20 + y * 0.02)
                pygame.draw.line(screen, (shade, shade // 2, shade // 3), (0, y), (self.screen_width, y))
        
        # --- MANCHE DE GUITARE ---
        guitar_rect = pygame.Rect(self.guitar_start - 15, 0, self.guitar_width + 30, self.screen_height)
        guitar_surf = pygame.Surface((guitar_rect.width, guitar_rect.height), pygame.SRCALPHA)
        
        for i in range(guitar_rect.width):
            alpha = int(100 + (i / guitar_rect.width) * 50)
            pygame.draw.line(guitar_surf, (20, 20, 30, alpha), (i, 0), (i, guitar_rect.height))
        
        screen.blit(guitar_surf, guitar_rect)
        pygame.draw.rect(screen, (80, 120, 180), guitar_rect, 2, border_radius=10)
        
        # --- LIGNE DE FRAPPE & CORDES ---
        hit_line_y = rhythm_model.hit_line_y
        
        pygame.draw.line(screen, (200, 200, 200), 
                         (self.guitar_start - 15, hit_line_y), 
                         (self.guitar_start + self.guitar_width + 15, hit_line_y), 3)

        for i, x in enumerate(self.lane_x):
            color = self.lane_colors[i]
            
            # Corde
            pygame.draw.line(screen, (color[0]//3, color[1]//3, color[2]//3), (x, 0), (x, self.screen_height), 2)
            
            # Cible
            pygame.draw.circle(screen, (0, 0, 0), (x, hit_line_y), 32)
            pygame.draw.circle(screen, color, (x, hit_line_y), 30, 4)
            pygame.draw.circle(screen, (255, 255, 0), (x, hit_line_y), 18, 2)
            pygame.draw.circle(screen, (255, 255, 255), (x, hit_line_y), 5)
        
        # --- NOTES ---
        for note in rhythm_model.notes:
            if note["active"]:
                lane_index = rhythm_model.lanes.index(note["lane"])
                x_pos = self.lane_x[lane_index]
                color = self.lane_colors[lane_index]
                y_pos = int(note["y"])
                
                # Queue
                duration = note.get("duration", 0)
                tail_len = 20 + int(note_speed * 10) 
                if duration > 0:
                    tail_len = int(duration * note_speed)

                tail_surf = pygame.Surface((14, tail_len), pygame.SRCALPHA)
                tail_surf.fill((*color, 150))
                screen.blit(tail_surf, (x_pos - 7, y_pos - tail_len))

                # Tête
                pygame.draw.circle(screen, (255, 255, 255), (x_pos, y_pos), 26)
                pygame.draw.circle(screen, color, (x_pos, y_pos), 22)
                pygame.draw.circle(screen, (0, 0, 0), (x_pos, y_pos), 10)
        
        # --- PARTICULES ---
        for particle in self.particles:
            size = int(particle['life'] / 3)
            if size > 0:
                surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*particle['color'], 200), (size, size), size)
                screen.blit(surf, (particle['x']-size, particle['y']-size))
        self.update_particles()
        
        # --- HUD COMBAT ---
        hud_h = int(self.screen_height * 0.15)
        hud_bg = pygame.Surface((self.screen_width, hud_h), pygame.SRCALPHA)
        hud_bg.fill((10, 10, 20, 220))
        screen.blit(hud_bg, (0, 0))
        pygame.draw.line(screen, (255, 50, 50), (0, hud_h), (self.screen_width, hud_h), 3)
        
        # Titre du combat
        combat_title = self.title_font.render("COMBAT RHYTHM", True, (255, 215, 0))
        screen.blit(combat_title, (self.screen_width//2 - combat_title.get_width()//2, 10))
        
        # HP JOUEUR (Gauche)
        player_hp_width = int(self.screen_width * 0.3)
        self.draw_health_bar(
            screen, 
            20, 
            int(hud_h * 0.5),
            player_hp_width,
            int(hud_h * 0.3),
            player_model.getHealth(),
            100,
            f"{player_model.getName()}",
            is_player=True
        )
        
        # HP BOSS (Droite)
        boss_hp_width = int(self.screen_width * 0.3)
        boss_hp_x = self.screen_width - boss_hp_width - 20
        self.draw_health_bar(
            screen,
            boss_hp_x,
            int(hud_h * 0.5),
            boss_hp_width,
            int(hud_h * 0.3),
            boss_model.getHealth(),
            100,  # Max HP du boss
            f"{boss_model.getName()}",
            is_player=False
        )
        
        # --- FEEDBACK CENTRAL ---
        if rhythm_model.feedback and rhythm_model.feedback_timer > 0:
            fb_col = (255, 255, 255)
            
            if "MISS" in rhythm_model.feedback:
                fb_col = (255, 0, 0)
            elif "PERFECT" in rhythm_model.feedback: 
                fb_col = (255, 255, 0)
            elif "EXCELLENT" in rhythm_model.feedback: 
                fb_col = (0, 255, 255)
            elif "GOOD" in rhythm_model.feedback:
                fb_col = (50, 255, 50)
            elif "OK" in rhythm_model.feedback:
                fb_col = (255, 200, 100)
            elif "DMG" in rhythm_model.feedback:
                fb_col = (255, 100, 100)
            
            fb_surf = self.big_font.render(rhythm_model.feedback, True, fb_col)
            fb_shadow = self.big_font.render(rhythm_model.feedback, True, (0, 0, 0))
            
            fb_x = self.screen_width//2 - fb_surf.get_width()//2
            fb_y = self.screen_height//2
            
            screen.blit(fb_shadow, (fb_x + 3, fb_y + 3))
            screen.blit(fb_surf, (fb_x, fb_y))
            
            # Combo
            if rhythm_model.combo > 1:
                combo_surf = self.combo_font.render(f"COMBO x{rhythm_model.combo}", True, (255, 100, 255))
                combo_shadow = self.combo_font.render(f"COMBO x{rhythm_model.combo}", True, (100, 0, 100))
                
                combo_x = self.screen_width//2 - combo_surf.get_width()//2
                combo_y = fb_y + 80
                
                screen.blit(combo_shadow, (combo_x + 2, combo_y + 2))
                screen.blit(combo_surf, (combo_x, combo_y))

        # --- TOUCHES ---
        keys = ["C", "V", "B", "N"]
        for i, x in enumerate(self.lane_x):
            txt = self.title_font.render(keys[i], True, self.lane_colors[i])
            shadow = self.title_font.render(keys[i], True, (0, 0, 0))
            
            txt_x = x - txt.get_width()//2
            txt_y = self.screen_height - 40
            
            screen.blit(shadow, (txt_x + 2, txt_y + 2))
            screen.blit(txt, (txt_x, txt_y))

        # --- COMPTE À REBOURS ---
        if countdown_val > 0:
            over = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            over.fill((0, 0, 0, 150))
            screen.blit(over, (0, 0))
            
            col = (100, 255, 100) if countdown_val > 3 else ((255, 200, 0) if countdown_val > 1 else (255, 50, 50))
            
            ready = self.title_font.render("PRÊT POUR LE COMBAT ?", True, (255, 255, 255))
            screen.blit(ready, (self.screen_width//2 - ready.get_width()//2, self.screen_height//2 - 150))
            
            nb = self.huge_font.render(str(countdown_val), True, col)
            nb_shadow = self.huge_font.render(str(countdown_val), True, (0, 0, 0))
            
            nb_x = self.screen_width//2 - nb.get_width()//2
            nb_y = self.screen_height//2 - nb.get_height()//2
            
            screen.blit(nb_shadow, (nb_x + 5, nb_y + 5))
            screen.blit(nb, (nb_x, nb_y))