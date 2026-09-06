import pygame

class AudioManager:
    def __init__(self):
        self.jump_sound = pygame.mixer.Sound("assets/sfx/sndJump.wav")
        self.double_jump_sound = pygame.mixer.Sound("assets/sfx/sndDJump.wav")
        self.death_sound = pygame.mixer.Sound("assets/sfx/sndDeath.wav")
        self.coin_sound = pygame.mixer.Sound("assets/sfx/coin.wav")
        self.shoot_sound = pygame.mixer.Sound("assets/sfx/sndShoot.wav")
        self.save_sound = pygame.mixer.Sound("assets/sfx/sndItem.wav") #temporary