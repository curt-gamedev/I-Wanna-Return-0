

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x = 0
        self.y = 0

    def update(self, player_rect, map_width, map_height, mode):
        if mode == "horizontal_follow":
            self.update_follow(player_rect, map_width, map_height)
        else:
            self.update_snap(player_rect, map_width, map_height)

    def update_snap(self, player_rect, map_width, map_height):
        self.x = (player_rect.centerx // self.width) * self.width
        self.y = (player_rect.centery // self.height) * self.height

        max_x = max(0, map_width - self.width)
        max_y = max(0, map_height - self.height)

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def update_follow(self, player_rect, map_width, map_height):
        left_boundary = self.width * 0.25
        right_boundary = self.height * 0.65

        player_screen_x = player_rect.centerx - self.x

        if player_screen_x < left_boundary:
            self.x = player_rect.centerx - left_boundary
        elif player_screen_x > right_boundary:
            self.x = player_rect.centerx - right_boundary

        max_x = max(0, map_width - self.width)

        self.x = max(0, min(self.x, max_x))

        self.y = 0

    def apply_rect(self, rect):
        return rect.move(-self.x, -self.y)

    def apply_position(self, x, y):
        return (x - self.x, y - self.y)