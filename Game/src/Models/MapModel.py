

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
                    tilewidth = int(root.attrib.get('tilewidth', 32))
                    tileheight = int(root.attrib.get('tileheight', 32))
                    self.tile_size = tilewidth

                   
                   
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
                            flip_row = []
                            for c in range(width):
                                idx = r * width + c
                                if idx < len(nums):
                                    gid = nums[idx]
                                   
                                   
                                    flip_flags = 0
                                    if gid & FLIP_H:
                                        flip_flags |= 1 
                                    if gid & FLIP_V:
                                        flip_flags |= 2  
                                    if gid & FLIP_D:
                                        flip_flags |= 4  
                                  
                                  
                                    gid = gid & ~(FLIP_H | FLIP_V | FLIP_D)
                                    row.append(gid)
                                    flip_row.append(flip_flags)
                                else:
                                    row.append(0)
                                    flip_row.append(0)
                            matrix.append(row)
                            flips.append(flip_row)
                        layers.append((layer_name, matrix))
                        flip_layers.append((layer_name, flips))
                        layers_by_name[layer_name] = matrix

                  
                  
                    self.flip_layers = {name: flips for name, flips in flip_layers}

                   
                    merged = [[0 for _ in range(width)] for _ in range(height)]
                    merged_flips = [[0 for _ in range(width)] for _ in range(height)]
                    for i, (_name, layer) in enumerate(layers):
                        
                        flip_layer = flip_layers[i][1] if i < len(flip_layers) else None
                        for y in range(height):
                            for x in range(width):
                                gid = layer[y][x]
                                if gid:
                                    merged[y][x] = gid
                                    if flip_layer:
                                        merged_flips[y][x] = flip_layer[y][x]

                    self.tiles = merged
                    self.tile_flips = merged_flips 
                   
                    self.layers = layers_by_name
                    
                    self.layer_ordered = layers
                    self.width = width
                    self.height = height
                    self.tilewidth = tilewidth
                    self.tileheight = tileheight

                  
                  
                    self.object_layers = {}
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
                                props_elem = obj.find('properties')
                                if props_elem is not None:
                                    for prop in props_elem.findall('property'):
                                        props[prop.attrib.get('name')] = prop.attrib.get('value', prop.attrib.get('type'))
                                objs.append({'x': ox, 'y': oy, 'width': ow, 'height': oh, 'gid': gid, 'name': objname, 'type': otype, 'properties': props})
                            except Exception:
                                continue
                        self.object_layers[layer_name] = objs

                   
                    self.tile_kinds = {} 
                    self.tilesets = []  
                    tileset_elems = root.findall('tileset')  
                    


                    for tileset_elem in tileset_elems:
                        source = tileset_elem.attrib.get('source')
                        firstgid = int(tileset_elem.attrib.get('firstgid', 1))
                        tsx_path = os.path.join(tmx_dir, source) if source else None
                        if not tsx_path or not os.path.exists(tsx_path):
                            
                            tsx_guess = os.path.join(os.path.dirname(tmx_dir), source) if source else None
                            if tsx_guess and os.path.exists(tsx_guess):
                                tsx_path = tsx_guess


                        image_surface = None
                        tileset_columns = 0
                        tileset_tilecount = 0
                        if tsx_path and os.path.exists(tsx_path):
                            try:
                                tsx_data = open(tsx_path, 'r', encoding='utf-8').read()
                                tsx_root = ET.fromstring(tsx_data)
                                image_elem = tsx_root.find('image')
                                if image_elem is not None:
                                    img_src = image_elem.attrib.get('source')
                                   
                                    img_path = os.path.join(os.path.dirname(tsx_path), img_src)
                                    if not os.path.exists(img_path):
                                       
                                        alt = os.path.join(os.path.dirname(os.path.dirname(tsx_path)), img_src)
                                        if os.path.exists(alt):
                                            img_path = alt

                                    if os.path.exists(img_path):
                                        try:
                                            surf = pygame.image.load(img_path)
                                            try:
                                                image_surface = surf.convert_alpha()
                                                Logger.debug('MapModel.__init__', 'TSX image loaded with alpha', path=img_path)
                                            except Exception:
                                                

                                                try:
                                                    surf2 = surf.convert()
                                                    col = surf2.get_at((0, 0))
                                                    surf2.set_colorkey(col)
                                                    image_surface = surf2
                                                    Logger.debug('MapModel.__init__', 'TSX image loaded without alpha - colorkey set', path=img_path, colorkey=col)
                                                except Exception:
                                                    image_surface = None
                                        except Exception:
                                            image_surface = None


                                    else:
                                      
                                        try:
                                            basename = os.path.basename(img_src)
                                            search_root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(tmx_path)))) if os.path.dirname(os.path.dirname(os.path.dirname(tmx_path))) else os.path.dirname(tmx_path)
                                            found = None
                                            for root_dir, dirs, files in os.walk(search_root):
                                                if basename in files:
                                                    candidate = os.path.join(root_dir, basename)
                                                    try:
                                                        surf = pygame.image.load(candidate)
                                                        try:
                                                            image_surface = surf.convert_alpha()
                                                            found = candidate
                                                            Logger.debug('MapModel.__init__', 'Found TSX image by basename search (alpha)', candidate=candidate)
                                                            break
                                                        except Exception:
                                                            try:
                                                                surf2 = surf.convert()
                                                                col = surf2.get_at((0, 0))
                                                                surf2.set_colorkey(col)
                                                                image_surface = surf2
                                                                found = candidate
                                                                Logger.debug('MapModel.__init__', 'Found TSX image by basename search (colorkey)', candidate=candidate, colorkey=col)
                                                                break
                                                            except Exception:
                                                                continue
                                                    except Exception:
                                                        continue
                                            if not found:
                                                Logger.debug('MapModel.__init__', 'TSX image not found (fallback search failed)', expected=os.path.join(os.path.dirname(tsx_path), img_src))
                                        except Exception as e:
                                            Logger.error('MapModel.__init__', e)

                                tileset_columns = int(tsx_root.attrib.get('columns', 0))
                                tileset_tilecount = int(tsx_root.attrib.get('tilecount', 0))
                               
                               
                                if image_surface is not None:
                                    try:
                                        img_w, img_h = image_surface.get_size()
                                        inferred_columns = img_w // tilewidth if tilewidth > 0 else 0
                                        inferred_rows = img_h // tileheight if tileheight > 0 else 0
                                        inferred_tilecount = inferred_columns * inferred_rows
                                        if inferred_columns > 0 and tileset_columns != inferred_columns:
                                            Logger.debug('MapModel.__init__', 'Tileset columns mismatch - using inferred value', tsx_columns=tileset_columns, inferred_columns=inferred_columns)
                                            tileset_columns = inferred_columns
                                        if inferred_tilecount > 0 and tileset_tilecount != inferred_tilecount:
                                            Logger.debug('MapModel.__init__', 'Tileset tilecount mismatch - using inferred value', tsx_tilecount=tileset_tilecount, inferred_tilecount=inferred_tilecount)
                                            tileset_tilecount = inferred_tilecount
                                    except Exception as e:
                                        Logger.error('MapModel.__init__', e)
                            except Exception as e:
                                Logger.error('MapModel.__init__', e)

                       
                        columns = tileset_columns if tileset_columns > 0 else max(1, (tileset_tilecount or 0))
                        for gid_index in range(tileset_tilecount):
                            gid = firstgid + gid_index
                            try:
                                if image_surface:
                                    col = gid_index % columns
                                    row = gid_index // columns
                                    rect = pygame.Rect(col * tilewidth, row * tileheight, tilewidth, tileheight)
                                  
                                  
                                    tile_surf = pygame.Surface((tilewidth, tileheight), pygame.SRCALPHA, 32)
                                    tile_surf.blit(image_surface, (0, 0), rect)
                                    try:
                                        tile_surf = tile_surf.convert_alpha()
                                    except Exception:
                                       
                                       
                                        pass
                                else:
                                
                                    tile_surf = pygame.Surface((tilewidth, tileheight))
                                  
                                  
                                    color = ((gid * 37) % 256, (gid * 61) % 256, (gid * 97) % 256)
                                    tile_surf.fill(color)
                               
                                class _Tile:
                                    def __init__(self, image):
                                        self.image = image
                                self.tile_kinds[gid] = _Tile(tile_surf)
                            except Exception:
                                continue
                        
                      
                        self.tilesets.append({
                            'firstgid': firstgid,
                            'source': source,
                            'tilecount': tileset_tilecount,
                            'columns': tileset_columns
                        })

                    try:
                        used_gids = set()
                        for row in self.tiles:
                            for v in row:
                                if isinstance(v, int) and v > 0:
                                    used_gids.add(v)
                        missing = [g for g in sorted(used_gids) if g not in self.tile_kinds]
                        if missing:
                            Logger.debug('MapModel.__init__', 'Missing GIDs found - creating placeholders', missing_count=len(missing), missing_sample=missing[:20])
                        for gid in missing:
                            try:
                                tile_surf = pygame.Surface((tilewidth, tileheight))
                                color = ((gid * 37) % 256, (gid * 61) % 256, (gid * 97) % 256)
                                tile_surf.fill(color)
                                class _Tile2:
                                    def __init__(self, image):
                                        self.image = image
                                self.tile_kinds[gid] = _Tile2(tile_surf)
                            except Exception:
                                continue
                    except Exception as e:
                        Logger.error('MapModel.__init__', e)

                    Logger.debug("MapModel.__init__", "TMX map parsed successfully", width=width, height=height, tilewidth=tilewidth, tileheight=tileheight, tilesets=len(self.tilesets), object_layers=list(self.object_layers.keys()))

                else:
                  
                    self.tile_kinds = {}
                   
                   
                    self.tile_flips = []
                    for line in data.split("\n"):
                        if line.strip(): 
                            row = []
                            for tile_number in line:
                                try:
                                    row.append(int(tile_number))
                                except ValueError:
                                    Logger.debug("MapModel.__init__", "Invalid tile number, skipping", tile=tile_number)
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
            if isinstance(tile_kinds, list):
                self.tile_kinds = tile_kinds.copy()  # Store a copy
                Logger.debug("MapModel.setTileKinds", "Tile kinds set", count=len(self.tile_kinds))
            else:
                Logger.error("MapModel.setTileKinds", ValueError("Tile kinds must be a list"))
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
            # Return a deep copy to prevent external modification
            return [row.copy() for row in self.tiles] if hasattr(self, 'tiles') and self.tiles else []
        except Exception as e:
            Logger.error("MapModel.getTiles", e)
            return []
    
    def setTiles(self, tiles):
       
        try:
            if isinstance(tiles, list):
                # Store a deep copy
                self.tiles = [row.copy() if isinstance(row, list) else row for row in tiles]
                Logger.debug("MapModel.setTiles", "Tiles set", rows=len(self.tiles))
            else:
                Logger.error("MapModel.setTiles", ValueError("Tiles must be a list"))
        except Exception as e:
            Logger.error("MapModel.setTiles", e)



    def get_spawn_points(self, layer_name="spawn"):
      
        try:
            if not hasattr(self, 'object_layers'):
                Logger.debug("MapModel.get_spawn_points", "No object_layers found in map")
                return []
            
            if layer_name in self.object_layers:
                spawn_objects = self.object_layers[layer_name]
                
                if spawn_objects:
                    Logger.debug("MapModel.get_spawn_points", 
                               f"Found {len(spawn_objects)} spawn points in layer '{layer_name}'")
                    return spawn_objects
            

            all_spawn_points = []
            for layer, objects in self.object_layers.items():
                for obj in objects:
                    if obj.get('type', '').lower() == 'spawn':
                        all_spawn_points.append(obj)
            
            if all_spawn_points:
                Logger.debug("MapModel.get_spawn_points", 
                           f"Found {len(all_spawn_points)} spawn points across all layers")
                return all_spawn_points
            
            Logger.debug("MapModel.get_spawn_points", "No spawn points found in any layer")
            return []
            
        except Exception as e:
            Logger.error("MapModel.get_spawn_points", e)
            return []