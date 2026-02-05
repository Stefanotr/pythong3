from Utils.Logger import Logger

class CaracterModel:
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
        self._current_action = "idle"  # idle, attacking, drinking, dodging
        self._action_timer = 0  # Timer for action animation

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type
       
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name

    def getX(self):
        return self._x
    
    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y
    
    def setY(self, y):
        self._y = y

    def getHealth(self):
        return self._health
    
    def setHealth(self, health):
        self._health = health

    def getDamage(self):
        return self._damage
    
    def setDamage(self, damage):
        try:
            
            if damage < 0:
                raise ValueError("Damage can't be negative")
            self._damage = damage

        except ValueError as e:
            Logger.error("CaracterModel.setDamage",e)

    def getAccuracy(self):
        return self._accuracy
    
    def setAccuracy(self, accuracy):
        try:
            
            if accuracy < 0:
                raise ValueError("Accuracy can't be negative")
            self._accuracy = accuracy
            
        except ValueError as e:
            Logger.error("CaracterModel.setAccuracy",e)

    def getCurrentAction(self):
        return self._current_action
    
    def setCurrentAction(self, action, duration=30):
        """
        Set the current action for the character.
        
        Args:
            action: Action type (idle, attacking, drinking, dodging)
            duration: How long to display this action (in frames)
        """
        self._current_action = action
        self._action_timer = duration
        Logger.debug("CaracterModel.setCurrentAction", f"Action set to {action}", duration=duration)
    
    def getActionTimer(self):
        return self._action_timer
    
    def updateActionTimer(self):
        """Decrement action timer, reset to idle when done"""
        if self._action_timer > 0:
            self._action_timer -= 1
        elif self._current_action != "idle":
            self._current_action = "idle"

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
