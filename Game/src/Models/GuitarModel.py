
        try:
            self._name = name
            self._base_damage = base_damage
            self._special_effect = special_effect
            self._effect_chance = effect_chance
            Logger.debug("GuitarModel.__init__", "Guitar model initialized", 
                       name=name, base_damage=base_damage, 
                       special_effect=special_effect, effect_chance=effect_chance)
        except Exception as e:
            Logger.error("GuitarModel.__init__", e)
            raise
        
    def getName(self):
        return self._name
    
    def setName(self, name):
        try:
            if not name:
                raise ValueError("Guitar name can't be NULL")
            self._name = name
        except Exception as e:
            Logger.error("GuitarModel.setName", e)
    
    def getBaseDamage(self):
        return self._base_damage
    
    def setBaseDamage(self, damage):
        try:
            if damage < 0:
                raise ValueError("Base damage can't be negative")
            self._base_damage = damage
        except Exception as e:
            Logger.error("GuitarModel.setBaseDamage", e)
    
    def getSpecialEffect(self):
        return self._special_effect
    
    def setSpecialEffect(self, effect):
        self._special_effect = effect
    
    def getEffectChance(self):
        return self._effect_chance
    
    def setEffectChance(self, chance):
        try:
            if not 0 <= chance <= 100:
                raise ValueError("Effect chance must be between 0 and 100")
            self._effect_chance = chance
        except Exception as e:
            Logger.error("GuitarModel.setEffectChance", e)
    
    def getDescription(self):
        try:
            desc = f"{self._name} (Dégâts: {self._base_damage})"
            if self._special_effect:
                desc += f"\nEffet spécial: {self._special_effect} ({self._effect_chance}% chance)"
            return desc
        except Exception as e:
            Logger.error("GuitarModel.getDescription", e)
            return "Unknown Guitar"

class GuitarFactory:
    
    @staticmethod
    def createLaPelle():
        try:
            guitar = GuitarModel("La Pelle", 5)
            Logger.debug("GuitarFactory.createLaPelle", "La Pelle created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createLaPelle", e)
            raise
    
    @staticmethod
    def createElectroChoc():
        try:
            guitar = GuitarModel("L'Électro-Choc", 12, "paralyze", 25)
            Logger.debug("GuitarFactory.createElectroChoc", "L'Électro-Choc created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createElectroChoc", e)
            raise
    
    @staticmethod
    def createHacheDeGuerre():
        try:
            guitar = GuitarModel("La Hache de Guerre", 20, "bleed", 40)
            Logger.debug("GuitarFactory.createHacheDeGuerre", "La Hache de Guerre created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createHacheDeGuerre", e)
            raise
    
    @staticmethod
    def createGuitareGonflable():
        try:
            guitar = GuitarModel("Guitare Gonflable", 3)
            Logger.debug("GuitarFactory.createGuitareGonflable", "Guitare Gonflable created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createGuitareGonflable", e)
            raise