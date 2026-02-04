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
    
    # === GETTERS / SETTERS ===
    
    def getScore(self):
        """
        Get the current score.
        
        Returns:
            int: Current score value
        """
        try:
            return self.score
        except Exception as e:
            Logger.error("RhythmModel.getScore", e)
            return 0
    
    def setScore(self, score):
        """
        Set the score value.
        
        Args:
            score: Score value to set
        """
        try:
            self.score = max(0, int(score))
            Logger.debug("RhythmModel.setScore", "Score set", score=self.score)
        except Exception as e:
            Logger.error("RhythmModel.setScore", e)
    
    def getCombo(self):
        """
        Get the current combo count.
        
        Returns:
            int: Current combo value
        """
        try:
            return self.combo
        except Exception as e:
            Logger.error("RhythmModel.getCombo", e)
            return 0
    
    def setCombo(self, combo):
        """
        Set the combo count.
        
        Args:
            combo: Combo value to set
        """
        try:
            self.combo = max(0, int(combo))
            # Update max combo if current combo exceeds it
            if self.combo > self.max_combo:
                self.setMaxCombo(self.combo)
            Logger.debug("RhythmModel.setCombo", "Combo set", combo=self.combo)
        except Exception as e:
            Logger.error("RhythmModel.setCombo", e)
    
    def getMaxCombo(self):
        """
        Get the maximum combo achieved.
        
        Returns:
            int: Maximum combo value
        """
        try:
            return self.max_combo
        except Exception as e:
            Logger.error("RhythmModel.getMaxCombo", e)
            return 0
    
    def setMaxCombo(self, max_combo):
        """
        Set the maximum combo value.
        
        Args:
            max_combo: Maximum combo value to set
        """
        try:
            self.max_combo = max(0, int(max_combo))
            Logger.debug("RhythmModel.setMaxCombo", "Max combo set", max_combo=self.max_combo)
        except Exception as e:
            Logger.error("RhythmModel.setMaxCombo", e)
    
    def getFeedback(self):
        """
        Get the current feedback message.
        
        Returns:
            str: Feedback message
        """
        try:
            return self.feedback
        except Exception as e:
            Logger.error("RhythmModel.getFeedback", e)
            return ""
    
    def setFeedback(self, feedback):
        """
        Set the feedback message.
        
        Args:
            feedback: Feedback message string
        """
        try:
            self.feedback = str(feedback) if feedback else ""
            Logger.debug("RhythmModel.setFeedback", "Feedback set", feedback=self.feedback)
        except Exception as e:
            Logger.error("RhythmModel.setFeedback", e)
    
    def getFeedbackTimer(self):
        """
        Get the feedback timer value.
        
        Returns:
            int: Feedback timer value
        """
        try:
            return self.feedback_timer
        except Exception as e:
            Logger.error("RhythmModel.getFeedbackTimer", e)
            return 0
    
    def setFeedbackTimer(self, timer):
        """
        Set the feedback timer value.
        
        Args:
            timer: Timer value to set
        """
        try:
            self.feedback_timer = max(0, int(timer))
            Logger.debug("RhythmModel.setFeedbackTimer", "Feedback timer set", timer=self.feedback_timer)
        except Exception as e:
            Logger.error("RhythmModel.setFeedbackTimer", e)
    
    def getHitLineY(self):
        """
        Get the Y position of the hit line.
        
        Returns:
            int: Y coordinate of hit line
        """
        try:
            return self.hit_line_y
        except Exception as e:
            Logger.error("RhythmModel.getHitLineY", e)
            return 500
    
    def setHitLineY(self, y):
        """
        Set the Y position of the hit line.
        
        Args:
            y: Y coordinate for hit line
        """
        try:
            self.hit_line_y = int(y)
            Logger.debug("RhythmModel.setHitLineY", "Hit line Y set", y=self.hit_line_y)
        except Exception as e:
            Logger.error("RhythmModel.setHitLineY", e)
    
    def getLanes(self):
        """
        Get the list of lane identifiers.
        
        Returns:
            list: List of lane strings
        """
        try:
            return self.lanes.copy()  # Return a copy to prevent external modification
        except Exception as e:
            Logger.error("RhythmModel.getLanes", e)
            return []
    
    def setLanes(self, lanes):
        """
        Set the list of lane identifiers.
        
        Args:
            lanes: List of lane strings
        """
        try:
            if isinstance(lanes, list):
                self.lanes = lanes.copy()  # Store a copy
                Logger.debug("RhythmModel.setLanes", "Lanes set", lanes=self.lanes)
            else:
                Logger.error("RhythmModel.setLanes", ValueError("Lanes must be a list"))
        except Exception as e:
            Logger.error("RhythmModel.setLanes", e)
    
    def getNotes(self):
        """
        Get the list of notes.
        
        Returns:
            list: List of note dictionaries
        """
        try:
            return self.notes.copy()  # Return a copy to prevent external modification
        except Exception as e:
            Logger.error("RhythmModel.getNotes", e)
            return []
    
    def setNotes(self, notes):
        """
        Set the list of notes.
        
        Args:
            notes: List of note dictionaries
        """
        try:
            if isinstance(notes, list):
                self.notes = notes.copy()  # Store a copy
                Logger.debug("RhythmModel.setNotes", "Notes set", note_count=len(self.notes))
            else:
                Logger.error("RhythmModel.setNotes", ValueError("Notes must be a list"))
        except Exception as e:
            Logger.error("RhythmModel.setNotes", e)