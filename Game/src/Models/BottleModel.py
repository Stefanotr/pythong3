
        try:
            self._name = name
            self._accuracy_penalty = accuracy_penalty
            self._bonus_damage = bonus_damage
            self._alcohol_level = alcohol_level
            Logger.debug("BottleModel.__init__", "Bottle model initialized", 
                        name=name, alcohol_level=alcohol_level, 
                        bonus_damage=bonus_damage, accuracy_penalty=accuracy_penalty)
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
                raise ValueError("Bottle name can't be NULL")
            self._name = name
            Logger.debug("BottleModel.setName", "Bottle name set", name=name)
        except ValueError as e:
            Logger.error("BottleModel.setName", e)
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
                raise ValueError("alcohol_level can't be negative")
            self._alcohol_level = alcohol_level
            Logger.debug("BottleModel.setAlcoholLevel", "Alcohol level set", alcohol_level=alcohol_level)
        except ValueError as e:
            Logger.error("BottleModel.setAlcoholLevel", e)
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
            Logger.debug("BottleModel.setBonusDamage", "Bonus damage set", bonus_damage=bonus_damage)
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
            Logger.debug("BottleModel.setAccuracyPenalty", "Accuracy penalty set", accuracy_penalty=accuracy_penalty)
        except Exception as e:
            Logger.error("BottleModel.setAccuracyPenalty", e)

    

        

    
        
