from Utils.Logger import Logger

class GuitarModel:
    """
    Modèle pour les guitares (armes du jeu)
    """
    def __init__(self, name, base_damage, special_effect=None, effect_chance=0):
        self._name = name
        self._base_damage = base_damage
        self._special_effect = special_effect  # "paralyze", "bleed", "stun"
        self._effect_chance = effect_chance  # Probabilité de l'effet (0-100)
        
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
        """Retourne une description de la guitare"""
        desc = f"{self._name} (Dégâts: {self._base_damage})"
        if self._special_effect:
            desc += f"\nEffet spécial: {self._special_effect} ({self._effect_chance}% chance)"
        return desc


# Guitares prédéfinies pour le jeu
class GuitarFactory:
    """Factory pour créer les différentes guitares du jeu"""
    
    @staticmethod
    def create_la_pelle():
        """Guitare de départ - La Pelle"""
        return GuitarModel("La Pelle", 5)
    
    @staticmethod
    def create_electro_choc():
        """Guitare électrique - L'Électro-Choc"""
        return GuitarModel("L'Électro-Choc", 12, "paralyze", 25)
    
    @staticmethod
    def create_hache_de_guerre():
        """Guitare ultime - La Hache de Guerre"""
        return GuitarModel("La Hache de Guerre", 20, "bleed", 40)