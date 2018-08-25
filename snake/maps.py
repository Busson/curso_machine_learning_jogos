'''
DeepLearning Snake
Copyright (C) 2018 by Antonio J. Grandson Busson <busson@outlook.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import pygame
import numpy as np
import random 

random.seed(0)

#DIMENSOES
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
MAP_WIDTH = 30
MAP_HEIGHT = 30
TILE_WIDTH = int(WINDOW_WIDTH/MAP_WIDTH)
TILE_HEIGHT = int(WINDOW_HEIGHT/MAP_HEIGHT)

#MAPA
MAP = np.zeros((MAP_WIDTH, MAP_HEIGHT))




def draw_map(screen):
    for (x,y), value in np.ndenumerate(MAP):
        if value == 2:
            pygame.draw.rect(screen, (100,100,100), pygame.Rect(x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
        elif value == 3:
            pygame.draw.rect(screen, (255,40,40), pygame.Rect(x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))


def reg_snake_in_map(snakes_data): 
    global MAP
    for key, snake in snakes_data.items():
        for snake_piece in snake["corpo"]:
            x, y = snake_piece
            if MAP[x,y] != 2 and MAP[x,y] != 3:
                MAP[x,y] = 1       

def is_a_mortal_tile(tile_value):
    if tile_value > 0 and tile_value < 3:
        return True
    return False

def is_a_apple_tile(tile_value):
    if tile_value == 3:
        return True
    return False

def remove_apple_from_map(x,y):
    global MAP
   
    MAP[x][y] = 0

def get_apple_position():
    global MAP
    for (x, y), value in np.ndenumerate(MAP):
        if value == 3:
            return (x,y)

    return -1,-1

def create_apple_in_map():
    global MAP
    
    rand_x = random.randint(1, MAP_WIDTH-1)
    rand_y = random.randint(1, MAP_HEIGHT-1)

    if MAP[rand_x][rand_y] == 0:
        MAP[rand_x][rand_y] = 3
    else:
        create_apple_in_map()

def unreg_snake_in_map():
    global MAP
    for (x, y), _ in np.ndenumerate(MAP):
        if MAP[x,y] != 2 and MAP[x,y] != 3:
            MAP[x,y] = 0

def create_map_radome():
    global MAP
    for (x,y), value in np.ndenumerate(MAP):

        if (x == 0 or x == 29) or (y == 0 or y == 29):
            MAP[x,y] = 2


def create_map_rooms(): 
    global MAP
    for (x,y), value in np.ndenumerate(MAP):

        if (x == 0 or x == 29) or (y == 0 or y == 29):
            MAP[x,y] = 2

        if (x == 10 or x == 20) or (y == 10 or y == 20):
            MAP[x,y] = 2

            if (y == 10 or y == 20):
                MAP[14][y] = 0
                MAP[15][y] = 0
                MAP[16][y] = 0  
                MAP[4][y] = 0
                MAP[5][y] = 0 
                MAP[24][y] = 0
                MAP[25][y] = 0

            if (x == 10 or x == 20):  
                MAP[x][14] = 0
                MAP[x][15] = 0
                MAP[x][16] = 0  
                MAP[x][4] = 0
                MAP[x][5] = 0 
                MAP[x][24] = 0
                MAP[x][25] = 0


def create_map_rocks():
    global MAP
    for (x,y), value in np.ndenumerate(MAP):

        if (x < 5 or x > 23) or (y < 5 or y > 23):
            if x%3 == 0 and y%3 == 0:
                MAP[x,y] = 2
        else: 
            if x%4 == 0 and y%4 == 0:
                MAP[x,y] = 2
        