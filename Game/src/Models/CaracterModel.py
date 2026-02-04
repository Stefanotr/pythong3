"""
CaracterModel Module

Base model class for all characters in the game (player, enemies, bosses, NPCs).
Provides common character properties like health, damage, accuracy, and position.
"""

from Utils.Logger import Logger


# === CHARACTER MODEL CLASS ===

class CaracterModel:
    """
    Base model class for all characters in the game.
    Possible types: PNJ, SBIRE, BOSS, PLAYER (can be extended as needed).
    Manages character stats, position, and basic combat functionality.
    """
    def __init__(self, name, x=175, y=175, type="PNJ"):

        #Types possible: PNJ, SBIRE, BOSS, PLAYER (we can add more if needed)
        self._type = type
        self._name = name
        self._health = 100
        self._damage=5
        self._accuracy=1
        self._x = x
        self._y = y
        self._drunkenness = 0
        self._coma_risk = 0
        self._selected_bottle = None

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type
       
    def getName(self):
        return self._name
    
    # === INITIALIZATION ===
    
    def __init__(self, name, x=175, y=175):
        """
        Initialize the character model.
        
        Args:
            name: Character name
            x: Initial X position (default: 175)
            y: Initial Y position (default: 175)
        """
        try:
            self._name = name
            self._health = 100
            self._damage = 5
            self._accuracy = 1
            self._x = x
            self._y = y
            Logger.debug("CaracterModel.__init__", "Character model initialized", name=name, x=x, y=y)
        except Exception as e:
            Logger.error("CaracterModel.__init__", e)
            raise

    # === GETTERS / SETTERS ===
    
    def getName(self):
        """
        Get the character name.
        
        Returns:
            str: Character name
        """
        try:
            return self._name
        except Exception as e:
            Logger.error("CaracterModel.getName", e)
            return ""

    def setName(self, name):
        """
        Set the character name.
        
        Args:
            name: Character name
        """
        try:
            self._name = name
            Logger.debug("CaracterModel.setName", "Character name set", name=name)
        except Exception as e:
            Logger.error("CaracterModel.setName", e)

    def getX(self):
        """
        Get the X position.
        
        Returns:
            int: X coordinate
        """
        try:
            return self._x
        except Exception as e:
            Logger.error("CaracterModel.getX", e)
            return 0

    def setX(self, x):
        """
        Set the X position.
        
        Args:
            x: X coordinate
        """
        try:
            self._x = x
            Logger.debug("CaracterModel.setX", "X position set", x=x)
        except Exception as e:
            Logger.error("CaracterModel.setX", e)

    def getY(self):
        """
        Get the Y position.
        
        Returns:
            int: Y coordinate
        """
        try:
            return self._y
        except Exception as e:
            Logger.error("CaracterModel.getY", e)
            return 0

    def setY(self, y):
        """
        Set the Y position.
        
        Args:
            y: Y coordinate
        """
        try:
            self._y = y
            Logger.debug("CaracterModel.setY", "Y position set", y=y)
        except Exception as e:
            Logger.error("CaracterModel.setY", e)

    def getHealth(self):
        """
        Get the current health.
        
        Returns:
            int: Current health value
        """
        try:
            return self._health
        except Exception as e:
            Logger.error("CaracterModel.getHealth", e)
            return 0

    def setHealth(self, health):
        """
        Set the health value.
        
        Args:
            health: Health value (can be negative, will be clamped in combat)
        """
        try:
            self._health = health
            Logger.debug("CaracterModel.setHealth", "Health set", health=health)
        except Exception as e:
            Logger.error("CaracterModel.setHealth", e)

    def getDamage(self):
        """
        Get the damage value.
        
        Returns:
            int: Damage value
        """
        try:
            return self._damage
        except Exception as e:
            Logger.error("CaracterModel.getDamage", e)
            return 0

    def setDamage(self, damage):
        """
        Set the damage value.
        
        Args:
            damage: Damage value (must be >= 0)
        """
        try:
            if damage < 0:
                raise ValueError("Damage can't be negative")
            self._damage = damage
            Logger.debug("CaracterModel.setDamage", "Damage set", damage=damage)
        except ValueError as e:
            Logger.error("CaracterModel.setDamage", e)
        except Exception as e:
            Logger.error("CaracterModel.setDamage", e)

    def getAccuracy(self):
        """
        Get the accuracy value.
        
        Returns:
            float: Accuracy value (typically 0.0 to 1.0)
        """
        try:
            return self._accuracy
        except Exception as e:
            Logger.error("CaracterModel.getAccuracy", e)
            return 0.0

    def setAccuracy(self, accuracy):
        """
        Set the accuracy value.
        
        Args:
            accuracy: Accuracy value (must be >= 0)
        """
        try:
            if accuracy < 0:
                raise ValueError("Accuracy can't be negative")
            self._accuracy = accuracy
            Logger.debug("CaracterModel.setAccuracy", "Accuracy set", accuracy=accuracy)
        except ValueError as e:
            Logger.error("CaracterModel.setAccuracy", e)
        except Exception as e:
            Logger.error("CaracterModel.setAccuracy", e)

    # === COMBAT METHODS ===
    
    @staticmethod
    def attack(caracter1, caracter2):
        """
        Static method to perform an attack from one character to another.
        Reduces caracter1's health by caracter2's damage.
        
        Args:
            caracter1: Character receiving damage
            caracter2: Character dealing damage
        """
        try:
            current_health = caracter1.getHealth()
            damage = caracter2.getDamage()
            new_health = current_health - damage
            caracter1.setHealth(new_health)
            Logger.debug("CaracterModel.attack", "Attack performed", 
                        attacker=caracter2.getName(), 
                        defender=caracter1.getName(),
                        damage=damage,
                        new_health=new_health)
        except Exception as e:
            Logger.error("CaracterModel.attack", e)

    def attack(caracter1,caracter2):

        caracter1.setHealth(caracter1.getHealth()-caracter2.getDamage())

    def getDrunkenness(self):
        return self._drunkenness

    def setDrunkenness(self, drunkenness):
        self._drunkenness = drunkenness

    def getComaRisk(self):
        return self._coma_risk

    def setComaRisk(self, coma_risk):
        self._coma_risk = coma_risk

    def getSelectedBottle(self):
        return self._selected_bottle

    def setSelectedBottle(self, bottle):
        self._selected_bottle = bottle
