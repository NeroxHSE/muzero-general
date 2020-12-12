import os
import sys
import pygame

from block import Block
from tank import Tank

class GameFunc:
    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        self.main_rect = pygame.Rect(settings.main_rect)
        self.blocks = pygame.sprite.Group()
        self.tank1 = None
        self.game_over = False


    def reset(self):
        self.game_over = False
        self.tank1 = None
        self.map_reader_txt()   


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()   

    def update_screen(self):
        self.screen.fill(self.settings.scoreboard_bg)
        self.screen.fill(self.settings.battlefield_bg, self.main_rect)

        self.blocks.update()
        self.check_collide_tb()
        self.tank1.update()

        pygame.display.flip()

    def map_reader_txt(self):
        path = 'Maps/level_1.goose'
        txt_map = []

        with open(path, 'r') as f:
            for line in f:
                txt_map.append(list(line))

        y = 0
        for line in txt_map:
            x = 0
            for tile in line:
                if tile is '1':
                    block = Block((x * 64 + 32, y * 64 + 32), tile, self.screen)
                    self.blocks.add(block)
                if tile is '2':
                    block = Block((x * 64 + 32, y * 64 + 32), tile, self.screen)
                    self.blocks.add(block) 
                if tile is '3':
                    self.tank1 = Tank((x * 64 + 48, y * 64 + 48), self.settings, self.screen )
                x += 1
            y += 1

    def check_collide_tb(self):
        collide = pygame.sprite.spritecollideany(self.tank1, self.blocks)
        block_hit_list = pygame.sprite.spritecollide(self.tank1, self.blocks, False)
        for block in block_hit_list:
            if block.finish_block == True:
                self.game_over = True
        if collide:
            if type(collide) == Block:
                self.tank1.bump_block()
                
                
                  
