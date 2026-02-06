"""
CombatController Module

Handles turn-based combat logic and player/enemy actions.
Manages combat flow, status effects, and turn switching.
"""

import pygame
import random
from Utils.Logger import Logger
from Controllers import BaseController


class CombatController(BaseController):
    """Controller for managing turn-based combat logic."""

    def __init__(self, combat_model):
        try:
            self.combat = combat_model
            self.player = combat_model.getPlayer()
            self.enemy = combat_model.getEnemy()

            self.action_delay = 0
            self.action_cooldown = 30
            Logger.debug("CombatController.__init__", "Initialized", player=self.player.getName(), enemy=self.enemy.getName())
        except Exception as e:
            Logger.error("CombatController.__init__", e)
            raise

    def update(self):
        try:
            if self.action_delay > 0:
                self.action_delay -= 1

            if not self.combat.isPlayerTurn() and self.action_delay == 0:
                try:
                    self.enemyTurn()
                    self.action_delay = self.action_cooldown * 2
                except Exception as e:
                    Logger.error("CombatController.update", e)
        except Exception as e:
            Logger.error("CombatController.update", e)

    def handle_input(self, event):
        try:
            if event.type == pygame.KEYDOWN:
                Logger.debug("CombatController.handle_input", "Key pressed", key=pygame.key.name(event.key), is_player_turn=self.combat.isPlayerTurn(), action_delay=self.action_delay)
                
                if not self.combat.isPlayerTurn():
                    Logger.debug("CombatController.handle_input", "Not player turn, ignoring input")
                    return
                
                if self.action_delay > 0:
                    Logger.debug("CombatController.handle_input", "Action delay active, ignoring input", delay=self.action_delay)
                    return
                
                # Simple attack (A)
                if event.key == pygame.K_a:
                    Logger.debug("CombatController.handle_input", "Simple Attack triggered")
                    try:
                        self.playerSimpleAttack()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handle_input", e)

                # Power Chord (P)
                elif event.key == pygame.K_p:
                    Logger.debug("CombatController.handle_input", "Power Chord triggered")
                    try:
                        self.playerPowerChord()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handle_input", e)

                # Dégueulando (D)
                elif event.key == pygame.K_d:
                    Logger.debug("CombatController.handle_input", "Dégueulando triggered")
                    try:
                        self.playerDegueulando()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handle_input", e)

                # Drink (B)
                elif event.key == pygame.K_b:
                    Logger.debug("CombatController.handle_input", "Drink triggered")
                    try:
                        self.playerDrink()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handle_input", e)
        except Exception as e:
            Logger.error("CombatController.handle_input", e)

    def handleInput(self, event):
        return self.handle_input(event)

    # --- Player attack utilities ---
    def _performPlayerAttack(self, base_damage, action_name, hit_message, miss_message, is_powerful=False):
        try:
            if self.combat.getPlayerStatus("paralyzed") > 0:
                self.combat.addToCombatLog(f"{self.player.getName()} is paralyzed!")
                self.endPlayerTurn()
                return False

            if self.combat.getPlayerStatus("stunned") > 0:
                self.combat.addToCombatLog(f"{self.player.getName()} is stunned!")
                self.endPlayerTurn()
                return False

            # Set animation
            self.player.setCurrentAction(action_name, 30)

            # Damage calculation
            damage = base_damage if not is_powerful else int(base_damage * 2.5)

            # Drunkenness bonus
            try:
                drunkenness = self.player.getDrunkenness()
            except Exception:
                drunkenness = 0

            if drunkenness >= 50 and not is_powerful:
                damage = int(damage * 1.5)
                self.combat.addToCombatLog("Drunkenness bonus! (+50% damage)")

            # Accuracy
            try:
                accuracy = max(20, min(100, int(self.player.getAccuracy() * 100)))
            except Exception:
                accuracy = 50

            if random.randint(1, 100) <= accuracy:
                final_damage = max(1, int(damage))
                self.enemy.setHealth(max(0, self.enemy.getHealth() - final_damage))
                self.combat.addToCombatLog(hit_message.format(player=self.player.getName(), damage=final_damage))
                Logger.debug("CombatController._performPlayerAttack", "Hit", damage=final_damage)
                return True
            else:
                self.combat.addToCombatLog(miss_message.format(player=self.player.getName()))
                Logger.debug("CombatController._performPlayerAttack", "Missed")
                return False
        except Exception as e:
            Logger.error("CombatController._performPlayerAttack", e)
            return False

    # --- Player actions ---
    def playerSimpleAttack(self):
        try:
            base_damage = self.player.getDamage()
            success = self._performPlayerAttack(
                base_damage,
                "attacking",
                "{player} strikes with guitar! ({damage} damage)",
                "{player} misses the attack!",
                is_powerful=False,
            )

            if success and self.combat.checkCombatEnd():
                return
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerSimpleAttack", e)

    def playerPowerChord(self):
        try:
            player_hp = self.player.getHealth()
            if player_hp <= 10:
                self.combat.addToCombatLog("Not enough HP for Power Chord! (need 10 HP)")
                return

            self.player.setHealth(player_hp - 10)

            base_damage = self.player.getDamage()
            success = self._performPlayerAttack(
                base_damage,
                "attacking",
                "POWER CHORD! {player} deals {damage} damage!",
                "{player} misses the power chord!",
                is_powerful=True,
            )

            if success:
                if random.randint(1, 100) <= 30:
                    self.combat.setEnemyStatus("stunned", 1)
                    self.combat.addToCombatLog(f"{self.enemy.getName()} is stunned!")
                    Logger.debug("CombatController.playerPowerChord", "Enemy stunned")

                if self.combat.checkCombatEnd():
                    return

            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerPowerChord", e)

    def playerDegueulando(self):
        try:
            drunkenness = self.player.getDrunkenness()
            if drunkenness < 60:
                self.combat.addToCombatLog("Not drunk enough! (Need 60% drunkenness)")
                return

            self.player.setCurrentAction("drinking", 30)
            self.combat.setEnemyStatus("disgusted", 2)
            self.combat.addToCombatLog(f"DEGUEULANDO! {self.enemy.getName()} is paralyzed with disgust!")
            self.player.setDrunkenness(max(0, drunkenness - 20))
            Logger.debug("CombatController.playerDegueulando", "Executed", drunkenness_cost=20)
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerDegueulando", e)

    def playerDrink(self):
        try:
            # Check if player has inventory and items
            if not hasattr(self.player, 'inventory') or not self.player.inventory:
                self.combat.addToCombatLog("No inventory available!")
                return

            # Get selected bottle from inventory
            selected_bottle = self.player.inventory.get_selected_item()
            if not selected_bottle:
                self.combat.addToCombatLog("No bottle selected!")
                return

            self.player.setCurrentAction("drinking", 30)
            self.player.drink(selected_bottle)
            drunkenness = self.player.getDrunkenness()
            self.combat.addToCombatLog(f"{self.player.getName()} drinks {selected_bottle.getName()}! (Drunkenness: {drunkenness}%)")
            
            # Remove the bottle from inventory after drinking
            self.player.inventory.consume_selected()
            
            # Update selected bottle to the new selected item (or None if inventory is empty)
            self.player.setSelectedBottle(self.player.inventory.get_selected_item())
            
            Logger.debug("CombatController.playerDrink", "Player drank", bottle=selected_bottle.getName(), drunkenness=drunkenness)

            if self.player.getHealth() <= 0:
                self.combat.setDiedFromComa(True)
                self.combat.addToCombatLog(f"ALCOHOLIC COMA! {self.player.getName()} collapses!")
                self.combat.checkCombatEnd()
                return

            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerDrink", e)

    # --- Enemy logic ---
    def enemyTurn(self):
        try:
            if self.combat.getEnemyStatus("paralyzed") > 0 or self.combat.getEnemyStatus("disgusted") > 0:
                self.combat.addToCombatLog(f"{self.enemy.getName()} is unable to act!")
                self.endEnemyTurn()
                return

            if self.combat.getEnemyStatus("stunned") > 0:
                self.combat.addToCombatLog(f"{self.enemy.getName()} is stunned!")
                self.endEnemyTurn()
                return

            action = random.choice(["attack", "attack", "heavy_attack"])
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
        try:
            damage = self.enemy.getDamage()
            try:
                accuracy = max(20, min(100, int(self.enemy.getAccuracy() * 100)))
            except Exception:
                accuracy = 50

            if random.randint(1, 100) <= accuracy:
                self.enemy.setCurrentAction("attacking", 30)
                self.player.setHealth(max(0, self.player.getHealth() - damage))
                self.combat.addToCombatLog(f"{self.enemy.getName()} attacks! ({damage} damage)")
                Logger.debug("CombatController.enemySimpleAttack", "Hit", damage=damage)
                if self.combat.checkCombatEnd():
                    return
            else:
                self.player.setCurrentAction("dodging", 20)
                self.combat.addToCombatLog(f"{self.enemy.getName()} misses the attack!")
                Logger.debug("CombatController.enemySimpleAttack", "Missed")

            self.endEnemyTurn()
        except Exception as e:
            Logger.error("CombatController.enemySimpleAttack", e)

    def enemyHeavyAttack(self):
        try:
            heavy_damage = int(self.enemy.getDamage() * 1.8)
            if random.randint(1, 100) <= 60:
                self.enemy.setCurrentAction("attacking", 30)
                self.player.setHealth(max(0, self.player.getHealth() - heavy_damage))
                self.combat.addToCombatLog(f"{self.enemy.getName()} strikes violently! ({heavy_damage} damage)")
                Logger.debug("CombatController.enemyHeavyAttack", "Hit", damage=heavy_damage)
                if random.randint(1, 100) <= 25:
                    self.combat.setPlayerStatus("stunned", 1)
                    self.combat.addToCombatLog(f"{self.player.getName()} is stunned!")
                if self.combat.checkCombatEnd():
                    return
            else:
                self.player.setCurrentAction("dodging", 20)
                self.combat.addToCombatLog(f"{self.enemy.getName()} misses the heavy attack!")
                Logger.debug("CombatController.enemyHeavyAttack", "Missed")

            self.endEnemyTurn()
        except Exception as e:
            Logger.error("CombatController.enemyHeavyAttack", e)

    def endPlayerTurn(self):
        try:
            self.combat.applyBleedingDamage()
            self.combat.decrementStatusEffects()
            self.combat.switchTurn()
            Logger.debug("CombatController.endPlayerTurn", "Ended")
        except Exception as e:
            Logger.error("CombatController.endPlayerTurn", e)

    def endEnemyTurn(self):
        try:
            self.combat.applyBleedingDamage()
            self.combat.decrementStatusEffects()
            self.combat.switchTurn()
            Logger.debug("CombatController.endEnemyTurn", "Ended")
        except Exception as e:
            Logger.error("CombatController.endEnemyTurn", e)
