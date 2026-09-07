import pygame
from animation import PlayerAnimation
from bullet import Bullet
from paths import resource_path

class Player:
    SPRITE_SIZE = 32

    # Original-style player collision rectangle
    COLLIDER_WIDTH = 11
    COLLIDER_HEIGHT = 21

    COLLIDER_OFFSET_X = 12
    COLLIDER_OFFSET_Y = 11

    def __init__(self, x, y, audio):

        # -------------------------
        # PHYSICS
        # -------------------------
        self.audio = audio

        self.move_speed = 3.0

        self.gravity = 0.4
        self.max_fall_speed = 9.0

        self.first_jump_speed = -8.5
        self.double_jump_speed = -7.0

        self.jump_release_multiplier = 0.45

        # -------------------------
        # POSITION
        # -------------------------

        # x/y represent the top-left of the 32x32 visual sprite
        self.x = float(x)
        self.y = float(y)

        self.velocity_y = 0.0

        # -------------------------
        # JUMP STATE
        # -------------------------

        self.grounded = False
        self.double_jump_available = True

        # -------------------------
        # FACING
        # -------------------------

        self.facing_right = True

        # -------------------------
        # COLLISION RECT
        # -------------------------

        self.rect = pygame.Rect(
            round(self.x) + self.COLLIDER_OFFSET_X,
            round(self.y) + self.COLLIDER_OFFSET_Y,
            self.COLLIDER_WIDTH,
            self.COLLIDER_HEIGHT
        )

        # Animation
        self.animation = PlayerAnimation()

        # Shooting
        self.bullet_image = pygame.image.load(resource_path("assets/Bullet_1.png")).convert_alpha()
        self.bullets = []

        # Handy while developing
        self.show_hitbox = False

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update(self, move_left, move_right, jump_pressed, jump_released, collision_rects, map_width):

        # -------------------------
        # HORIZONTAL MOVEMENT
        # -------------------------
        move_x = 0
        if move_left:
            move_x -= self.move_speed
        if move_right:
            move_x += self.move_speed
        self.x += move_x
		
		#update collider after horizontal movement
        self._sync_rect_from_position()
		
		#horizontal collision
        for solid in collision_rects:
            if self.rect.colliderect(solid):
                if move_x > 0:
                    self.rect.right = solid.left
                elif move_x < 0:
                    self.rect.left = solid.right
                self.x = float(self.rect.x - self._get_collider_offset_x())

        # Facing direction
        if move_left and not move_right:
            self.facing_right = False

        if move_right and not move_left:
            self.facing_right = True

        # -------------------------
        # JUMPING
        # -------------------------

        if jump_pressed:
            if self._is_on_ground(collision_rects):
                 # First jump
                self.velocity_y = self.first_jump_speed
                self.double_jump_available = True
                self.audio.jump_sound.play()
            elif self.double_jump_available:
                # Double jump
                self.velocity_y = self.double_jump_speed
                self.double_jump_available = False
                self.audio.double_jump_sound.play()

        # Jump cancel / short hop
        if jump_released and self.velocity_y < 0:
            self.velocity_y *= self.jump_release_multiplier

        # -------------------------
        # GRAVITY
        # -------------------------

        self.velocity_y += self.gravity

        if self.velocity_y > self.max_fall_speed:
            self.velocity_y = self.max_fall_speed

        # -------------------------
		# VERTICAL MOVEMENT
		# -------------------------

        self.y += self.velocity_y

        self._sync_rect_from_position()

        self.grounded = False

        for solid in collision_rects:
            if self.rect.colliderect(solid):
				# Falling onto platform
                if self.velocity_y > 0:
                    self.rect.bottom = solid.top
                    self.y = float( self.rect.y - self.COLLIDER_OFFSET_Y  )
                    self.velocity_y = 0.0
                    self.grounded = True
                    self.double_jump_available = True
				# Hitting ceiling
                elif self.velocity_y < 0:
                    self.rect.top = solid.bottom
                    self.y = float( self.rect.y - self.COLLIDER_OFFSET_Y  )
                    self.velocity_y = 0.0
		
        # If we're resting directly on a platform, count as grounded
        # even if fractional gravity didn't move the collider into it this frame.
        if not self.grounded and self.velocity_y >= 0:
            for solid in collision_rects:
                ground_check = self.rect.move(0, 1)

                if ground_check.colliderect(solid):
                    self.rect.bottom = solid.top
                    self._sync_position_from_rect()

                    self.velocity_y = 0.0
                    self.grounded = True
                    self.double_jump_available = True
                    break


        # -------------------------
        # SCREEN BOUNDS
        # -------------------------
        if self.rect.left < 0:
            self.rect.left = 0
            self._sync_position_from_rect()

        if self.rect.right > map_width:
            self.rect.right = map_width
            self._sync_position_from_rect()

        self._update_animation(move_left, move_right)

    # --------------------------------------------------
    # COLLISION HELPERS
    # --------------------------------------------------

    def _sync_rect_from_position(self):
        offset_x = self._get_collider_offset_x()
        self.rect.x = (round(self.x) + offset_x)
        self.rect.y = (round(self.y) + self.COLLIDER_OFFSET_Y)

    def _sync_position_from_rect(self):
        offset_x = self._get_collider_offset_x()
        self.x = float(self.rect.x - offset_x)
        self.y = float(self.rect.y - self.COLLIDER_OFFSET_Y)

    def _get_collider_offset_x(self):
        if self.facing_right:
            return self.COLLIDER_OFFSET_X
        return (self.SPRITE_SIZE - self.COLLIDER_OFFSET_X - self.COLLIDER_WIDTH)
        
    def _is_on_ground(self, collision_rects):
        ground_check = self.rect.move(0, 1)
        for solid in collision_rects:
            if ground_check.colliderect(solid):
                return True
        return False
	
    # --------------------------------------------------
    # ANIMATION
    # --------------------------------------------------
    def _update_animation(self, move_left, move_right):

        # Determine state
        if not self.grounded:

            if self.velocity_y < 0:
                new_state = "jump"
            else:
                new_state = "fall"

        elif move_left != move_right:
            new_state = "run"

        else:
            new_state = "idle"

        self.animation.set_state(new_state)
        self.animation.update()

    # -------
    # RESPAWN
    # -------
    def respawn(self, x, y):
        self.x = float(x)
        self.y = float(y)

        self.velocity_y = 0.0
        self.grounded = False

        # Use whichever jump-state system you're currently using:
        self.double_jump_available = True

        self._sync_rect_from_position()
                
                
    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self, screen, camera):

        image = self.animation.get_frame()

        if image is None:
            return

        # Our source art faces right.
        # Flip it when facing left.
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        draw_x = round(self.x - camera.x)
        draw_y = round(self.y - camera.y)
        screen.blit(image, ( draw_x, draw_y ))

        # Temporary collider visualization
        if self.show_hitbox:
            debug_rect = self.rect.move(-camera.x, -camera.y)
            pygame.draw.rect(screen, (255, 0, 255), debug_rect, 1)

    def shoot(self):
        direction = 1 if self.facing_right else -1
        bullet_x = self.rect.centerx
        bullet_y = self.rect.centery
        return Bullet(bullet_x, bullet_y, direction, self.bullet_image)
			
			
			