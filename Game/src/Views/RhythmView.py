import pygame
import math

class RhythmView:
    def __init__(self, screen_width, screen_height, background_image_path="Game/Assets/stage.png", character_view=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.character_view = character_view  # Optional character view
        
        # --- 1. CHARGEMENT DU BACKGROUND ---
        self.background_image = None
        self.overlay = None
        
        image_path = background_image_path

        try:
            loaded_img = pygame.image.load(image_path).convert()
            self.background_image = pygame.transform.scale(loaded_img, (screen_width, screen_height))
            
            # Voile noir plus léger
            self.overlay = pygame.Surface((screen_width, screen_height))
            self.overlay.fill((0, 0, 0))
            self.overlay.set_alpha(100) 
            print(f"Background chargé : {image_path}")
            
        except FileNotFoundError:
            print(f"Image non trouvée ({image_path}). Mode Dégradé activé.")
            self.background_image = None

        # --- 2. FONTS ---
        self.font = pygame.font.SysFont("Arial", int(screen_height * 0.025), bold=True)
        self.big_font = pygame.font.SysFont("Arial", int(screen_height * 0.08), bold=True)
        self.combo_font = pygame.font.SysFont("Arial", int(screen_height * 0.05), bold=True)
        self.title_font = pygame.font.SysFont("Arial", int(screen_height * 0.035), bold=True)
        self.score_font = pygame.font.SysFont("Arial", int(screen_height * 0.06), bold=True)
        
        # Police GÉANTE pour le compte à rebours
        self.huge_font = pygame.font.SysFont("Arial", int(screen_height * 0.3), bold=True)
        
        # Couleurs néon pour les 4 cordes
        self.lane_colors = [
            (255, 20, 147),   # Rose (C)
            (0, 255, 255),    # Cyan (V)
            (50, 255, 50),    # Vert (B)
            (255, 215, 0)     # Or (N)
        ]
        
        # Positions des cordes
        guitar_width = screen_width * 0.4
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

    def clamp(self, value, min_val=0, max_val=255):
        return max(min_val, min(int(value), max_val))

    def draw_health_bar(self, screen, x, y, width, height, current, maximum, label, color_good, color_bad):
        ratio = current / maximum if maximum > 0 else 0
        
        # Fond
        pygame.draw.rect(screen, (20, 20, 20), (x - 2, y - 2, width + 4, height + 4), border_radius=8)
        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height), border_radius=6)
        
        # Remplissage
        filled_width = int(width * ratio)
        if ratio > 0.5:
            c1, c2 = color_good, (int(color_good[0]*0.8), int(color_good[1]*0.8), int(color_good[2]*0.8))
        else:
            c1, c2 = color_bad, (int(color_bad[0]*0.8), int(color_bad[1]*0.5), int(color_bad[2]*0.5))
            
        if filled_width > 0:
             pygame.draw.rect(screen, c1, (x, y, filled_width, height), border_radius=6)
        
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2, border_radius=6)
        
        # Label
        label_surf = self.font.render(label, True, (255, 255, 255))
        screen.blit(label_surf, (x, y - 20))
        
        # Valeur %
        hp_text = self.font.render(f"{int(current)}%", True, (255, 255, 255))
        screen.blit(hp_text, (x + width//2 - hp_text.get_width()//2, y + height//2 - hp_text.get_height()//2))

    def draw_precision_zones(self, screen, hit_line_y):
        """
        NOUVEAU : Afficher les zones de précision autour de la ligne de frappe
        pour aider le joueur à comprendre le système
        """
        # Zone PERFECT (±50ms @ 0.5 speed = ±25px)
        perfect_height = int(50 * 0.5)  # 25px
        perfect_rect = pygame.Rect(
            self.guitar_start - 15,
            hit_line_y - perfect_height,
            self.guitar_width + 30,
            perfect_height * 2
        )
        # Overlay jaune très transparent
        perfect_surf = pygame.Surface((perfect_rect.width, perfect_rect.height), pygame.SRCALPHA)
        perfect_surf.fill((255, 255, 0, 15))  # Jaune très pâle
        screen.blit(perfect_surf, perfect_rect)
        
        # Zone EXCELLENT (±100ms = ±50px)
        excellent_height = int(100 * 0.5)
        excellent_rect = pygame.Rect(
            self.guitar_start - 15,
            hit_line_y - excellent_height,
            self.guitar_width + 30,
            excellent_height * 2
        )
        excellent_surf = pygame.Surface((excellent_rect.width, excellent_rect.height), pygame.SRCALPHA)
        excellent_surf.fill((0, 255, 255, 10))  # Cyan très pâle
        screen.blit(excellent_surf, excellent_rect)
        
        # Zone GOOD (±150ms = ±75px)
        good_height = int(150 * 0.5)
        good_rect = pygame.Rect(
            self.guitar_start - 15,
            hit_line_y - good_height,
            self.guitar_width + 30,
            good_height * 2
        )
        good_surf = pygame.Surface((good_rect.width, good_rect.height), pygame.SRCALPHA)
        good_surf.fill((50, 255, 50, 8))  # Vert très pâle
        screen.blit(good_surf, good_rect)

    def draw(self, screen, rhythm_model, character_model, note_speed=0.5, countdown_val=0):
        self.time += 1
        
        # --- A. FOND ---
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
            screen.blit(self.overlay, (0, 0))
        else:
            for y in range(self.screen_height):
                shade = int(20 + y * 0.02)
                pygame.draw.line(screen, (shade, shade // 2, shade // 3), (0, y), (self.screen_width, y))
        
        # Personnage affichage géré par RhythmPageView

        
        # --- B. MANCHE DE GUITARE ---
        guitar_rect = pygame.Rect(self.guitar_start - 15, 0, self.guitar_width + 30, self.screen_height)
        guitar_surf = pygame.Surface((guitar_rect.width, guitar_rect.height), pygame.SRCALPHA)
        
        # Dégradé vertical du manche
        for i in range(guitar_rect.width):
            alpha = int(100 + (i / guitar_rect.width) * 50)
            pygame.draw.line(guitar_surf, (20, 20, 30, alpha), (i, 0), (i, guitar_rect.height))
        
        screen.blit(guitar_surf, guitar_rect)
        pygame.draw.rect(screen, (80, 120, 180), guitar_rect, 2, border_radius=10)
        
        # --- ZONES DE PRÉCISION (NOUVEAU) ---
        hit_line_y = rhythm_model.hit_line_y
        self.draw_precision_zones(screen, hit_line_y)
        
        # --- C. CORDES & LIGNE DE FRAPPE ---
        
        # Ligne blanche horizontale (frette principale)
        pygame.draw.line(screen, (200, 200, 200), 
                         (self.guitar_start - 15, hit_line_y), 
                         (self.guitar_start + self.guitar_width + 15, hit_line_y), 3)

        for i, x in enumerate(self.lane_x):
            color = self.lane_colors[i]
            
            # Corde
            pygame.draw.line(screen, (color[0]//3, color[1]//3, color[2]//3), (x, 0), (x, self.screen_height), 2)
            
            # Cible (Hit Circle) - Plus visible
            pygame.draw.circle(screen, (0, 0, 0), (x, hit_line_y), 32)
            pygame.draw.circle(screen, color, (x, hit_line_y), 30, 4)  # Bordure plus épaisse
            
            # Zone PERFECT intérieure
            pygame.draw.circle(screen, (255, 255, 0), (x, hit_line_y), 18, 2)
            
            # Point central
            pygame.draw.circle(screen, (255, 255, 255), (x, hit_line_y), 5)
        
        # --- D. NOTES ---
        for note in rhythm_model.notes:
            if note["active"] and "y" in note:  # Only draw if Y position is set
                lane_index = rhythm_model.lanes.index(note["lane"])
                x_pos = self.lane_x[lane_index]
                color = self.lane_colors[lane_index]
                y_pos = int(note["y"])
                
                # 1. Queue (Sustain)
                duration = note.get("duration", 0)
                tail_len = 20 + int(note_speed * 10) 
                if duration > 0:
                     tail_len = int(duration * note_speed)

                tail_surf = pygame.Surface((14, tail_len), pygame.SRCALPHA)
                tail_surf.fill((*color, 150))
                screen.blit(tail_surf, (x_pos - 7, y_pos - tail_len))

                # 2. Tête de note
                pygame.draw.circle(screen, (255, 255, 255), (x_pos, y_pos), 26)
                pygame.draw.circle(screen, color, (x_pos, y_pos), 22)
                pygame.draw.circle(screen, (0, 0, 0), (x_pos, y_pos), 10)
        
        # --- E. PARTICULES ---
        for particle in self.particles:
            size = int(particle['life'] / 3)
            if size > 0:
                surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*particle['color'], 200), (size, size), size)
                screen.blit(surf, (particle['x']-size, particle['y']-size))
        self.update_particles()
        
        # --- F. HUD ---
        hud_h = int(self.screen_height * 0.12)
        hud_bg = pygame.Surface((self.screen_width, hud_h), pygame.SRCALPHA)
        hud_bg.fill((10, 10, 20, 200))
        screen.blit(hud_bg, (0, 0))
        pygame.draw.line(screen, (100, 100, 255), (0, hud_h), (self.screen_width, hud_h), 2)
        
        # Jauge Hype
        hype_col = (0, 255, 255) if rhythm_model.crowd_satisfaction > 80 else (50, 255, 50)
        if rhythm_model.crowd_satisfaction < 40: hype_col = (255, 50, 50)
        label_hype = "EN FEU" if rhythm_model.crowd_satisfaction > 80 else "PUBLIC"
        if rhythm_model.crowd_satisfaction < 40: label_hype = "EN COLERE"
        
        self.draw_health_bar(screen, 20, int(hud_h*0.4), int(self.screen_width*0.25), int(hud_h*0.35), 
                             rhythm_model.crowd_satisfaction, 100, label_hype, hype_col, (50, 0, 0))
        
        # Score & Cash
        score_txt = self.score_font.render(f"{rhythm_model.score:,}", True, (255, 215, 0))
        screen.blit(score_txt, (self.screen_width//2 - score_txt.get_width()//2, hud_h//2 - 20))
        
        # Label SCORE
        score_label = self.font.render("SCORE", True, (200, 200, 200))
        screen.blit(score_label, (self.screen_width//2 - score_label.get_width()//2, int(hud_h*0.1)))
        
        # Display earned cash - calculate in real-time based on current performance
        # If cash_earned was set (end of game), use that; otherwise estimate from current hits
        if hasattr(rhythm_model, 'cash_earned') and rhythm_model.cash_earned > 0:
            # Use actual final cash amount
            display_cash = rhythm_model.cash_earned
        else:
            # Calculate cash based on total hits and player level
            # 1$ per hit × (player_level + 1)
            try:
                player_level = character_model.getLevel() if hasattr(character_model, 'getLevel') else 0
            except:
                player_level = 0
            
            total_hits = getattr(rhythm_model, 'total_hits', 0)
            base_hit_cash = total_hits * 1  # 1$ per hit
            display_cash = base_hit_cash * (player_level + 1)
        
        cash_txt = self.score_font.render(f"{display_cash}$", True, (100, 255, 100))
        screen.blit(cash_txt, (self.screen_width - cash_txt.get_width() - 20, hud_h//2 - 20))

        # Feedback & Combo
        if rhythm_model.feedback and rhythm_model.feedback_timer > 0:
            fb_col = (255, 255, 255)
            
            # Couleurs selon le feedback
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
            elif "LATE" in rhythm_model.feedback or "EARLY" in rhythm_model.feedback:
                fb_col = (150, 150, 150)
            
            fb_surf = self.big_font.render(rhythm_model.feedback, True, fb_col)
            fb_shadow = self.big_font.render(rhythm_model.feedback, True, (0, 0, 0))
            
            fb_x = self.screen_width//2 - fb_surf.get_width()//2
            fb_y = self.screen_height//2
            
            screen.blit(fb_shadow, (fb_x + 3, fb_y + 3))
            screen.blit(fb_surf, (fb_x, fb_y))
            
            if rhythm_model.combo > 1:
                combo_surf = self.combo_font.render(f"COMBO x{rhythm_model.combo}", True, (255, 100, 255))
                combo_shadow = self.combo_font.render(f"COMBO x{rhythm_model.combo}", True, (100, 0, 100))
                
                combo_x = self.screen_width//2 - combo_surf.get_width()//2
                combo_y = fb_y + 80
                
                screen.blit(combo_shadow, (combo_x + 2, combo_y + 2))
                screen.blit(combo_surf, (combo_x, combo_y))

        # Touches
        keys = ["C", "V", "B", "N"]
        for i, x in enumerate(self.lane_x):
            txt = self.title_font.render(keys[i], True, self.lane_colors[i])
            shadow = self.title_font.render(keys[i], True, (0, 0, 0))
            
            txt_x = x - txt.get_width()//2
            txt_y = self.screen_height - 40
            
            screen.blit(shadow, (txt_x + 2, txt_y + 2))
            screen.blit(txt, (txt_x, txt_y))
        
        # --- F.2 HUD BAS DE L'ÉCRAN (LEVEL et ALCOOL) ---
        try:
            # Level en bas à gauche
            level = character_model.getLevel() if hasattr(character_model, 'getLevel') else 1
            level_text = self.font.render(f"LEVEL {level}", True, (100, 255, 100))
            screen.blit(level_text, (20, self.screen_height - 50))
            
            # Alcool en bas à droite
            alcohol = character_model.getDrunkenness() if hasattr(character_model, 'getDrunkenness') else 0
            alcohol_color = (255, 100, 100) if alcohol > 60 else (100, 255, 100)
            alcohol_text = self.font.render(f"ALCOHOL: {alcohol}%", True, alcohol_color)
            screen.blit(alcohol_text, (self.screen_width - alcohol_text.get_width() - 20, self.screen_height - 50))
        except Exception as e:
            pass

        # --- G. OVERLAY COMPTE À REBOURS ---
        if countdown_val > 0:
            over = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            over.fill((0, 0, 0, 150))
            screen.blit(over, (0, 0))
            
            col = (100, 255, 100) if countdown_val > 3 else ((255, 200, 0) if countdown_val > 1 else (255, 50, 50))
            ready = self.title_font.render("PRÊT ?", True, (255, 255, 255))
            screen.blit(ready, (self.screen_width//2 - ready.get_width()//2, self.screen_height//2 - 150))
            
            nb = self.huge_font.render(str(countdown_val), True, col)
            nb_shadow = self.huge_font.render(str(countdown_val), True, (0, 0, 0))
            
            nb_x = self.screen_width//2 - nb.get_width()//2
            nb_y = self.screen_height//2 - nb.get_height()//2
            
            screen.blit(nb_shadow, (nb_x + 5, nb_y + 5))
            screen.blit(nb, (nb_x, nb_y))