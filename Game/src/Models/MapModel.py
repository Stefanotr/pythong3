"""
MapModel Module

Represents the game map loaded from a file.
Manages tile data, tile types, and map dimensions.
"""

import pygame
from Utils.Logger import Logger


class MapModel:

    def __init__(self, mapFile, tileKinds, tileSize):
        """
        Initialize the map model by loading map data from file.
        
        Args:
            map_file: Path to the map file
            tile_kinds: List of TileModel instances representing tile types
            tile_size: Size of each tile in pixels
        """
        try:
            self.tile_kinds = tileKinds
            self.tile_size = tileSize
            Logger.debug("MapModel.__init__", "Loading map", mapFile=mapFile, tileSize=tileSize)
            
            try:
                with open(mapFile, "r") as file:
                    data = file.read()
                Logger.debug("MapModel.__init__", "Map file read successfully", mapFile=mapFile)
            except FileNotFoundError as e:
                Logger.error("MapModel.__init__", e)
                self.tiles = []
                raise
            except Exception as e:
                Logger.error("MapModel.__init__", e)
                self.tiles = []
                raise
            
            try:
                self.tiles = []
                if str(mapFile).lower().endswith('.tmx'):
                    import os
                    import xml.etree.ElementTree as ET

                    tmxPath = mapFile
                    tmxDir = os.path.dirname(tmxPath)

                    root = ET.fromstring(data)
                    width = int(root.attrib.get('width', 0))
                    height = int(root.attrib.get('height', 0))
                    tilewidth = int(root.attrib.get('tilewidth', 32))
                    tileheight = int(root.attrib.get('tileheight', 32))
                    self.tile_size = tilewidth

                    layers = []
                    layersByName = {}
                    flipLayers = []
                    FLIP_H = 0x80000000
                    FLIP_V = 0x40000000
                    FLIP_D = 0x20000000
                    
                    for layer in root.findall('layer'):
                        layerName = layer.attrib.get('name', '')
                        dataElem = layer.find('data')
                        if dataElem is None or dataElem.text is None:
                            matrix = [[0]*width for _ in range(height)]
                            flips = [[0]*width for _ in range(height)]
                            layers.append((layerName, matrix))
                            flipLayers.append((layerName, flips))
                            layersByName[layerName] = matrix
                            continue
                        csv = dataElem.text.strip()
                        nums = [int(n) for n in csv.replace('\n', ',').split(',') if n.strip()]
                        matrix = []
                        flips = []
                        for r in range(height):
                            row = []
                            flipRow = []
                            for c in range(width):
                                idx = r * width + c
                                if idx < len(nums):
                                    gid = nums[idx]
                                    flipFlags = 0
                                    if gid & FLIP_H:
                                        flipFlags |= 1
                                    if gid & FLIP_V:
                                        flipFlags |= 2
                                    if gid & FLIP_D:
                                        flipFlags |= 4
                                    gid = gid & ~(FLIP_H | FLIP_V | FLIP_D)
                                    row.append(gid)
                                    flipRow.append(flipFlags)
                                else:
                                    row.append(0)
                                    flipRow.append(0)
                            matrix.append(row)
                            flips.append(flipRow)
                        layers.append((layerName, matrix))
                        flipLayers.append((layerName, flips))
                        layersByName[layerName] = matrix

                    self.flip_layers = {name: flips for name, flips in flip_layers}

                    merged = [[0 for _ in range(width)] for _ in range(height)]
                    mergedFlips = [[0 for _ in range(width)] for _ in range(height)]
                    for i, (_name, layer) in enumerate(layers):
                        flipLayer = flipLayers[i][1] if i < len(flipLayers) else None
                        for y in range(height):
                            for x in range(width):
                                gid = layer[y][x]
                                if gid:
                                    merged[y][x] = gid
                                    if flipLayer:
                                        mergedFlips[y][x] = flipLayer[y][x]

                    self.tiles = merged
                    self.tileFlips = mergedFlips
                    self.layers = layersByName
                    self.layerOrdered = layers
                    self.width = width
                    self.height = height
                    self.tilewidth = tilewidth
                    self.tileheight = tileheight

                    self.objectLayers = {}
                    for objgroup in root.findall('objectgroup'):
                        layerName = objgroup.attrib.get('name', '')
                        objs = []
                        for obj in objgroup.findall('object'):
                            try:
                                ox = int(float(obj.attrib.get('x', 0)))
                                oy = int(float(obj.attrib.get('y', 0)))
                                ow = int(float(obj.attrib.get('width', 0)))
                                oh = int(float(obj.attrib.get('height', 0)))
                                gid = obj.attrib.get('gid')
                                objname = obj.attrib.get('name', '')
                                otype = obj.attrib.get('type', '')
                                props = {}
                                propsElem = obj.find('properties')
                                if propsElem is not None:
                                    for prop in propsElem.findall('property'):
                                        props[prop.attrib.get('name')] = prop.attrib.get('value', prop.attrib.get('type'))
                                objs.append({'x': ox, 'y': oy, 'width': ow, 'height': oh, 'gid': gid, 'name': objname, 'type': otype, 'properties': props})
                            except Exception:
                                continue
                        self.objectLayers[layerName] = objs

                    self.tile_kinds = {}
                    self.tilesets = []
                    tilesetElems = root.findall('tileset')
                    
                    for tilesetElem in tilesetElems:
                        source = tilesetElem.attrib.get('source')
                        firstgid = int(tilesetElem.attrib.get('firstgid', 1))
                        tsxPath = os.path.join(tmxDir, source) if source else None
                        if not tsxPath or not os.path.exists(tsxPath):
                            tsxGuess = os.path.join(os.path.dirname(tmxDir), source) if source else None
                            if tsxGuess and os.path.exists(tsxGuess):
                                tsxPath = tsxGuess

                        imageSurface = None
                        tilesetColumns = 0
                        tilesetTilecount = 0
                        if tsxPath and os.path.exists(tsxPath):
                            try:
                                tsxData = open(tsxPath, 'r', encoding='utf-8').read()
                                tsxRoot = ET.fromstring(tsxData)
                                imageElem = tsxRoot.find('image')
                                if imageElem is not None:
                                    imgSrc = imageElem.attrib.get('source')
                                    imgPath = os.path.join(os.path.dirname(tsxPath), imgSrc)
                                    if not os.path.exists(imgPath):
                                        alt = os.path.join(os.path.dirname(os.path.dirname(tsxPath)), imgSrc)
                                        if os.path.exists(alt):
                                            imgPath = alt

                                    if os.path.exists(imgPath):
                                        try:
                                            surf = pygame.image.load(imgPath)
                                            try:
                                                imageSurface = surf.convert_alpha()
                                                Logger.debug('MapModel.__init__', 'TSX image loaded with alpha', path=imgPath)
                                            except Exception:
                                                try:
                                                    surf2 = surf.convert()
                                                    col = surf2.get_at((0, 0))
                                                    surf2.set_colorkey(col)
                                                    imageSurface = surf2
                                                    Logger.debug('MapModel.__init__', 'TSX image loaded without alpha - colorkey set', path=imgPath, colorkey=col)
                                                except Exception:
                                                    imageSurface = None
                                        except Exception:
                                            imageSurface = None
                                    else:
                                        try:
                                            basename = os.path.basename(imgSrc)
                                            searchRoot = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(tmxPath)))) if os.path.dirname(os.path.dirname(os.path.dirname(tmxPath))) else os.path.dirname(tmxPath)
                                            found = None
                                            for rootDir, dirs, files in os.walk(searchRoot):
                                                if basename in files:
                                                    candidate = os.path.join(rootDir, basename)
                                                    try:
                                                        surf = pygame.image.load(candidate)
                                                        try:
                                                            imageSurface = surf.convert_alpha()
                                                            found = candidate
                                                            Logger.debug('MapModel.__init__', 'Found TSX image by basename search (alpha)', candidate=candidate)
                                                            break
                                                        except Exception:
                                                            try:
                                                                surf2 = surf.convert()
                                                                col = surf2.get_at((0, 0))
                                                                surf2.set_colorkey(col)
                                                                imageSurface = surf2
                                                                found = candidate
                                                                Logger.debug('MapModel.__init__', 'Found TSX image by basename search (colorkey)', candidate=candidate, colorkey=col)
                                                                break
                                                            except Exception:
                                                                continue
                                                    except Exception:
                                                        continue
                                            if not found:
                                                Logger.debug('MapModel.__init__', 'TSX image not found (fallback search failed)', expected=os.path.join(os.path.dirname(tsxPath), imgSrc))
                                        except Exception as e:
                                            Logger.error('MapModel.__init__', e)

                                tilesetColumns = int(tsxRoot.attrib.get('columns', 0))
                                tilesetTilecount = int(tsxRoot.attrib.get('tilecount', 0))
                                if imageSurface is not None:
                                    try:
                                        imgW, imgH = imageSurface.get_size()
                                        inferredColumns = imgW // tilewidth if tilewidth > 0 else 0
                                        inferredRows = imgH // tileheight if tileheight > 0 else 0
                                        inferredTilecount = inferredColumns * inferredRows
                                        if inferredColumns > 0 and tilesetColumns != inferredColumns:
                                            Logger.debug('MapModel.__init__', 'Tileset columns mismatch - using inferred value', tsxColumns=tilesetColumns, inferredColumns=inferredColumns)
                                            tilesetColumns = inferredColumns
                                        if inferredTilecount > 0 and tilesetTilecount != inferredTilecount:
                                            Logger.debug('MapModel.__init__', 'Tileset tilecount mismatch - using inferred value', tsxTilecount=tilesetTilecount, inferredTilecount=inferredTilecount)
                                            tilesetTilecount = inferredTilecount
                                    except Exception as e:
                                        Logger.error('MapModel.__init__', e)
                            except Exception as e:
                                Logger.error('MapModel.__init__', e)

                        columns = tilesetColumns if tilesetColumns > 0 else max(1, (tilesetTilecount or 0))
                        for gidIndex in range(tilesetTilecount):
                            gid = firstgid + gidIndex
                            try:
                                if imageSurface:
                                    col = gidIndex % columns
                                    row = gidIndex // columns
                                    rect = pygame.Rect(col * tilewidth, row * tileheight, tilewidth, tileheight)
                                    tileSurf = pygame.Surface((tilewidth, tileheight), pygame.SRCALPHA, 32)
                                    tileSurf.blit(imageSurface, (0, 0), rect)
                                    try:
                                        tileSurf = tileSurf.convert_alpha()
                                    except Exception:
                                        pass
                                else:
                                    tileSurf = pygame.Surface((tilewidth, tileheight))
                                    color = ((gid * 37) % 256, (gid * 61) % 256, (gid * 97) % 256)
                                    tileSurf.fill(color)
                                class _Tile:
                                    def __init__(self, image):
                                        self.image = image
                                self.tileKinds[gid] = _Tile(tileSurf)
                            except Exception:
                                continue
                        
                        self.tilesets.append({
                            'firstgid': firstgid,
                            'source': source,
                            'tilecount': tilesetTilecount,
                            'columns': tilesetColumns
                        })

                    try:
                        usedGids = set()
                        for row in self.tiles:
                            for v in row:
                                if isinstance(v, int) and v > 0:
                                    usedGids.add(v)
                        missing = [g for g in sorted(usedGids) if g not in self.tileKinds]
                        if missing:
                            Logger.debug('MapModel.__init__', 'Missing GIDs found - creating placeholders', missingCount=len(missing), missingSample=missing[:20])
                        for gid in missing:
                            try:
                                tileSurf = pygame.Surface((tilewidth, tileheight))
                                color = ((gid * 37) % 256, (gid * 61) % 256, (gid * 97) % 256)
                                tileSurf.fill(color)
                                class _Tile2:
                                    def __init__(self, image):
                                        self.image = image
                                self.tileKinds[gid] = _Tile2(tileSurf)
                            except Exception:
                                continue
                    except Exception as e:
                        Logger.error('MapModel.__init__', e)

                    Logger.debug("MapModel.__init__", "TMX map parsed successfully", width=width, height=height, tilewidth=tilewidth, tileheight=tileheight, tilesets=len(self.tilesets), objectLayers=list(self.objectLayers.keys()))

                else:
                    self.tileKinds = {}
                    self.tileFlips = []
                    for line in data.split("\n"):
                        if line.strip():
                            row = []
                            for tileNumber in line:
                                try:
                                    row.append(int(tileNumber))
                                except ValueError:
                                    Logger.debug("MapModel.__init__", "Invalid tile number, skipping", tile=tileNumber)
                                    continue
                            if row:
                                self.tiles.append(row)
                    Logger.debug("MapModel.__init__", "Map parsed successfully", 
                               rows=len(self.tiles), 
                               cols=len(self.tiles[0]) if self.tiles else 0)
            except Exception as e:
                Logger.error("MapModel.__init__", e)
                self.tiles = []
                raise
                
        except Exception as e:
            Logger.error("MapModel.__init__", e)
            raise
    
    def getTileKinds(self):
        try:
            return self.tileKinds.copy() if hasattr(self, 'tileKinds') else []
        except Exception as e:
            Logger.error("MapModel.getTileKinds", e)
            return []
    
    def setTileKinds(self, tileKinds):
        try:
            if isinstance(tileKinds, (list, dict)):
                self.tileKinds = tileKinds.copy() if hasattr(tileKinds, 'copy') else tileKinds
                Logger.debug("MapModel.setTileKinds", "Tile kinds set", count=len(self.tileKinds) if isinstance(self.tileKinds, dict) else "N/A")
            else:
                Logger.error("MapModel.setTileKinds", ValueError("Tile kinds must be a list or dict"))
        except Exception as e:
            Logger.error("MapModel.setTileKinds", e)
    
    def getTileSize(self):
        try:
            return self.tileSize
        except Exception as e:
            Logger.error("MapModel.getTileSize", e)
            return 32
    
    def setTileSize(self, tileSize):
        try:
            self.tileSize = max(1, int(tileSize))
            Logger.debug("MapModel.setTileSize", "Tile size set", tileSize=self.tileSize)
        except Exception as e:
            Logger.error("MapModel.setTileSize", e)
    
    def getTiles(self):
        try:
            return [row.copy() for row in self.tiles] if hasattr(self, 'tiles') and self.tiles else []
        except Exception as e:
            Logger.error("MapModel.getTiles", e)
            return []
    
    def setTiles(self, tiles):
        try:
            if isinstance(tiles, list):
                self.tiles = [row.copy() if isinstance(row, list) else row for row in tiles]
                Logger.debug("MapModel.setTiles", "Tiles set", rows=len(self.tiles))
            else:
                Logger.error("MapModel.setTiles", ValueError("Tiles must be a list"))
        except Exception as e:
            Logger.error("MapModel.setTiles", e)

    def getSpawnPoints(self, layerName="spawn"):
        try:
            if not hasattr(self, 'objectLayers'):
                Logger.debug("MapModel.getSpawnPoints", "No objectLayers found in map")
                return []
            
            if layerName in self.objectLayers:
                spawnObjects = self.objectLayers[layerName]
                
                if spawnObjects:
                    Logger.debug("MapModel.getSpawnPoints", 
                               f"Found {len(spawnObjects)} spawn points in layer '{layerName}'")
                    return spawnObjects
            
            allSpawnPoints = []
            for layer, objects in self.objectLayers.items():
                for obj in objects:
                    if obj.get('type', '').lower() == 'spawn':
                        allSpawnPoints.append(obj)
            
            if allSpawnPoints:
                Logger.debug("MapModel.getSpawnPoints", 
                           f"Found {len(allSpawnPoints)} spawn points across all layers")
                return allSpawnPoints
            
            Logger.debug("MapModel.getSpawnPoints", "No spawn points found in any layer")
            return []
            
        except Exception as e:
            Logger.error("MapModel.getSpawnPoints", e)
            return []