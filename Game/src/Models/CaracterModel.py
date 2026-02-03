from Utils.Logger import Logger
from Models.BottleModel import BottleModel
import random
class CaracterModel:
    def __init__(self, name, x=175, y=175, type="PNJ"):

        #Types possible: PNJ, SBIRE, BOSS, PLAYER (we can add more if needed)
        self._type=type
        self._name = name
        self._health = 100
        self._damage=5
        self._accuracy=1
        self._drunkenness = 0
        self._x = x
        self._y = y
        self._coma_risk = 0
        self._selected_bottle=""
        
    
    def getType(self):
        return self._type
    
    def setType(self, type):
        self._type = type

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

    def getDrunkenness(self):
        return self._drunkenness

    def setDrunkenness(self, drunkenness):
        
        try:
            if self.getType() != "PLAYER":
                raise TypeError("Caracter is not PLAYER")
        except Exception as e:
            Logger.error("CaracterModel.setDrunkenness",e)
        
        if drunkenness > 100:
            self._drunkenness = 100
        elif drunkenness < 0:
            self._drunkenness = 0
        else:
            self._drunkenness = drunkenness
    
    def getComaRisk(self):
        return self._coma_risk

    def setComaRisk(self, coma_risk):
        try:
            if not 0 <= coma_risk <= 100:
                raise ValueError("coma_risk need to be between 0 and 100")
            self._coma_risk = coma_risk
        except Exception as e:
            Logger.error("BottleModel.setRisqueComa",e)

    def getSelectedBottle(self):
        return self._selected_bottle
    
    def setSelectedBottle(self, selected_bottle):
        try:
            if not isinstance(selected_bottle, BottleModel):
                raise TypeError("selected_bottle is not a BottleModel")
            self._selected_bottle = selected_bottle
        except Exception as e:
            Logger.error("CaracterModel.setSelectedBottle",e)







    def scale(self, player_level):

        try:
            if self.getType() != "BOSS":
                raise TypeError("Caracter is not BOSS")
        except Exception as e:
            Logger.error("CaracterModel.scale",e)

        scaled_boss_health=self.getHealth()*player_level
        scaled_boss_damage=self.getDamage()*player_level

        self.setHealth(scaled_boss_health)
        self.setDamage(scaled_boss_damage)


    def drink(self, selected_bottle):

        Logger.debug("CaracterModel.drink",selected_bottle)

        try:
            if self.getType() != "PLAYER":
                raise TypeError("Caracter is not PLAYER")
            try:
                if not isinstance(selected_bottle, BottleModel):
                    raise TypeError("selected_bottle is not a BottleModel")
            except Exception as e:
                Logger.error("CaracterModel.drink",e)

        except Exception as e:
            Logger.error("CaracterModel.drink",e)
            

        Logger.debug("CaracterModel.drink",f"{self.getName()} drink {selected_bottle.getName()}")

        
        self.setDrunkenness(self.getDrunkenness() + selected_bottle.getAlcoholLevel())

        if self.getDrunkenness() > 100:
            self.setDrunkenness(100)

        
        self.setDamage(self.getDamage() + selected_bottle.getBonusDamage())
        self.setAccuracy(self.getAccuracy() - selected_bottle.getAccuracyPenalty())

    
        tirage = random.randint(1, 100)

        if tirage <= self.getComaRisk():
            print("ALCOHOLIC COMA !")
            self.setHealth(0)
