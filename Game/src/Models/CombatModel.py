from Utils.Logger import Logger


class CombatModel:

    def __init__(self, player, enemy):
        try:
            self._player = player
            self._enemy = enemy
            
            try:
                self._playerMaxHealth = player.getHealth()
            except Exception:
                self._playerMaxHealth = 100
            
            try:
                self._enemyMaxHealth = enemy.getHealth()
            except Exception:
                self._enemyMaxHealth = 100
            
            self._turn = 1
            self._isPlayerTurn = True
            self._combatLog = []
            self._combatFinished = False
            self._winner = None
            
            self._playerStatus = {
                "paralyzed": 0,
                "bleeding": 0,
                "stunned": 0
            }
            self._enemyStatus = {
                "paralyzed": 0,
                "bleeding": 0,
                "stunned": 0,
                "disgusted": 0
            }
            
            self._diedFromComa = False
            
            Logger.debug("CombatModel.__init__", 
                        f"Combat started: {player.getName()} vs {enemy.getName()}",
                        player_hp=player.getHealth(),
                        enemy_hp=enemy.getHealth())
        except Exception as e:
            Logger.error("CombatModel.__init__", e)
            raise


    def getPlayer(self):
        return self._player
    
    def getEnemy(self):
        return self._enemy

    def getPlayerMaxHealth(self):
        try:
            return getattr(self, '_playerMaxHealth', max(100, self._player.getHealth()))
        except Exception as e:
            Logger.error('CombatModel.getPlayerMaxHealth', e)
            return max(100, self._player.getHealth() if hasattr(self._player, 'getHealth') else 100)

    def getEnemyMaxHealth(self):
        try:
            return getattr(self, '_enemyMaxHealth', max(100, self._enemy.getHealth()))
        except Exception as e:
            Logger.error('CombatModel.getEnemyMaxHealth', e)
            return max(100, self._enemy.getHealth() if hasattr(self._enemy, 'getHealth') else 100)
    
    def getTurn(self):
        try:
            return self._turn
        except Exception as e:
            Logger.error("CombatModel.getTurn", e)
            return 1
    
    def setTurn(self, turn):
        try:
            self._turn = max(1, turn)
            Logger.debug("CombatModel.setTurn", "Turn set", turn=self._turn)
        except Exception as e:
            Logger.error("CombatModel.setTurn", e)
    
    def incrementTurn(self):
        try:
            self._turn += 1
            Logger.debug("CombatModel.incrementTurn", "Turn incremented", turn=self._turn)
        except Exception as e:
            Logger.error("CombatModel.incrementTurn", e)
    
    def isPlayerTurn(self):
        try:
            return self._isPlayerTurn
        except Exception as e:
            Logger.error("CombatModel.isPlayerTurn", e)
            return True
    
    def setIsPlayerTurn(self, value):
        try:
            self._isPlayerTurn = bool(value)
            Logger.debug("CombatModel.setIsPlayerTurn", "Turn set", isPlayerTurn=self._isPlayerTurn)
        except Exception as e:
            Logger.error("CombatModel.setIsPlayerTurn", e)
    
    def switchTurn(self):
        try:
            self._isPlayerTurn = not self._isPlayerTurn
            if self._isPlayerTurn:
                self.incrementTurn()
            Logger.debug("CombatModel.switchTurn", 
                        f"Turn {self._turn} - {'Player' if self._isPlayerTurn else 'Enemy'} turn")
        except Exception as e:
            Logger.error("CombatModel.switchTurn", e)


    def getCombatLog(self):
        try:
            return self._combatLog.copy()
        except Exception as e:
            Logger.error("CombatModel.getCombatLog", e)
            return []
    
    def setCombatLog(self, log):
        try:
            if isinstance(log, list):
                self._combatLog = log.copy()
                Logger.debug("CombatModel.setCombatLog", "Combat log set", messageCount=len(self._combatLog))
            else:
                Logger.error("CombatModel.setCombatLog", ValueError("Combat log must be a list"))
        except Exception as e:
            Logger.error("CombatModel.setCombatLog", e)
    
    def addToCombatLog(self, message):
        try:
            self._combatLog.append(message)
            Logger.debug("CombatModel.addToCombatLog", message)
            
            if len(self._combatLog) > 10:
                self._combatLog.pop(0)
        except Exception as e:
            Logger.error("CombatModel.addToCombatLog", e)
    
    def setDiedFromComa(self, value):
        try:
            self._diedFromComa = value
            Logger.debug("CombatModel.setDiedFromComa", "Coma death flag set", value=value)
        except Exception as e:
            Logger.error("CombatModel.setDiedFromComa", e)
    
    def getDiedFromComa(self):
        try:
            return self._diedFromComa
        except Exception as e:
            Logger.error("CombatModel.getDiedFromComa", e)
            return False
    
    def isCombatFinished(self):
        try:
            return self._combatFinished
        except Exception as e:
            Logger.error("CombatModel.isCombatFinished", e)
            return False
    
    def setCombatFinished(self, finished):
        try:
            self._combatFinished = bool(finished)
            Logger.debug("CombatModel.setCombatFinished", "Combat finished status set", finished=self._combatFinished)
        except Exception as e:
            Logger.error("CombatModel.setCombatFinished", e)
    
    def getWinner(self):
        try:
            return self._winner
        except Exception as e:
            Logger.error("CombatModel.getWinner", e)
            return None
    
    def setWinner(self, winner):
        try:
            if winner in ["PLAYER", "ENEMY", None]:
                self._winner = winner
                Logger.debug("CombatModel.setWinner", "Winner set", winner=winner)
            else:
                Logger.error("CombatModel.setWinner", ValueError(f"Invalid winner: {winner}"))
        except Exception as e:
            Logger.error("CombatModel.setWinner", e)


    def getPlayerStatus(self, statusType):
        try:
            return self._playerStatus.get(statusType, 0)
        except Exception as e:
            Logger.error("CombatModel.getPlayerStatus", e)
            return 0
    
    def setPlayerStatus(self, statusType, turns):
        try:
            self._playerStatus[statusType] = turns
            Logger.debug("CombatModel.setPlayerStatus", f"Player {statusType} set to {turns} turns")
        except Exception as e:
            Logger.error("CombatModel.setPlayerStatus", e)
    
    def getEnemyStatus(self, statusType):
        try:
            return self._enemyStatus.get(statusType, 0)
        except Exception as e:
            Logger.error("CombatModel.getEnemyStatus", e)
            return 0
    
    def setEnemyStatus(self, statusType, turns):
        try:
            self._enemyStatus[statusType] = turns
            Logger.debug("CombatModel.setEnemyStatus", f"Enemy {statusType} set to {turns} turns")
        except Exception as e:
            Logger.error("CombatModel.setEnemyStatus", e)
    
    def decrementStatusEffects(self):
        try:
            for status in self._playerStatus:
                if self._playerStatus[status] > 0:
                    self._playerStatus[status] -= 1
            
            for status in self._enemyStatus:
                if self._enemyStatus[status] > 0:
                    self._enemyStatus[status] -= 1
            
            Logger.debug("CombatModel.decrementStatusEffects", "Status effects decremented")
        except Exception as e:
            Logger.error("CombatModel.decrementStatusEffects", e)
    
    def applyBleedingDamage(self):
        try:
            if self._playerStatus["bleeding"] > 0:
                bleedDamage = 2
                currentHp = self._player.getHealth()
                self._player.setHealth(max(0, currentHp - bleedDamage))
                self.addToCombatLog(f"{self._player.getName()} loses {bleedDamage} HP (bleeding)")
                Logger.debug("CombatModel.applyBleedingDamage", "Player bleeding damage applied", damage=bleedDamage)
            
            if self._enemyStatus["bleeding"] > 0:
                bleedDamage = 2
                currentHp = self._enemy.getHealth()
                self._enemy.setHealth(max(0, currentHp - bleedDamage))
                self.addToCombatLog(f"{self._enemy.getName()} loses {bleedDamage} HP (bleeding)")
                Logger.debug("CombatModel.applyBleedingDamage", "Enemy bleeding damage applied", damage=bleedDamage)
        except Exception as e:
            Logger.error("CombatModel.applyBleedingDamage", e)
    
    
    
    def checkCombatEnd(self):
        try:
            playerHp = self._player.getHealth()
            enemyHp = self._enemy.getHealth()
            
            if playerHp <= 0:
                self.setCombatFinished(True)
                self.setWinner("ENEMY")
                
                if self._diedFromComa:
                    self.addToCombatLog(f"ALCOHOLIC COMA! {self._player.getName()} collapsed from drinking too much!")
                    Logger.debug("CombatModel.checkCombatEnd", "Player died from alcoholic coma")
                else:
                    self.addToCombatLog(f"{self._player.getName()} was defeated by {self._enemy.getName()}!")
                    Logger.debug("CombatModel.checkCombatEnd", "Player defeated by enemy")
                
                return True
            
            if enemyHp <= 0:
                self.setCombatFinished(True)
                self.setWinner("PLAYER")
                self.addToCombatLog(f"{self._enemy.getName()} is defeated!")
                Logger.debug("CombatModel.checkCombatEnd", "Player wins!")
                return True
            
            return False
        except Exception as e:
            Logger.error("CombatModel.checkCombatEnd", e)
            return False
    
    def resetCombat(self):
        try:
            self.setTurn(1)
            self.setIsPlayerTurn(True)
            self.setCombatLog([])
            self.setCombatFinished(False)
            self.setWinner(None)
            
            for status in self._playerStatus:
                self._playerStatus[status] = 0
            for status in self._enemyStatus:
                self._enemyStatus[status] = 0
            
            self._diedFromComa = False
            
            Logger.debug("CombatModel.resetCombat", "Combat reset")
        except Exception as e:
            Logger.error("CombatModel.resetCombat", e)