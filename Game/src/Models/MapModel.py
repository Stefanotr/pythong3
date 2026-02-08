

import pygame
from Utils.Logger import Logger


class MapModel:

    def __init__(self, map_file, tile_kinds, tile_size):
   
        try:
            self.tile_kinds = tile_kinds
            self.tile_size = tile_size
            Logger.debug("MapModel.__init__", "Loading map", map_file=map_file, tile_size=tile_size)
            
            try:
                with open(map_file, "r") as file:
                    data = file.read()
                Logger.debug("MapModel.__init__", "Map file read successfully", map_file=map_file)
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
                if str(map_file).lower().endswith('.tmx'):
                    import os
                    import xml.etree.ElementTree as ET

                    tmx_path = map_file
                    tmx_dir = os.path.dirname(tmx_path)

                    root = ET.fromstring(data)
                    width = int(root.attrib.get('width', 0))
                    height = int(root.attrib.get('height', 0))
                    tile_width = int(root.attrib.get('tile_width', 32))
                    tile_height = int(root.attrib.get('tile_height', 32))
                    self.tile_size = tile_width

                    layers = []
                    layers_by_name = {}
                    flip_layers = []
                    FLIP_H = 0x80000000
                    FLIP_V = 0x40000000
                    FLIP_D = 0x20000000
                    
                    for layer in root.findall('layer'):
                        layer_name = layer.attrib.get('name', '')
                        data_elem = layer.find('data')
                        if data_elem is None or data_elem.text is None:
                            matrix = [[0]*width for _ in range(height)]
                            flips = [[0]*width for _ in range(height)]
                            layers.append((layer_name, matrix))
                            flip_layers.append((layer_name, flips))
                            layers_by_name[layer_name] = matrix
                            continue
                        csv = data_elem.text.strip()
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
                        layers.append((layer_name, matrix))
                        flip_layers.append((layer_name, flips))
                        layers_by_name[layer_name] = matrix

                    self.flip_layers = {name: flips for name, flips in flip_layers}

                    merged = [[0 for _ in range(width)] for _ in range(height)]
                    mergedFlips = [[0 for _ in range(width)] for _ in range(height)]
                    for i, (_name, layer) in enumerate(layers):
                        flipLayer = flip_layers[i][1] if i < len(flip_layers) else None
                        for y in range(height):
                            for x in range(width):
                                gid = layer[y][x]
                                if gid:
                                    merged[y][x] = gid
                                    if flipLayer:
                                        mergedFlips[y][x] = flipLayer[y][x]

                    self.tiles = merged
                    self.tile_flips = mergedFlips
                    self.layers = layers_by_name
                    self.layerOrdered = layers
                    self.width = width
                    self.height = height
                    self.tile_width = tile_width
                    self.tile_height = tile_height

                    self.objectLayers = {}
                    for objgroup in root.findall('objectgroup'):
                        layer_name = objgroup.attrib.get('name', '')
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
                        self.objectLayers[layer_name] = objs

                    self.tile_kinds = {}
                    self.tilesets = []
                    tilesetElems = root.findall('tileset')
                    
                    for tilesetElem in tilesetElems:
                        source = tilesetElem.attrib.get('source')
                        firstgid = int(tilesetElem.attrib.get('firstgid', 1))
                        tsxPath = os.path.join(tmx_dir, source) if source else None
                        if not tsxPath or not os.path.exists(tsxPath):
                            tsxGuess = os.path.join(os.path.dirname(tmx_dir), source) if source else None
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
                                            searchRoot = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(tmx_path)))) if os.path.dirname(os.path.dirname(os.path.dirname(tmx_path))) else os.path.dirname(tmx_path)
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
                                        inferredColumns = imgW // tile_width if tile_width > 0 else 0
                                        inferredRows = imgH // tile_height if tile_height > 0 else 0
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
                                    rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                                    tileSurf = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA, 32)
                                    tileSurf.blit(imageSurface, (0, 0), rect)
                                    try:
                                        tileSurf = tileSurf.convert_alpha()
                                    except Exception:
                                        pass
                                else:
                                    tileSurf = pygame.Surface((tile_width, tile_height))
                                    color = ((gid * 37) % 256, (gid * 61) % 256, (gid * 97) % 256)
                                    tileSurf.fill(color)
                                class _Tile:
                                    def __init__(self, image):
                                        self.image = image
                                self.tile_kinds[gid] = _Tile(tileSurf)
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
                        missing = [g for g in sorted(usedGids) if g not in self.tile_kinds]
                        if missing:
                            Logger.debug('MapModel.__init__', 'Missing GIDs found - creating placeholders', missingCount=len(missing), missingSample=missing[:20])
                        for gid in missing:
                            try:
                                tileSurf = pygame.Surface((tile_width, tile_height))
                                color = ((gid * 37) % 256, (gid * 61) % 256, (gid * 97) % 256)
                                tileSurf.fill(color)
                                class _Tile2:
                                    def __init__(self, image):
                                        self.image = image
                                self.tile_kinds[gid] = _Tile2(tileSurf)
                            except Exception:
                                continue
                    except Exception as e:
                        Logger.error('MapModel.__init__', e)

                    Logger.debug("MapModel.__init__", "TMX map parsed successfully", width=width, height=height, tile_width=tile_width, tile_height=tile_height, tilesets=len(self.tilesets), objectLayers=list(self.objectLayers.keys()))

                else:
                    self.tile_kinds = {}
                    self.tile_flips = []
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
            return self.tile_kinds.copy() if hasattr(self, 'tile_kinds') else []
        except Exception as e:
            Logger.error("MapModel.getTileKinds", e)
            return []
    
    def setTileKinds(self, tile_kinds):
        try:
            if isinstance(tile_kinds, (list, dict)):
                self.tile_kinds = tile_kinds.copy() if hasattr(tile_kinds, 'copy') else tile_kinds
                Logger.debug("MapModel.setTileKinds", "Tile kinds set", count=len(self.tile_kinds) if isinstance(self.tile_kinds, dict) else "N/A")
            else:
                Logger.error("MapModel.setTileKinds", ValueError("Tile kinds must be a list or dict"))
        except Exception as e:
            Logger.error("MapModel.setTileKinds", e)
    
    def getTileSize(self):
        try:
            return self.tile_size
        except Exception as e:
            Logger.error("MapModel.getTileSize", e)
            return 32
    
    def setTileSize(self, tile_size):
        try:
            self.tile_size = max(1, int(tile_size))
            Logger.debug("MapModel.setTileSize", "Tile size set", tile_size=self.tile_size)
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

    def getSpawnPoints(self, layer_name="spawn"):
        try:
            if not hasattr(self, 'objectLayers'):
                Logger.debug("MapModel.getSpawnPoints", "No objectLayers found in map")
                return []
            
            if layer_name in self.objectLayers:
                spawnObjects = self.objectLayers[layer_name]
                
                if spawnObjects:
                    Logger.debug("MapModel.getSpawnPoints", 
                               f"Found {len(spawnObjects)} spawn points in layer '{layer_name}'")
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