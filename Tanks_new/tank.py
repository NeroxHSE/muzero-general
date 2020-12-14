import pygame
#import game_func as gff


class Tank(pygame.sprite.Sprite):
    def __init__(self, pos, settings, screen):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.pos = pos
        self.now_img = pygame.transform.scale(pygame.image.load('Models/Players/player.png').convert_alpha(), (8 * 4, 8 * 4))
        
        self.rect = pygame.Rect(pos[0], pos[1], self.now_img.get_width(), self.now_img.get_height())
        
        self.rot = 0
        self.rotated_img = self.now_img
        self.bumped = False

    def get_rect(self):
        return self.rect


    def update(self):
        self.move_pos(pygame.key.get_pressed())
        self.screen.blit(self.rotated_img, self.rect)

    def move_pos(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.settings.speed
            self.img_rotation(0)
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.settings.speed
            self.img_rotation(180)
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.settings.speed
            self.img_rotation(270)
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.settings.speed
            self.img_rotation(90)

    def move_by_action(self, action):
        if action == 0:
            self.rect.y -= self.settings.speed
            self.img_rotation(0)
        elif action == 1:
            self.rect.y += self.settings.speed
            self.img_rotation(180)
        elif action == 2:
            self.rect.x += self.settings.speed
            self.img_rotation(270)
        elif action == 3:        
            self.rect.x -= self.settings.speed
            self.img_rotation(90)

    def img_rotation(self, deg):
        self.rotated_img = pygame.transform.rotate(self.now_img, deg)
        self.rot = deg

        if self.rect.top < self.settings.main_rect.top:
            self.rect.top = self.settings.main_rect.top
        elif self.rect.bottom > self.settings.main_rect.bottom:
            self.rect.bottom = self.settings.main_rect.bottom
        if self.rect.right > self.settings.main_rect.right:
            self.rect.right = self.settings.main_rect.right
        elif self.rect.left < self.settings.main_rect.left:
            self.rect.left = self.settings.main_rect.left

    def bump_block(self):
        if self.rot == 0:
            self.rect.y += self.settings.speed
        elif self.rot == 90:
            self.rect.x += self.settings.speed
        elif self.rot == 270:
            self.rect.x -= self.settings.speed
        elif self.rot == 180:
            self.rect.y -= self.settings.speed
