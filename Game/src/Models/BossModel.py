"""
BossModel Module

Represents boss enemies in the game.
Extends CaracterModel with boss-specific scaling functionality based on player level.
"""

from Utils.Logger import Logger
from Models.CaracterModel import CaracterModel
from Models.PlayerModel import PlayerModel


# === BOSS MODEL CLASS ===

class BossModel(CaracterModel):
    """
    Boss character model extending CaracterModel.
    Provides scaling functionality to adjust boss difficulty based on player level.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name, x=175, y=175):
        """
        Initialize the boss model.
        
        Args:
            name: Boss character name
            x: Initial X position
            y: Initial Y position
        """
        try:
            super().__init__(name, x, y)
            Logger.debug("BossModel.__init__", "Boss model initialized", name=name, x=x, y=y)
        except Exception as e:
            Logger.error("BossModel.__init__", e)
            raise

    # === CLASS METHODS ===
    
    @classmethod
    def from_config(cls, boss_config, x=175, y=175):
        """
        Create a BossModel instance from a configuration dictionary.
        Typically loaded from JSON via AssetManager.
        
        Args:
            boss_config: Boss configuration dictionary containing:
                - name: Boss name
                - attributes: dict with base_health, base_damage, base_accuracy
            x: Initial X position
            y: Initial Y position
            
        Returns:
            BossModel: Configured boss instance
        """
        try:
            # Extract boss name from config
            boss_name = boss_config.get("name", "Unknown Boss")
            
            # Create boss instance
            boss = cls(boss_name, x, y)
            
            # Apply attributes if present
            attributes = boss_config.get("attributes", {})
            if attributes:
                health = attributes.get("base_health")
                damage = attributes.get("base_damage")
                accuracy = attributes.get("base_accuracy")
                
                if health is not None:
                    boss.setHealth(health)
                if damage is not None:
                    boss.setDamage(damage)
                if accuracy is not None:
                    boss.setAccuracy(accuracy)
                
                Logger.debug("BossModel.from_config", "Boss created from config",
                           name=boss_name, health=health, damage=damage, accuracy=accuracy)
            
            return boss
        except Exception as e:
            Logger.error("BossModel.from_config", e)
            raise
    
    # === SCALING METHODS ===
    
    def scale(self, player):
        """
        Scale boss stats based on player level.
        Increases boss health and damage proportionally to player level.
        
        Args:
            player: PlayerModel instance to scale against
        """
        try:
            # Validate player type
            if not isinstance(player, PlayerModel):
                raise TypeError("player must be a PlayerModel instance")
            
            # Get player level
            try:
                player_level = player.getLevel()
                if player_level <= 0:
                    player_level = 1  # Minimum level of 1
                Logger.debug("BossModel.scale", "Scaling boss", player_level=player_level)
            except Exception as e:
                Logger.error("BossModel.scale", e)
                player_level = 1  # Default to level 1 if error
            
            # Calculate scaled stats
            try:
                current_health = self.getHealth()
                current_damage = self.getDamage()
                
                scaled_boss_health = current_health * player_level
                scaled_boss_damage = current_damage * player_level
                
                self.setHealth(scaled_boss_health)
                self.setDamage(scaled_boss_damage)
                
                Logger.debug("BossModel.scale", "Boss scaled", 
                           original_health=current_health, 
                           scaled_health=scaled_boss_health,
                           original_damage=current_damage,
                           scaled_damage=scaled_boss_damage)
            except Exception as e:
                Logger.error("BossModel.scale", e)
                raise
                
        except TypeError as e:
            Logger.error("BossModel.scale", e)
        except Exception as e:
            Logger.error("BossModel.scale", e)