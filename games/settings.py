import pygame

class Settings:
    def __init__(self):
        self.screen_sizes = (1096, 960)
        self.main_rect = pygame.Rect(32, 32, 1096, 960)
        self.multiply_size = 4
        self.FPS = 60
        self.anim_frame = 6
        self.scoreboard_bg = (100, 100, 100)
        self.battlefield_bg = (0, 0, 0)
        self.speed = 64

