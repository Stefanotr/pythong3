from Utils.Logger import Logger

class BottleModel:

    def __init__(self, name, alcohol_level=30, bonus_damage=0, accuracy_penalty=0):
        self._name = name
        self._accuracy_penalty = accuracy_penalty
        self._bonus_damage=bonus_damage
        self._alcohol_level=alcohol_level


    def getName(self):
        return self._name


    def setName(self, name):
        try:
            if not name:
                raise ValueError("Bottle name can't be NULL")
            self._name = name
        except Exception as e:
            Logger.error("BottleModel.setName",e)

  
    def getAlcoholLevel(self):
        return self._alcohol_level

    
    def setAlcoholLevel(self, alcohol_level):
        try:
            if alcohol_level < 0:
                raise ValueError("alcohol_level can't be negative")
            self._alcohol_level = alcohol_level
        except Exception as e:
            Logger.error("BottleModel.setAlcoholLevel",e)


    def getBonusDamage(self):
        return self._bonus_damage


    def setBonusDamage(self, bonus_damage):
        self._bonus_damage = bonus_damage


    def getAccuracyPenalty(self):
        return self._accuracy_penalty

    def setAccuracyPenalty(self, accuracy_penalty):
        self._accuracy_penalty = accuracy_penalty


    

        


    
        
