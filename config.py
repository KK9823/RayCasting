# This file contains some general (high level) parameters that can be used to tweak the simulation
from math import pi

# screen resolution
width = 1200
height = 600

# camera settings
fov = pi/3
rays = 600

framerate = 60

# Map
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