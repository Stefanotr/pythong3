from Utils.Logger import Logger

class CaracterModel:
    def __init__(self, name, x=175, y=175, type="PNJ"):

        #Types possible: PNJ, SBIRE, BOSS, PLAYER (we can add more if needed)
        self._type=type
        self._name = name
        self._health = 100
        self._damage=5
        self._alcohol_level = 0
        self._x = x
        self._y = y
    
    def getType(self):
        return self._type
    
    def setType(self, type):
        self._type = type

    def getX(self):
        return self._x
    
    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y
    
    def setY(self, y):
        self._y = y

    def getHealth(self):
        return self._health
    
    def setHealth(self, health):
        self._health = health

    def getDamage(self):
        return self._damage
    
    def setDamage(self, damage):
        try:
            
            if damage < 0:
                raise ValueError
        except ValueError:
            print("Damage ne peut pas être négatif")

        self._damage = damage
        

    def getAlcoholLevel(self):
        return self._alcohol_level

    def setAlcoholLevel(self, alcohol_level):
        
        try:
            if self.getType() != "PLAYER":
                raise TypeError
        except TypeError:
            print("Error.setAlcoholLevel.CaracterModel :Caracter is not PLAYER")
        
        if alcohol_level > 100:
            self._alcohol_level = 100
        elif alcohol_level < 0:
            self._alcohol_level = 0
        else:
            self._alcohol_level = alcohol_level



    def scale(self, player_level):

        try:
            if self.getType() != "BOSS":
                raise TypeError
        except TypeError:
            print("Error.scale.CaracterModel :Caracter is not BOSS")

        scaled_boss_health=self.getHealth()*player_level
        scaled_boss_damage=self.getDamage()*player_level

        self.setHealth(scaled_boss_health)
        self.setDamage(scaled_boss_damage)