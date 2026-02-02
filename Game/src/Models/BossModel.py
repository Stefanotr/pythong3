import pygame

class BossModel():

    def __init__(self):

        self._health=100
        self._damage=5
        self._position_x=5
        self._position_y=5




    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            self._health = 0
        else:
            self._health = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if value < 0:
            raise ValueError("damage ne peut pas être négatif")
        self._damage = value
    
    @property
    def position_x(self):
        return self._position_x

    @position_x.setter
    def position_x(self, value):
        self._position_x = value

    @property
    def position_y(self):
        return self._position_y

    @position_y.setter
    def position_y(self, value):
        self._position_y = value



    
    def scale(self, player_level):

        scaled_boss_health=self.health()*player_level
        scaled_boss_damage=self.damage()*player_level

        self.health(scaled_boss_health)
        self.damage(scaled_boss_damage)



        


        