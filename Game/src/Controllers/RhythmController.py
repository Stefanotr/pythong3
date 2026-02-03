"""
RhythmController Module

Handles rhythm game input and note timing.
Manages note movement, hit detection, scoring, and combo system.
"""

import pygame
from Utils.Logger import Logger


# === RHYTHM CONTROLLER CLASS ===

class RhythmController:
    """
    Controller for managing rhythm game mechanics.
    Handles note updates, input processing, hit detection, and scoring.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, rhythm_model, character_model, screen_height, view):
        """
        Initialize the rhythm controller.
        
        Args:
            rhythm_model: RhythmModel instance containing game state
            character_model: Character model for health updates
            screen_height: Screen height for adaptive speed calculation
            view: RhythmView instance for particle effects
        """
        try:
            self.rhythm = rhythm_model
            self.character = character_model
            self.view = view
            self.speed = screen_height * 0.006  # Adaptive speed
            
            # Adjust hit line based on screen height
            self.rhythm.hit_line_y = int(screen_height * 0.75)
            
            try:
                pygame.mixer.init()
                Logger.debug("RhythmController.__init__", "Pygame mixer initialized")
            except Exception as e:
                Logger.error("RhythmController.__init__", e)
            
            # Key mapping for the 4 guitar strings
            self.key_map = {
                pygame.K_c: "LANE1",
                pygame.K_v: "LANE2",
                pygame.K_b: "LANE3",
                pygame.K_n: "LANE4"
            }
            Logger.debug("RhythmController.__init__", "Rhythm controller initialized", speed=self.speed)
        except Exception as e:
            Logger.error("RhythmController.__init__", e)
            raise
        self.rhythm = rhythm_model
        self.character = character_model
        self.view = view
        self.speed = screen_height * 0.006  # Vitesse adaptative
        
        # Ajuster la ligne de frappe selon la hauteur d'écran
        self.rhythm.hit_line_y = int(screen_height * 0.75)
        
        pygame.mixer.init()
        
        # Touches C V B N pour les 4 cordes
        self.key_map = {
            pygame.K_c: "LANE1",
            pygame.K_v: "LANE2",
            pygame.K_b: "LANE3",
            pygame.K_n: "LANE4"
        }

    def update(self):
        # Décrémenter le timer du feedback
        if self.rhythm.feedback_timer > 0:
            self.rhythm.feedback_timer -= 1
        else:
            self.rhythm.feedback = ""
        
        # Mettre à jour les notes
        for note in self.rhythm.notes:
            if note["active"]:
                note["y"] += self.speed
            
            # Note manquée
            if note["y"] > self.rhythm.hit_line_y + 80 and note["active"]:
                note["active"] = False
                self.rhythm.feedback = "MISS!"
                self.rhythm.feedback_timer = 30
                self.rhythm.score = max(0, self.rhythm.score - 10)
                self.rhythm.combo = 0
                
                current_hp = self.character.getHealth()
                self.character.setHealth(max(0, current_hp - 2))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map:
                lane = self.key_map[event.key]
                self.check_hit(lane)

    def check_hit(self, lane):
        perfect_margin = 30
        good_margin = 50
        ok_margin = 75
        
        hit_found = False

        for note in self.rhythm.notes:
            if note["active"] and note["lane"] == lane:
                distance = abs(note["y"] - self.rhythm.hit_line_y)
                
                if distance < ok_margin:
                    note["active"] = False
                    hit_found = True
                    
                    # Position de la note pour les particules
                    lane_index = self.rhythm.lanes.index(lane)
                    x_pos = self.view.lane_x[lane_index]
                    color = self.view.lane_colors[lane_index]
                    
                    # Calculer le score selon la précision
                    if distance < perfect_margin:
                        points = 200
                        self.rhythm.feedback = "PERFECT!"
                        hp_gain = 4
                        self.view.create_particles(x_pos, self.rhythm.hit_line_y, color)
                    elif distance < good_margin:
                        points = 125
                        self.rhythm.feedback = "EXCELLENT!"
                        hp_gain = 3
                        self.view.create_particles(x_pos, self.rhythm.hit_line_y, color)
                    else:
                        points = 60
                        self.rhythm.feedback = "GOOD"
                        hp_gain = 1
                    
                    # Combo bonus
                    self.rhythm.combo += 1
                    if self.rhythm.combo > self.rhythm.max_combo:
                        self.rhythm.max_combo = self.rhythm.combo
                    
                    combo_multiplier = 1 + (self.rhythm.combo // 5) * 0.5
                    self.rhythm.score += int(points * combo_multiplier)
                    
                    self.rhythm.feedback_timer = 25
                    
                    # Gains de stats
                    hp = self.character.getHealth()
                    if hp < 100:
                        self.character.setHealth(min(100, hp + hp_gain))
                    
                    drunk = self.character.getDrunkenness()
                    self.character.setDrunkenness(min(100, drunk + 1))
                    
                    break
        
        if not hit_found:
            self.rhythm.feedback = "TROP TÔT!"
            self.rhythm.feedback_timer = 20
            self.rhythm.combo = 0
            self.rhythm.score = max(0, self.rhythm.score - 5)