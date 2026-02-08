from Utils.Logger import Logger


class BottleModel:

    def __init__(self, name, alcohol_level=30, bonus_damage=0, accuracy_penalty=0):
        try:
            self._name = name
            self._accuracy_penalty = accuracy_penalty
            self._bonus_damage = bonus_damage
            self._alcohol_level = alcohol_level
            
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
            return self._alcohol_level
        except Exception as e:
            Logger.error("BottleModel.getAlcoholLevel", e)
            return 0

    def setAlcoholLevel(self, alcohol_level):
        try:
            if alcohol_level < 0:
                raise ValueError("Alcohol level cannot be negative")
            self._alcohol_level = alcohol_level
            Logger.debug("BottleModel.setAlcoholLevel", f"Level set: {alcohol_level}%")
        except Exception as e:
            Logger.error("BottleModel.setAlcoholLevel", e)


    def getBonusDamage(self):
        try:
            return self._bonus_damage
        except Exception as e:
            Logger.error("BottleModel.getBonusDamage", e)
            return 0

    def setBonusDamage(self, bonus_damage):
        try:
            self._bonus_damage = bonus_damage
            Logger.debug("BottleModel.setBonusDamage", f"Damage bonus: +{bonus_damage}")
        except Exception as e:
            Logger.error("BottleModel.setBonusDamage", e)


    def getAccuracyPenalty(self):
        try:
            return self._accuracy_penalty
        except Exception as e:
            Logger.error("BottleModel.getAccuracyPenalty", e)
            return 0.0

    def setAccuracyPenalty(self, accuracy_penalty):
        try:
            self._accuracy_penalty = accuracy_penalty
            Logger.debug("BottleModel.setAccuracyPenalty", f"Penalty: -{accuracy_penalty}%")
        except Exception as e:
            Logger.error("BottleModel.setAccuracyPenalty", e)

