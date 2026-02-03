class RhythmModel:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.feedback = ""
        self.feedback_timer = 0
        
        self.hit_line_y = 500  # Sera ajusté dans le contrôleur
        
        # 4 cordes
        self.lanes = ["LANE1", "LANE2", "LANE3", "LANE4"]
        
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