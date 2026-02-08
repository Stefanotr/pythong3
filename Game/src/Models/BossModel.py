
        try:
            super().__init__(name, x, y)
            Logger.debug("BossModel.__init__", "Boss model initialized", name=name, x=x, y=y)
        except Exception as e:
            Logger.error("BossModel.__init__", e)
            raise

    
    @classmethod
    def from_config(cls, boss_config, x=175, y=175):
        try:
            boss_name = boss_config.get("name", "Unknown Boss")
            
            boss = cls(boss_name, x, y)
            
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
    
    
    def scale(self, player):
        try:
            if not isinstance(player, PlayerModel):
                raise TypeError("player must be a PlayerModel instance")
            
            try:
                player_level = player.getLevel()
                if player_level <= 0:
                    player_level = 1
                Logger.debug("BossModel.scale", "Scaling boss", player_level=player_level)
            except Exception as e:
                Logger.error("BossModel.scale", e)
                player_level = 1
            
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