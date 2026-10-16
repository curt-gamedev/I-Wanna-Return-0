import pygame
from paths import resource_path

SFX_VOLUME = 0.35

class AudioManager:
    def __init__(self):
        self.sfx_volume = SFX_VOLUME
        self.sounds = []

        self.jump_sound = self._load_sound("sndJump.wav")
        self.double_jump_sound = self._load_sound("sndDJump.wav")
        self.death_sound = self._load_sound("sndDeath.wav")
        self.coin_sound = self._load_sound("coin.wav")
        self.shoot_sound = self._load_sound("sndShoot.wav")
        self.save_sound = self._load_sound("sndItem.wav")

    def _load_sound(self, filename):
        sound = pygame.mixer.Sound(resource_path(f"assets/sfx/{filename}"))
        sound.set_volume(self.sfx_volume)
        self.sounds.append(sound)
        return sound    

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds:
            sound.set_volume(self.sfx_volume)