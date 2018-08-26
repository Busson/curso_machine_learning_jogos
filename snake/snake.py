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
from maps import *
from neural_net import *


def create_snake_body(head_position, size, initial_orientation):
    snake_pieces = []
    dir_vector = (0,0)

    if initial_orientation == "norte":
        dir_vector = (0,1)
    elif initial_orientation == "sul":
        dir_vector = (0,-1)
    elif initial_orientation == "leste":
        dir_vector = (-1,0)
    elif initial_orientation == "oeste":
        dir_vector = (1,0)

    last_pos = head_position
    for i in range(0,size):
        piece_position = (last_pos[0]+(i*dir_vector[0]), last_pos[1]+(i*dir_vector[1]))
        snake_pieces.append(piece_position)
    
    return snake_pieces

def create_snake(head_position, size, color, initial_orientation):
    snake_pieces = create_snake_body(head_position, size, initial_orientation)    
    snake = {"corpo": snake_pieces, "pontos": 0, "orientacao": initial_orientation, "cor": color, "vivo": True, "ini_pos": head_position, "ini_size": size, "init_ori": initial_orientation}
    return snake

def draw_snake(screen, snake):
    for snake_piece in snake["corpo"]:
        x, y = snake_piece
        color = snake["cor"]
        if snake["vivo"] == False:
            color = (100,100,100)
        pygame.draw.rect(screen, snake["cor"], pygame.Rect(x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT))


def kill_snake(snake):
    snake["vivo"] = False
    #snake["corpo"].pop(0)
    #snake["corpo"].pop(0)


def snake_sense(snake):
    global MAP
    front = 0
    right = 0
    left = 0

    x, y = snake["corpo"][0]

    if snake["orientacao"] == "norte":
        front = MAP[x, (y-1) if y > 0 else (MAP_HEIGHT-1)]
        right = MAP[(x+1) if x < (MAP_WIDTH-1) else 0, y]
        left = MAP[(x-1) if x > 0 else (MAP_WIDTH-1) , y]

    elif snake["orientacao"] == "sul":
        front = MAP[x, (y+1) if y < (MAP_HEIGHT-1) else 0]
        right = MAP[(x-1) if x > 0 else (MAP_WIDTH-1) , y]
        left = MAP[(x+1) if x < (MAP_WIDTH-1) else 0, y]

    elif snake["orientacao"] == "leste":
        front = MAP[(x+1) if x < (MAP_WIDTH-1) else 0, y]
        right = MAP[x, (y+1) if y < (MAP_HEIGHT-1) else 0]
        left = MAP[x, (y-1) if y > 0 else (MAP_HEIGHT-1)]
    
    elif snake["orientacao"] == "oeste":
        front = MAP[(x-1) if x > 0 else (MAP_WIDTH-1) , y]
        right = MAP[x, (y-1) if y > 0 else (MAP_HEIGHT-1)]
        left = MAP[x, (y+1) if y < (MAP_HEIGHT-1) else 0]

    #print("F:", front, "R:", right, "L:", left)

    if left > 0 and left < 3:
        left = 1
    if front > 0 and front < 3:
        front = 1
    if right > 0 and right < 3:
        right = 1

    return left, front, right


def get_snake_sense_data(snake, MODE):
    
    left, front, right = snake_sense(snake) 

    x_data = np.zeros((3, 4))
    y_data = np.zeros((3, 1))

    if MODE == "hungry":
        x_data = np.zeros((3, 5))
        y_data = np.zeros((3, 2))

    for i in range(0,3):
        x_data[i][0] = left
        x_data[i][1] = front
        x_data[i][2] = right

        if i == 0:
            x_data[i][3] = -1
            if left != 1:
                y_data[i][0] = 1
        elif i == 1:
            x_data[i][3] = 0
            if front != 1:
                y_data[i][0] = 1
        elif i == 2:
            x_data[i][3] = 1
            if right != 1:
                y_data[i][0]= 1

        if MODE == "hungry":
            apple_ang = calc_angle_to_apple(snake)
            x_data[i][4] = apple_ang

            if apple_ang == -1 and i == 0:
                y_data[i][1]= 1
            elif apple_ang == 0 and i == 1:
                y_data[i][1]= 1
            elif apple_ang == 1 and i == 2:
                y_data[i][1]= 1

    return x_data, y_data

def feed_snake(snake):

    snake_tail = snake["corpo"][-1]
    dir_vector = (0,0)
    if snake["orientacao"] == "norte":
        dir_vector = (0,1)
    elif snake["orientacao"] == "sul":
        dir_vector = (0,-1)
    elif snake["orientacao"] == "leste":
        dir_vector = (-1,0)
    elif snake["orientacao"] == "oeste":
        dir_vector = (1,0)

    new_tail = (snake_tail[0]+dir_vector[0], snake_tail[1]+dir_vector[1])
    
    if new_tail[0] < 0:
        new_tail = ((MAP_WIDTH-1),new_tail[1])
    if new_tail[0] > (MAP_WIDTH-1):
        new_tail = (0,new_tail[1])
    if new_tail[1] < 0:
        new_tail = (new_tail[0], (MAP_HEIGHT-1))
    if new_tail[1] > (MAP_HEIGHT-1):
        new_tail = (new_tail[0], 0)      

    snake["corpo"].append(new_tail)
    snake["pontos"] += 1

