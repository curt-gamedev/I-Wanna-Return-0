import pygame
from paths import resource_path

class Animation:
    def __init__(self, frames, image_speed=0.2, loop=True):
        self.frames = frames
        self.image_speed = image_speed
        self.loop = loop
        self.image_index = 0.0

    def update(self):
        if not self.frames:
            return

        self.image_index += self.image_speed

        if self.loop:
            self.image_index %= len(self.frames)
        else:
            self.image_index = min(self.image_index, len(self.frames) - 1)

    def reset(self):
        self.image_index = 0.0

    def get_frame(self):
        if not self.frames:
            return None

        return self.frames[int(self.image_index)]


class PlayerAnimation:
    def __init__(self):

        idle_frames = [
            pygame.image.load(resource_path("assets/player/PlayerIdle_0.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerIdle_1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerIdle_2.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerIdle_3.png")).convert_alpha()
        ]

        run_frames = [
            pygame.image.load(resource_path("assets/player/PlayerRunning_0.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerRunning_1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerRunning_2.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerRunning_3.png")).convert_alpha()
        ]

        jump_frames = [
            pygame.image.load(resource_path("assets/player/PlayerJump_0.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerJump_1.png")).convert_alpha()
        ]

        fall_frames = [
            pygame.image.load(resource_path("assets/player/PlayerFall_0.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/PlayerFall_1.png")).convert_alpha()
        ]

        self.animations = {
            "idle": Animation(idle_frames, image_speed=0.2),
            "run": Animation(run_frames, image_speed=0.5),
            "jump": Animation(jump_frames, image_speed=0.2),
            "fall": Animation(fall_frames, image_speed=0.2)
        }

        self.state = "idle"
        self.current = self.animations[self.state]

    def set_state(self, state):
        if state == self.state:
            return

        self.state = state
        self.current = self.animations[state]

        # Start new animations from frame 0
        self.current.reset()

    def update(self):
        self.current.update()

    def get_frame(self):
        return self.current.get_frame()

class ScrollingText:
    def __init__(self, lines, font, start_y, speed=0.5, line_spacing=40):
        self.lines = lines
        self.font = font
        self.y = float(start_y)
        self.speed = speed
        self.line_spacing = line_spacing

    def update(self):
        self.y -= self.speed

    def draw(self, screen):
        for i, line in enumerate(self.lines):
            image = self.font.render(line, True, (255, 255, 255))

            rect = image.get_rect(centerx=screen.get_width() // 2)

            rect.y = round(self.y + i * self.line_spacing)

            screen.blit(image, rect)