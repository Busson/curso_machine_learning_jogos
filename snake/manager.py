import pygame
import tensorflow as tf
from snake import *
from neural_net import *

GAME = {}
TRAINING_INFO = {}

def initialize_game(IS_TRANING, GAME_MODE):
    global GAME
    pygame.init()
    create_neural_net(GAME_MODE)
    init_tensorflow(IS_TRANING)
    pygame.display.set_caption('DeepLearning Snake')
    GAME["screen"] = pygame.display.set_mode((600, 600))
    GAME["clock"] = pygame.time.Clock() 
    GAME["is_training"] = IS_TRANING
    if IS_TRANING: 
        GAME["clock_tick"] = 60
        TRAINING_INFO["max_pontuation"] = 0
        TRAINING_INFO["death_count"] = 0
    else: 
        GAME["clock_tick"] = 10
    GAME["end"] = False
    GAME["text_font"] = pygame.font.SysFont("comicsansms", 28)
    return True

def await_ticks_and_fill_screen():
    global GAME
    GAME["clock"].tick(GAME["clock_tick"])
    GAME["screen"].fill((0, 0, 0))
  

def update_best_pontuation(snake):
    global GAME
    if GAME["is_training"]:
        if snake["pontos"] > TRAINING_INFO["max_pontuation"]:
            TRAINING_INFO["max_pontuation"] = snake["pontos"]

def check_game_is_over(snakes_data):
    global GAME
    if game_is_over(snakes_data):
        restart_game(snakes_data)
        if GAME["is_training"]:
            TRAINING_INFO["death_count"] += 1 

def draw_game_info_and_flip():
    global GAME
    if GAME["is_training"]:
        text_top = GAME["text_font"].render("Modo Treino: Mortes: "+str(TRAINING_INFO["death_count"])+" | Maior Pontuacao: "+str(TRAINING_INFO["max_pontuation"])+" | veloc. "+str(GAME["clock_tick"]), True, (230, 230, 230))
        GAME["screen"].blit(text_top, (5, 5))
        text_bot = GAME["text_font"].render("Comandos: - veloc. (1) | + veloc. (2) | Salvar Aprendizado (S)", True, (230, 230, 230))
        GAME["screen"].blit(text_bot, (5, 565))
    pygame.display.flip()


def capture_key_events():
    player_decision = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_1 and GAME["is_training"]:
                GAME["clock_tick"] -= 10
                if GAME["clock_tick"] < 5:
                    GAME["clock_tick"] = 5
            if event.key == pygame.K_2 and GAME["is_training"]:
                GAME["clock_tick"] += 10
                if GAME["clock_tick"] > 60:
                    GAME["clock_tick"] = 60
            if event.key == pygame.K_s and GAME["is_training"]:
                save_learning()
            if event.key == pygame.K_LEFT:
                player_decision = -1
            if event.key == pygame.K_RIGHT:
                player_decision = 1

    return player_decision