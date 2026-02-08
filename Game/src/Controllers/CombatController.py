import pygame
import random
from Utils.Logger import Logger
from Controllers import BaseController


class CombatController(BaseController):

    def __init__(self, combatModel):
        try:
            self.combat = combatModel
            self.player = combatModel.getPlayer()
            self.enemy = combatModel.getEnemy()

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

    def handleInput(self, event):
        try:
            if event.type == pygame.KEYDOWN:
                Logger.debug("CombatController.handleInput", "Key pressed", key=pygame.key.name(event.key), isPlayerTurn=self.combat.isPlayerTurn(), actionDelay=self.action_delay)
                
                if not self.combat.isPlayerTurn():
                    Logger.debug("CombatController.handleInput", "Not player turn, ignoring input")
                    return
                
                if self.action_delay > 0:
                    Logger.debug("CombatController.handleInput", "Action delay active, ignoring input", delay=self.action_delay)
                    return
                
                if event.key == pygame.K_a:
                    Logger.debug("CombatController.handleInput", "Simple Attack triggered")
                    try:
                        self.playerSimpleAttack()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)

                elif event.key == pygame.K_p:
                    Logger.debug("CombatController.handleInput", "Power Chord triggered")
                    try:
                        self.playerPowerChord()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)

                elif event.key == pygame.K_d:
                    Logger.debug("CombatController.handleInput", "Dégueulando triggered")
                    try:
                        self.playerDegueulando()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)

                elif event.key == pygame.K_b:
                    Logger.debug("CombatController.handleInput", "Drink triggered")
                    try:
                        self.playerDrink()
                        self.action_delay = self.action_cooldown
                    except Exception as e:
                        Logger.error("CombatController.handleInput", e)
        except Exception as e:
            Logger.error("CombatController.handleInput", e)

    def performPlayerAttack(self, baseDamage, actionName, hitMessage, missMessage, isPowerful=False):
        try:
            if self.combat.getPlayerStatus("paralyzed") > 0:
                self.combat.addToCombatLog(f"{self.player.getName()} is paralyzed!")
                self.endPlayerTurn()
                return False

            if self.combat.getPlayerStatus("stunned") > 0:
                self.combat.addToCombatLog(f"{self.player.getName()} is stunned!")
                self.endPlayerTurn()
                return False

            self.player.setCurrentAction(actionName, 30)

            damage = baseDamage if not isPowerful else int(baseDamage * 2.5)

            try:
                drunkenness = self.player.getDrunkenness()
            except Exception:
                drunkenness = 0

            if drunkenness >= 50 and not isPowerful:
                damage = int(damage * 1.5)
                self.combat.addToCombatLog("Drunkenness bonus! (+50% damage)")

            try:
                accuracy = max(20, min(100, int(self.player.getAccuracy() * 100)))
            except Exception:
                accuracy = 50

            if random.randint(1, 100) <= accuracy:
                finalDamage = max(1, int(damage))
                self.enemy.setHealth(max(0, self.enemy.getHealth() - finalDamage))
                self.combat.addToCombatLog(hitMessage.format(player=self.player.getName(), damage=finalDamage))
                Logger.debug("CombatController.performPlayerAttack", "Hit", damage=finalDamage)
                return True
            else:
                self.combat.addToCombatLog(missMessage.format(player=self.player.getName()))
                Logger.debug("CombatController.performPlayerAttack", "Missed")
                return False
        except Exception as e:
            Logger.error("CombatController.performPlayerAttack", e)
            return False

    def playerSimpleAttack(self):
        try:
            baseDamage = self.player.getDamage()
            success = self.performPlayerAttack(
                baseDamage,
                "attacking",
                "{player} strikes with guitar! ({damage} damage)",
                "{player} misses the attack!",
                isPowerful=False,
            )

            if success and self.combat.checkCombatEnd():
                return
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerSimpleAttack", e)

    def playerPowerChord(self):
        try:
            playerHp = self.player.getHealth()
            if playerHp <= 10:
                self.combat.addToCombatLog("Not enough HP for Power Chord! (need 10 HP)")
                return

            self.player.setHealth(playerHp - 10)

            baseDamage = self.player.getDamage()
            success = self.performPlayerAttack(
                baseDamage,
                "attacking",
                "POWER CHORD! {player} deals {damage} damage!",
                "{player} misses the power chord!",
                isPowerful=True,
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
            Logger.debug("CombatController.playerDegueulando", "Executed", drunkennessCost=20)
            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerDegueulando", e)

    def playerDrink(self):
        try:
            if not hasattr(self.player, 'inventory') or not self.player.inventory:
                self.combat.addToCombatLog("No inventory available!")
                return

            selectedBottle = self.player.inventory.getSelectedItem()
            if not selectedBottle:
                self.combat.addToCombatLog("No bottle selected!")
                return

            self.player.setCurrentAction("drinking", 30)
            self.player.drink(selectedBottle)
            drunkenness = self.player.getDrunkenness()
            self.combat.addToCombatLog(f"{self.player.getName()} drinks {selectedBottle.getName()}! (Drunkenness: {drunkenness}%)")
            
            self.player.inventory.consumeSelected()
            
            self.player.setSelectedBottle(self.player.inventory.getSelectedItem())
            
            Logger.debug("CombatController.playerDrink", "Player drank", bottle=selectedBottle.getName(), drunkenness=drunkenness)

            if self.player.getHealth() <= 0:
                self.combat.setDiedFromComa(True)
                self.combat.addToCombatLog(f"ALCOHOLIC COMA! {self.player.getName()} collapses!")
                self.combat.checkCombatEnd()
                return

            self.endPlayerTurn()
        except Exception as e:
            Logger.error("CombatController.playerDrink", e)

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
            heavyDamage = int(self.enemy.getDamage() * 1.8)
            if random.randint(1, 100) <= 60:
                self.enemy.setCurrentAction("attacking", 30)
                self.player.setHealth(max(0, self.player.getHealth() - heavyDamage))
                self.combat.addToCombatLog(f"{self.enemy.getName()} strikes violently! ({heavyDamage} damage)")
                Logger.debug("CombatController.enemyHeavyAttack", "Hit", damage=heavyDamage)
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
