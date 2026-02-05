"""
CombatModel Module

Manages turn-based combat state and logic.
Tracks combat turns, status effects, combat log, and victory conditions.
"""

from Utils.Logger import Logger


# === COMBAT MODEL CLASS ===

class CombatModel:
    """
    Model for managing turn-based combat state.
    Handles combat flow, status effects, combat log, and win/loss conditions.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, player, enemy):
        """
        Initialize the combat model with player and enemy.
        
        Args:
            player: Player character model
            enemy: Enemy character model
        """
        try:
            self._player = player
            self._enemy = enemy
            # Store initial max health values for UI scaling
            try:
                self._player_max_health = player.getHealth()
            except Exception:
                self._player_max_health = 100
            try:
                self._enemy_max_health = enemy.getHealth()
            except Exception:
                self._enemy_max_health = 100
            self._turn = 1
            self._is_player_turn = True
            self._combat_log = []
            self._combat_finished = False
            self._winner = None
            
            # Status effects
            self._player_status = {
                "paralyzed": 0,  # Remaining turns
                "bleeding": 0,
                "stunned": 0
            }
            self._enemy_status = {
                "paralyzed": 0,
                "bleeding": 0,
                "stunned": 0,
                "disgusted": 0  # For Dégueulando attack
            }
            
            # Alcoholic coma death flag
            self._died_from_coma = False
            
            Logger.debug("CombatModel.__init__", 
                        f"Combat started: {player.getName()} vs {enemy.getName()}",
                        player_hp=player.getHealth(),
                        enemy_hp=enemy.getHealth())
        except Exception as e:
            Logger.error("CombatModel.__init__", e)
            raise
    
    # === GETTERS / SETTERS ===
    
    def getPlayer(self):
        return self._player
    
    def getEnemy(self):
        return self._enemy

    def getPlayerMaxHealth(self):
        try:
            return getattr(self, '_player_max_health', max(100, self._player.getHealth()))
        except Exception as e:
            Logger.error('CombatModel.getPlayerMaxHealth', e)
            return max(100, self._player.getHealth() if hasattr(self._player, 'getHealth') else 100)

    def getEnemyMaxHealth(self):
        try:
            return getattr(self, '_enemy_max_health', max(100, self._enemy.getHealth()))
        except Exception as e:
            Logger.error('CombatModel.getEnemyMaxHealth', e)
            return max(100, self._enemy.getHealth() if hasattr(self._enemy, 'getHealth') else 100)
    
    def getTurn(self):
        """
        Get the current turn number.
        
        Returns:
            int: Current turn number
        """
        try:
            return self._turn
        except Exception as e:
            Logger.error("CombatModel.getTurn", e)
            return 1
    
    def setTurn(self, turn):
        """
        Set the turn number.
        
        Args:
            turn: Turn number to set
        """
        try:
            self._turn = max(1, turn)
            Logger.debug("CombatModel.setTurn", "Turn set", turn=self._turn)
        except Exception as e:
            Logger.error("CombatModel.setTurn", e)
    
    def incrementTurn(self):
        """
        Increment the turn number by one.
        """
        try:
            self._turn += 1
            Logger.debug("CombatModel.incrementTurn", "Turn incremented", turn=self._turn)
        except Exception as e:
            Logger.error("CombatModel.incrementTurn", e)
    
    def isPlayerTurn(self):
        """
        Check if it's the player's turn.
        
        Returns:
            bool: True if player's turn, False if enemy's turn
        """
        try:
            return self._is_player_turn
        except Exception as e:
            Logger.error("CombatModel.isPlayerTurn", e)
            return True
    
    def setIsPlayerTurn(self, value):
        """
        Set whether it's the player's turn.
        
        Args:
            value: True for player's turn, False for enemy's turn
        """
        try:
            self._is_player_turn = bool(value)
            Logger.debug("CombatModel.setIsPlayerTurn", "Turn set", is_player_turn=self._is_player_turn)
        except Exception as e:
            Logger.error("CombatModel.setIsPlayerTurn", e)
    
    def switchTurn(self):
        self._is_player_turn = not self._is_player_turn
        if self._is_player_turn:
            self.incrementTurn()
        Logger.debug("CombatModel.switchTurn", 
                    f"Turn {self._turn} - {'Player' if self._is_player_turn else 'Enemy'} turn")
    
    def getCombatLog(self):
        """
        Get the combat log messages.
        
        Returns:
            list: List of combat log messages
        """
        try:
            return self._combat_log.copy()  # Return a copy to prevent external modification
        except Exception as e:
            Logger.error("CombatModel.getCombatLog", e)
            return []
    
    def setCombatLog(self, log):
        """
        Set the combat log messages.
        
        Args:
            log: List of combat log messages
        """
        try:
            if isinstance(log, list):
                self._combat_log = log.copy()  # Store a copy
                Logger.debug("CombatModel.setCombatLog", "Combat log set", message_count=len(self._combat_log))
            else:
                Logger.error("CombatModel.setCombatLog", ValueError("Combat log must be a list"))
        except Exception as e:
            Logger.error("CombatModel.setCombatLog", e)
    
    def addToCombatLog(self, message):
        self._combat_log.append(message)
        Logger.debug("CombatModel.addToCombatLog", message)
        
        # Keep only the last 10 messages
        if len(self._combat_log) > 10:
            self._combat_log.pop(0)
    
    def setDiedFromComa(self, value):
        """
        Set the flag indicating player died from alcoholic coma.
        
        Args:
            value: Boolean indicating if player died from coma
        """
        try:
            self._died_from_coma = value
            Logger.debug("CombatModel.setDiedFromComa", "Coma death flag set", value=value)
        except Exception as e:
            Logger.error("CombatModel.setDiedFromComa", e)
    
    def getDiedFromComa(self):
        """
        Get the flag indicating if player died from alcoholic coma.
        
        Returns:
            bool: True if player died from coma, False otherwise
        """
        try:
            return self._died_from_coma
        except Exception as e:
            Logger.error("CombatModel.getDiedFromComa", e)
            return False
    
    def isCombatFinished(self):
        """
        Check if combat is finished.
        
        Returns:
            bool: True if combat is finished, False otherwise
        """
        try:
            return self._combat_finished
        except Exception as e:
            Logger.error("CombatModel.isCombatFinished", e)
            return False
    
    def setCombatFinished(self, finished):
        """
        Set the combat finished status.
        
        Args:
            finished: True if combat is finished, False otherwise
        """
        try:
            self._combat_finished = bool(finished)
            Logger.debug("CombatModel.setCombatFinished", "Combat finished status set", finished=self._combat_finished)
        except Exception as e:
            Logger.error("CombatModel.setCombatFinished", e)
    
    def getWinner(self):
        """
        Get the winner of the combat.
        
        Returns:
            str: Winner identifier ("PLAYER" or "ENEMY") or None if not finished
        """
        try:
            return self._winner
        except Exception as e:
            Logger.error("CombatModel.getWinner", e)
            return None
    
    def setWinner(self, winner):
        """
        Set the winner of the combat.
        
        Args:
            winner: Winner identifier ("PLAYER" or "ENEMY")
        """
        try:
            if winner in ["PLAYER", "ENEMY", None]:
                self._winner = winner
                Logger.debug("CombatModel.setWinner", "Winner set", winner=winner)
            else:
                Logger.error("CombatModel.setWinner", ValueError(f"Invalid winner: {winner}"))
        except Exception as e:
            Logger.error("CombatModel.setWinner", e)
    
    # === STATUS EFFECTS ===
    
    def getPlayerStatus(self, status_type):
        return self._player_status.get(status_type, 0)
    
    def setPlayerStatus(self, status_type, turns):
        self._player_status[status_type] = turns
    
    def getEnemyStatus(self, status_type):
        return self._enemy_status.get(status_type, 0)
    
    def setEnemyStatus(self, status_type, turns):
        self._enemy_status[status_type] = turns
    
    def decrementStatusEffects(self):
        """
        Decrement all active status effects by one turn.
        Called at the end of each turn.
        """
        try:
            for status in self._player_status:
                if self._player_status[status] > 0:
                    self._player_status[status] -= 1
            
            for status in self._enemy_status:
                if self._enemy_status[status] > 0:
                    self._enemy_status[status] -= 1
            Logger.debug("CombatModel.decrementStatusEffects", "Status effects decremented")
        except Exception as e:
            Logger.error("CombatModel.decrementStatusEffects", e)
    
    def applyBleedingDamage(self):
        """
        Apply bleeding damage to characters with active bleeding status.
        Called at the end of each turn.
        """
        try:
            if self._player_status["bleeding"] > 0:
                bleed_damage = 2
                current_hp = self._player.getHealth()
                self._player.setHealth(max(0, current_hp - bleed_damage))
                self.addToCombatLog(f"{self._player.getName()} loses {bleed_damage} HP (bleeding)")
                Logger.debug("CombatModel.applyBleedingDamage", "Player bleeding damage applied", damage=bleed_damage)
            
            if self._enemy_status["bleeding"] > 0:
                bleed_damage = 2
                current_hp = self._enemy.getHealth()
                self._enemy.setHealth(max(0, current_hp - bleed_damage))
                self.addToCombatLog(f"{self._enemy.getName()} loses {bleed_damage} HP (bleeding)")
                Logger.debug("CombatModel.applyBleedingDamage", "Enemy bleeding damage applied", damage=bleed_damage)
        except Exception as e:
            Logger.error("CombatModel.applyBleedingDamage", e)
    
    # === COMBAT CHECKS ===
    
    def checkCombatEnd(self):
        """
        Check if the combat has ended (player or enemy health <= 0).
        
        Returns:
            bool: True if combat is finished, False otherwise
        """
        try:
            player_hp = self._player.getHealth()
            enemy_hp = self._enemy.getHealth()
            
            if player_hp <= 0:
                self.setCombatFinished(True)
                self.setWinner("ENEMY")
                
                # Check if player died from alcoholic coma
                if self._died_from_coma:
                    self.addToCombatLog(f"ALCOHOLIC COMA! {self._player.getName()} collapsed from drinking too much!")
                    Logger.debug("CombatModel.checkCombatEnd", "Player died from alcoholic coma")
                else:
                    self.addToCombatLog(f"{self._player.getName()} was defeated by {self._enemy.getName()}!")
                    Logger.debug("CombatModel.checkCombatEnd", "Player defeated by enemy")
                
                return True
            
            if enemy_hp <= 0:
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
        """
        Reset the combat state (for restarting combat).
        Resets turns, status effects, and combat log.
        """
        try:
            self.setTurn(1)
            self.setIsPlayerTurn(True)
            self.setCombatLog([])
            self.setCombatFinished(False)
            self.setWinner(None)
            
            # Reset status effects
            for status in self._player_status:
                self._player_status[status] = 0
            for status in self._enemy_status:
                self._enemy_status[status] = 0
            
            # Reset coma death flag
            self._died_from_coma = False
            
            Logger.debug("CombatModel.resetCombat", "Combat reset")
        except Exception as e:
            Logger.error("CombatModel.resetCombat", e)