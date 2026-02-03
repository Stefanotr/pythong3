from Models.CaracterModel import CaracterModel
from Utils.Logger import Logger
from Models.BottleModel import BottleModel
import random

class PlayerModel(CaracterModel):

    def __init__(self, name, x=175, y=175):
        super().__init__(name, x, y)

        self._coma_risk = 0
        self._selected_bottle=""
        self._drunkenness = 0
        self._level=0

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
    
    def getDrunkenness(self):
        return self._drunkenness

    def setDrunkenness(self, drunkenness):
        
        if drunkenness > 100:
            self._drunkenness = 100
        elif drunkenness < 0:
            self._drunkenness = 0
        else:
            self._drunkenness = drunkenness
    
    def geLevel(self):
        return self._level

    def setLevel(self, level):
            self._level = level
    
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
