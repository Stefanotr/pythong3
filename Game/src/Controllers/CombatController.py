"""
CombatController Module

Handles turn-based combat logic and player/enemy actions.
Manages combat flow, status effects, and turn switching.
"""

import pygame
import random
from Utils.Logger import Logger


# === COMBAT CONTROLLER CLASS ===

class CombatController:
    """
    Controller for managing turn-based combat logic.
    Handles player actions, enemy AI, status effects, and combat flow.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, combat_model):
        """
        Initialize the combat controller.
        
        Args:
            combat_model: CombatModel instance containing combat state
        """
        try:
            self.combat = combat_model
            self.player = combat_model.getPlayer()
            self.enemy = combat_model.getEnemy()
            
            self.action_delay = 0  # Delay to prevent actions that are too fast
            self.action_cooldown = 30  # frames (0.5 sec at 60fps)
            Logger.debug("CombatController.__init__", "Combat controller initialized", 
                        player=self.player.getName(), enemy=self.enemy.getName())
        except Exception as e:
            Logger.error("CombatController.__init__", e)
            raise
        
    # === UPDATE ===
    
    def update(self):
        """
        Update combat state.
        Decrements action delay and triggers enemy turn if appropriate.
        """
        try:
            # Decrement action delay
            if self.action_delay > 0:
                self.action_delay -= 1
            
            # If it's enemy's turn and no delay, enemy attacks automatically
            if not self.combat.isPlayerTurn() and self.action_delay == 0:
                try:
                    self.enemyTurn()
                    self.action_delay = self.action_cooldown * 2  # Double delay for enemy
                except Exception as e:
                    Logger.error("CombatController.update", e)
        except Exception as e:
            Logger.error("CombatController.update", e)
    
    # === INPUT HANDLING ===
    
    def handleInput(self, event):
        """
        Handle player input events.
        
        Args:
            event: Pygame event object
        """
        try:
            if event.type == pygame.KEYDOWN and self.combat.isPlayerTurn() and self.action_delay == 0:
                
                # Simple attack (A)
                if event.key == pygame.K_a:
                    try:
                        self.playerSimpleAttack()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)
                
                # Power Chord (P) - Consumes health
                elif event.key == pygame.K_p:
                    try:
                        self.playerPowerChord()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)
                
                # Dégueulando (D) - Special alcohol-related attack
                elif event.key == pygame.K_d:
                    try:
                        self.playerDegueulando()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)
                
                # Drink (B) - Increases stats
                elif event.key == pygame.K_b:
                    try:
                        self.playerDrink()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)
        except Exception as e:
            Logger.error("CombatController.handleInput", e)
    
    # === PLAYER ACTIONS ===
    
    def playerSimpleAttack(self):
        """
        Perform a simple attack with the guitar.
        Calculates damage based on player stats and accuracy.
        """
        try:
            if self.combat.getPlayerStatus("paralyzed") > 0:
                self.combat.addToCombatLog(f"⚡ {self.player.getName()} is paralyzed!")
                self.endPlayerTurn()
                return
            
            if self.combat.getPlayerStatus("stunned") > 0:
                self.combat.addToCombatLog(f"💫 {self.player.getName()} is stunned!")
                self.endPlayerTurn()
                return
            
            # Calculate damage
            base_damage = self.player.getDamage()
            
            # Drunkenness bonus (if > 50%)
            try:
                drunkenness = self.player.getDrunkenness()
                if drunkenness >= 50:
                    base_damage = int(base_damage * 1.5)
                    self.combat.addToCombatLog(f"🍺 Drunkenness bonus! (+50% damage)")
                    Logger.debug("CombatController.playerSimpleAttack", "Drunkenness bonus applied", 
                               drunkenness=drunkenness, base_damage=base_damage)
            except Exception as e:
                Logger.error("CombatController.playerSimpleAttack", e)
            
            # Accuracy penalty
            try:
                accuracy = self.player.getAccuracy()
                hit_chance = max(20, min(100, accuracy * 100))
            except Exception as e:
                Logger.error("CombatController.playerSimpleAttack", e)
                hit_chance = 50  # Default hit chance
            
            if random.randint(1, 100) <= hit_chance:
                # Hit!
                try:
                    final_damage = max(1, int(base_damage))
                    current_hp = self.enemy.getHealth()
                    self.enemy.setHealth(max(0, current_hp - final_damage))
                    
                    self.combat.addToCombatLog(f"🎸 {self.player.getName()} strikes with guitar! ({final_damage} damage)")
                    Logger.debug("CombatController.playerSimpleAttack", "Attack hit", damage=final_damage)
                    
                    # Check combat end
                    if self.combat.checkCombatEnd():
                        return
                except Exception as e:
                    Logger.error("CombatController.playerSimpleAttack", e)
            else:
                # Missed!
                self.combat.addToCombatLog(f"💨 {self.player.getName()} misses the attack!")
                Logger.debug("CombatController.playerSimpleAttack", "Attack missed")
            
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerSimpleAttack", e)
    
    def playerPowerChord(self):
        """
        Power Chord - Powerful attack that costs health.
        Deals massive damage but consumes 10 HP.
        """
        try:
            if self.combat.getPlayerStatus("paralyzed") > 0:
                self.combat.addToCombatLog(f"⚡ {self.player.getName()} is paralyzed!")
                self.endPlayerTurn()
                return
            
            # Cost: 10 HP
            try:
                player_hp = self.player.getHealth()
                if player_hp <= 10:
                    self.combat.addToCombatLog(f"❌ Not enough HP for Power Chord!")
                    Logger.debug("CombatController.playerPowerChord", "Insufficient HP", hp=player_hp)
                    return
                
                self.player.setHealth(player_hp - 10)
                Logger.debug("CombatController.playerPowerChord", "HP cost paid", hp_lost=10, remaining_hp=self.player.getHealth())
            except Exception as e:
                Logger.error("CombatController.playerPowerChord", e)
                return
            
            # Massive damage
            try:
                power_damage = int(self.player.getDamage() * 2.5)
                current_hp = self.enemy.getHealth()
                self.enemy.setHealth(max(0, current_hp - power_damage))
                
                self.combat.addToCombatLog(f"⚡🎸 POWER CHORD ! {power_damage} damage!")
                Logger.debug("CombatController.playerPowerChord", "Power chord executed", damage=power_damage)
            except Exception as e:
                Logger.error("CombatController.playerPowerChord", e)
            
            # Chance to stun enemy
            try:
                if random.randint(1, 100) <= 30:
                    self.combat.setEnemyStatus("stunned", 1)
                    self.combat.addToCombatLog(f"💫 {self.enemy.getName()} is stunned!")
                    Logger.debug("CombatController.playerPowerChord", "Enemy stunned")
            except Exception as e:
                Logger.error("CombatController.playerPowerChord", e)
            
            # Check combat end
            if self.combat.checkCombatEnd():
                return
            
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerPowerChord", e)
    
    def playerDegueulando(self):
        """
        Dégueulando - Vomit on enemy (requires drunkenness > 60%).
        Paralyzes enemy with disgust and reduces player's drunkenness.
        """
        try:
            drunkenness = self.player.getDrunkenness()
            
            if drunkenness < 60:
                self.combat.addToCombatLog(f"❌ Not drunk enough to vomit! (requires 60%)")
                Logger.debug("CombatController.playerDegueulando", "Insufficient drunkenness", 
                           drunkenness=drunkenness, required=60)
                return
            
            # Paralyze enemy with disgust
            try:
                self.combat.setEnemyStatus("disgusted", 2)
                self.combat.addToCombatLog(f"🤮 DÉGUEULANDO ! {self.enemy.getName()} is paralyzed with disgust!")
                Logger.debug("CombatController.playerDegueulando", "Enemy paralyzed with disgust")
            except Exception as e:
                Logger.error("CombatController.playerDegueulando", e)
            
            # Reduce drunkenness
            try:
                self.player.setDrunkenness(max(0, drunkenness - 20))
                Logger.debug("CombatController.playerDegueulando", "Drunkenness reduced", 
                           old_drunkenness=drunkenness, new_drunkenness=self.player.getDrunkenness())
            except Exception as e:
                Logger.error("CombatController.playerDegueulando", e)
            
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerDegueulando", e)
    
    def playerDrink(self):
        """
        Drink to increase stats.
        Consumes selected bottle and increases drunkenness, damage, and reduces accuracy.
        """
        try:
            selected_bottle = self.player.getSelectedBottle()
            
            if not selected_bottle:
                self.combat.addToCombatLog(f"❌ No bottle selected!")
                Logger.debug("CombatController.playerDrink", "No bottle selected")
                return
            
            # Drink
            try:
                self.player.drink(selected_bottle)
                
                drunkenness = self.player.getDrunkenness()
                self.combat.addToCombatLog(f"🍺 {self.player.getName()} drinks {selected_bottle.getName()}! (Drunkenness: {drunkenness}%)")
                Logger.debug("CombatController.playerDrink", "Player drank", 
                           bottle=selected_bottle.getName(), drunkenness=drunkenness)
            except Exception as e:
                Logger.error("CombatController.playerDrink", e)
                return
            
            # Check coma risk
            try:
                if self.player.getHealth() <= 0:
                    # Set coma death flag before checking combat end
                    self.combat.setDiedFromComa(True)
                    self.combat.addToCombatLog(f"💀 ALCOHOLIC COMA! {self.player.getName()} collapses from drinking too much!")
                    Logger.debug("CombatController.playerDrink", "Alcoholic coma triggered")
                    self.combat.checkCombatEnd()
                    return
            except Exception as e:
                Logger.error("CombatController.playerDrink", e)
            
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerDrink", e)
    
    # === ENEMY TURN ===
    
    def enemyTurn(self):
        """
        Simple AI for enemy turn.
        Randomly chooses between normal attack and heavy attack.
        """
        try:
            if self.combat.getEnemyStatus("paralyzed") > 0 or self.combat.getEnemyStatus("disgusted") > 0:
                self.combat.addToCombatLog(f"😵 {self.enemy.getName()} is unable to act!")
                self.endEnemyTurn()
                return
            
            if self.combat.getEnemyStatus("stunned") > 0:
                self.combat.addToCombatLog(f"💫 {self.enemy.getName()} is stunned!")
                self.endEnemyTurn()
                return
            
            # Simple random AI
            action = random.choice(["attack", "attack", "heavy_attack"])  # More chances for normal attack
            
            try:
                if action == "attack":
                    self.enemySimpleAttack()
                else:
                    self.enemyHeavyAttack()
            except Exception as e:
                Logger.error("CombatController.enemyTurn", e)
                self.endEnemyTurn()
        except Exception as e:
            Logger.error("CombatController.enemyTurn", e)
    
    def enemySimpleAttack(self):
        """
        Enemy simple attack.
        Calculates damage based on enemy stats and accuracy.
        """
        try:
            damage = self.enemy.getDamage()
            
            # Enemy accuracy
            try:
                accuracy = self.enemy.getAccuracy()
                hit_chance = max(20, min(100, accuracy * 100))
            except Exception as e:
                Logger.error("CombatController.enemySimpleAttack", e)
                hit_chance = 50  # Default hit chance
            
            if random.randint(1, 100) <= hit_chance:
                try:
                    current_hp = self.player.getHealth()
                    self.player.setHealth(max(0, current_hp - damage))
                    
                    self.combat.addToCombatLog(f"👊 {self.enemy.getName()} attacks! ({damage} damage)")
                    Logger.debug("CombatController.enemySimpleAttack", "Enemy attack hit", damage=damage)
                    
                    # Check combat end
                    if self.combat.checkCombatEnd():
                        return
                except Exception as e:
                    Logger.error("CombatController.enemySimpleAttack", e)
            else:
                self.combat.addToCombatLog(f"💨 {self.enemy.getName()} misses the attack!")
                Logger.debug("CombatController.enemySimpleAttack", "Enemy attack missed")
            
            self.endEnemyTurn()
        except Exception as e:
            Logger.error("CombatController.enemySimpleAttack", e)
    
    def enemyHeavyAttack(self):
        """
        Enemy heavy attack.
        Deals more damage but is less accurate. Has chance to stun player.
        """
        try:
            heavy_damage = int(self.enemy.getDamage() * 1.8)
            
            # Less accurate
            if random.randint(1, 100) <= 60:
                try:
                    current_hp = self.player.getHealth()
                    self.player.setHealth(max(0, current_hp - heavy_damage))
                    
                    self.combat.addToCombatLog(f"💥 {self.enemy.getName()} strikes violently! ({heavy_damage} damage)")
                    Logger.debug("CombatController.enemyHeavyAttack", "Enemy heavy attack hit", damage=heavy_damage)
                    
                    # Chance to stun player
                    try:
                        if random.randint(1, 100) <= 25:
                            self.combat.setPlayerStatus("stunned", 1)
                            self.combat.addToCombatLog(f"💫 {self.player.getName()} is stunned!")
                            Logger.debug("CombatController.enemyHeavyAttack", "Player stunned")
                    except Exception as e:
                        Logger.error("CombatController.enemyHeavyAttack", e)
                    
                    # Check combat end
                    if self.combat.checkCombatEnd():
                        return
                except Exception as e:
                    Logger.error("CombatController.enemyHeavyAttack", e)
            else:
                self.combat.addToCombatLog(f"💨 {self.enemy.getName()} misses the heavy attack!")
                Logger.debug("CombatController.enemyHeavyAttack", "Enemy heavy attack missed")
            
            self.endEnemyTurn()
        except Exception as e:
            Logger.error("CombatController.enemyHeavyAttack", e)
    
    # === TURN END ===
    
    def endPlayerTurn(self):
        """
        End player turn.
        Applies bleeding damage, decrements status effects, and switches turn.
        """
        try:
            self.combat.applyBleedingDamage()
            self.combat.decrementStatusEffects()
            self.combat.switchTurn()
            Logger.debug("CombatController.endPlayerTurn", "Player turn ended")
        except Exception as e:
            Logger.error("CombatController.endPlayerTurn", e)
    
    def endEnemyTurn(self):
        """
        End enemy turn.
        Applies bleeding damage, decrements status effects, and switches turn.
        """
        try:
            self.combat.applyBleedingDamage()
            self.combat.decrementStatusEffects()
            self.combat.switchTurn()
            Logger.debug("CombatController.endEnemyTurn", "Enemy turn ended")
        except Exception as e:
            Logger.error("CombatController.endEnemyTurn", e)