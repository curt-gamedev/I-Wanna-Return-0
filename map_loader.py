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
        layer = self.tmx_data.get_layer_by_name("Spawns")
        if layer is None:
            return
        for obj in layer:
            self.spawns[obj.name] = (round(obj.x), round(obj.y))
    
    def _load_collisions(self):
        layer = self.tmx_data.get_layer_by_name("Collisions")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.collisions.append(rect)
	
    def _load_hazards(self):
        layer = self.tmx_data.get_layer_by_name("Hazards")
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
        layer = self.tmx_data.get_layer_by_name("Saves")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.saves.append({"name": obj.name, "rect": rect, "shootable": obj.properties.get("shootable", False)})
            
    def _load_collectables(self):
        layer = self.tmx_data.get_layer_by_name("Collectables")
        if layer is None:
            return
        for obj in layer:
            rect = pygame.Rect(round(obj.x), round(obj.y), round(obj.width), round(obj.height))
            self.collectables.append({"name": obj.name, "rect": rect})
            
    def _load_warps(self):
        layer = self.tmx_data.get_layer_by_name("Warps")
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
            
    def draw(self, screen):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, image in layer.tiles():
                    screen.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight) )

    def draw_debug_collisions(self, screen):
        for rect in self.collisions:
            pygame.draw.rect(screen, (0, 255, 0), rect, 1)

    def draw_debug_hazards(self,screen):
        for hazard in self.hazards:	
            pygame.draw.polygon(screen, (255, 0, 0), hazard["points"], 1)
			
    def draw_debug_saves(self,screen):
        for save in self.saves:
            pygame.draw.rect(screen, (0,0,255), save["rect"], 1)
            
    def draw_debug_collectables(self, screen):
        for collectable in self.collectables:
            pygame.draw.rect(screen, (255, 255, 0), collectable["rect"], 1)



    
			
			
			
			
			
			
			
			
			
			
