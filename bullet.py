

class Bullet:
    def __init__(self, x, y, direction, image):
        self.image = image

        self.x = float(x)
        self.y = float(y)

        self.speed = 16.0
        self.direction = direction

        self.timer = 40
        self.active = True

        self.rect = self.image.get_rect(
            center=(round(self.x), round(self.y))
        )

    def update(self, collision_rects):
        if not self.active:
            return

        # Lifetime
        self.timer -= 1

        if self.timer < 0:
            self.active = False
            return

        # Movement
        self.x += self.speed * self.direction

        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        # Destroy on solid collision
        for solid in collision_rects:
            if self.rect.colliderect(solid):
                self.active = False
                break

    def draw(self, screen, camera):
        if self.active:
            draw_rect = self.rect.move(-camera.x, -camera.y)
            screen.blit(self.image, draw_rect)