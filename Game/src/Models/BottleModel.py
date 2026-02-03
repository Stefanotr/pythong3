"""
BottleModel Module

Represents consumable bottles (alcoholic beverages) in the game.
Manages bottle properties like alcohol level, damage bonus, and accuracy penalty.
"""

from Utils.Logger import Logger


# === BOTTLE MODEL CLASS ===

class BottleModel:
    """
    Model for consumable bottles (alcoholic beverages).
    Tracks alcohol level, damage bonuses, and accuracy penalties.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name, alcohol_level=30, bonus_damage=0, accuracy_penalty=0):
        """
        Initialize the bottle model.
        
        Args:
            name: Bottle name
            alcohol_level: Alcohol content level (default: 30)
            bonus_damage: Damage bonus when consumed (default: 0)
            accuracy_penalty: Accuracy penalty when consumed (default: 0)
        """
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

    # === GETTERS / SETTERS ===
    
    def getName(self):
        """
        Get the bottle name.
        
        Returns:
            str: Bottle name
        """
        try:
            return self._name
        except Exception as e:
            Logger.error("BottleModel.getName", e)
            return ""

    def setName(self, name):
        """
        Set the bottle name.
        
        Args:
            name: Bottle name (cannot be empty)
        """
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
        """
        Get the alcohol level.
        
        Returns:
            int: Alcohol level value
        """
        try:
            return self._alcohol_level
        except Exception as e:
            Logger.error("BottleModel.getAlcoholLevel", e)
            return 0

    def setAlcoholLevel(self, alcohol_level):
        """
        Set the alcohol level.
        
        Args:
            alcohol_level: Alcohol level value (must be >= 0)
        """
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
        """
        Get the damage bonus.
        
        Returns:
            int: Damage bonus value
        """
        try:
            return self._bonus_damage
        except Exception as e:
            Logger.error("BottleModel.getBonusDamage", e)
            return 0

    def setBonusDamage(self, bonus_damage):
        """
        Set the damage bonus.
        
        Args:
            bonus_damage: Damage bonus value
        """
        try:
            self._bonus_damage = bonus_damage
            Logger.debug("BottleModel.setBonusDamage", "Bonus damage set", bonus_damage=bonus_damage)
        except Exception as e:
            Logger.error("BottleModel.setBonusDamage", e)

    def getAccuracyPenalty(self):
        """
        Get the accuracy penalty.
        
        Returns:
            float: Accuracy penalty value
        """
        try:
            return self._accuracy_penalty
        except Exception as e:
            Logger.error("BottleModel.getAccuracyPenalty", e)
            return 0.0

    def setAccuracyPenalty(self, accuracy_penalty):
        """
        Set the accuracy penalty.
        
        Args:
            accuracy_penalty: Accuracy penalty value
        """
        try:
            self._accuracy_penalty = accuracy_penalty
            Logger.debug("BottleModel.setAccuracyPenalty", "Accuracy penalty set", accuracy_penalty=accuracy_penalty)
        except Exception as e:
            Logger.error("BottleModel.setAccuracyPenalty", e)


    

        


    
        
