from Utils.Logger import Logger


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
        
        Logger.debug("RhythmModel.__init__", "Rhythm model initialized")

    def getCrowdStatus(self):
        try:
            if self.crowdSatisfaction >= 80:
                return "EN FEU 🔥"
            elif self.crowdSatisfaction >= 50:
                return "CONTENT 🙂"
            elif self.crowdSatisfaction >= 20:
                return "ENNUYÉ 😐"
            else:
                return "EN COLÈRE 🤬"
        except Exception as e:
            Logger.error("RhythmModel.getCrowdStatus", e)
            return "CONTENT 🙂"

    def reset(self):
        try:
            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.total_hits = 0
            self.crowd_satisfaction = 50
            self.cash_earned = 0
            self.feedback = ""
            
            for note in self.notes:
                note["active"] = True
            
            Logger.debug("RhythmModel.reset", "Rhythm model reset")
        except Exception as e:
            Logger.error("RhythmModel.reset", e)