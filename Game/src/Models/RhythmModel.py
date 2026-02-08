class RhythmModel:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.total_hits = 0
        
        self.crowd_satisfaction = 50 
        
        self.cash_earned = 0
        
        self.feedback = ""
        self.feedback_timer = 0
        
        self.hit_line_y = 0 
        
        self.lanes = ["LANE1", "LANE2", "LANE3", "LANE4"]
        
        self.notes = []

    def get_crowd_status(self):
        if self.crowd_satisfaction >= 80:
            return "EN FEU 🔥"
        elif self.crowd_satisfaction >= 50:
            return "CONTENT 🙂"
        elif self.crowd_satisfaction >= 20:
            return "ENNUYÉ 😐"
        else:
            return "EN COLÈRE 🤬"

    def reset(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.total_hits = 0
        self.crowd_satisfaction = 50
        self.cash_earned = 0
        self.feedback = ""
        for note in self.notes:
            note["active"] = True