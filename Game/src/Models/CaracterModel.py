from Utils.Logger import Logger

class CaracterModel:
    def __init__(self, name, x=175, y=175):

        #Types possible: PNJ, SBIRE, BOSS, PLAYER (we can add more if needed)

        self._name = name
        self._health = 100
        self._damage=5
        self._accuracy=1
        self._x = x
        self._y = y

    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name

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
                raise ValueError("Damage can't be negative")
            self._damage = damage

        except ValueError as e:
            Logger.error("CaracterModel.setDamage",e)

    def getAccuracy(self):
        return self._accuracy
    
    def setAccuracy(self, accuracy):
        try:
            
            if accuracy < 0:
                raise ValueError("Accuracy can't be negative")
            self._accuracy = accuracy
            
        except ValueError as e:
            Logger.error("CaracterModel.setAccuracy",e)


    def attack(caracter1,caracter2):

        caracter1.setHealth(caracter1.getHealth()-caracter2.getDamage())
