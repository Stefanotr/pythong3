"""
RhythmController Module

Handles rhythm game input and note timing.
Manages note movement, hit detection, scoring, and combo system.
"""

import pygame
from Utils.Logger import Logger
from Controllers import BaseController


# === RHYTHM CONTROLLER CLASS ===

class RhythmController(BaseController):
    """
    Controller for managing rhythm game mechanics.
    Handles note updates, input processing, hit detection, and scoring.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, rhythm_model, character_model, screen_height, view, boss_model=None):
        """
        Initialize the rhythm controller.
        
        Args:
            rhythm_model: RhythmModel instance containing game state
            character_model: Character model for health updates
            screen_height: Screen height for adaptive speed calculation
            view: RhythmView instance for particle effects
            boss_model: Optional boss model for attack simulation on missed notes
        """
        try:
            self.rhythm = rhythm_model
            self.character = character_model
            self.view = view
            self.speed = screen_height * 0.006  # Adaptive speed
            
            # Boss model for attack simulation
            self.boss = boss_model
            if self.boss is None:
                # Create default boss if none provided
                from Models.CaracterModel import CaracterModel
                self.boss = CaracterModel("Boss", 80, 80)
                self.boss.setDamage(8)  # Default boss damage
                Logger.debug("RhythmController.__init__", "Default boss created for rhythm game")
            else:
                Logger.debug("RhythmController.__init__", "Using provided boss model", 
                           boss_name=self.boss.getName(), boss_damage=self.boss.getDamage())
            
            # Adjust hit line based on screen height
            self.rhythm.setHitLineY(int(screen_height * 0.75))
            
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
            if self.rhythm.getFeedbackTimer() > 0:
                self.rhythm.setFeedbackTimer(self.rhythm.getFeedbackTimer() - 1)
            else:
                self.rhythm.setFeedback("")
            
            # Update notes
            try:
                for note in self.rhythm.getNotes():
                    if note.get("active", False):
                        try:
                            note["y"] += self.speed
                        except Exception as e:
                            Logger.error("RhythmController.update", e)
                            continue
                    
                    # Missed note - simulate boss attack
                    try:
                        if note.get("y", 0) > self.rhythm.getHitLineY() + 80 and note.get("active", False):
                            note["active"] = False
                            self.rhythm.setFeedback("MISS!")
                            self.rhythm.setFeedbackTimer(30)
                            self.rhythm.setScore(max(0, self.rhythm.getScore() - 10))
                            self.rhythm.setCombo(0)
                            
                            # Simulate boss attack instead of passive HP loss
                            try:
                                boss_damage = self.boss.getDamage()
                                current_hp = self.character.getHealth()
                                new_hp = max(0, current_hp - boss_damage)
                                self.character.setHealth(new_hp)
                                
                                # Update feedback to show boss attack
                                self.rhythm.setFeedback(f"{self.boss.getName()} attacks! -{boss_damage} HP!")
                                Logger.debug("RhythmController.update", "Note missed, boss attack simulated", 
                                           boss_name=self.boss.getName(), 
                                           damage=boss_damage, 
                                           player_hp=new_hp)
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
            if event.type == pygame.KEYDOWN and event.key in self.key_map:
                try:
                    lane = self.key_map[event.key]
                    self.checkHit(lane)
                except Exception as e:
                    Logger.error("RhythmController.handle_input", e)
        except Exception as e:
            Logger.error("RhythmController.handle_input", e)

    # Backwards compatible alias
    def handleInput(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handle_input(event)

    # === HIT DETECTION ===
    
    def checkHit(self, lane):
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

            for note in self.rhythm.getNotes():
                try:
                    if note.get("active", False) and note.get("lane") == lane:
                        distance = abs(note.get("y", 0) - self.rhythm.getHitLineY())
                        
                        if distance < ok_margin:
                            note["active"] = False
                            hit_found = True
                            
                            # Note position for particles
                            try:
                                lane_index = self.rhythm.getLanes().index(lane)
                                x_pos = self.view.lane_x[lane_index]
                                color = self.view.lane_colors[lane_index]
                            except Exception as e:
                                Logger.error("RhythmController.checkHit", e)
                                x_pos = 0
                                color = (255, 255, 255)
                            
                            # Calculate score based on accuracy
                            try:
                                if distance < perfect_margin:
                                    points = 200
                                    self.rhythm.setFeedback("PERFECT!")
                                    hp_gain = 4
                                    self.view.createParticles(x_pos, self.rhythm.getHitLineY(), color)
                                elif distance < good_margin:
                                    points = 125
                                    self.rhythm.setFeedback("EXCELLENT!")
                                    hp_gain = 3
                                    self.view.createParticles(x_pos, self.rhythm.getHitLineY(), color)
                                else:
                                    points = 60
                                    self.rhythm.setFeedback("GOOD")
                                    hp_gain = 1
                                
                                Logger.debug("RhythmController.checkHit", "Note hit", 
                                           lane=lane, distance=distance, points=points)
                            except Exception as e:
                                Logger.error("RhythmController.checkHit", e)
                            
                            # Combo bonus
                            try:
                                self.rhythm.setCombo(self.rhythm.getCombo() + 1)
                                if self.rhythm.getCombo() > self.rhythm.getMaxCombo():
                                    self.rhythm.setMaxCombo(self.rhythm.getCombo())
                                
                                combo_multiplier = 1 + (self.rhythm.getCombo() // 5) * 0.5
                                self.rhythm.setScore(self.rhythm.getScore() + int(points * combo_multiplier))
                                
                                self.rhythm.setFeedbackTimer(25)
                            except Exception as e:
                                Logger.error("RhythmController.checkHit", e)
                            
                            # Stat gains
                            try:
                                hp = self.character.getHealth()
                                if hp < 100:
                                    self.character.setHealth(min(100, hp + hp_gain))
                                
                                drunk = self.character.getDrunkenness()
                                self.character.setDrunkenness(min(100, drunk + 1))
                            except Exception as e:
                                Logger.error("RhythmController.checkHit", e)
                            
                            break
                except Exception as e:
                    Logger.error("RhythmController.checkHit", e)
                    continue
            
            if not hit_found:
                self.rhythm.setFeedback("TOO EARLY!")
                self.rhythm.setFeedbackTimer(20)
                self.rhythm.setCombo(0)
                self.rhythm.setScore(max(0, self.rhythm.getScore() - 5))
                Logger.debug("RhythmController.checkHit", "Hit too early", lane=lane)
        except Exception as e:
            Logger.error("RhythmController.checkHit", e)