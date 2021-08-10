# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import json
from config import WIDTH, HEIGHT, INIT, GAME, QUIT, OVER
from init_screen import init_screen
from game_screen import game_screen
from game_over_screen import over_screen

# Tenta ler um arquivo de highscore, se não houver, cria um novo
try:
    with open('highscores.json', 'r') as highscores_json:
        k = highscores_json.read()
        highscore_salvo = json.loads(k)

except:
    with open('highscores.json', 'w') as highscores_json:
        highscore_salvo = {"high_score": 0}
        dict_json = json.dumps(highscore_salvo)
        highscores_json.write(dict_json)

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Meteors Evolved')

state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state = game_screen(window, highscore_salvo)
    elif state == OVER:
        state = over_screen(window, highscore_salvo)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados