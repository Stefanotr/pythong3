from Utils.Logger import Logger


class GuitarModel:

    def __init__(self, name, baseDamage, specialEffect=None, effectChance=0):
        try:
            self._name = name
            self._baseDamage = baseDamage
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
        return self._baseDamage

    def setBaseDamage(self, damage):
        try:
            if damage < 0:
                raise ValueError("Base damage cannot be negative")
            self._baseDamage = damage
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
            desc = f"{self._name} (Damage: +{self._baseDamage})"
            if self._specialEffect:
                desc += f" | Effect: {self._specialEffect} ({self._effectChance}%)"
            return desc
        except Exception as e:
            Logger.error("GuitarModel.getDescription", e)
            return "Unknown Guitar"
class GuitarFactory:
    """
    Factory class for creating predefined guitars in the game.
    Provides static methods to create different guitar types.
    """
    
    @staticmethod
    def createLaPelle():
        """
        Create the starting guitar - La Pelle.
        
        Returns:
            GuitarModel: Starting guitar instance
        """
        try:
            guitar = GuitarModel("La Pelle", 5)
            Logger.debug("GuitarFactory.createLaPelle", "La Pelle created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createLaPelle", e)
            raise
    
    @staticmethod
    def createElectroChoc():
        """
        Create the electric guitar - L'Électro-Choc.
        
        Returns:
            GuitarModel: Electric guitar instance with paralyze effect
        """
        try:
            guitar = GuitarModel("L'Électro-Choc", 12, "paralyze", 25)
            Logger.debug("GuitarFactory.createElectroChoc", "L'Électro-Choc created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createElectroChoc", e)
            raise
    
    @staticmethod
    def createHacheDeGuerre():
        """
        Create the ultimate guitar - La Hache de Guerre.
        
        Returns:
            GuitarModel: Ultimate guitar instance with bleed effect
        """
        try:
            guitar = GuitarModel("La Hache de Guerre", 20, "bleed", 40)
            Logger.debug("GuitarFactory.createHacheDeGuerre", "La Hache de Guerre created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createHacheDeGuerre", e)
            raise
    
    @staticmethod
    def createGuitareGonflable():
        """
        Create the inflatable guitar - Guitare Gonflable.
        Found on the ground in Act 2, weaker than La Pelle.
        
        Returns:
            GuitarModel: Inflatable guitar instance with lower damage
        """
        try:
            guitar = GuitarModel("Guitare Gonflable", 3)
            Logger.debug("GuitarFactory.createGuitareGonflable", "Guitare Gonflable created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.createGuitareGonflable", e)
            raise