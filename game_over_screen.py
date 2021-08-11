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
    font_3 = pygame.font.SysFont('LICENSE.txt', 30)
    text1 = font.render('GAME', True, (255, 0, 0))
    text2 = font.render('OVER!', True, (255, 0, 0))
    text3 = font_2.render('score: {}'.format(score), True, (255, 0, 0))
    text4 = font_3.render('Pressione qualquer tecla para voltar a tela', True, (255, 255, 255))
    text5 = font_3.render('de inicío e jogar novamente', True, (255, 255, 255))
    background.blit(text1, (50, 100))
    background.blit(text2, (50, 200))
    background.blit(text3, (50, 300))
    background.blit(text4, (10, 450))
    background.blit(text5, (10, 500))
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
                state = INIT
                running = False


        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state