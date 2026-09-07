import pygame
import random
import math


class BloodParticle:
    def __init__(self, x, y):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.0, 5.0)

        self.x = float(x)
        self.y = float(y)

        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed

        self.gravity = 0.15

        self.life = 100
        self.radius = random.choice((2, 2, 2, 3))

    def update(self):
        self.velocity_y += self.gravity

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.life -= 1

    def draw(self, screen, camera):
        draw_x = round(self.x - camera.x)
        draw_y = round(self.y - camera.y)
        pygame.draw.circle(
            screen,
            (150, 0, 0),
            (draw_x, draw_y),
            self.radius
            )
        