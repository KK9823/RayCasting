import pygame
from sys import exit
import math


class Player:
    def __init__(self, x, y, angle=0, fov=math.pi/2, rays=400):
        self.x = x
        self.y = y
        self.angle = angle
        self.fov = fov
        self.rays = rays
        self.speed = 0.03
        self.camera_sens = 0.02
        self.wall_width = width/rays

    def getinput(self):
        keys = pygame.key.get_pressed()

        speed = self.speed*2 if keys[pygame.K_LSHIFT] else self.speed

        if keys[pygame.K_w]:
            angle = self.angle
            self.x += speed * math.cos(angle)
            self.y -= speed * math.sin(angle)
        elif keys[pygame.K_s]:
            angle = self.angle + math.pi
            self.x += speed * math.cos(angle)
            self.y -= speed * math.sin(angle)

        if keys[pygame.K_a]:
            angle = self.angle + math.pi/2
            self.x += speed * math.cos(angle)
            self.y -= speed * math.sin(angle)
        elif keys[pygame.K_d]:
            angle = self.angle - math.pi/2
            self.x += speed * math.cos(angle)
            self.y -= speed * math.sin(angle)

        if keys[pygame.K_LEFT]:
            self.angle += self.camera_sens
        elif keys[pygame.K_RIGHT]:
            self.angle -= self.camera_sens

    def make_rays(self):
        start = self.angle + self.fov/2
        diff = self.fov / self.rays
        ray_angles = [0.0] * self.rays
        for i in range(self.rays):
            ray_angles[i] = start - i*diff

        return ray_angles

    def draw_walls(self):
        lst = self.make_rays()
        prev_side = None
        prev_h = None
        diff = 10           # if abs(prev_h-h) > diff, we assume they are different walls

        for i, ray in enumerate(lst):
            d, hx, hy, side = calc_dist(self.x, self.y, ray)
            # Fisheye correction
            d *= math.cos(ray - self.angle)


            # Compute wall height
            h = calc_height(d)
            h = max(0, min(height, h))

            # Distance shading
            brightness = 255 * math.exp(-d * 0.15)

            brightness = max(0, min(255, brightness))

            # Draw the rectangle
            surf = pygame.Surface((self.wall_width, h))
            surf.fill((brightness, brightness, brightness))

            rect = surf.get_rect(topleft=(i * self.wall_width, (height-h)/2))
            screen.blit(surf,rect)

            # If it is a corner, draw a black line instead (black rectangle slice)
            if prev_side is not None and (prev_side != side or abs(prev_h-h) > diff):
                pygame.draw.line(
                    screen,
                    (0,0,0),
                    (i * self.wall_width, (height - h) / 2),
                    (i * self.wall_width, (height + h) / 2),
                    1
                )

            # else, draw black strips on top and bottom (as borders)
            else:
                # Top strip
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (i * self.wall_width, (height - h) / 2),
                    (i * self.wall_width + self.wall_width, (height - h) / 2),
                    1
                )

                # Bottom strip
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (i * self.wall_width, (height + h) / 2),
                    (i * self.wall_width + self.wall_width, (height + h) / 2),
                    1
                )

            prev_side = side
            prev_h = h

    def update(self):
        self.angle %= 2 * math.pi
        self.getinput()
        self.draw_walls()



def make_surfs_and_rects(reverse=False):

    fade_rate = 1.5
    shrink = 0.995

    res = []
    h = height/40
    cur = 0
    while True:
        surf = pygame.Surface((width,h))
        v = max(0, 200-cur*fade_rate)
        surf.fill((v, v, v))

        if not reverse:
            rect = surf.get_rect(topleft=(0,cur))
        else:
            rect = surf.get_rect(bottomleft=(0,height-cur))
        res.append((surf,rect))

        cur += h
        h = int(h*shrink)

        if h <= 0.1:
            break

    return res

def draw_surfs_and_rects(lst):
    for surf, rect in lst:
        screen.blit(surf, rect)

def process_map(map):
    res = []
    px = py = 0
    for ri, row in enumerate(map):
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
    return res, Player(px, py)


def calc_dist(x, y, angle):
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

        if get_val(map_y, map_x) == 1:
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



def get_val(ri,ci):
    if ri < 0 or ri >= len(map): return 1
    if ci < 0 or ci >= len(map[ri]): return 1
    if map[ri][ci] == 1: return 1
    return 0

def calc_height(dist):
    return height - dist * (height/20)

def draw_minimap(player):
    TILE = 8

    # Draw map
    for ri, row in enumerate(map):
        for ci, val in enumerate(row):
            color = (80, 80, 80) if val == 1 else (10, 10, 10)
            pygame.draw.rect(screen, color, (ci*TILE, ri*TILE, TILE, TILE))

    # Player position
    px = player.x * TILE
    py = player.y * TILE
    pygame.draw.circle(screen, (255, 0, 0), (px, py), 3)

    # Draw rays
    rays = player.make_rays()
    for ray_angle in rays:
        dist, hx, hy, side = calc_dist(player.x, player.y, ray_angle)

        # Convert hit position to minimap scale
        hx *= TILE
        hy *= TILE

        pygame.draw.line(
            screen,
            (0, 255, 0),     # ray color
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


pygame.init()

width = 1200
height = 600

raw_map = [
    "111111111111111111111111111111111111",
    "111111111111111    111111     111111",
    "11111111111         111            1",
    "11111111                    11     1",
    "11111                        1     1",
    "11            111     1111      1111",
    "11 C    1     111     1            1",
    "11            111     1     11     1",
    "1111111111            1     11     1",
    "1111111111           11     11     1",
    "11       1    111    11  11 11 11  1",
    "111           111    11  11111111  1",
    "111111        111   111            1",
    "111111111111111111111111111111111111"
]

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
framerate = 60

ceiling = make_surfs_and_rects()
floor = make_surfs_and_rects(True)

map, player = process_map(raw_map)


while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    draw_surfs_and_rects(ceiling)
    draw_surfs_and_rects(floor)

    player.update()
    draw_minimap(player)

    pygame.display.update()
    clock.tick(framerate)