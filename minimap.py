# Minimap drawing functions

import pygame
import math
import helpers

# Pretty self-explanatory function name, draws the minimap
def draw_minimap(screen, player):
    TILE = 8
    map = player.map

    # Draw map
    for ri, row in enumerate(map):
        for ci, val in enumerate(row):
            color = (80, 80, 80) if val == 1 else (10, 10, 10) #grey if a wall, black otherwise
            pygame.draw.rect(screen, color, (ci*TILE, ri*TILE, TILE, TILE))

    # Calculate player position
    px = player.x * TILE
    py = player.y * TILE
    pygame.draw.circle(screen, (255, 0, 0), (px, py), 3)

    # Draw rays
    rays = player.make_rays()
    for ray_angle in rays:
        dist, hx, hy, side = helpers.calc_dist(player.x, player.y, ray_angle, map)

        # Convert hit position to minimap scale
        hx *= TILE
        hy *= TILE

        pygame.draw.line(
            screen,
            (0, 255, 0),     # ray color (green)
            (px, py),        # player position
            (hx, hy),        # hit position
            1                # thickness
        )

    # minimap label
    font = pygame.font.SysFont(None, 24)
    text = font.render("minimap", True, (255, 255, 255))

    minimap_width = len(map[0]) * TILE
    minimap_height = len(map) * TILE

    text_x = minimap_width / 2 - text.get_width() / 2
    text_y = minimap_height + 5  # 5 pixels below minimap

    draw_text_with_outline(screen, "minimap", text_x, text_y, font)


# This function draws the text "minimap" under the minimap
def draw_text_with_outline(surface, text, x, y, font):
    # Outline
    outline = font.render(text, True, (0, 0, 0))
    surface.blit(outline, (x-1, y))
    surface.blit(outline, (x+1, y))
    surface.blit(outline, (x, y-1))
    surface.blit(outline, (x, y+1))

    # Main text
    main = font.render(text, True, (255, 255, 255))
    surface.blit(main, (x, y))
