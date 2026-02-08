
        try:
            super().__init__(name, x, y)
            self._coma_risk = 0
            self._selected_bottle = ""
            self._drunkenness = 0
            self._level = 0
            
            from Models.InventoryModel import InventoryModel
            self.inventory = InventoryModel()
            
            default_beer = BottleModel("Beer", alcohol_level=15, bonus_damage=3, accuracy_penalty=5)
            self.inventory.add_item(default_beer)
            
            Logger.debug("PlayerModel.__init__", "Player model initialized", name=name, x=x, y=y)
        except Exception as e:
            Logger.error("PlayerModel.__init__", e)
            raise

    
    def getComaRisk(self):
        try:
            return self._coma_risk
        except Exception as e:
            Logger.error("PlayerModel.getComaRisk", e)
            return 0

    def setComaRisk(self, coma_risk):
        try:
            if not 0 <= coma_risk <= 100:
                raise ValueError("coma_risk need to be between 0 and 100")
            self._coma_risk = coma_risk
            Logger.debug("PlayerModel.setComaRisk", "Coma risk set", coma_risk=coma_risk)
        except ValueError as e:
            Logger.error("PlayerModel.setComaRisk", e)
        except Exception as e:
            Logger.error("PlayerModel.setComaRisk", e)

    def getSelectedBottle(self):
        try:
            return self._selected_bottle
        except Exception as e:
            Logger.error("PlayerModel.getSelectedBottle", e)
            return ""

    def setSelectedBottle(self, selected_bottle):
        try:
            if not isinstance(selected_bottle, BottleModel):
                raise TypeError("selected_bottle is not a BottleModel")
            self._selected_bottle = selected_bottle
            Logger.debug("PlayerModel.setSelectedBottle", "Bottle selected", bottle=selected_bottle.getName())
        except TypeError as e:
            Logger.error("PlayerModel.setSelectedBottle", e)
        except Exception as e:
            Logger.error("PlayerModel.setSelectedBottle", e)

    def getDrunkenness(self):
        try:
            return self._drunkenness
        except Exception as e:
            Logger.error("PlayerModel.getDrunkenness", e)
            return 0

    def setDrunkenness(self, drunkenness):
        try:
            if drunkenness > 100:
                self._drunkenness = 100
            elif drunkenness < 0:
                self._drunkenness = 0
            else:
                self._drunkenness = drunkenness
            Logger.debug("PlayerModel.setDrunkenness", "Drunkenness set", drunkenness=self._drunkenness)
        except Exception as e:
            Logger.error("PlayerModel.setDrunkenness", e)

    def getLevel(self):
        try:
            return self._level
        except Exception as e:
            Logger.error("PlayerModel.getLevel", e)
            return 0

    def setLevel(self, level):
        try:
            self._level = level
            Logger.debug("PlayerModel.setLevel", "Level set", level=level)
        except Exception as e:
            Logger.error("PlayerModel.setLevel", e)

    
    def drink(self, selected_bottle):
        try:
            Logger.debug("PlayerModel.drink", "Drinking bottle", bottle=selected_bottle.getName() if selected_bottle else "None")

            try:
                if hasattr(self, 'getType') and self.getType() != "PLAYER":
                    raise TypeError("Caracter is not PLAYER")
            except AttributeError:
                pass
            except Exception as e:
                Logger.error("PlayerModel.drink", e)
                return

            try:
                if not isinstance(selected_bottle, BottleModel):
                    raise TypeError("selected_bottle is not a BottleModel")
            except TypeError as e:
                Logger.error("PlayerModel.drink", e)
                return

            Logger.debug("PlayerModel.drink", f"{self.getName()} drinks {selected_bottle.getName()}")

            try:
                self.setDrunkenness(self.getDrunkenness() + selected_bottle.getAlcoholLevel())
                if self.getDrunkenness() > 100:
                    self.setDrunkenness(100)
            except Exception as e:
                Logger.error("PlayerModel.drink", e)

            try:
                self.setDamage(self.getDamage() + selected_bottle.getBonusDamage())
                penalty = selected_bottle.getAccuracyPenalty()
                try:
                    if penalty > 1:
                        penalty = penalty / 100.0
                except Exception:
                    pass
                new_accuracy = self.getAccuracy() - penalty
                self.setAccuracy(max(0.1, new_accuracy))
            except Exception as e:
                Logger.error("PlayerModel.drink", e)

            try:
                if self.getDrunkenness() >= 60:
                    tirage = random.randint(1, 100)
                    if tirage <= self.getComaRisk():
                        Logger.debug("PlayerModel.drink", "ALCOHOLIC COMA triggered", coma_risk=self.getComaRisk(), roll=tirage, drunkenness=self.getDrunkenness())
                        self.setHealth(0)
            except Exception as e:
                Logger.error("PlayerModel.drink", e)
                
        except Exception as e:
            Logger.error("PlayerModel.drink", e)

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
    
    def getLevel(self):
        return self._level

    def setLevel(self, level):
            self._level = level
    
    def drink(self, selected_bottle):

        Logger.debug("CaracterModel.drink",selected_bottle)

        try:
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
        penalty = selected_bottle.getAccuracyPenalty()
        try:
            if penalty > 1:
                penalty = penalty / 100.0
        except Exception:
            pass
        new_accuracy = self.getAccuracy() - penalty
        self.setAccuracy(max(0.1, new_accuracy))

    
        try:
            if self.getDrunkenness() >= 60:
                tirage = random.randint(1, 100)
                if tirage <= self.getComaRisk():
                    Logger.debug("PlayerModel.drink", "ALCOHOLIC COMA triggered", coma_risk=self.getComaRisk(), roll=tirage, drunkenness=self.getDrunkenness())
                    self.setHealth(0)
        except Exception as e:
            Logger.error("PlayerModel.drink", e)
