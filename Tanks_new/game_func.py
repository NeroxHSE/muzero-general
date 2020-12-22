import os
import sys
import pygame
import numpy as np
from .block import Block
from .tank import Tank
from .maze import draw_maze, maze_generation
import math
import matplotlib.pyplot as plt
import cv2
from PIL import Image


class GameFunc:
    def __init__(self, settings, screen):
        pygame.init()
        self.screen = screen
        self.settings = settings
        self.main_rect = pygame.Rect(settings.main_rect)
        self.blocks = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.tank1 = None
        self.game_over = False
        self.last = None
        draw_maze(maze_generation(7,6))
        self.map_in_txt = self.map_reader_txt()
        self.get_observation()
        self.collisions_happened = 0


    def to_play(self):
        return 0

    def step(self, action):
        if action == 0:
            self.tank1.move_by_action(0)
            done = self.game_over
        elif action == 1:
            self.tank1.move_by_action(1)
            done = self.game_over
        elif action == 2:
            self.tank1.move_by_action(2)
            done = self.game_over
        elif action == 3:    
            self.tank1.move_by_action(3)
            done = self.game_over

        return self.get_observation(), self.get_reward(done), done  
        
    def rect_distance(self, rect1, rect2):
        x1, y1 = rect1.topleft
        x1b, y1b = rect1.bottomright
        x2, y2 = rect2.topleft
        x2b, y2b = rect2.bottomright
        left = x2b < x1
        right = x1b < x2
        top = y2b < y1
        bottom = y1b < y2
        if bottom and left:
            return math.hypot(x2b-x1, y2-y1b)
        elif left and top:
            return math.hypot(x2b-x1, y2b-y1)
        elif top and right:
            return math.hypot(x2-x1b, y2b-y1)
        elif right and bottom:
            return math.hypot(x2-x1b, y2-y1b)
        elif left:
            return x1 - x2b
        elif right:
            return x2 - x1b
        elif top:
            return y1 - y2b
        elif bottom:
            return y2 - y1b
        else:  
            return 0

    def render(self):
        self.check_events()
        self.update_screen()
        self.clock.tick(self.settings.FPS)

    def calculate_reward(self):

        reward = 0
        #if self.tank1.get_collision() > self.collisions_happened:
        #    self.collisions_happened = self.tank1.get_collision()
        #    reward-=1

        for block in self.blocks:
            block_rect, finish = block.get_rect()
            if finish == True:
                break
        now = self.rect_distance(self.tank1.get_rect(), block_rect)
        if self.last == None:
            self.last = now
            reward-=1
            return reward
        if self.last - now >= 0:
            self.last = now
            reward+=1
            return reward
        else:
            reward-=1
            return reward

        
        #print(1-self.rect_distance(self.tank1.get_rect(), block_rect)/1000)
        #return 1-self.rect_distance(self.tank1.get_rect(), block_rect)/1000

    def get_reward(self, done):
        if not done:
            reward = self.calculate_reward()
            return reward
        else:
            return 100

    

    def reset(self):
        self.game_over = False
        self.blocks = pygame.sprite.Group()
        self.tank1 = None
        self.collisions_happened = 0 
        draw_maze(maze_generation(7,6))
        self.map_in_txt = self.map_reader_txt()
        return self.get_observation()

    def get_observation(self): #возвращает карту с позицией танка
        #print(self.map_in_txt, np.shape(self.map_in_txt))
       # print(np.shape())
        #fig, ax = plt.subplots()

        #plt.imshow(pygame.surfarray.array3d(self.screen))
        #plt.show(block=False)
        #np.reshape(pygame.surfarray.array3d(self.screen), (3, 1096, 960))
        scr = pygame.surfarray.array3d(self.screen)#.transpose(2,1,0)

        img = Image.fromarray(scr)

        return np.array(img.resize((96,96))).transpose(2,1,0)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.calculate_reward()      

    def update_screen(self):
       # self.screen.fill(self.settings.scoreboard_bg)
        self.screen.fill(self.settings.battlefield_bg, self.main_rect)

        self.blocks.update()
        self.check_collide_tb()
        self.tank1.update()
        pygame.display.flip()

    def map_reader_txt(self):
        path = 'Tanks_new/Maps/level_1.goose'
        txt_map = []
        matrix_map = None

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
                    self.tank1 = Tank((x * 64 + 32, y * 64 + 32), self.settings, self.screen )
                x += 1
            y += 1

        rows = [row for row in open(path).read().split('\n')] 
        matrix = []
        for i in range(len(rows)-1):
            matrix.append(list(map(int, rows[i])))
        
        return np.reshape(np.array(matrix, dtype="int32"), (1,14,15))

    def check_collide_tb(self):
        collide = pygame.sprite.spritecollideany(self.tank1, self.blocks)
        block_hit_list = pygame.sprite.spritecollide(self.tank1, self.blocks, False)
        for block in block_hit_list:
            if block.finish_block == True:
                self.game_over = True
        if collide:
            if type(collide) == Block:
                self.tank1.bump_block()
                self.tank1.collision_counter()
                
                
                  