def decision_to_vector(decision, orientation):
    move_vector = (0,0)
    new_orientation = orientation
    if orientation == "norte":
        if decision == 0:
            move_vector = (0,-1)
        elif decision == 1:
            move_vector = (1,0)
            new_orientation = "leste"
        elif decision == -1:
            move_vector = (-1,0)
            new_orientation = "oeste"
    elif orientation == "sul":
        if decision == 0:
            move_vector = (0,1)
        elif decision == 1:
            move_vector = (-1,0)
            new_orientation = "oeste"
        elif decision == -1:
            move_vector = (1,0)
            new_orientation = "leste"
    elif orientation == "leste":      
        if decision == 0:
            move_vector = (1,0)
        elif decision == 1:
            move_vector = (0,1)
            new_orientation = "sul"
        elif decision == -1:
            move_vector = (0,-1)
            new_orientation = "norte"
    elif orientation == "oeste":
        if decision == 0:
            move_vector = (-1,0)
        elif decision == 1:
            move_vector = (0,-1)
            new_orientation = "norte"
        elif decision == -1:
            move_vector = (0,1)
            new_orientation = "sul"

    return  move_vector, new_orientation

def move_snake(snake, decision):    
    global MAP

    if  snake["vivo"] == False:
        return

    move_vector, snake["orientacao"] = decision_to_vector(decision, snake["orientacao"])
    nex_pos = (snake["corpo"][0][0] + move_vector[0], snake["corpo"][0][1]+ move_vector[1])   

    #VERIFICANDO OS LIMITES DO MAPA
    if nex_pos[0] >= MAP_WIDTH:
        nex_pos = (0, nex_pos[1])
    if nex_pos[1] >= MAP_HEIGHT:
        nex_pos = (nex_pos[0], 0)
    
    if nex_pos[0] < 0:
        nex_pos = (MAP_WIDTH-1, nex_pos[1])
    if nex_pos[1] < 0:
        nex_pos = (nex_pos[0], MAP_HEIGHT-1)
    
    for index in range(len(snake["corpo"])-1,0, -1):
        snake["corpo"][index] = snake["corpo"][index-1] 

    snake["corpo"][0] = nex_pos

    #print(snake["corpo"][0],snake["corpo"][1])
    
    x, y = snake["corpo"][0]

    if is_a_apple_tile(MAP[x,y]):
        remove_apple_from_map(x,y)
        feed_snake(snake)
        create_apple_in_map()

    
    if is_a_mortal_tile(MAP[x,y]):
        kill_snake(snake)
        return 


def calc_angle_to_apple(snake):
   
    apple = get_apple_position()
    if apple[0] == -1:
        return -2

    #print(apple)

    in_front = 0
    in_left = 0
    in_right = 0

    snake_head = snake["corpo"][0]

    if snake["orientacao"] == "norte":
        if apple[0] == snake_head[0]:
            in_front = 1
        elif apple[0] > snake_head[0]:
            in_right = 1
        elif apple[0] < snake_head[0]:
            in_left = 1
    elif snake["orientacao"] == "sul":
        if apple[0] == snake_head[0]:
            in_front = 1
        elif apple[0] < snake_head[0]:
            in_right = 1
        elif apple[0] > snake_head[0]:
            in_left = 1
    elif snake["orientacao"] == "leste":
        if apple[1] == snake_head[1]:
            in_front = 1
        elif apple[1] > snake_head[1]:
            in_right = 1
        elif apple[1] < snake_head[1]:
            in_left = 1
    elif snake["orientacao"] == "oeste":
        if apple[1] == snake_head[1]:
            in_front = 1
        elif apple[1] < snake_head[1]:
            in_right = 1
        elif apple[1] > snake_head[1]:
            in_left = 1

    if in_left == 1:
        return -1
    elif in_front == 1:
        return 0
    elif in_right == 1:
        return 1


def restart_game(snakes_data):
    for key, snake in snakes_data.items():
        snake["vivo"] = True
        snake["corpo"] = create_snake_body(snake["ini_pos"], snake["ini_size"], snake["orientacao"])
        snake["pontos"] = 0  

def game_is_over(snakes_data):

    num_player = len(snakes_data.items())
    num_alive = 0
    for key, snake in snakes_data.items():
        if snake["vivo"] == True:
            num_alive += 1
    
    if num_player == 1 and num_alive == 0:
        return True
    if num_alive == (num_player-1):
        return True 

    return False
    