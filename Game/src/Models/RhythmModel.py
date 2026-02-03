"""
RhythmModel Module

Manages rhythm game state including notes, score, combo, and feedback.
Tracks note positions, hit detection, and game progression.
"""

from Utils.Logger import Logger


# === RHYTHM MODEL CLASS ===

class RhythmModel:
    """
    Model for rhythm game state.
    Manages notes, scoring, combo system, and feedback messages.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self):
        """
        Initialize the rhythm model with default values.
        Sets up score, combo, feedback, and initial note patterns.
        """
        try:
            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.feedback = ""
            self.feedback_timer = 0
            
            self.hit_line_y = 500  # Will be adjusted in the controller
            
            # 4 guitar strings/lanes
            self.lanes = ["LANE1", "LANE2", "LANE3", "LANE4"]
            
            # Initial note pattern
            self.notes = [
                {"lane": "LANE1", "y": 0, "active": True},
                {"lane": "LANE3", "y": -80, "active": True},
                {"lane": "LANE2", "y": -160, "active": True},
                {"lane": "LANE4", "y": -240, "active": True},
                {"lane": "LANE1", "y": -320, "active": True},
                {"lane": "LANE2", "y": -400, "active": True},
                {"lane": "LANE3", "y": -480, "active": True},
                {"lane": "LANE4", "y": -560, "active": True},
                {"lane": "LANE1", "y": -640, "active": True},
                {"lane": "LANE4", "y": -720, "active": True},
                {"lane": "LANE2", "y": -800, "active": True},
                {"lane": "LANE3", "y": -880, "active": True},
            ]
            Logger.debug("RhythmModel.__init__", "Rhythm model initialized", 
                        initial_notes=len(self.notes))
        except Exception as e:
            Logger.error("RhythmModel.__init__", e)
            raise