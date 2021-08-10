import pygame
import random
from os import path
from itertools import cycle
from config import IMG_DIR, BLACK, FPS, GAME, QUIT


PISCA = pygame.USEREVENT + 0

def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'inicio.png')).convert()
    background_rect = background.get_rect()

    second_background = pygame.image.load(path.join(IMG_DIR, 'inicio_2.png')).convert()
    second_background_rect = second_background.get_rect()

    second_background_rect.center = background_rect.center
    pisca_surfaces = cycle([background, second_background])
    pisca_superficie = next(pisca_surfaces)
    pygame.time.set_timer(PISCA, 1000)

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False
            
            if event.type == PISCA:
                pisca_superficie = next(pisca_surfaces)

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(pisca_superficie, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state