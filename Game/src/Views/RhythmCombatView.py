import pygame
import math
from Views.CaracterView import CaracterView
from Utils.AssetManager import AssetManager

class RhythmCombatView:

    def __init__(self, screen_width, screen_height, boss_max_health=3000, player_max_health=100, background_image_path="Game/Assets/managerevade.png"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boss_max_health = boss_max_health  
        self.player_max_health = player_max_health  
        
        self.game_width = 1920  
        self.game_height = 1080  
        
        self.game_offset_x = (screen_width - self.game_width) // 2
        self.game_offset_y = (screen_height - self.game_height) // 2
        
        self.background_image = None
        self.overlay = None
        
        image_path = background_image_path
        try:
            loaded_img = pygame.image.load(image_path).convert()
            
            self.background_image = pygame.transform.scale(loaded_img, (screen_width, screen_height))
            self.overlay = pygame.Surface((screen_width, screen_height))
            self.overlay.fill((0, 0, 0))
            self.overlay.set_alpha(120)
        except FileNotFoundError:
            pass

        self.font = pygame.font.SysFont("Arial", int(self.game_height * 0.0158), bold=True)
        self.big_font = pygame.font.SysFont("Arial", int(self.game_height * 0.047), bold=True)
        self.combo_font = pygame.font.SysFont("Arial", int(self.game_height * 0.0315), bold=True)
        self.title_font = pygame.font.SysFont("Arial", int(self.game_height * 0.021), bold=True)
        self.huge_font = pygame.font.SysFont("Arial", int(self.game_height * 0.21), bold=True)
        
        try:
            asset_manager = AssetManager()
            player_config = asset_manager.loadPlayerConfig()
            print(f"[INFO] RhythmCombatView: Successfully loaded player_config with {len(player_config.get('actions', {}))} actions")
        except Exception as e:
            print(f"[ERROR] RhythmCombatView: Failed to load player_config: {e}")
            player_config = None
        
        self.player_view = CaracterView("Game/Assets/lola.png", baseName="lola", 
                                       spriteSize=(200, 200),
                                       characterConfig=player_config,
                                       gameMode="rhythmCombat")
        self.boss_view = None  
        
        self.lane_colors = [
            (255, 20, 147),   
            (0, 255, 255),    
            (50, 255, 50),    
            (255, 215, 0)     
        ]
        
        guitar_width = self.game_width * 0.4
        guitar_start = (self.game_width - guitar_width) / 2
        spacing = guitar_width / 5
        
        self.lane_x = [
            self.game_offset_x + int(guitar_start + spacing),
            self.game_offset_x + int(guitar_start + spacing * 2),
            self.game_offset_x + int(guitar_start + spacing * 3),
            self.game_offset_x + int(guitar_start + spacing * 4)
        ]
        
        self.guitar_start = self.game_offset_x + int(guitar_start)
        self.guitar_width = int(guitar_width)
        
        self.particles = []
        self.time = 0

    def createParticles(self, x, y, color):
        for _ in range(12):
            angle = pygame.math.Vector2(1, 0).rotate((_ * 30))
            self.particles.append({
                'x': x, 'y': y,
                'vx': angle.x * 4, 'vy': angle.y * 4,
                'life': 25, 'color': color
            })

    def updateParticles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def drawHealthBar(self, screen, x, y, width, height, current, maximum, label, is_player=True):

        ratio = current / maximum if maximum > 0 else 0
        
        if is_player:
            color_good = (50, 255, 50)   
            color_bad = (255, 50, 50)
        else:
            color_good = (255, 100, 255)  
            color_bad = (255, 50, 50)
        
        pygame.draw.rect(screen, (20, 20, 20), (x - 2, y - 2, width + 4, height + 4), borderRadius=8)
        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height), borderRadius=6)
        
        filled_width = int(width * ratio)
        if ratio > 0.5:
            color = color_good
        else:
            color = color_bad
            
        if filled_width > 0:
            pygame.draw.rect(screen, color, (x, y, filled_width, height), borderRadius=6)
        
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2, borderRadius=6)
        
        label_surf = self.font.render(label, True, (255, 255, 255))
        screen.blit(label_surf, (x, y - 20))
        
        hp_text = self.font.render(f"{int(current)}/{int(maximum)}", True, (255, 255, 255))
        screen.blit(hp_text, (x + width//2 - hp_text.get_width()//2, y + height//2 - hp_text.get_height()//2))

    def draw(self, screen, rhythm_model, player_model, boss_model, note_speed=0.5, countdown_val=0):

        self.time += 1
        
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
            screen.blit(self.overlay, (0, 0))
        else:
            for y in range(self.screen_height):
                shade = int(20 + y * 0.02)
                pygame.draw.line(screen, (shade, shade // 2, shade // 3), (0, y), (self.screen_width, y))
        
        guitar_rect = pygame.Rect(self.guitar_start - 15, self.game_offset_y, self.guitar_width + 30, self.game_height)
        guitar_surf = pygame.Surface((guitar_rect.width, guitar_rect.height), pygame.SRCALPHA)
        
        for i in range(guitar_rect.width):
            alpha = int(100 + (i / guitar_rect.width) * 50)
            pygame.draw.line(guitar_surf, (20, 20, 30, alpha), (i, 0), (i, guitar_rect.height))
        
        screen.blit(guitar_surf, guitar_rect)
        pygame.draw.rect(screen, (80, 120, 180), guitar_rect, 2, borderRadius=10)
        
        hit_line_y = rhythm_model.hit_line_y
        
        pygame.draw.line(screen, (200, 200, 200), 
                         (self.guitar_start - 15, hit_line_y), 
                         (self.guitar_start + self.guitar_width + 15, hit_line_y), 3)

        for i, x in enumerate(self.lane_x):
            color = self.lane_colors[i]
            
            pygame.draw.line(screen, (color[0]//3, color[1]//3, color[2]//3), (x, self.game_offset_y), (x, self.game_offset_y + self.game_height), 2)
            
            pygame.draw.circle(screen, (0, 0, 0), (x, hit_line_y), 32)
            pygame.draw.circle(screen, color, (x, hit_line_y), 30, 4)
            pygame.draw.circle(screen, (255, 255, 0), (x, hit_line_y), 18, 2)
            pygame.draw.circle(screen, (255, 255, 255), (x, hit_line_y), 5)
        
        for note in rhythm_model.notes:
            if note["active"]:
                lane_index = rhythm_model.lanes.index(note["lane"])
                x_pos = self.lane_x[lane_index]
                color = self.lane_colors[lane_index]
                y_pos = int(note["y"])
                
                duration = note.get("duration", 0)
                tail_len = 20 + int(note_speed * 10) 
                if duration > 0:
                    tail_len = int(duration * note_speed)

                tail_surf = pygame.Surface((14, tail_len), pygame.SRCALPHA)
                tail_surf.fill((*color, 150))
                screen.blit(tail_surf, (x_pos - 7, y_pos - tail_len))

                pygame.draw.circle(screen, (255, 255, 255), (x_pos, y_pos), 26)
                pygame.draw.circle(screen, color, (x_pos, y_pos), 22)
                pygame.draw.circle(screen, (0, 0, 0), (x_pos, y_pos), 10)
        
        for particle in self.particles:
            size = int(particle['life'] / 3)
            if size > 0:
                surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*particle['color'], 200), (size, size), size)
                screen.blit(surf, (particle['x']-size, particle['y']-size))
        self.updateParticles()
        
        hud_h = int(self.screen_height * 0.10)  
        hud_bg = pygame.Surface((self.screen_width, hud_h), pygame.SRCALPHA)
        hud_bg.fill((10, 10, 20, 220))
        screen.blit(hud_bg, (0, 0))
        pygame.draw.line(screen, (255, 50, 50), (0, hud_h), (self.screen_width, hud_h), 3)
        
        combat_title = self.title_font.render("COMBAT RHYTHM", True, (255, 215, 0))
        screen.blit(combat_title, (self.screen_width//2 - combat_title.get_width()//2, 5))
        
        try:
            level = player_model.getLevel() if hasattr(player_model, 'getLevel') else 1
            total_hits = getattr(rhythm_model, 'totalHits', 0)
            base_hit_cash = total_hits * 2  
            display_cash = base_hit_cash * (level + 1)
            cash_text = self.font.render(f"CASH: ${display_cash}", True, (100, 200, 255))
            screen.blit(cash_text, (self.screen_width//2 - cash_text.get_width()//2, int(hud_h * 0.5)))
        except Exception as e:
            pass
        
        try:
            current_player_health = player_model.getHealth()
            if current_player_health > self.player_max_health:
                
                self.player_max_health = current_player_health
        except Exception:
            pass
        
        player_hp_width = int(self.screen_width * 0.12)  
        player_hp_x = 30  
        self.drawHealthBar(
            screen, 
            player_hp_x, 
            int(hud_h * 0.5),
            player_hp_width,
            int(hud_h * 0.20),
            player_model.getHealth(),
            self.player_max_health,
            f"{player_model.getName()}",
            is_player=True
        )
        
        boss_hp_width = int(self.screen_width * 0.12)  
        boss_hp_x = self.screen_width - boss_hp_width - 30  
        
        boss_current_health = boss_model.getHealth()
        if boss_current_health != getattr(self, '_last_displayed_boss_health', None):
            from Utils.Logger import Logger
            Logger.debug("RhythmCombatView.draw", "Boss health display",
                        current_health=boss_current_health,
                        max_health=self.boss_max_health,
                        boss_name=boss_model.getName())
            self._last_displayed_boss_health = boss_current_health
        
        self.drawHealthBar(
            screen,
            boss_hp_x,
            int(hud_h * 0.5),
            boss_hp_width,
            int(hud_h * 0.20),
            boss_current_health,
            self.boss_max_health,  
            f"{boss_model.getName()}",
            is_player=False
        )
        
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
            
            if rhythm_model.combo > 1:
                combo_surf = self.combo_font.render(f"COMBO x{rhythm_model.combo}", True, (255, 100, 255))
                combo_shadow = self.combo_font.render(f"COMBO x{rhythm_model.combo}", True, (100, 0, 100))
                
                combo_x = self.screen_width//2 - combo_surf.get_width()//2
                combo_y = fb_y + 80
                
                screen.blit(combo_shadow, (combo_x + 2, combo_y + 2))
                screen.blit(combo_surf, (combo_x, combo_y))

        keys = ["C", "V", "B", "N"]
        for i, x in enumerate(self.lane_x):
            txt = self.title_font.render(keys[i], True, self.lane_colors[i])
            shadow = self.title_font.render(keys[i], True, (0, 0, 0))
            
            txt_x = x - txt.get_width()//2
            txt_y = self.screen_height - 40
            
            screen.blit(shadow, (txt_x + 2, txt_y + 2))
            screen.blit(txt, (txt_x, txt_y))
        
        try:
            
            player_x = int(self.screen_width * 0.25)  
            player_y = self.screen_height // 2  
            self.player_view.drawCaracter(screen, player_model, offset=(player_x, player_y), isMap=True)
            
            if self.boss_view is None and boss_model:
                
                boss_asset = "Game/Assets/ManagerCorrompu.png"
                boss_base_name = "manager"
                
                try:
                    asset_manager = AssetManager()
                    boss_config = asset_manager.getBossByBame("Manager Corrompu")
                    print(f"[INFO] RhythmCombatView: Successfully loaded boss_config for Manager Corrompu")
                except Exception as e:
                    print(f"[ERROR] RhythmCombatView: Failed to load boss_config: {e}")
                    boss_config = None
                
                self.boss_view = CaracterView(boss_asset, baseName=boss_base_name, 
                                             spriteSize=(200, 200),
                                             characterConfig=boss_config,
                                             gameMode="rhythmCombat")
            
            if self.boss_view:
                boss_x = int(self.screen_width * 0.75)  
                boss_y = self.screen_height // 2  
                self.boss_view.drawCaracter(screen, boss_model, offset=(boss_x, boss_y), isMap=True)
        except Exception as e:
            pass
        
        try:
            
            level = player_model.getLevel() if hasattr(player_model, 'getLevel') else 1
            level_text = self.font.render(f"LEVEL {level}", True, (100, 255, 100))
            screen.blit(level_text, (20, self.screen_height - 50))
            
            alcohol = player_model.getDrunkenness() if hasattr(player_model, 'getDrunkenness') else 0
            alcohol_color = (255, 100, 100) if alcohol > 60 else (100, 255, 100)
            alcohol_text = self.font.render(f"ALCOHOL: {alcohol}%", True, alcohol_color)
            screen.blit(alcohol_text, (self.screen_width - alcohol_text.get_width() - 20, self.screen_height - 50))
        except Exception as e:
            pass

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