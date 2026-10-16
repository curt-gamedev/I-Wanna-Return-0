import pygame
from pytmx.util_pygame import load_pygame

class MapLoader:

    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)

        self.width = (self.tmx_data.width * self.tmx_data.tilewidth)
        self.height = (self.tmx_data.height * self.tmx_data.tileheight)

        # Optional background image filename from Tiled map properties
        # If missing, Game draws the default sky-blue background.
        self.background: str | None = self.tmx_data.properties.get("background")

        self.spawns = {}
        self.collisions = []
        self.hazards = []
        self.hazard_sprites = []
        self.saves = []
        self.collectables = []
        self.warps = []
        self.water = []
        self.moving_spikes = []
        self.triggers = []

        self._load_spawns()
        self._load_collisions()
        self._load_hazards()
        self._load_saves()
        self._load_collectables()
        self._load_warps()
        self._load_water()
        self._load_moving_spikes()
        self._load_triggers()

    
    #-----------------------
    # LOADING FROM TMX
    #---------------------
    def _load_spawns(self):
        layer = self._get_layer("Spawns")
        if layer is None:
            return
        for obj in layer:
            self.spawns[obj.name] = (round(obj.x), round(obj.y))
    
    def _load_collisions(self):
        layer = self._get_layer("Collisions")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.collisions.append(rect)
	
    def _load_hazards(self):
        '''
        Hazard object
        -- has image? YES
        |       |
        |       -- draw sprite
        |       -- read direction
        |       -- generate collision
        |       -- continue
        -- has image? NO
                |
                -- does it have polygon points?
                    -- load old manual polygon
                    #SUPER IMPORTANT FOR SOME EDGE CASE SCENARIOS THAT SHOULDNT COLLIDE IN TRADITIONAL FANGAME PHYSICS
        '''
        layer = self._get_layer("Hazards")
        if layer is None:
            return

        for obj in layer:
            # --------------------------------
            # TILE-OBJECT HAZARDS
            # e.g. automatically placed spikes
            # --------------------------------
            if getattr(obj, "image", None) is not None:

                x = round(obj.x)
                y = round(obj.y)
                width = round(obj.width)
                height = round(obj.height)

                direction = obj.properties.get("direction")

                self.hazard_sprites.append({
                    "name": obj.name,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "image": obj.image,
                    "direction": direction
                })

                # Generate default spike collision
                if direction == "up":
                    polygon = [
                        (x, y + height),
                        (x + width // 2, y),
                        (x + width, y + height) ]
                elif direction == "down":
                    polygon = [
                        (x, y),
                        (x + width // 2, y + height),
                        (x + width, y) ]
                elif direction == "left":
                    polygon = [
                        (x + width, y),
                        (x, y + height // 2),
                        (x + width, y + height) ]
                elif direction == "right":
                    polygon = [
                        (x, y),
                        (x + width, y + height // 2),
                        (x, y + height) ]
                else:
                    polygon = None

                if polygon is not None:
                    self.hazards.append({"name": obj.name, "points": polygon})

                # We completely handled this tile object.
                # Don't also try treating it as a hand-drawn polygon. 
                continue

            # --------------------------------
            # MANUALLY DRAWN POLYGON HAZARDS
            # --------------------------------
            if not hasattr(obj, "points"):
                continue
            if not obj.points:
                continue

            polygon = []

            for point in obj.points:
                polygon.append((round(point.x), round(point.y)))

            self.hazards.append({"name": obj.name, "points": polygon})
    
    def _load_saves(self):
        layer = self._get_layer("Saves")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.saves.append({"name": obj.name, "rect": rect, "shootable": obj.properties.get("shootable", False)})
            
    def _load_collectables(self):
        layer = self._get_layer("Collectables")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.collectables.append({"name": obj.name, "rect": rect})
            
    def _load_warps(self):
        layer = self._get_layer("Warps")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.warps.append({
                "name": obj.name, 
                "rect": rect, 
                "target_room": obj.properties.get("target_room"),
                "locked": obj.properties.get("locked", False) })

    def _load_water(self):
        layer = self._get_layer("Water")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.water.append(rect)

    def _load_moving_spikes(self):
        layer = self._get_layer("MovingSpikes")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect( round(obj.x), round(obj.y), round(obj.width), round(obj.height) )
            self.moving_spikes.append({
                "name": obj.name,
                "rect": rect,
                "direction": obj.properties.get("direction", "up"),
                "distance": obj.properties.get("distance", 96),
                "speed": obj.properties.get("speed", 4) })


    def _load_triggers(self):
        layer = self._get_layer("Triggers")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect( round(obj.x), round(obj.y), round(obj.width), round(obj.height) )
            self.triggers.append({
                "name": obj.name,
                "rect": rect,
                "action": obj.properties.get("action"),
                "target": obj.properties.get("target"),
                "once": obj.properties.get("once", True)  })

    def _get_layer(self, name):
        try:
            return self.tmx_data.get_layer_by_name(name)
        except ValueError:
            return None
    
    #--------------
    # DRAWING
    #---------
            
    def draw(self, screen, camera_x=0, camera_y=0):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    world_x = x * self.tmx_data.tilewidth
                    world_y = y * self.tmx_data.tileheight
                    screen_x = world_x - camera_x
                    screen_y = world_y - camera_y
                    screen.blit(image, (screen_x, screen_y) )

    def draw_debug_collisions(self, screen, camera):
        for rect in self.collisions:
            debug_rect = rect.move(-camera.x, -camera.y)
            pygame.draw.rect(screen, (0, 255, 0), debug_rect, 1)

    def draw_debug_hazards(self, screen, camera):
        for hazard in self.hazards:
            points = [
                (x - camera.x, y - camera.y)
                for x, y in hazard["points"] ]
            pygame.draw.polygon(screen, (255, 0, 0), points, 1)
			
    def draw_debug_saves(self,screen, camera):
        for save in self.saves:
            debug_rect = save["rect"].move(-camera.x, -camera.y)
            pygame.draw.rect(screen, (0,0,255), debug_rect, 1)
            
    def draw_debug_collectables(self, screen, camera):
        for collectable in self.collectables:
            debug_rect = collectable["rect"].move(-camera.x, -camera.y)
            pygame.draw.rect(screen, (255, 255, 0), debug_rect, 1)

    def draw_hazard_sprites(self, screen, camera):
        for hazard in self.hazard_sprites:
            draw_x = hazard["x"] - camera.x
            draw_y = hazard["y"] - camera.y

            screen.blit(
                hazard["image"],
                (draw_x, draw_y))



    
			
			
			
			
			
			
			
			
			
			
