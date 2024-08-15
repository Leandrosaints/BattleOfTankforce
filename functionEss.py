import math
import random

import pygame
from config import *

class LevelTransitionText:
    def __init__(self, text, start_pos, center_pos, font, color, speed):
        self.text = text
        self.start_pos = start_pos
        self.current_pos = list(start_pos)
        self.center_pos = center_pos
        self.font = font
        self.color = color
        self.speed = speed
        self.alpha = 255  # Opacidade inicial do texto
        self.fade_out = False

    def update(self):
        if not self.fade_out:
            # Move o texto em direção ao centro
            direction_x = self.center_pos[0] - self.current_pos[0]
            direction_y = self.center_pos[1] - self.current_pos[1]
            distance = math.hypot(direction_x, direction_y)

            if distance > self.speed:
                self.current_pos[0] += self.speed * direction_x / distance
                self.current_pos[1] += self.speed * direction_y / distance
            else:
                self.current_pos = list(self.center_pos)
                self.fade_out = True
        else:
            # Desaparece o texto
            if self.alpha > 0:
                self.alpha -= 5  # Diminui a opacidade
            else:
                self.alpha = 0

    def draw(self, surface):
        text_surface = self.font.render(self.text, True,RED)
        text_surface.set_alpha(self.alpha)  # Ajusta a opacidade do texto
        surface.blit(text_surface, self.current_pos)

    def is_done(self):
        # Verifica se a transição foi concluída
        return self.alpha == 0
class Item:
    def __init__(self, pos, item_type, list_img):
        self.x, self.y = pos
        self.type = item_type
        self.img = list_img[item_type]
        self.img_scale = pygame.transform.scale(self.img, (15, 15))
        self.width, self.height = (10, 10)
        self.speed = 2

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.img_scale, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bombardeiro:
    def __init__(self,aeronave, bombs, speed):
        self.x = -80
        self.y =  HEIGHT // 2 - 30
        self.speed = speed
        self.dropping_bomb = False
        self.bomb_timer = 30
        self.aeronave = aeronave
        self.bomb = bombs

    def update(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.aeronave.remove(self)

        if not self.dropping_bomb and random.random() < 0.05:
            self.bomb.append(Bomb((self.x + 40, self.y + 20)))
            self.dropping_bomb = True

        if self.dropping_bomb:
            self.bomb_timer -= 1
            if self.bomb_timer <= 0:
                self.dropping_bomb = False
                self.bomb_timer = 30

    def draw(self, surface, img_aero):
        surface.blit(img_aero, (self.x, self.y))


# Classe de Bomba

class Bomb:
    def __init__(self, pos):
        self.x, self.y = pos
        self.x_speed = 2  # Velocidade na horizontal
        self.y_speed = 1  # Velocidade na vertical
        #self.bomb = bomb
        #self.enemies = enemies_list
        #self.explosions = explo_list
    def update(self, bomb, enemies, explosions):
        # Atualiza a posição da bomba
        self.x += self.x_speed
        self.y += self.y_speed


        # Remove a bomba se ela sair da tela
        if self.y > HEIGHT or self.x > WIDTH or self.x < 0:
            bomb.remove(self)
        else:
            # Verifica colisão com inimigos
            for enemy in enemies[:]:
                if pygame.Rect(self.x, self.y, 10, 20).colliderect(enemy.get_rect()):
                    bomb.remove(self)
                    # Adiciona uma nova explosão baseada na posição da bomba
                    explosions.append({"pos": (self.x + 5, self.y + 10), "radius": 0})
                    break

    def draw(self, surface, bomb_img):
        # Desenha a bomba na tela
        surface.blit(bomb_img, (self.x, self.y))
