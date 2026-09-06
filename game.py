import pygame
from player import Player
from map_loader import MapLoader
from input_manager import InputManager
from audio_manager import AudioManager
from blood_particle import BloodParticle
from objects import Coin, Warp, SavePoint
from animation import ScrollingText

def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)):
            intersect_x = ((xj - xi) * (y - yi) / (yj - yi) + xi)
            if x < intersect_x:
                inside = not inside
        j = i
    return inside

def rect_hits_polygon(rect, polygon):
    # 1. Is any corner of the player inside the polygon?
    corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]

    for corner in corners:
        if point_in_polygon(corner, polygon):
            return True

    # 2. Is any polygon point inside the player?
    for point in polygon:
        if rect.collidepoint(point):
            return True

    # 3. Does any polygon edge cross the player's rectangle?
    for i in range(len(polygon)):
        start = polygon[i]
        end = polygon[(i + 1) % len(polygon)]

        if rect.clipline(start, end):
            return True

    return False

    
class Game:

    WIDTH = 800
    HEIGHT = 608
    FPS = 50
    DEFAULT_BACKGROUND_COLOR = (135, 206, 235)
    TITLE = "I Wanna Return 0"
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        self.clock = pygame.time.Clock()
        
        # Input
        self.input = InputManager()
        
        # Sound effects
        self.audio = AudioManager()

        # Death particle effect
        self.blood_particles = []

        # Player
        self.respawn_x = 96
        self.respawn_y = 96
        self.player = Player(self.respawn_x, self.respawn_y, self.audio)
        self.player_dead = False

        # Game over
        self.game_over_font = pygame.font.Font(None, 96)
        self.restart_font = pygame.font.Font(None, 35)

        # Reusable object assets
        # Coin collectable
        self.coin_sheet = pygame.image.load("assets/coin_gold.png").convert_alpha()
        # Warps
        self.warp_image = pygame.image.load("assets/Warp.png").convert_alpha()
        # Saves
        self.save_image = pygame.image.load("assets/Save_0.png").convert_alpha()
        self.save_active_image = pygame.image.load("assets/Save_1.png").convert_alpha()
        
        # Room State
        self.game_map = None
        self.background = None
        self.current_room = None

        # Dynamic room objects
        self.coins = []
        self.warps = []
        self.saves = []
        self.end_text = None
        self.end_font = pygame.font.Font(None, 36  )

        # Load starting room 
        self.load_room("room_start.tmx")

        self.second_timer = 0 # for the once per second update checks
        self.deaths = 0
        self.elapsed_seconds = 0
        self.stats_display_mode = ""
        # RUNNING
        self.running = True
    
    # --------------
    # MAIN GAME LOOP
    # --------------
    def run(self):
        while self.running:
            self.clock.tick(self.FPS)

            # Events
            self.input.begin_frame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                self.input.handle_event(event)
            self.input.update_held_input()
            
            # Update and Draw
            self.update()
            self.draw()

        pygame.quit()
	
             
    # kill_player
    def _kill_player(self):
        if self.player_dead:
            return
        
        self.player_dead = True
        self.deaths += 1
        
        death_x = self.player.rect.centerx
        death_y = self.player.rect.centery

        self.audio.death_sound.play()

        for _ in range(60):
            self.blood_particles.append(BloodParticle(death_x, death_y))
    
    # restart
    def _restart(self):
        self.player.respawn(self.respawn_x, self.respawn_y)
        self.player_dead = False
        self.blood_particles.clear()
		
	#-------------------------
	# UPDATES
	# ------------------------
    def update(self):

        if self.input.restart_pressed:
            if not self.player_dead:
                self.deaths += 1
            self._restart()
            return
        
        if not self.player_dead:
            self.player.update(
                self.input.move_left, 
                self.input.move_right, 
                self.input.jump_pressed, 
                self.input.jump_released, 
                self.game_map.collisions, 
                self.WIDTH
            )

            if self.input.shoot_pressed:
                bullet = self.player.shoot()
                self.player.bullets.append(bullet)
                self.audio.shoot_sound.play()

            if self.player.rect.top > self.game_map.height:
                self._kill_player()
            
            self._update_hazards()
        
            for coin in self.coins:
                coin.update()
                if not coin.collected and coin.check(self.player.rect):
                    coin.collect()
                    self.audio.coin_sound.play()
                    #print("COIN COLLECTED")
                    if all(coin.collected for coin in self.coins):
                        for warp in self.warps:
                            warp.unlock()
                            #print("WARP UNLOCKED: ", warp.visible)
                        
            for warp in self.warps:
                if warp.check(self.player.rect):
                    self.load_room(warp.target_room)
        
        for particle in self.blood_particles:
            particle.update()

        for bullet in self.player.bullets:
            bullet.update(self.game_map.collisions)
            
        self.player.bullets = [bullet for bullet in self.player.bullets if bullet.active]

        self._update_saves()
        for save in self.saves:
            save.update()

        self.blood_particles = [particle for particle in self.blood_particles if particle.life > 0]

        if self.end_text:
            self.end_text.update()

        # updates only once per second here
        self.second_timer += 1
        if self.second_timer >= self.FPS:
            self.second_timer = 0
            self._update_once_per_second()
        
    
    def _update_hazards(self):
        for hazard in self.game_map.hazards:
            if rect_hits_polygon(self.player.rect, hazard["points"]):
                self._kill_player()
                break

    def _update_saves(self):
        for save in self.saves:
            if save.shootable:
                for bullet in self.player.bullets:
                    if bullet.active and bullet.rect.colliderect(save.rect):
                        bullet.active = False
                        self.respawn_x = self.player.x
                        self.respawn_y = self.player.y
                        save.activate()
                        self.audio.save_sound.play()
                        break
            else:
                if self.player.rect.colliderect(save.rect):
                    if self.input.shoot_pressed:
                        self.respawn_x = self.player.x
                        self.respawn_y = self.player.y
                        save.activate()
                        self.audio.save_sound.play()

    def _update_once_per_second(self):
        self.elapsed_seconds += 1
        self.input.check_controller_connection()
        self._update_window_stats()

    def _update_window_stats(self):
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        time_text = f"{hours}:{minutes:02}:{seconds:02}"
        pygame.display.set_caption(f"{self.TITLE} | Deaths: {self.deaths} | Time: {time_text}")

	
	#-------------------------
	# DRAW
	#-------------------------
    def draw(self):

        if self.background:
            self.screen.blit(self.background, (0,0))
        else:
            self.screen.fill(self.DEFAULT_BACKGROUND_COLOR)

        self.game_map.draw(self.screen)

        for bullet in self.player.bullets:
            bullet.draw(self.screen)
        
        for particle in self.blood_particles:
            particle.draw(self.screen)
            
        for coin in self.coins:
            coin.draw(self.screen)
            
        for warp in self.warps:
            warp.draw(self.screen, self.warp_image)

        for save in self.saves:
            save.draw(self.screen)
            
        if not self.player_dead:
            self.player.draw(self.screen)
            
        if self.player_dead:
            self._draw_game_over()
	
        #DEBUG
        #self.game_map.draw_debug_collisions(self.screen)
        #self.game_map.draw_debug_hazards(self.screen)
        #self.game_map.draw_debug_saves(self.screen)
        #self.game_map.draw_debug_collectables(self.screen)

        if self.end_text:
            self.end_text.draw(self.screen)
	
        pygame.display.flip()
	
    def _draw_game_over(self):
        game_over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        restart_text = self.restart_font.render("press 'r' or Y/Triangle to try again", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 45))
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 30))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.draw.line(self.screen, (255, 255, 255), (self.WIDTH // 2 - 140, self.HEIGHT // 2), (self.WIDTH // 2 + 140, self.HEIGHT // 2), 2)
        self.screen.blit(restart_text, restart_rect)
    
    # ---------------
    # ROOM STUFF
    # ---------------
    def load_room(self, filename, spawn_name="player_start"):
        self.current_room = filename

        # Load the TMX room
        self.game_map = MapLoader(f"assets/maps/{filename}")

        # Background
        if self.game_map.background:
            self.background = pygame.image.load(f"assets/backgrounds/{self.game_map.background}").convert()
        else:
            self.background = None

        # ------------
        # Player Spawn
        # ------------
        if spawn_name in self.game_map.spawns: 
            spawn_x, spawn_y = self.game_map.spawns[spawn_name]

            self.respawn_x = spawn_x
            self.respawn_y = spawn_y

            self.player.respawn(spawn_x, spawn_y)

        # Room Objects
        self.coins = []
        self.warps = []
        self.saves = []

        for collectable in self.game_map.collectables:
            if collectable["name"] == "coin":
                self.coins.append( Coin(collectable["rect"], self.coin_sheet) )

        for warp_data in self.game_map.warps:
            warp = Warp(
                warp_data["rect"], 
                warp_data["target_room"],
                warp_data["locked"] )
            self.warps.append(warp)

        for save_data in self.game_map.saves:
            self.saves.append(SavePoint(save_data["rect"], self.save_image, self.save_active_image))

        if self.current_room == "room_end.tmx":
            self.end_text = ScrollingText(
                [
                    "process finished with exit code 0",
                    "",
                    "",
                    "",
                    "",
                    "That's it for now!",
                    "Thanks for playing!"
                ],
                self.end_font,
                start_y=self.HEIGHT + 32,
                speed=0.75,
                line_spacing=45
            )
        else:
            self.end_text = None
















