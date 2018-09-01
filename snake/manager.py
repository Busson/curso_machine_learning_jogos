import pygame
import tensorflow as tf
from snake import *
from neural_net import *
from maps import *


GAME = {}
TRAINING_INFO = {}

CONST_RESTART_TIME = 5

def initialize_game(IS_TRANING, BOT_MODE):
    global GAME
    pygame.init()
    create_neural_net(BOT_MODE)
    init_tensorflow(IS_TRANING, BOT_MODE)
    pygame.display.set_caption('DeepLearning Snake')
    GAME["screen"] = pygame.display.set_mode((600, 600))
    GAME["clock"] = pygame.time.Clock() 
    GAME["is_training"] = IS_TRANING
    GAME["bot_mode"] = BOT_MODE
    if IS_TRANING: 
        GAME["clock_tick"] = 60
        TRAINING_INFO["max_pontuation"] = 0
        TRAINING_INFO["death_count"] = 0
    else: 
        GAME["clock_tick"] = 10
        GAME["snakes_points"] = {}
    GAME["end"] = False
    GAME["text_font"] = pygame.font.SysFont("comicsansms", 28)
    
    if BOT_MODE == "hungry":
        create_apple_in_map()

    GAME["player_current_key"] = 0
    GAME["game_is_over"] = False
    GAME["restart_counter"] = CONST_RESTART_TIME

def await_ticks_and_fill_screen():
    global GAME
    GAME["clock"].tick(GAME["clock_tick"])
    GAME["screen"].fill((0, 0, 0))
  

def update_best_pontuation(snake, snake_name):
    global GAME

    if GAME["game_is_over"]:
        return

    if GAME["is_training"]:
        if snake["pontos"] > TRAINING_INFO["max_pontuation"]:
            TRAINING_INFO["max_pontuation"] = snake["pontos"]
    else:
        GAME["snakes_points"][snake_name] = snake["pontos"]

def check_game_is_over(snakes_data):
    global GAME
    
    if GAME["game_is_over"]:
        GAME["restart_counter"] -= 1.0/GAME["clock_tick"]
        if GAME["restart_counter"] < 0:
            restart_game(snakes_data)
            GAME["game_is_over"] = False    
            GAME["restart_counter"] = CONST_RESTART_TIME   
    else:
        if game_is_over(snakes_data):
            if GAME["is_training"]:
                restart_game(snakes_data)
                TRAINING_INFO["death_count"] += 1 
            else:
                 GAME["game_is_over"] = True

    

def draw_game_info_and_flip():
    global GAME
    if GAME["is_training"]:
        text_top = GAME["text_font"].render("Modo Treino: Mortes: "+str(TRAINING_INFO["death_count"])+" | Maior Pontuacao: "+str(TRAINING_INFO["max_pontuation"])+" | veloc. "+str(GAME["clock_tick"]), True, (230, 230, 230))
        GAME["screen"].blit(text_top, (5, 5))
        text_bot = None
        if GAME["bot_mode"] == "hungry":
            text_bot = GAME["text_font"].render("Comandos: - veloc. (1) | + veloc. (2) | Salvar Aprendizado (S)", True, (230, 230, 230))
        else:
            text_bot = GAME["text_font"].render("Comandos: - veloc. (1) | + veloc. (2)", True, (230, 230, 230))    
        GAME["screen"].blit(text_bot, (5, 565))
    else:
        aux_var = 0
        for key, point in GAME["snakes_points"].items():
            stg = str(key)+": "+str(point)
            text_game = GAME["text_font"].render(stg, True, (230, 230, 230))
            GAME["screen"].blit(text_game, (30, 5+aux_var))   
            aux_var += 20

    if GAME["game_is_over"]:
        GAME["screen"].fill((0, 0, 0))
        winner_name = ""
        best_point = 0
        for key, point in GAME["snakes_points"].items():
            stg = str(key)+": "+str(point)+" pontos"
            text_game = GAME["text_font"].render(stg, True, (230, 230, 230))
            GAME["screen"].blit(text_game, ((WINDOW_WIDTH/2)-(text_game.get_width()/2), (WINDOW_HEIGHT/2)-50+aux_var))   
            aux_var += 20
            if point > best_point:
                best_point = point
                winner_name = key

        
        text_game_over = GAME["text_font"].render("VENCEDOR: "+str(winner_name), True, (230, 230, 230))
        GAME["screen"].blit(text_game_over,((WINDOW_WIDTH/2)-(text_game_over.get_width()/2), (WINDOW_HEIGHT/2)-70 ))

        text_game_over = GAME["text_font"].render("reiniciando o jogo em ... "+str(int(GAME["restart_counter"])), True, (230, 230, 230))
        GAME["screen"].blit(text_game_over,((WINDOW_WIDTH/2)-(text_game_over.get_width()/2), (WINDOW_HEIGHT/2)-20+aux_var ))

    pygame.display.flip()

def capture_key_events():
    global GAME
    GAME["player_current_key"] = 0

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_1 and GAME["is_training"]:
                GAME["clock_tick"] -= 10
                if GAME["clock_tick"] < 10:
                    GAME["clock_tick"] = 10
            if event.key == pygame.K_2 and GAME["is_training"]:
                GAME["clock_tick"] += 10
                if GAME["clock_tick"] > 60:
                    GAME["clock_tick"] = 60
            if event.key == pygame.K_s and GAME["is_training"]:
                save_learning(GAME["bot_mode"])
            if event.key == pygame.K_LEFT:
                GAME["player_current_key"] = -1
            if event.key == pygame.K_RIGHT:
                GAME["player_current_key"] = 1
