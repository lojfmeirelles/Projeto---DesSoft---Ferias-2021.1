import pygame
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, OVER
from assets import load_assets, DESTROY_SOUND, BOOM_SOUND, BACKGROUND, SCORE_FONT
from sprites import Second_Meteor, Ship, Meteor, Bullet, Explosion


def game_screen(window, highscore_salvo):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo de meteoros
    all_sprites = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_yellow_meteors = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_meteors'] = all_meteors
    groups['all_bullets'] = all_bullets
    groups['all_yellow_meteors'] = all_yellow_meteors

    # Criando o jogador
    player = Ship(groups, assets)
    all_sprites.add(player)

    # Criando os meteoros que tiram uma vida
    for i in range(8):
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    # Criando os meteoros que tiram 2 vidas de uma vez
    for t in range(2):
        yellow_meteor = Second_Meteor(assets)
        all_sprites.add(yellow_meteor)
        all_yellow_meteors.add(yellow_meteor)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}
    high_score = highscore_salvo['high_score']
    score = 0
    lives = 3

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_UP:
                        player.speedy -= 8
                    if event.key == pygame.K_DOWN:
                        player.speedy += 8
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_SPACE:
                        player.shoot()
    

                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 8
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 8
                        if event.key == pygame.K_UP:
                            player.speedy += 8
                        if event.key == pygame.K_DOWN:
                            player.speedy -= 8

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos meteoros
        all_sprites.update()

        if state == PLAYING:
            # Verifica se houve colisão entre tiro e meteoro tipo 1
            hits = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True, pygame.sprite.collide_mask)
            for meteor in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                m = Meteor(assets)
                all_sprites.add(m)
                all_meteors.add(m)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(meteor.rect.center, assets)
                all_sprites.add(explosao)

                # Ganhou pontos!
                score += 100
                if score % 1000 == 0:
                    lives += 1
                elif score % 3000 == 0:
                    new_meteor = Meteor(assets)
                    all_sprites.add(new_meteor)
                    all_meteors.add(new_meteor)

            # Verifica se houve colisão entre tiro e meteoro tipo 1
            hits_2 = pygame.sprite.groupcollide(all_yellow_meteors, all_bullets, True, True, pygame.sprite.collide_mask)
            for yellow_meteor in hits_2: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                k = Second_Meteor(assets)
                all_sprites.add(k)
                all_meteors.add(k)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(yellow_meteor.rect.center, assets)
                all_sprites.add(explosao) 

                # Ganhou pontos!
                score += 200
                if score % 1000 == 0:
                    lives += 1
                elif score % 6000 == 0:
                    new_meteor = Second_Meteor(assets)
                    all_sprites.add(new_meteor)
                    all_yellow_meteors.add(new_meteor)

            # Verifica se houve colisão entre player 1 e meteoro tipo 1
            hits = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                player.kill()
                lives -= 1
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
                n = Meteor(assets)
                all_sprites.add(n)
                all_meteors.add(n)
            
            # Verifica se houve colisão entre player 1 e meteoro tipo 2
            hits_2 = pygame.sprite.spritecollide(player, all_yellow_meteors, True, pygame.sprite.collide_mask)
            if len(hits_2) > 0:
                # Toca o som da colisão
                assets[BOOM_SOUND].play()
                player.kill()
                lives -= 2
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
                y = Second_Meteor(assets)
                all_sprites.add(y)
                all_yellow_meteors.add(y)
            

        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Ship(groups, assets)
                    all_sprites.add(player)

        #Gravando high score
        if score > highscore_salvo['high_score']:
            highscore_salvo['high_score'] = score

        # ----- Gera saídas
        window.fill(BLACK)  # Preenche com a cor branca
        window.blit(assets[BACKGROUND], (0, 0))
        # Desenhando meteoros
        all_sprites.draw(window)

        # Desenhando o score
        text_surface = assets[SCORE_FONT].render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_surface, text_rect)

        # Desenhando as vidas
        text_surface = assets[SCORE_FONT].render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  # Mostra o novo frame para o jogador
    
    pygame.mixer.quit()

    state = OVER

    return state