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


CONST_TRAIN_MODE = True
CONST_BOT_MODE = "hungry"

#create_map_rooms()
#create_map_radome()

snakes_data = {}
if CONST_TRAIN_MODE: 
    snakes_data["bot_snake"] = create_snake((15,15), 12, (0, 255, 128), "norte")
else:
    snakes_data["player_snake"] = create_snake((7,15), 3, (0, 128, 255), "norte") 
    snakes_data["bot_snake"] = create_snake((21,15), 3, (0, 255, 128), "norte") 


#inicializando os componentes do jogo
initialize_game(CONST_TRAIN_MODE, CONST_BOT_MODE)

#laço principal do jogo
while not GAME["end"]:

    #controla a velocidade do jogo e limpa o canvas
    await_ticks_and_fill_screen()

    #registra as posições onde as cobras estão passando
    reg_snake_in_map(snakes_data)

    #obtem os eventos de tecla
    capture_key_events()

    #processamento de cada cobra no jogo
    for key, snake in snakes_data.items():
        #as cobras bots e cobra jogador sao tratadas de maneiras diferentes
        if key == "player_snake":
           #move a cobra jogador de acordo com a tecla pressionada 
           move_snake(snake, GAME["player_current_key"])  
           
        else:
           #a funcao abaixo obtem os dados de sensoriamento da cobra que sao usados na rede neural 
           x_data, y_data = get_snake_sense_data(snake, CONST_BOT_MODE)
           bot_mov = feed_neural_net(snake, x_data, y_data, CONST_TRAIN_MODE, CONST_BOT_MODE)
           #a decisao de movimento retornada pela rede neural é usada para mover a cobra
           move_snake(snake, bot_mov) 
           
        #as informações da cobra sao enviadas para o core do jogo que atualizar a melhor pontuacao alcancada 
        update_best_pontuation(snake, key) 
               
        #desenha todas as cobras do mapa no canvas  
        draw_snake(GAME["screen"], snake) 
    
    #desenha todos os elementos do mapa no canvas
    draw_map(GAME["screen"])

    #limpa os registros do mapa
    unreg_snake_in_map()

    #checa se a partida terminou
    check_game_is_over(snakes_data)

    #desenha as informacoes do jogo no canvas e faz o flip para a tela
    draw_game_info_and_flip()
    



  