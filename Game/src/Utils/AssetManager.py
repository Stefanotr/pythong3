import json
import os
from pathlib import Path
from Utils.Logger import Logger


class AssetManager:

    CONFIG_DIR = "Assets"
    PROGRESSION_DIR = "Progression"
    BOSSES_CONFIG_FILE = "bosses_config.json"
    PLAYER_CONFIG_FILE = "player_config.json"
    GAME_MODES = ["map", "dialogue", "combat", "rhythm", "rhythm_combat"]

    def __init__(self, base_path="Game"):
        try:
            self.base_path = base_path
            self.config_dir = os.path.join(base_path, self.CONFIG_DIR)
            self.progression_dir = os.path.join(base_path, self.PROGRESSION_DIR)
            os.makedirs(self.config_dir, exist_ok=True)
            os.makedirs(self.progression_dir, exist_ok=True)
            self.bosses_config_path = os.path.join(self.config_dir, self.BOSSES_CONFIG_FILE)
            self.player_config_path = os.path.join(self.config_dir, self.PLAYER_CONFIG_FILE)
            
            Logger.debug("AssetManager.__init__", "AssetManager initialized", 
                        base_path=base_path,
                        config_dir=self.config_dir,
                        progression_dir=self.progression_dir)
        except Exception as e:
            Logger.error("AssetManager.__init__", e)
            raise

    def loadBossesConfig(self):
        """
        Load boss configuration from JSON file.
        
        Returns:
            dict: Boss configuration data
        """
        try:
            if not os.path.exists(self.bosses_config_path):
                Logger.warn("AssetManager.loadBossesConfig", 
                           f"Boss config file not found: {self.bosses_config_path}")
                return {}
            
            with open(self.bosses_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                Logger.debug("AssetManager.loadBossesConfig", 
                           f"Loaded boss config with {len(config.get('bosses', []))} bosses")
                return config
        except json.JSONDecodeError as e:
            Logger.error("AssetManager.loadBossesConfig", f"Invalid JSON: {e}")
            return {}
        except Exception as e:
            Logger.error("AssetManager.loadBossesConfig", e)
            return {}
    
    def saveBossesConfig(self, config):
        """
        Save boss configuration to JSON file.
        
        Args:
            config: Boss configuration data
        """
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.bosses_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                Logger.debug("AssetManager.saveBossesConfig", 
                           f"Saved boss config to {self.bosses_config_path}")
        except Exception as e:
            Logger.error("AssetManager.saveBossesConfig", e)
            raise
    
    def getBossByBame(self, boss_name):
        """
        Get a specific boss configuration by name.
        
        Args:
            boss_name: Name of the boss
            
        Returns:
            dict: Boss configuration or None if not found
        """
        try:
            config = self.loadBossesConfig()
            bosses = config.get("bosses", [])
            
            for boss in bosses:
                if boss.get("name") == boss_name:
                    return boss
            
            Logger.warn("AssetManager.getBossByBame", f"Boss not found: {boss_name}")
            return None
        except Exception as e:
            Logger.error("AssetManager.getBossByBame", e)
            return None
    
    def getBossByAct(self, act_num):
        """
        Get boss configuration for a specific act.
        
        Args:
            act_num: Act number (1, 2, 3, etc.)
            
        Returns:
            dict: Boss configuration or None if not found
        """
        try:
            config = self.loadBossesConfig()
            bosses = config.get("bosses", [])
            
            for boss in bosses:
                if boss.get("act") == act_num:
                    return boss
            
            Logger.warn("AssetManager.getBossByAct", f"Boss not found for act: {act_num}")
            return None
        except Exception as e:
            Logger.error("AssetManager.getBossByAct", e)
            return None
    

    def loadPlayerConfig(self):
        """
        Load player base configuration from JSON file.
        
        Returns:
            dict: Player configuration data (the 'player' object from JSON)
        """
        try:
            if not os.path.exists(self.player_config_path):
                Logger.warn("AssetManager.loadPlayerConfig", 
                           f"Player config file not found: {self.player_config_path}")
                return {}
            
            with open(self.player_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                player_data = config.get('player', {})
                Logger.debug("AssetManager.loadPlayerConfig", 
                           f"Loaded player config with {len(player_data.get('actions', {}))} actions")
                return player_data
        except json.JSONDecodeError as e:
            Logger.error("AssetManager.loadPlayerConfig", f"Invalid JSON: {e}")
            return {}
        except Exception as e:
            Logger.error("AssetManager.loadPlayerConfig", e)
            return {}
    
    def save_player_config(self, config):
        """
        Save player configuration to JSON file.
        
        Args:
            config: Player configuration data
        """
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.player_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                Logger.debug("AssetManager.save_player_config", 
                           f"Saved player config to {self.player_config_path}")
        except Exception as e:
            Logger.error("AssetManager.save_player_config", e)
            raise
    

    def save_player_progression(self, player_name, progression_data):
        """
        Save player progression data.
        
        Args:
            player_name: Name of the player (used as filename)
            progression_data: Player progression data (dict)
        """
        try:
            os.makedirs(self.progression_dir, exist_ok=True)
            safe_name = "".join(c for c in player_name if c.isalnum() or c in (' ', '_')).rstrip()
            progression_file = os.path.join(self.progression_dir, f"{safe_name}_progression.json")
            
            with open(progression_file, 'w', encoding='utf-8') as f:
                json.dump(progression_data, f, indent=4, ensure_ascii=False)
                Logger.debug("AssetManager.save_player_progression", 
                           f"Saved progression for {player_name}", 
                           file=progression_file)
        except Exception as e:
            Logger.error("AssetManager.save_player_progression", e)
            raise
    
    def load_player_progression(self, player_name):
        """
        Load player progression data.
        
        Args:
            player_name: Name of the player
            
        Returns:
            dict: Progression data or empty dict if not found
        """
        try:
            safe_name = "".join(c for c in player_name if c.isalnum() or c in (' ', '_')).rstrip()
            progression_file = os.path.join(self.progression_dir, f"{safe_name}_progression.json")
            
            if not os.path.exists(progression_file):
                Logger.warn("AssetManager.load_player_progression", 
                           f"Progression file not found for {player_name}")
                return {}
            
            with open(progression_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                Logger.debug("AssetManager.load_player_progression", 
                           f"Loaded progression for {player_name}")
                return data
        except json.JSONDecodeError as e:
            Logger.error("AssetManager.load_player_progression", f"Invalid JSON: {e}")
            return {}
        except Exception as e:
            Logger.error("AssetManager.load_player_progression", e)
            return {}
    
    def list_saved_progressions(self):
        """
        List all saved player progressions.
        
        Returns:
            list: List of player names with saved progression
        """
        try:
            if not os.path.exists(self.progression_dir):
                return []
            
            saved_players = []
            for file in os.listdir(self.progression_dir):
                if file.endswith("_progression.json"):
                    player_name = file.replace("_progression.json", "")
                    saved_players.append(player_name)
            
            return saved_players
        except Exception as e:
            Logger.error("AssetManager.list_saved_progressions", e)
            return []
    

    def get_asset_image_path(self, asset_path):
        """
        Normalize asset image path (for cross-platform compatibility).
        
        Args:
            asset_path: Relative asset path (e.g., "Game/Assets/lola.png")
            
        Returns:
            str: Normalized asset path
        """
        try:
            return asset_path.replace("\\", "/")
        except Exception as e:
            Logger.error("AssetManager.get_asset_image_path", e)
            return asset_path
    
    def asset_exists(self, asset_path):
        """
        Check if an asset file exists.
        
        Args:
            asset_path: Path to asset (relative to project root)
            
        Returns:
            bool: True if asset exists
        """
        try:
            return os.path.exists(asset_path)
        except Exception as e:
            Logger.error("AssetManager.asset_exists", e)
            return False

