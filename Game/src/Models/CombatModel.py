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
            
            Logger.debug("CombatModel.__init__", 
                        f"Combat started: {player.getName()} vs {enemy.getName()}",
                        player_hp=player.getHealth(),
                        enemy_hp=enemy.getHealth())
        except Exception as e:
            Logger.error("CombatModel.__init__", e)
            raise
        self._player = player
        self._enemy = enemy
        self._turn = 1
        self._is_player_turn = True
        self._combat_log = []
        self._combat_finished = False
        self._winner = None
        
        # Effets de statut
        self._player_status = {
            "paralyzed": 0,  # Nombre de tours restants
            "bleeding": 0,
            "stunned": 0
        }
        self._enemy_status = {
            "paralyzed": 0,
            "bleeding": 0,
            "stunned": 0,
            "disgusted": 0  # Pour l'attaque Dégueulando
        }
        
        Logger.debug("CombatModel.__init__", 
                    f"Combat started: {player.getName()} vs {enemy.getName()}",
                    player_hp=player.getHealth(),
                    enemy_hp=enemy.getHealth())
    
    # === GETTERS / SETTERS ===
    
    def getPlayer(self):
        return self._player
    
    def getEnemy(self):
        return self._enemy
    
    def getTurn(self):
        return self._turn
    
    def incrementTurn(self):
        self._turn += 1
    
    def isPlayerTurn(self):
        return self._is_player_turn
    
    def switchTurn(self):
        self._is_player_turn = not self._is_player_turn
        if self._is_player_turn:
            self.incrementTurn()
        Logger.debug("CombatModel.switchTurn", 
                    f"Turn {self._turn} - {'Player' if self._is_player_turn else 'Enemy'} turn")
    
    def getCombatLog(self):
        return self._combat_log
    
    def addToCombatLog(self, message):
        self._combat_log.append(message)
        Logger.debug("CombatModel.addToCombatLog", message)
        
        # Garder seulement les 10 derniers messages
        if len(self._combat_log) > 10:
            self._combat_log.pop(0)
    
    def isCombatFinished(self):
        return self._combat_finished
    
    def getWinner(self):
        return self._winner
    
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
                self.addToCombatLog(f"💉 {self._player.getName()} perd {bleed_damage} HP (saignement)")
                Logger.debug("CombatModel.applyBleedingDamage", "Player bleeding damage applied", damage=bleed_damage)
            
            if self._enemy_status["bleeding"] > 0:
                bleed_damage = 2
                current_hp = self._enemy.getHealth()
                self._enemy.setHealth(max(0, current_hp - bleed_damage))
                self.addToCombatLog(f"💉 {self._enemy.getName()} perd {bleed_damage} HP (saignement)")
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
                self._combat_finished = True
                self._winner = "ENEMY"
                self.addToCombatLog(f"💀 {self._player.getName()} est K.O. !")
                Logger.debug("CombatModel.checkCombatEnd", "Enemy wins!")
                return True
            
            if enemy_hp <= 0:
                self._combat_finished = True
                self._winner = "PLAYER"
                self.addToCombatLog(f"🏆 {self._enemy.getName()} est vaincu !")
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
            self._turn = 1
            self._is_player_turn = True
            self._combat_log = []
            self._combat_finished = False
            self._winner = None
            
            # Reset status effects
            for status in self._player_status:
                self._player_status[status] = 0
            for status in self._enemy_status:
                self._enemy_status[status] = 0
            
            Logger.debug("CombatModel.resetCombat", "Combat reset")
        except Exception as e:
            Logger.error("CombatModel.resetCombat", e)