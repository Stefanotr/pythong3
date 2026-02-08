import pygame
from Utils.Logger import Logger
from Models.PlayerModel import PlayerModel

class CaracterView:

    def __init__(self, image_path, base_name ="", sprite_size =None, character_config =None, game_mode ="combat"):

        try:
            self.base_image_path = image_path
            self.base_name = base_name
            self.character_config = character_config  
            self.game_mode = game_mode
            
            if sprite_size:
                self.sprite_size = sprite_size
            elif character_config and 'sizes' in character_config:
                mode_sizes = character_config['sizes'].get(game_mode, {})
                if mode_sizes:
                    self.sprite_size = (mode_sizes.get('width', 200), mode_sizes.get('height', 200))
                else:
                    self.sprite_size = (200, 200)  
            else:
                self.sprite_size = sprite_size or (200, 200)  
            
            self.sprite = None
            self.action_sprites = {}  
            
            self.animation_frame = 0  
            self.animation_speed = 8  
            
            self.loadSprite(image_path)
            
            try:
                self.font = pygame.font.SysFont(None, 36)
                self.small_font = pygame.font.SysFont(None, 18)  
                self.big_font = pygame.font.SysFont(None, 32)  
                Logger.debug("CaracterView.__init__", "Fonts initialized")
            except Exception as e:
                Logger.error("CaracterView.__init__", e)
                
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 18)
                
        except Exception as e:
            Logger.error("CaracterView.__init__", e)
            raise

    def loadSprite(self, image_path):

        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            
            self.sprite = pygame.transform.scale(original_image, self.sprite_size)
            Logger.debug("CaracterView.loadSprite", "Character image loaded", image_path =image_path, size=self.sprite_size)
        except FileNotFoundError as e:
            Logger.error("CaracterView.loadSprite", f"Image not found: {image_path}")
            
            self.sprite = pygame.Surface(self.sprite_size)
            self.sprite.fill((255, 0, 255))
            Logger.debug("CaracterView.loadSprite", "Using default character sprite")
        except Exception as e:
            Logger.error("CaracterView.loadSprite", e)

    def resetToBaseSprite(self):

        try:
            
            self.action_sprites = {}
            
            self.loadSprite(self.base_image_path)
            Logger.debug("CaracterView.resetToBaseSprite", "Sprite reset to base image", base=self.base_image_path)
        except Exception as e:
            Logger.error("CaracterView.resetToBaseSprite", e)

    def getActionImagePath(self, base_name, action):

        if self.character_config and 'actions' in self.character_config:
            actions_config = self.character_config['actions']
            if action in actions_config:
                image_path = actions_config[action]
                Logger.debug("CaracterView.getActionImagePath", 
                            f"Loaded from JSON config: {base_name}.{action} = {image_path}")
                return image_path
            else:
                Logger.debug("CaracterView.getActionImagePath",
                            f"Action '{action}' not found in JSON config for {base_name}")
        else:
            Logger.debug("CaracterView.getActionImagePath",
                        f"No character_config available for {base_name} (config is {'None' if not self.character_config else 'missing actions'})")
        
        try:
            from Utils.AssetManager import AssetManager
            
            if base_name in ["agent", "manager", "motard", "grosBill"]:
                asset_manager = AssetManager()
                
                boss_names = {
                    "agent": "Security Agent",
                    "manager": "Manager Corrompu",
                    "motard": "Gros Bill",
                    "grosBill": "Gros Bill"
                }
                
                boss_name = boss_names.get(base_name, base_name)
                try:
                    boss_config = asset_manager.getBossByBame(boss_name)
                    if boss_config and 'actions' in boss_config:
                        if action in boss_config['actions']:
                            image_path = boss_config['actions'][action]
                            Logger.debug("CaracterView.getActionImagePath",
                                        f"Loaded from boss config: {boss_name}.{action} = {image_path}")
                            return image_path
                except Exception as e:
                    Logger.debug("CaracterView.getActionImagePath",
                                f"Failed to load from boss config: {e}")
        except ImportError as e:
            Logger.debug("CaracterView.getActionImagePath",
                        f"AssetManager not available: {e}")
        
        action_map = {
            
            "lola": {
                "idle": "Game/Assets/lola.png",
                "drinking": "Game/Assets/lolaquiboit (1).png",
                "attacking": "Game/Assets/lolaquilancesabasse (1).png",
                "dodging": "Game/Assets/lolaquisebaisse (2).png",
                
                "movingLeft": [
                    "Game/Assets/lolacoursgauche.png",
                    "Game/Assets/lolagaucheframe1.png"
                ],
                
                "movingRight": [
                    "Game/Assets/lolacoursdroite.png",
                    "Game/Assets/lola.png"
                ],
                
                "musique": [
                    "Game/Assets/lolamusique1.png",
                    "Game/Assets/lolamusique2.png",
                    "Game/Assets/lolamusique3.png"
                ]
            },
            
            "agent": {
                "idle": "Game/Assets/Agentdesecurité.png",
                "attacking": "Game/Assets/agentdesecuritquitape (1).png",
                "dodging": "Game/Assets/agentdesecuritequisebaisse (1).png"
            },
            
            "manager": {
                "idle": "Game/Assets/ManagerCorrompu.png",
                "attacking": "Game/Assets/managerquitape (1).png",
                "dodging": "Game/Assets/managercorrompuquisebaisse (1).png"
            },
            
            "motard": {
                "idle": "Game/Assets/chefdesmotards.png",
                "attacking": "Game/Assets/motardquidonnedescoupsdepieds (1).png",
                "dodging": "Game/Assets/motardquisebaisse (1).png"
            }
        }
        
        if base_name in action_map and action in action_map[base_name]:
            return action_map[base_name][action]
        return None

    def updateCharacterSprite(self, character):

        if not self.base_name:
            return  
        
        action = character.getCurrentAction()
        
        action_paths = self.getActionImagePath(self.base_name, action)
        if not action_paths:
            
            self.sprite = self.loadSpriteForPath(self.base_image_path)
            return
        
        if isinstance(action_paths, list):
            
            frame_index = (self.animation_frame // self.animation_speed) % len(action_paths)
            action_path = action_paths[frame_index]
            cache_key = f"{self.base_name}_{action}_{frame_index}"
        else:
            
            action_path = action_paths
            cache_key = f"{self.base_name}_{action}"
        
        if cache_key in self.action_sprites:
            self.sprite = self.action_sprites[cache_key]
            return
        
        if action_path:
            try:
                original_image = pygame.image.load(action_path).convert_alpha()
                sprite = pygame.transform.scale(original_image, self.sprite_size)
                self.action_sprites[cache_key] = sprite  
                self.sprite = sprite
                Logger.debug("CaracterView.updateCharacterSprite", 
                           f"Sprite updated for action: {action}", baseName =self.base_name)
            except Exception as e:
                Logger.error("CaracterView.updateCharacterSprite", e)
        else:
            
            self.sprite = self.loadSpriteForPath(self.base_image_path)

    def loadSpriteForPath(self, path):

        try:
            original_image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(original_image, self.sprite_size)
        except Exception as e:
            Logger.error("CaracterView.loadSpriteForPath", e)
            sprite = pygame.Surface(self.spriteSize)
            sprite.fill((255, 0, 255))
            return sprite

    def drawCaracter(self, screen, caracter, offset=(0, 0), is_map =False):

        try:
            
            self.animation_frame += 1
            
            if self.base_name:
                self.updateCharacterSprite(caracter)
                caracter.updateActionTimer()
            
            try:
                x = caracter.getX()
                y = caracter.getY()
            except Exception as e:
                Logger.error("CaracterView.drawCaracter", e)
                return

            offset_x, offset_y = offset
            sprite_w, sprite_h = self.sprite.get_size()
            draw_x = int(x + offset_x - sprite_w // 2)
            draw_y = int(y + offset_y - sprite_h // 2)

            try:
                screen.blit(self.sprite, (draw_x, draw_y))
            except Exception as e:
                Logger.error("CaracterView.drawCaracter", e)

            if is_map:
                try:
                    name = caracter.getName()
                    
                    name_font = self.big_font if self.game_mode in ["rhythm", "rhythmCombat"] else self.small_font
                    name_surface = name_font.render(name, True, (255, 255, 255))
                    name_x = draw_x + sprite_w // 2 - name_surface.get_width() // 2
                    name_y = draw_y - name_surface.get_height() - 5
                    screen.blit(name_surface, (name_x, name_y))
                except Exception as e:
                    Logger.error("CaracterView.drawCaracter", e)

        except Exception as e:
            Logger.error("CaracterView.drawCaracter", e)
