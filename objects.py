import pygame


class Trigger:
    def __init__(self, rect):
        self.rect = rect
        self.active = True

    def check(self, player_rect):
        return self.active and self.rect.colliderect(player_rect)
        
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

    def draw(self, screen, image):
        if self.visible:
            screen.blit(image, self.rect.topleft)

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

    def draw(self, screen):
        if self.collected:
            return

        screen.blit(
            self.frames[self.frame_index],
            self.rect.topleft
        )

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

    def draw(self, screen):
        if self.active_timer > 0:
            image = self.active_image
        else:
            image = self.normal_image

        screen.blit(image, self.rect.topleft)



