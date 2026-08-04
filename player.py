# Player Class

import pygame
import math

import config
import helpers

class Player:
    def __init__(self, x, y, screen, map, angle=0, fov=math.pi/3, rays=600):
        self.x = x
        self.y = y
        self.screen = screen
        self.map = map
        self.angle = angle
        self.fov = fov
        self.rays = rays
        self.speed = 0.03
        self.camera_sens = 0.02
        self.wall_width = config.width/rays

    def move(self):
        keys = pygame.key.get_pressed()

        speed = self.speed*2 if keys[pygame.K_LSHIFT] else self.speed
        angle = 0

        # Player Movements
        if keys[pygame.K_w] and keys[pygame.K_s]:
            if keys[pygame.K_a] and keys[pygame.K_d]:
                speed = 0
            elif keys[pygame.K_a]:
                angle = self.angle + math.pi / 2
            elif keys[pygame.K_d]:
                angle = self.angle - math.pi / 2
            else:
                speed = 0

        elif keys[pygame.K_w]:
            if keys[pygame.K_a] and keys[pygame.K_d]:
                angle = self.angle
            elif keys[pygame.K_a]:
                angle = self.angle + math.pi/4
            elif keys[pygame.K_d]:
                angle = self.angle - math.pi/4
            else:
                angle = self.angle

        elif keys[pygame.K_s]:
            if keys[pygame.K_a] and keys[pygame.K_d]:
                angle = self.angle + math.pi
            elif keys[pygame.K_a]:
                angle = self.angle + math.pi * 3/4
            elif keys[pygame.K_d]:
                angle = self.angle - math.pi * 3/4
            else:
                angle = self.angle + math.pi

        else:
            if keys[pygame.K_a] and keys[pygame.K_d]:
                speed = 0
            elif keys[pygame.K_a]:
                angle = self.angle + math.pi / 2
            elif keys[pygame.K_d]:
                angle = self.angle - math.pi / 2
            else:
                speed = 0

        new_x = self.x + speed * math.cos(angle)
        new_y = self.y - speed * math.sin(angle)

        # Only move the player if the new position in any direction is NOT a wall
        if not helpers.is_wall(new_x, self.y, self.map):
            self.x = new_x
        if not helpers.is_wall(self.x, new_y, self.map):
            self.y = new_y

        # Camera movements
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
        diff = 20           # if abs(prev_h-h) > diff, we assume they are different walls

        for i, ray in enumerate(lst):
            d, hx, hy, side = helpers.calc_dist(self.x, self.y, ray, self.map)
            # Fisheye correction
            angle_diff = ray - self.angle
            d *= math.cos(angle_diff)



            # Compute wall height
            h = helpers.calc_height(d)
            h = max(0, min(config.height, h))

            # Distance shading
            brightness = 255 * math.exp(-d * 0.15)
            brightness = max(0, min(255, brightness))

            # Draw the rectangle
            surf = pygame.Surface((self.wall_width, h))
            surf.fill((brightness, brightness, brightness))

            rect = surf.get_rect(topleft=(i * self.wall_width, (config.height-h)/2))
            self.screen.blit(surf,rect)

            # If it is a corner, draw a black line instead (black rectangle slice)
            if prev_side is not None and (prev_side != side or abs(prev_h-h) > diff):
                pygame.draw.line(
                    self.screen,
                    (0,0,0),
                    (i * self.wall_width, (config.height - h) / 2),
                    (i * self.wall_width, (config.height + h) / 2),
                    1
                )

            # else, draw black strips on top and bottom (as borders)
            else:
                # Top strip
                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),
                    (i * self.wall_width, (config.height - h) / 2),
                    (i * self.wall_width + self.wall_width, (config.height - h) / 2),
                    1
                )

                # Bottom strip
                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),
                    (i * self.wall_width, (config.height + h) / 2),
                    (i * self.wall_width + self.wall_width, (config.height + h) / 2),
                    1
                )

            prev_side = side
            prev_h = h

    def update(self):
        self.angle %= 2 * math.pi
        self.move()
        self.draw_walls()
