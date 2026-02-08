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

    def setPlayer(self, player):
        self.player = player
        Logger.debug("GameSequenceController.setPlayer", "Player set in sequence controller",
                   name=player.getName() if player else None)

    def getPlayer(self):
        return self.player

    def setBoss(self, boss):
        self.boss = boss
        Logger.debug("GameSequenceController.setBoss", "Boss set in sequence controller",
                   name=boss.getName() if boss else None)

    def getBoss(self):
        return self.boss

    def getCurrentStage(self):
        return self.current_stage

    def getCurrentStageName(self):
        satge_names = {
            1: "Rhythm Page",
            2: "Map",
            3: "Act 1",
            4: "Map",
            5: "Act 2",
            6: "Rhythm Page",
            7: "Map",
            8: "Rhythm Combat"
        }
        return satge_names.get(self.current_stage, "Unknown Stage")

    def setStage(self, stage_number):
        if 1 <= stage_number <= 8:
            old_stage = self.current_stage
            self.current_stage = stage_number
            Logger.debug("GameSequenceController.setStage", "Stage changed",
                       from_stage=old_stage, to_stage=stage_number,
                       stage_name=self.getCurrentStageName())
            return True
        else:
            Logger.debug("GameSequenceController.setStage", "Invalid stage number",
                       requestedStage=stage_number)
            return False

    def advanceStage(self):
        if self.current_stage < 8:
            self.setStage(self.current_stage + 1)
            return True
        else:
            Logger.debug("GameSequenceController.advanceStage", "Already at final stage")
            return False

    def getNextView(self):
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

    def handleNumericInput(self, key_number):
        if not self.is_admin:
            Logger.debug("GameSequenceController.handleNumericInput", "Stage navigation blocked: admin only")
            return False

        if 1 <= key_number <= 8:
            self.setStage(key_number)
            Logger.debug("GameSequenceController.handleNumericInput", "Stage jumped (ADMIN)", stage=key_number)
            return True
        return False
