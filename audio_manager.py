import pygame
from paths import resource_path

class AudioManager:
    def __init__(self):
        self.jump_sound = pygame.mixer.Sound(resource_path("assets/sfx/sndJump.wav"))
        self.double_jump_sound = pygame.mixer.Sound(resource_path("assets/sfx/sndDJump.wav"))
        self.death_sound = pygame.mixer.Sound(resource_path("assets/sfx/sndDeath.wav"))
        self.coin_sound = pygame.mixer.Sound(resource_path("assets/sfx/coin.wav"))
        self.shoot_sound = pygame.mixer.Sound(resource_path("assets/sfx/sndShoot.wav"))
        self.save_sound = pygame.mixer.Sound(resource_path("assets/sfx/sndItem.wav")) #temporary