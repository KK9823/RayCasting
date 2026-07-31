import pygame
from sys import exit
import math

import config
from player import Player
import helpers
import minimap

pygame.init()

# Setting up the screen and clock
screen = pygame.display.set_mode((config.width, config.height))
clock = pygame.time.Clock()

# Create surfaces and rectangles for floor and ceiling
ceiling = helpers.make_surfs_and_rects()
floor = helpers.make_surfs_and_rects(True)

# Process the map and create player object
map, player_pos = helpers.process_map(config.raw_map)
px, py = player_pos
player = Player(px, py, screen, map, 0, config.fov, config.rays)


while True:
    # "empty" the screen at the start of every frame
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw ceiling and floor
    helpers.draw_surfs_and_rects(screen, ceiling)
    helpers.draw_surfs_and_rects(screen, floor)

    # Call update method on player and draw the minimap
    player.update()
    minimap.draw_minimap(screen, player)

    pygame.display.update()
    clock.tick(config.framerate)