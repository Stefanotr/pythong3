from Utils.Logger import Logger


class GuitarModel:

    def __init__(self, name, base_damage, specialEffect=None, effectChance=0):
        try:
            self._name = name
            self._base_damage = base_damage
            self._specialEffect = specialEffect
            self._effectChance = effectChance
            Logger.debug("GuitarModel.__init__", f"Guitar created: {name}")
        except Exception as e:
            Logger.error("GuitarModel.__init__", e)
            raise

        
    def getName(self):
        return self._name

    def setName(self, name):
        try:
            if not name:
                raise ValueError("Name cannot be empty")
            self._name = name
        except Exception as e:
            Logger.error("GuitarModel.setName", e)

    
    def getBaseDamage(self):
        return self._base_damage

    def setBaseDamage(self, damage):
        try:
            if damage < 0:
                raise ValueError("Base damage cannot be negative")
            self._base_damage = damage
        except Exception as e:
            Logger.error("GuitarModel.setBaseDamage", e)

    
    def getSpecialEffect(self):
        return self._specialEffect

    def setSpecialEffect(self, effect):
        self._specialEffect = effect

    
    def getEffectChance(self):
        return self._effectChance

    def setEffectChance(self, chance):
        try:
            if not 0 <= chance <= 100:
                raise ValueError("Effect chance must be 0-100")
            self._effectChance = chance
        except Exception as e:
            Logger.error("GuitarModel.setEffectChance", e)

    
    def getDescription(self):
        try:
            desc = f"{self._name} (Damage: +{self._base_damage})"
            if self._specialEffect:
                desc += f" | Effect: {self._specialEffect} ({self._effectChance}%)"
            return desc
        except Exception as e:
            Logger.error("GuitarModel.getDescription", e)
            return "Unknown Guitar"
class GuitarFactory:
    
    
    
    def createLaPelle():
        
        try:
            guitar = GuitarModel("La Pelle", 5)
            Logger.debug("GuitarFactory.createLaPelle", "La Pelle created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createLaPelle", e)
            raise
    
   
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