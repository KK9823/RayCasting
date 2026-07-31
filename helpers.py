# Helper functions used in the project

import pygame
import math
import config


# This function makes the surfaces and rectangles used for the ground and ceiling
# Called only once at the start, the surfaces and rectangles are reused every frame
# Pass in True to make floor, False for ceiling
def make_surfs_and_rects(reverse=False):
    fade_rate = 1.5
    shrink = 0.995

    res = []
    h = config.height/40
    cur = 0
    while True:
        surf = pygame.Surface((config.width,h))
        v = max(0, 200-cur*fade_rate)
        surf.fill((v, v, v))

        if not reverse:
            rect = surf.get_rect(topleft=(0,cur))
        else:
            rect = surf.get_rect(bottomleft=(0,config.height-cur))
        res.append((surf,rect))

        cur += h
        h = int(h*shrink)

        if h <= 0.1:
            break

    return res


# Takes in a list of tuples of surfaces and rectangles and draws them on the screen
def draw_surfs_and_rects(screen, lst):
    for surf, rect in lst:
        screen.blit(surf, rect)


# Process the raw map into a format we can use, also returns the player position
def process_map(raw_map):
    res = []
    px = py = 0
    for ri, row in enumerate(raw_map):
        r = []
        for ci, val in enumerate(row):
            if val == " ":
                r.append(0)
            elif val == "1":
                r.append(1)
            elif val == "C":
                r.append(0)
                px = ci
                py = ri
        res.append(r)
    return res, (px, py)


# Takes the start position (x,y) of a ray and the direction it will go
# Returns the distance the ray goes until it hits a wall on the map
def calc_dist(x, y, angle, map):
    dx = math.cos(angle)
    dy = -math.sin(angle)

    map_x = int(x)
    map_y = int(y)

    delta_dist_x = abs(1 / dx) if dx != 0 else float('inf')
    delta_dist_y = abs(1 / dy) if dy != 0 else float('inf')

    if dx < 0:
        step_x = -1
        side_dist_x = (x - map_x) * delta_dist_x
    else:
        step_x = 1
        side_dist_x = (map_x + 1 - x) * delta_dist_x

    if dy < 0:
        step_y = -1
        side_dist_y = (y - map_y) * delta_dist_y
    else:
        step_y = 1
        side_dist_y = (map_y + 1 - y) * delta_dist_y

    while True:
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_x += step_x
            side = 0
        else:
            side_dist_y += delta_dist_y
            map_y += step_y
            side = 1

        if get_val(map_y, map_x, map) == 1:
            break

    if side == 0:
        dist = side_dist_x - delta_dist_x
        hit_x = x + dx * dist
        hit_y = y + dy * dist
    else:
        dist = side_dist_y - delta_dist_y
        hit_x = x + dx * dist
        hit_y = y + dy * dist

    return dist, hit_x, hit_y, side


# Just a wrapper so that indexes out of range returns a wall
def get_val(ri,ci, map):
    if ri < 0 or ri >= len(map): return 1
    if ci < 0 or ci >= len(map[ri]): return 1
    if map[ri][ci] == 1: return 1
    return 0


# Takes the distance a ray goes before it hits a wall
# Returns the height of the rectangle that should be rendered by that ray
def calc_height(dist):
    return config.height - dist * (config.height/20)