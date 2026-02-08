from Utils.Logger import Logger


class CaracterModel:

    def __init__(self, name, x=175, y=175, characterType="PNJ"):
        try:
            self._type = characterType
            self._name = name
            self._health = 100
            self._damage = 5
            self._accuracy = 1
            self._x = x
            self._y = y
            self._drunkenness = 0
            self._comaRisk = 0
            self._selectedBottle = None
            self._currentAction = "idle"
            self._actionTimer = 0
            self._currency = 0
            
            Logger.debug("CaracterModel.__init__", f"Character created: {name}", x=x, y=y)
        except Exception as e:
            Logger.error("CaracterModel.__init__", e)
            raise


    def getType(self):
        return self._type

    def setType(self, characterType):
        self._type = characterType


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
                raise ValueError("Damage cannot be negative")
            self._damage = damage
        except ValueError as e:
            Logger.error("CaracterModel.setDamage", e)

    def addDamage(self, amount):
        self.setDamage(self._damage + amount)


    def getAccuracy(self):
        return self._accuracy

    def setAccuracy(self, accuracy):
        try:
            if accuracy < 0:
                raise ValueError("Accuracy cannot be negative")
            self._accuracy = accuracy
        except ValueError as e:
            Logger.error("CaracterModel.setAccuracy", e)


    def getCurrentAction(self):
        return self._currentAction

    def setCurrentAction(self, action, duration=30):
        self._currentAction = action
        self._actionTimer = duration
        Logger.debug("CaracterModel.setCurrentAction", f"Action: {action}", duration=duration)

    def getActionTimer(self):
        return self._actionTimer

    def updateActionTimer(self):
        if self._actionTimer > 0:
            self._actionTimer -= 1
        elif self._currentAction != "idle":
            self._currentAction = "idle"


    def getDrunkenness(self):
        return self._drunkenness

    def setDrunkenness(self, drunkenness):
        self._drunkenness = drunkenness

    def addDrunkenness(self, amount):
        self._drunkenness = min(100, self._drunkenness + amount)


    def getComaRisk(self):
        return self._comaRisk

    def setComaRisk(self, comaRisk):
        try:
            if not 0 <= comaRisk <= 100:
                raise ValueError("Coma risk must be between 0 and 100")
            self._comaRisk = comaRisk
        except ValueError as e:
            Logger.error("CaracterModel.setComaRisk", e)

    def addComaRisk(self, amount):
        self.setComaRisk(min(100, self._comaRisk + amount))


    def getSelectedBottle(self):
        return self._selectedBottle

    def setSelectedBottle(self, bottle):
        self._selectedBottle = bottle


    def getCurrency(self):
        try:
            return self._currency
        except Exception as e:
            Logger.error("CaracterModel.getCurrency", e)
            return 0

    def setCurrency(self, amount):
        try:
            self._currency = max(0, amount)
            Logger.debug("CaracterModel.setCurrency", "Currency set", amount=self._currency)
        except Exception as e:
            Logger.error("CaracterModel.setCurrency", e)

    def addCurrency(self, amount):
        try:
            self._currency = max(0, self._currency + amount)
            Logger.debug("CaracterModel.addCurrency", "Currency added", amount=amount, total=self._currency)
        except Exception as e:
            Logger.error("CaracterModel.addCurrency", e)

    def removeCurrency(self, amount):
        try:
            self._currency = max(0, self._currency - amount)
            Logger.debug("CaracterModel.removeCurrency", "Currency removed", amount=amount, total=self._currency)
        except Exception as e:
            Logger.error("CaracterModel.removeCurrency", e)


    def takeDamage(self, damageAmount):
        newHealth = max(0, self._health - damageAmount)
        self.setHealth(newHealth)

    def isAlive(self):
        return self._health > 0