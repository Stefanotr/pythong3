from Models.CaracterModel import CaracterModel
from Utils.Logger import Logger
from Models.BottleModel import BottleModel
import random


class PlayerModel(CaracterModel):

    def __init__(self, name, x=175, y=175):
        try:
            super().__init__(name, x, y, characterType="PLAYER")
            self._level = 0
            
            from Models.InventoryModel import InventoryModel
            self.inventory = InventoryModel()
            
            defaultBeer = BottleModel("Beer", alcoholLevel=15, bonusDamage=3, accuracyPenalty=5)
            self.inventory.addItem(defaultBeer)
            
            Logger.debug("PlayerModel.__init__", f"Player initialized: {name}")
        except Exception as e:
            Logger.error("PlayerModel.__init__", e)
            raise


    def getLevel(self):
        try:
            return self._level
        except Exception as e:
            Logger.error("PlayerModel.getLevel", e)
            return 0

    def setLevel(self, level):
        try:
            self._level = level
            Logger.debug("PlayerModel.setLevel", f"Level set to {level}")
        except Exception as e:
            Logger.error("PlayerModel.setLevel", e)

    def addLevel(self, amount):
        self.setLevel(self._level + amount)


    def drinkBottle(self, selectedBottle):
        try:
            if not isinstance(selectedBottle, BottleModel):
                raise TypeError("selectedBottle is not a BottleModel")
            
            Logger.debug("PlayerModel.drinkBottle", f"{self.getName()} drinks {selectedBottle.getName()}")

            self.addDrunkenness(selectedBottle.getAlcoholLevel())

            self.addDamage(selectedBottle.getBonusDamage())
            
            penalty = selectedBottle.getAccuracyPenalty()
            if penalty > 1:
                penalty = penalty / 100.0
            newAccuracy = max(0.1, self.getAccuracy() - penalty)
            self.setAccuracy(newAccuracy)

            if self.getDrunkenness() >= 60:
                roll = random.randint(1, 100)
                if roll <= self.getComaRisk():
                    Logger.debug("PlayerModel.drinkBottle", f"COMA TRIGGERED at {roll}% risk")
                    self.setHealth(0)
                    
        except Exception as e:
            Logger.error("PlayerModel.drinkBottle", e)


    def getInventory(self):
        return self.inventory

    def setInventory(self, inventory):
        self.inventory = inventory
