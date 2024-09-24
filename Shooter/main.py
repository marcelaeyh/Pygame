#!/usr/bin/env python3

import pygame, sys, random

# Clases 
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bala.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5 # Mueve el laser de disparo

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("asteroid.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1 # Mueve los meteoritos

        # Limite de la pantalla
        if self.rect.y > 600: 
            self.rect.y = -10
            self.rect.x = random.randrange(890)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        # Mover la nave con el mouse solo en x
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = min(mouse_pos[0], 890)
        self.rect.y = 510

# Funciones 
def draw_score_info(screen, font, score, high_score):
    # Texto para el score y high score
    score_text = font.render(f"Score: {score}", True, black)
    high_score_text = font.render(f"Record: {high_score}", True, black)
    screen.blit(score_text, [10, 10])
    screen.blit(high_score_text, [10, 40])

def display_message(screen, messages, score, high_score):

    # Texto para las pantallas de Continuar y Game Over
    font = pygame.font.SysFont("serif", 30)
    screen.fill(white)

    for i, message in enumerate(messages):
        text = font.render(message, True, black)
        center_x = (size[0] // 2) - (text.get_width() // 2)
        center_y = (size[1] // 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y + i * 80])

    draw_score_info(screen, font, score, high_score)  # Mostrar el score y high score en ambas pantallas también
    pygame.display.flip()

# Cuando el juego se reinicia:
def reset_game(meteor_count):
    global all_sprite_list, meteor_list, laser_list, player, score
    
    # Inicializar listas
    all_sprite_list = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    laser_list = pygame.sprite.Group()

    # Crear los meteoritos
    for i in range(meteor_count):
        meteor = Meteor()
        meteor.rect.x = random.randrange(100, 900)
        meteor.rect.y = random.randrange(400)
        meteor_list.add(meteor)
        all_sprite_list.add(meteor)

    # Crear el jugador
    player = Player()
    all_sprite_list.add(player)

    score = 0  # Reiniciar el score al comenzar un nuevo juego

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Iniciar pygame
pygame.init()

# Pantalla y tiempos
size = (1000, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False # Inicia el while principal

# El juego comienza en este modo
game_state = "playing"

# Contadores
score = 0
high_score = 0
initial_meteor_count = 5
current_meteor_count = initial_meteor_count

# Visbilidad del mouse
pygame.mouse.set_visible(0)

# Fuente de los textos
font = pygame.font.SysFont("serif", 30)

# Condiciones iniciales
reset_game(current_meteor_count)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Para cada estado de juego hago algo
        if game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Animar el laser que se dispara 
                laser = Laser()
                laser.rect.x = player.rect.x + 55
                laser.rect.y = player.rect.y - 20
                all_sprite_list.add(laser)
                laser_list.add(laser)

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_meteor_count = initial_meteor_count # Reiniciar el juego desde cero
                    game_state = "playing"
                    reset_game(current_meteor_count)
                elif event.key == pygame.K_e:
                    done = True # Salir del juego al dar click en E

        elif game_state == "continue":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Añadir más meteoritos al reiniciar el juego y continuar jugando
                current_meteor_count += 4
                game_state = "playing"
                reset_game(current_meteor_count)

    # Todo lo que pasa cuando estas en la pantalla de jugar
    if game_state == "playing":
        all_sprite_list.update() # Actualizar movimientos, etc de las clases 

        # Detecta colisiones con los meteoritos y pasa a game over 
        meteor_hit_list = pygame.sprite.spritecollide(player, meteor_list, False)
        if meteor_hit_list:
            game_state = "game_over"

        # Detecta cuando ya no hay meteoritos y continua
        if len(meteor_list) == 0:
            game_state = "continue"

        # Detecta cuando un lase colisiona con un meteorito
        for laser in laser_list:
            meteor_laser_list = pygame.sprite.spritecollide(laser, meteor_list, True)
            for meteor in meteor_laser_list:
                # Elimina el laser 
                all_sprite_list.remove(laser)
                laser_list.remove(laser)
                score += 1 # Sube el score
                high_score = max(high_score, score) # sube el high score si es el caso

            # Si el laser llega al inicio de la pantalla tambien lo elimina
            if laser.rect.y < -10:
                all_sprite_list.remove(laser)
                laser_list.remove(laser)

        # Dibujar todo en la pantalla
        screen.fill(white)
        all_sprite_list.draw(screen)
        draw_score_info(screen, font, score, high_score)

    # Lo que pasa en el modo game over 
    elif game_state == "game_over":
        display_message(screen, [
            "Game Over", 
            "Presione ESPACIO para reiniciar o E para salir"
        ], score, high_score)

    # Lo que pasa en el modo continue 
    elif game_state == "continue":
        display_message(screen, [
            "Presione ESPACIO para continuar",
            "Se añadirán más meteoritos"
        ], score, high_score)

    pygame.display.flip()
    clock.tick(80)

pygame.quit()



