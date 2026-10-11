import pygame


class Trigger:
    def __init__(self, rect):
        self.rect = rect
        self.active = True

    def check(self, player_rect):
        return self.active and self.rect.colliderect(player_rect)

class ActionTrigger(Trigger):
    def __init__(self, rect, action, target, once=True):
        super().__init__(rect)
        self.action = action
        self.target = target
        self.once = once

    def activate(self):
        if self.once:
            self.active = False

    def reset(self):
        self.active = True
        
class Warp(Trigger):
    def __init__(self, rect, target_room, locked=False):
        super().__init__(rect)

        self.target_room = target_room

        if locked:
            self.lock()
        else:
            self.unlock()

    def unlock(self):
        self.visible = True
        self.active = True

    def lock(self):
        self.visible = False
        self.active = False

    def draw(self, screen, image, camera):
        if self.visible:
            draw_rect = self.rect.move(-camera.x, -camera.y)
            screen.blit(image, draw_rect.topleft)

class Collectable(Trigger):
    def __init__(self, rect):
        super().__init__(rect)
        self.collected = False

    def collect(self):
        self.collected = True
        self.active = False


class Coin(Collectable):
    def __init__(self, rect, spritesheet):
        super().__init__(rect)

        self.frames = []

        frame_width = 32
        frame_height = 32

        for i in range(8):
            frame = spritesheet.subsurface(
                pygame.Rect(
                    i * frame_width,
                    0,
                    frame_width,
                    frame_height
                )
            ).copy()

            self.frames.append(frame)

        self.frame_index = 0
        self.animation_timer = 0

        # At 50 FPS, this means one frame every 4 ticks
        self.animation_speed = 4

    def update(self):
        if self.collected:
            return

        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

    def draw(self, screen, camera):
        if self.collected:
            return

        draw_rect = self.rect.move(-camera.x, -camera.y)

        screen.blit(self.frames[self.frame_index], draw_rect.topleft)

class SavePoint:
    def __init__(self, rect, normal_image, active_image, shootable=False):
        self.rect = rect

        self.normal_image = normal_image
        self.active_image = active_image
        self.shootable = shootable

        self.active_timer = 0
        self.flash_duration = 50   # 1 second at 50 FPS

    def activate(self):
        self.active_timer = self.flash_duration

    def update(self):
        if self.active_timer > 0:
            self.active_timer -= 1

    def draw(self, screen, camera):
        if self.active_timer > 0:
            image = self.active_image
        else:
            image = self.normal_image

        draw_rect = self.rect.move(-camera.x, -camera.y)
        screen.blit(image, draw_rect.topleft)


class MovingSpike:

    def __init__(self, name, rect, image, direction, distance, speed):
        self.name = name

        self.start_x = float(rect.x)
        self.start_y = float(rect.y)

        self.x = self.start_x
        self.y = self.start_y

        self.rect = rect.copy()

        self.image = image

        self.direction = direction
        self.distance = distance
        self.speed = speed

        self.moving = False

        self._set_target_position()


    def _set_target_position(self):

        self.target_x = self.start_x
        self.target_y = self.start_y

        if self.direction == "up":
            self.target_y -= self.distance

        elif self.direction == "down":
            self.target_y += self.distance

        elif self.direction == "left":
            self.target_x -= self.distance

        elif self.direction == "right":
            self.target_x += self.distance

    def get_collision_polygon(self):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.width
        h = self.rect.height

        if self.direction == "up":
            return [
                (x, y + h),
                (x + w // 2, y),
                (x + w, y + h) ]
        elif self.direction == "down":
            return [
                (x, y),
                (x + w // 2, y + h),
                (x + w, y) ]
        elif self.direction == "left":
            return [
                (x + w, y),
                (x, y + h // 2),
                (x + w, y + h) ]
        elif self.direction == "right":
            return [
                (x, y),
                (x + w, y + h // 2),
                (x, y + h) ]
        return []


    def activate(self):
        self.moving = True

    def update(self):

        if not self.moving:
            return
        if self.x < self.target_x:
            self.x = min(self.x + self.speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.speed, self.target_x)
        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)


    def reset(self):

        self.x = self.start_x
        self.y = self.start_y

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        self.moving = False


    def draw(self, screen, camera):

        draw_rect = self.rect.move(
            -camera.x,
            -camera.y )

        screen.blit(
            self.image,
            draw_rect.topleft )



