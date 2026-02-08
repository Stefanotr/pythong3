

from enum import Enum
from Utils.Logger import Logger


class GameStage(Enum):
    RHYTHM_PAGE_1 = 1
    MAP_1 = 2
    ACT_1 = 3
    MAP_2 = 4
    ACT_2 = 5
    RHYTHM_PAGE_2 = 6
    MAP_3 = 7
    RHYTHM_COMBAT = 8


class GameSequenceController:

    
    def __init__(self):
        self.current_stage = GameStage.RHYTHM_PAGE_1.value
        self.player = None
        self.boss = None
        self.is_admin = False  
        Logger.debug("GameSequenceController.__init__", "Game sequence controller created")
    

    def set_player(self, player):
 
        self.player = player
        Logger.debug("GameSequenceController.set_player", "Player set in sequence controller", 
                   name=player.getName() if player else None)




    def get_player(self):
        return self.player
    


    def set_boss(self, boss):
    
        self.boss = boss
        Logger.debug("GameSequenceController.set_boss", "Boss set in sequence controller", 
                   name=boss.getName() if boss else None)
    


    def get_boss(self):
      
        return self.boss
    


    def get_current_stage(self):
        return self.current_stage
    

    def get_current_stage_name(self):
        stage_names = {
            1: "Rhythm Page",
            2: "Map",
            3: "Act 1",
            4: "Map",
            5: "Act 2",
            6: "Rhythm Page",
            7: "Map",
            8: "Rhythm Combat"
        }
        return stage_names.get(self.current_stage, "Unknown Stage")
    

    def set_stage(self, stage_number):
        
        if 1 <= stage_number <= 8:
            old_stage = self.current_stage
            self.current_stage = stage_number
            Logger.debug("GameSequenceController.set_stage", "Stage changed", 
                       from_stage=old_stage, to_stage=stage_number,
                       stage_name=self.get_current_stage_name())
            return True
        else:
            Logger.debug("GameSequenceController.set_stage", "Invalid stage number", 
                       requested_stage=stage_number)
            return False
    
    def advance_stage(self):
       
        if self.current_stage < 8:
            self.set_stage(self.current_stage + 1)
            return True
        else:
            Logger.debug("GameSequenceController.advance_stage", "Already at final stage")
            return False
    

    
    def get_next_view(self):
       

        stage_config = {
            1: {"view_type": "RhythmPageView"},
            2: {"view_type": "MapPageView", "map_act": 1},
            3: {"view_type": "Act1View"},
            4: {"view_type": "MapPageView", "map_act": 2},
            5: {"view_type": "Act2View"},
            6: {"view_type": "RhythmPageView"},
            7: {"view_type": "MapPageView", "map_act": 3},
            8: {"view_type": "RhythmCombatView"}
        }
        return stage_config.get(self.current_stage, {"view_type": "Unknown"})
    
    def is_last_stage(self):
        
        return self.current_stage == 8
    


    
    def handle_numeric_input(self, key_number):
        
       
        if not self.is_admin:
            Logger.debug("GameSequenceController.handle_numeric_input", "Stage navigation blocked: admin only")
            return False
        
        if 1 <= key_number <= 8:
            self.set_stage(key_number)
            Logger.debug("GameSequenceController.handle_numeric_input", "Stage jumped (ADMIN)", stage=key_number)
            return True
        return False
