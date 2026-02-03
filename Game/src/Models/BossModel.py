from Utils.Logger import Logger
from Models.CaracterModel import CaracterModel
from Models.PlayerModel import PlayerModel

class BossModel(CaracterModel):

    def __init__(self, name, x=175, y=175):
        super().__init__(name ,x, y)
    

    def scale(self, player):

        try:
            if not isinstance(player, PlayerModel):
                raise TypeError("Caracter is not BOSS")
        except Exception as e:
            Logger.error("CaracterModel.scale",e)

        scaled_boss_health=self.getHealth()*player.getLevel()
        scaled_boss_damage=self.getDamage()*player.getLevel()

        self.setHealth(scaled_boss_health)
        self.setDamage(scaled_boss_damage)