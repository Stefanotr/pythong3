import pygame
from Utils.Logger import Logger


class TileModel:

    def __init__(self, name, image, is_solid):
        try:
            self.name = name
            self.is_solid = is_solid
            
            try:
                surf = pygame.image.load(image)
                try:
                    self.image = surf.convert_alpha()
                    Logger.debug("TileModel.__init__", f"Tile loaded: {name}")
                except Exception:
                    try:
                        surf2 = surf.convert()
                        col = surf2.get_at((0, 0))
                        surf2.set_colorkey(col)
                        self.image = surf2
                    except Exception:
                        self.image = surf
            except FileNotFoundError:
                self.image = pygame.Surface((32, 32))
                self.image.fill((128, 128, 128))
                Logger.debug("TileModel.__init__", f"Default tile created for {name}")
                
        except Exception as e:
            Logger.error("TileModel.__init__", e)
            raise


    def getName(self):
        try:
            return self.name
        except Exception as e:
            Logger.error("TileModel.getName", e)
            return ""

    def setName(self, name):
        try:
            self.name = str(name)
        except Exception as e:
            Logger.error("TileModel.setName", e)


    def getImage(self):
        try:
            return self.image
        except Exception as e:
            Logger.error("TileModel.getImage", e)
            default = pygame.Surface((32, 32))
            default.fill((128, 128, 128))
            return default

    def setImage(self, image):
        try:
            if isinstance(image, str):
                surf = pygame.image.load(image)
                try:
                    self.image = surf.convert_alpha()
                except Exception:
                    try:
                        surf2 = surf.convert()
                        col = surf2.get_at((0, 0))
                        surf2.set_colorkey(col)
                        self.image = surf2
                    except Exception:
                        self.image = surf
            elif isinstance(image, pygame.Surface):
                self.image = image
            else:
                Logger.error("TileModel.setImage", "Image must be path or Surface")
        except Exception as e:
            Logger.error("TileModel.setImage", e)


    def getIsSolid(self):
        try:
            return self.isSolid
        except Exception as e:
            Logger.error("TileModel.getIsSolid", e)
            return False

    def setIsSolid(self, isSolid):
        try:
            self.is_solid = bool(is_solid)
        except Exception as e:
            Logger.error("TileModel.setIsSolid", e)
