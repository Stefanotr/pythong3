from Utils.Logger import Logger


class BottleModel:

    def __init__(self, name, alcoholLevel=30, bonusDamage=0, accuracyPenalty=0):
        try:
            self._name = name
            self._accuracyPenalty = accuracyPenalty
            self._bonusDamage = bonusDamage
            self._alcoholLevel = alcoholLevel
            
            Logger.debug("BottleModel.__init__", f"Bottle created: {name}")
        except Exception as e:
            Logger.error("BottleModel.__init__", e)
            raise


    def getName(self):
        try:
            return self._name
        except Exception as e:
            Logger.error("BottleModel.getName", e)
            return ""

    def setName(self, name):
        try:
            if not name:
                raise ValueError("Name cannot be empty")
            self._name = name
            Logger.debug("BottleModel.setName", f"Name set: {name}")
        except Exception as e:
            Logger.error("BottleModel.setName", e)


    def getAlcoholLevel(self):
        try:
            return self._alcoholLevel
        except Exception as e:
            Logger.error("BottleModel.getAlcoholLevel", e)
            return 0

    def setAlcoholLevel(self, alcoholLevel):
        try:
            if alcoholLevel < 0:
                raise ValueError("Alcohol level cannot be negative")
            self._alcoholLevel = alcoholLevel
            Logger.debug("BottleModel.setAlcoholLevel", f"Level set: {alcoholLevel}%")
        except Exception as e:
            Logger.error("BottleModel.setAlcoholLevel", e)


    def getBonusDamage(self):
        try:
            return self._bonusDamage
        except Exception as e:
            Logger.error("BottleModel.getBonusDamage", e)
            return 0

    def setBonusDamage(self, bonusDamage):
        try:
            self._bonusDamage = bonusDamage
            Logger.debug("BottleModel.setBonusDamage", f"Damage bonus: +{bonusDamage}")
        except Exception as e:
            Logger.error("BottleModel.setBonusDamage", e)


    def getAccuracyPenalty(self):
        try:
            return self._accuracyPenalty
        except Exception as e:
            Logger.error("BottleModel.getAccuracyPenalty", e)
            return 0.0

    def setAccuracyPenalty(self, accuracyPenalty):
        try:
            self._accuracyPenalty = accuracyPenalty
            Logger.debug("BottleModel.setAccuracyPenalty", f"Penalty: -{accuracyPenalty}%")
        except Exception as e:
            Logger.error("BottleModel.setAccuracyPenalty", e)

