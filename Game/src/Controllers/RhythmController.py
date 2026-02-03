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

    # === UPDATE ===
    
    def update(self):
        """
        Update rhythm game state.
        Decrements feedback timer and updates note positions.
        """
        try:
            # Decrement feedback timer
            if self.rhythm.feedback_timer > 0:
                self.rhythm.feedback_timer -= 1
            else:
                self.rhythm.feedback = ""
            
            # Update notes
            try:
                for note in self.rhythm.notes:
                    if note.get("active", False):
                        try:
                            note["y"] += self.speed
                        except Exception as e:
                            Logger.error("RhythmController.update", e)
                            continue
                    
                    # Missed note
                    try:
                        if note.get("y", 0) > self.rhythm.hit_line_y + 80 and note.get("active", False):
                            note["active"] = False
                            self.rhythm.feedback = "MISS!"
                            self.rhythm.feedback_timer = 30
                            self.rhythm.score = max(0, self.rhythm.score - 10)
                            self.rhythm.combo = 0
                            
                            try:
                                current_hp = self.character.getHealth()
                                self.character.setHealth(max(0, current_hp - 2))
                                Logger.debug("RhythmController.update", "Note missed, player took damage")
                            except Exception as e:
                                Logger.error("RhythmController.update", e)
                    except Exception as e:
                        Logger.error("RhythmController.update", e)
                        continue
            except Exception as e:
                Logger.error("RhythmController.update", e)
        except Exception as e:
            Logger.error("RhythmController.update", e)

    # === INPUT HANDLING ===
    
    def handle_input(self, event):
        """
        Handle input events for rhythm game.
        
        Args:
            event: Pygame event object
        """
        try:
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_map:
                    try:
                        lane = self.key_map[event.key]
                        self.check_hit(lane)
                    except Exception as e:
                        Logger.error("RhythmController.handle_input", e)
        except Exception as e:
            Logger.error("RhythmController.handle_input", e)

    # === HIT DETECTION ===
    
    def check_hit(self, lane):
        """
        Check if a note was hit in the specified lane.
        Calculates score based on timing accuracy.
        
        Args:
            lane: Lane identifier (LANE1, LANE2, LANE3, LANE4)
        """
        try:
            perfect_margin = 30
            good_margin = 50
            ok_margin = 75
            
            hit_found = False

            for note in self.rhythm.notes:
                try:
                    if note.get("active", False) and note.get("lane") == lane:
                        distance = abs(note.get("y", 0) - self.rhythm.hit_line_y)
                        
                        if distance < ok_margin:
                            note["active"] = False
                            hit_found = True
                            
                            # Note position for particles
                            try:
                                lane_index = self.rhythm.lanes.index(lane)
                                x_pos = self.view.lane_x[lane_index]
                                color = self.view.lane_colors[lane_index]
                            except Exception as e:
                                Logger.error("RhythmController.check_hit", e)
                                x_pos = 0
                                color = (255, 255, 255)
                            
                            # Calculate score based on accuracy
                            try:
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
                                
                                Logger.debug("RhythmController.check_hit", "Note hit", 
                                           lane=lane, distance=distance, points=points)
                            except Exception as e:
                                Logger.error("RhythmController.check_hit", e)
                            
                            # Combo bonus
                            try:
                                self.rhythm.combo += 1
                                if self.rhythm.combo > self.rhythm.max_combo:
                                    self.rhythm.max_combo = self.rhythm.combo
                                
                                combo_multiplier = 1 + (self.rhythm.combo // 5) * 0.5
                                self.rhythm.score += int(points * combo_multiplier)
                                
                                self.rhythm.feedback_timer = 25
                            except Exception as e:
                                Logger.error("RhythmController.check_hit", e)
                            
                            # Stat gains
                            try:
                                hp = self.character.getHealth()
                                if hp < 100:
                                    self.character.setHealth(min(100, hp + hp_gain))
                                
                                drunk = self.character.getDrunkenness()
                                self.character.setDrunkenness(min(100, drunk + 1))
                            except Exception as e:
                                Logger.error("RhythmController.check_hit", e)
                            
                            break
                except Exception as e:
                    Logger.error("RhythmController.check_hit", e)
                    continue
            
            if not hit_found:
                self.rhythm.feedback = "TOO EARLY!"
                self.rhythm.feedback_timer = 20
                self.rhythm.combo = 0
                self.rhythm.score = max(0, self.rhythm.score - 5)
                Logger.debug("RhythmController.check_hit", "Hit too early", lane=lane)
        except Exception as e:
            Logger.error("RhythmController.check_hit", e)