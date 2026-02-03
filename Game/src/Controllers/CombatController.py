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
        self.combat = combat_model
        self.player = combat_model.getPlayer()
        self.enemy = combat_model.getEnemy()
        
        self.action_delay = 0  # Délai pour empêcher les actions trop rapides
        self.action_cooldown = 30  # frames (0.5 sec à 60fps)
        
    def update(self):
        """Mettre à jour l'état du combat"""
        # Décrémenter le délai d'action
        if self.action_delay > 0:
            self.action_delay -= 1
        
        # Si c'est le tour de l'ennemi et pas de délai, il attaque automatiquement
        if not self.combat.isPlayerTurn() and self.action_delay == 0:
            self.enemyTurn()
            self.action_delay = self.action_cooldown * 2  # Double délai pour l'ennemi
    
    def handleInput(self, event):
        """Gérer les inputs du joueur"""
        if event.type == pygame.KEYDOWN and self.combat.isPlayerTurn() and self.action_delay == 0:
            
            # Attaque simple (A)
            if event.key == pygame.K_a:
                self.playerSimpleAttack()
                self.action_delay = self.action_cooldown
            
            # Power Chord (P) - Consomme de l'énergie
            elif event.key == pygame.K_p:
                self.playerPowerChord()
                self.action_delay = self.action_cooldown
            
            # Dégueulando (D) - Attaque spéciale liée à l'alcool
            elif event.key == pygame.K_d:
                self.playerDegueulando()
                self.action_delay = self.action_cooldown
            
            # Boire (B) - Augmente les stats
            elif event.key == pygame.K_b:
                self.playerDrink()
                self.action_delay = self.action_cooldown
    
    # === ACTIONS DU JOUEUR ===
    
    def playerSimpleAttack(self):
        """Attaque simple avec la guitare"""
        if self.combat.getPlayerStatus("paralyzed") > 0:
            self.combat.addToCombatLog(f"⚡ {self.player.getName()} est paralysé !")
            self.endPlayerTurn()
            return
        
        if self.combat.getPlayerStatus("stunned") > 0:
            self.combat.addToCombatLog(f"💫 {self.player.getName()} est étourdi !")
            self.endPlayerTurn()
            return
        
        # Calculer les dégâts
        base_damage = self.player.getDamage()
        
        # Bonus d'ivresse (si > 50%)
        drunkenness = self.player.getDrunkenness()
        if drunkenness >= 50:
            base_damage = int(base_damage * 1.5)
            self.combat.addToCombatLog(f"🍺 Bonus d'ivresse ! (+50% dégâts)")
        
        # Malus de précision
        accuracy = self.player.getAccuracy()
        hit_chance = max(20, min(100, accuracy * 100))
        
        if random.randint(1, 100) <= hit_chance:
            # Touché !
            final_damage = max(1, int(base_damage))
            current_hp = self.enemy.getHealth()
            self.enemy.setHealth(max(0, current_hp - final_damage))
            
            self.combat.addToCombatLog(f"🎸 {self.player.getName()} frappe avec sa guitare ! ({final_damage} dégâts)")
            
            # Vérifier fin du combat
            if self.combat.checkCombatEnd():
                return
        else:
            # Raté !
            self.combat.addToCombatLog(f"💨 {self.player.getName()} rate son attaque !")
        
        self.endPlayerTurn()
    
    def playerPowerChord(self):
        """Power Chord - Attaque puissante qui coûte de la santé"""
        if self.combat.getPlayerStatus("paralyzed") > 0:
            self.combat.addToCombatLog(f"⚡ {self.player.getName()} est paralysé !")
            self.endPlayerTurn()
            return
        
        # Coût : 10 HP
        player_hp = self.player.getHealth()
        if player_hp <= 10:
            self.combat.addToCombatLog(f"❌ Pas assez de HP pour le Power Chord !")
            return
        
        self.player.setHealth(player_hp - 10)
        
        # Dégâts énormes
        power_damage = int(self.player.getDamage() * 2.5)
        current_hp = self.enemy.getHealth()
        self.enemy.setHealth(max(0, current_hp - power_damage))
        
        self.combat.addToCombatLog(f"⚡🎸 POWER CHORD ! {power_damage} dégâts !")
        
        # Chance d'étourdir l'ennemi
        if random.randint(1, 100) <= 30:
            self.combat.setEnemyStatus("stunned", 1)
            self.combat.addToCombatLog(f"💫 {self.enemy.getName()} est étourdi !")
        
        # Vérifier fin du combat
        if self.combat.checkCombatEnd():
            return
        
        self.endPlayerTurn()
    
    def playerDegueulando(self):
        """Dégueulando - Vomit sur l'ennemi (nécessite ivresse > 60%)"""
        drunkenness = self.player.getDrunkenness()
        
        if drunkenness < 60:
            self.combat.addToCombatLog(f"❌ Pas assez ivre pour vomir ! (nécessite 60%)")
            return
        
        # Paralyse l'ennemi de dégoût
        self.combat.setEnemyStatus("disgusted", 2)
        self.combat.addToCombatLog(f"🤮 DÉGUEULANDO ! {self.enemy.getName()} est paralysé de dégoût !")
        
        # Réduire l'ivresse
        self.player.setDrunkenness(max(0, drunkenness - 20))
        
        self.endPlayerTurn()
    
    def playerDrink(self):
        """Boire pour augmenter les stats"""
        selected_bottle = self.player.getSelectedBottle()
        
        if not selected_bottle:
            self.combat.addToCombatLog(f"❌ Aucune bouteille sélectionnée !")
            return
        
        # Boire
        self.player.drink(selected_bottle)
        
        drunkenness = self.player.getDrunkenness()
        self.combat.addToCombatLog(f"🍺 {self.player.getName()} boit {selected_bottle.getName()} ! (Ivresse: {drunkenness}%)")
        
        # Vérifier risque de coma
        if self.player.getHealth() <= 0:
            self.combat.addToCombatLog(f"💀 COMA ÉTHYLIQUE ! {self.player.getName()} s'effondre...")
            self.combat.checkCombatEnd()
            return
        
        self.endPlayerTurn()
    
    # === TOUR DE L'ENNEMI ===
    
    def enemyTurn(self):
        """IA simple pour le tour de l'ennemi"""
        if self.combat.getEnemyStatus("paralyzed") > 0 or self.combat.getEnemyStatus("disgusted") > 0:
            self.combat.addToCombatLog(f"😵 {self.enemy.getName()} est incapable d'agir !")
            self.endEnemyTurn()
            return
        
        if self.combat.getEnemyStatus("stunned") > 0:
            self.combat.addToCombatLog(f"💫 {self.enemy.getName()} est étourdi !")
            self.endEnemyTurn()
            return
        
        # IA aléatoire simple
        action = random.choice(["attack", "attack", "heavy_attack"])  # Plus de chances d'attaque normale
        
        if action == "attack":
            self.enemySimpleAttack()
        else:
            self.enemyHeavyAttack()
    
    def enemySimpleAttack(self):
        """Attaque simple de l'ennemi"""
        damage = self.enemy.getDamage()
        
        # Précision de l'ennemi
        accuracy = self.enemy.getAccuracy()
        hit_chance = max(20, min(100, accuracy * 100))
        
        if random.randint(1, 100) <= hit_chance:
            current_hp = self.player.getHealth()
            self.player.setHealth(max(0, current_hp - damage))
            
            self.combat.addToCombatLog(f"👊 {self.enemy.getName()} attaque ! ({damage} dégâts)")
            
            # Vérifier fin du combat
            if self.combat.checkCombatEnd():
                return
        else:
            self.combat.addToCombatLog(f"💨 {self.enemy.getName()} rate son attaque !")
        
        self.endEnemyTurn()
    
    def enemyHeavyAttack(self):
        """Attaque lourde de l'ennemi"""
        heavy_damage = int(self.enemy.getDamage() * 1.8)
        
        # Moins précis
        if random.randint(1, 100) <= 60:
            current_hp = self.player.getHealth()
            self.player.setHealth(max(0, current_hp - heavy_damage))
            
            self.combat.addToCombatLog(f"💥 {self.enemy.getName()} frappe violemment ! ({heavy_damage} dégâts)")
            
            # Chance d'étourdir le joueur
            if random.randint(1, 100) <= 25:
                self.combat.setPlayerStatus("stunned", 1)
                self.combat.addToCombatLog(f"💫 {self.player.getName()} est étourdi !")
            
            # Vérifier fin du combat
            if self.combat.checkCombatEnd():
                return
        else:
            self.combat.addToCombatLog(f"💨 {self.enemy.getName()} rate son attaque lourde !")
        
        self.endEnemyTurn()
    
    # === FIN DE TOUR ===
    
    def endPlayerTurn(self):
        """Fin du tour du joueur"""
        self.combat.applyBleedingDamage()
        self.combat.decrementStatusEffects()
        self.combat.switchTurn()
    
    def endEnemyTurn(self):
        """Fin du tour de l'ennemi"""
        self.combat.applyBleedingDamage()
        self.combat.decrementStatusEffects()
        self.combat.switchTurn()