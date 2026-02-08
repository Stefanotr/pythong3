from Utils.Logger import Logger
from Models.CaracterModel import CaracterModel
from Models.PlayerModel import PlayerModel


class BossModel(CaracterModel):

    def __init__(self, name, x=175, y=175):
        try:
            super().__init__(name, x, y, characterType="BOSS")
            Logger.debug("BossModel.__init__", f"Boss created: {name}")
        except Exception as e:
            Logger.error("BossModel.__init__", e)
            raise


    @classmethod
    def fromConfig(cls, bossConfig, x=175, y=175):
        try:
            bossName = bossConfig.get("name", "Unknown Boss")
            boss = cls(bossName, x, y)
            
            attributes = bossConfig.get("attributes", {})
            if attributes:
                health = attributes.get("base_health")
                damage = attributes.get("base_damage")
                accuracy = attributes.get("base_accuracy")
                
                if health is not None:
                    boss.setHealth(health)
                if damage is not None:
                    boss.setDamage(damage)
                if accuracy is not None:
                    boss.setAccuracy(accuracy)
                
                Logger.debug("BossModel.fromConfig", f"Boss config applied: {bossName}")
            
            return boss
        except Exception as e:
            Logger.error("BossModel.fromConfig", e)
            raise


    def scaleByPlayerLevel(self, player):
        try:
            if not isinstance(player, PlayerModel):
                raise TypeError("player must be PlayerModel")
            
            player_level = player.getLevel()
            if player_level <= 0:
                player_level = 1
            
            current_health = self.getHealth()
            current_damage = self.getDamage()
            
            scaled_health = current_health * player_level
            scaled_damage = current_damage * player_level
            
            self.setHealth(scaled_health)
            self.setDamage(scaled_damage)
            
            Logger.debug("BossModel.scaleByPlayerLevel", f"Scaled to level {player_level}")
                
        except Exception as e:
            Logger.error("BossModel.scaleByPlayerLevel", e)
