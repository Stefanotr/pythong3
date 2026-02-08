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
    
    def savePlayerConfig(self, config):
        
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.player_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                Logger.debug("AssetManager.savePlayerConfig", 
                           f"Saved player config to {self.player_config_path}")
        except Exception as e:
            Logger.error("AssetManager.savePlayerConfig", e)
            raise
    

    def savePlayerProgression(self, player_name, progression_data):
        
        try:
            os.makedirs(self.progression_dir, exist_ok=True)
            safe_name = "".join(c for c in player_name if c.isalnum() or c in (' ', '_')).rstrip()
            progression_file = os.path.join(self.progression_dir, f"{safe_name}_progression.json")
            
            with open(progression_file, 'w', encoding='utf-8') as f:
                json.dump(progression_data, f, indent=4, ensure_ascii=False)
                Logger.debug("AssetManager.savePlayerProgression", 
                           f"Saved progression for {player_name}", 
                           file=progression_file)
        except Exception as e:
            Logger.error("AssetManager.savePlayerProgression", e)
            raise
    
    def loadPlayerProgression(self, player_name):
        
        try:
            safe_name = "".join(c for c in player_name if c.isalnum() or c in (' ', '_')).rstrip()
            progression_file = os.path.join(self.progression_dir, f"{safe_name}_progression.json")
            
            if not os.path.exists(progression_file):
                Logger.warn("AssetManager.loadPlayerProgression", 
                           f"Progression file not found for {player_name}")
                return {}
            
            with open(progression_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                Logger.debug("AssetManager.loadPlayerProgression", 
                           f"Loaded progression for {player_name}")
                return data
        except json.JSONDecodeError as e:
            Logger.error("AssetManager.loadPlayerProgression", f"Invalid JSON: {e}")
            return {}
        except Exception as e:
            Logger.error("AssetManager.loadPlayerProgression", e)
            return {}
    
    def listSavedProgressions(self):
        
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
            Logger.error("AssetManager.listSavedProgressions", e)
            return []
    

    def getAssetImagePath(self, asset_path):
   
        try:
            return asset_path.replace("\\", "/")
        except Exception as e:
            Logger.error("AssetManager.getAssetImagePath", e)
            return asset_path
    
    def assetExists(self, asset_path):
       
        try:
            return os.path.exists(asset_path)
        except Exception as e:
            Logger.error("AssetManager.assetExists", e)
            return False

