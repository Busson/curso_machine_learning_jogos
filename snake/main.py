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
from snake import *
from maps import *
from manager import *


TRAIN_MODE = True

snakes_data = {}

MATCH_NUMBER = 0

#create_map_rooms()
#create_map_radome()

create_apple_in_map()

if TRAIN_MODE: 
    snakes_data["bot_snake"] = create_snake((15,15), 5, (0, 255, 128), "norte", "hungry")
else:
    snakes_data["player_snake"] = create_snake((7,15), 5, (0, 255, 128), "norte") 
    snakes_data["bot_snake"] = create_snake((22,15), 5, (0, 255, 128), "norte", "hungry") 


train_best_score = 0


initialize_game(TRAIN_MODE)

while not GAME["end"]:

    await_ticks_and_fill_screen()

    reg_snake_in_map(snakes_data)

    capture_key_events()

    for key, snake in snakes_data.items():
        if key == "player_snake":
           move_snake(snake, None)  
        else:
        
           x_data, y_data = get_snake_sense_data(snake)
           #print(x_data, y_data) 
           bot_mov = feed_neural_net(snake, x_data, y_data, TRAIN_MODE)
           move_snake(snake, bot_mov) 

           update_best_pontuation(snake) 
               
           
        draw_snake(GAME["screen"], snake) 
    
    draw_map(GAME["screen"])

    check_game_is_over(snakes_data)
    
    unreg_snake_in_map()

    draw_game_info_and_flip()
    



  