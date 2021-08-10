import pygame
import random
from os import path
from config import IMG_DIR, BLACK, FPS, GAME, QUIT, INIT



def over_screen(screen, highscore_salvo):

    score = highscore_salvo['high_score']
    
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'starfield.png')).convert()
    background_rect = background.get_rect()
    font = pygame.font.SysFont('LICENSE.txt', 160)
    font_2 = pygame.font.SysFont('LICENSE.txt', 80)
    text1 = font.render('GAME', True, (255, 0, 0))
    text2 = font.render('OVER!', True, (255, 0, 0))
    text3 = font_2.render('score: {}'.format(score), True, (255, 0, 0))
    background.blit(text1, (50, 200))
    background.blit(text2, (50, 300))
    background.blit(text3, (50, 400))
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
            elif event.type == pygame.K_LCTRL:
                state = INIT
                running = False


        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state