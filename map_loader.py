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
        self.saves = []
        self.collectables = []
        self.warps = []

        self._load_spawns()
        self._load_collisions()
        self._load_hazards()
        self._load_saves()
        self._load_collectables()
        self._load_warps()
    
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
        layer = self._get_layer("Hazards")
        if layer is None:
            return
        for obj in layer:
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
                for x, y in hazard["points"]
            ]

            pygame.draw.polygon(
                screen,
                (255, 0, 0),
                points,
                1
            )
			
    def draw_debug_saves(self,screen, camera):
        for save in self.saves:
            debug_rect = save["rect"].move(-camera.x, -camera.y)
            pygame.draw.rect(screen, (0,0,255), debug_rect, 1)
            
    def draw_debug_collectables(self, screen, camera):
        for collectable in self.collectables:
            debug_rect = collectable["rect"].move(-camera.x, -camera.y)
            pygame.draw.rect(screen, (255, 255, 0), debug_rect, 1)



    
			
			
			
			
			
			
			
			
			
			
