
        try:
            self.map = map
            Logger.debug("MapView.__init__", "Map view initialized", 
                        tile_count=len(map.tiles) if hasattr(map, 'tiles') else 0)
            self._scaled_tile_cache = {}
        except Exception as e:
            Logger.error("MapView.__init__", e)
            raise
    
    
    def draw(self, screen, offset=(0, 0)):
        try:
            offset_x, offset_y = offset
            try:
                layers_to_draw = None
                if hasattr(self.map, 'layer_ordered') and isinstance(self.map.layer_ordered, list):
                    layers_to_draw = [layer_matrix for _name, layer_matrix in self.map.layer_ordered]
                elif hasattr(self.map, 'layers') and isinstance(self.map.layers, dict):
                    layers_to_draw = [self.map.tiles]
                else:
                    layers_to_draw = [self.map.tiles]

                for layer in layers_to_draw:
                    for y, row in enumerate(layer):
                        for x, tile in enumerate(row):
                            try:
                                if not tile:
                                    continue
                                location = (x * self.map.tile_size + offset_x, y * self.map.tile_size + offset_y)
                                tile_size = self.map.tile_size
                                
                                flip_flags = 0
                                if hasattr(self.map, 'tile_flips'):
                                    try:
                                        flip_flags = self.map.tile_flips[y][x]
                                    except (IndexError, TypeError):
                                        flip_flags = 0
                                
                                if tile in self.map.tile_kinds:
                                    image = self.map.tile_kinds[tile].image
                                    try:
                                        if not isinstance(image, pygame.Surface):
                                            raise TypeError('tile image not a Surface')
                                        cache_key = (id(image), tile_size, flip_flags)
                                        scaled = self._scaled_tile_cache.get(cache_key)
                                        if scaled is None:
                                            try:
                                                w, h = image.get_size()
                                                if (w, h) != (tile_size, tile_size):
                                                    scaled = pygame.transform.scale(image, (tile_size, tile_size))
                                                else:
                                                    scaled = image
                                                
                                                flip_h = bool(flip_flags & 1)
                                                flip_v = bool(flip_flags & 2)
                                                if flip_h or flip_v:
                                                    scaled = pygame.transform.flip(scaled, flip_h, flip_v)
                                            except Exception:
                                                scaled = image
                                            self._scaled_tile_cache[cache_key] = scaled
                                        screen.blit(scaled, location)
                                    except Exception as e:
                                        Logger.error('MapView.draw.blit', e)
                                        rect = (location[0], location[1], tile_size, tile_size)
                                        pygame.draw.rect(screen, (120, 0, 120), rect)
                                else:
                                    try:
                                        if not hasattr(self, '_unknown_gids'):
                                            self._unknown_gids = set()
                                        if tile not in self._unknown_gids:
                                            self._unknown_gids.add(tile)
                                            Logger.debug("MapView.draw", "Unknown tile type, drawing placeholder", tile=tile, position=(x, y))
                                        color = ((tile * 37) % 256, (tile * 61) % 256, (tile * 97) % 256) if isinstance(tile, int) else (150, 0, 150)
                                        rect = (location[0], location[1], tile_size, tile_size)
                                        pygame.draw.rect(screen, color, rect)
                                    except Exception as e:
                                        Logger.error("MapView.draw.placeholder", e)
                            except Exception as e:
                                Logger.error("MapView.draw.tile", e)
                                continue
            except Exception as e:
                Logger.error("MapView.draw", e)

        except Exception as e:
            Logger.error("MapView.draw", e)