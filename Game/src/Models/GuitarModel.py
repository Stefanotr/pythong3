"""
GuitarModel Module

Represents guitar weapons in the game.
Manages guitar properties like base damage, special effects, and effect chances.
"""

from Utils.Logger import Logger


# === GUITAR MODEL CLASS ===

class GuitarModel:
    """
    Model for guitar weapons in the game.
    Tracks base damage, special effects (paralyze, bleed, stun), and effect probabilities.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name, base_damage, special_effect=None, effect_chance=0):
        """
        Initialize the guitar model.
        
        Args:
            name: Guitar name
            base_damage: Base damage value
            special_effect: Special effect type ("paralyze", "bleed", "stun") or None
            effect_chance: Probability of special effect (0-100)
        """
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
        self._name = name
        self._base_damage = base_damage
        self._special_effect = special_effect  # "paralyze", "bleed", "stun"
        self._effect_chance = effect_chance  # Effect probability (0-100)
        
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
        """
        Get a description of the guitar.
        
        Returns:
            str: Formatted description string
        """
        try:
            desc = f"{self._name} (Dégâts: {self._base_damage})"
            if self._special_effect:
                desc += f"\nEffet spécial: {self._special_effect} ({self._effect_chance}% chance)"
            return desc
        except Exception as e:
            Logger.error("GuitarModel.getDescription", e)
            return "Unknown Guitar"


# === GUITAR FACTORY CLASS ===

class GuitarFactory:
    """
    Factory class for creating predefined guitars in the game.
    Provides static methods to create different guitar types.
    """
    
    @staticmethod
    def create_la_pelle():
        """
        Create the starting guitar - La Pelle.
        
        Returns:
            GuitarModel: Starting guitar instance
        """
        try:
            guitar = GuitarModel("La Pelle", 5)
            Logger.debug("GuitarFactory.create_la_pelle", "La Pelle created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.create_la_pelle", e)
            raise
    
    @staticmethod
    def create_electro_choc():
        """
        Create the electric guitar - L'Électro-Choc.
        
        Returns:
            GuitarModel: Electric guitar instance with paralyze effect
        """
        try:
            guitar = GuitarModel("L'Électro-Choc", 12, "paralyze", 25)
            Logger.debug("GuitarFactory.create_electro_choc", "L'Électro-Choc created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.create_electro_choc", e)
            raise
    
    @staticmethod
    def create_hache_de_guerre():
        """
        Create the ultimate guitar - La Hache de Guerre.
        
        Returns:
            GuitarModel: Ultimate guitar instance with bleed effect
        """
        try:
            guitar = GuitarModel("La Hache de Guerre", 20, "bleed", 40)
            Logger.debug("GuitarFactory.create_hache_de_guerre", "La Hache de Guerre created")
            return guitar
        except Exception as e:
            Logger.error("GuitarFactory.create_hache_de_guerre", e)
            raise