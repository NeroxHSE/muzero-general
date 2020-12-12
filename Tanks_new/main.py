import pygame
from maze import draw_maze, maze_generation
from settings import Settings
from game_func import GameFunc


def run_game():
    pygame.init()
    settings = Settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(settings.screen_sizes)
    pygame.display.set_caption('Environment')
    game = GameFunc(settings, screen)
    draw_maze(maze_generation(7,6))
    game.map_reader_txt()

    while not game.game_over:
        game.check_events()
        game.update_screen()
        clock.tick(settings.FPS)
        
run_game()
