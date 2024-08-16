import os
import random
import pygame
from config import HEIGHT, WIDTH

class SoldierAnimation:
    def __init__(self, idle_folder, run_folder):
        self.state = 'idle'
        self.idle_images = self.load_images(idle_folder)
        self.run_images = self.load_images(run_folder)
        self.current_images = self.idle_images
        self.index = 0
        self.image = self.current_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.moving = False
        # Definindo uma posição-alvo aleatória para cada soldado
        self.target_pos = (random.randint(WIDTH // 4, 3 * WIDTH // 4), HEIGHT // 2)

    def load_images(self, folder):
        images = []
        for filename in sorted(os.listdir(folder)):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            img = pygame.transform.scale(img, (25, 25))
            images.append(img)
        return images

    def set_state(self, state):
        if state != self.state:
            self.state = state
            if state == 'idle':
                self.current_images = self.idle_images
            elif state == 'run':
                self.current_images = self.run_images
            elif state == "agachado":
                self.ima= pygame.image.load('img/soldier/shoot/sprite_3.png').convert_alpha()
                self.image = pygame.transform.scale(self.ima, (25, 25))
            self.index = 0

    def update(self):
        self.index += 0.3

        if int(self.index) >= len(self.current_images):
            self.index = 0
        self.image = self.current_images[int(self.index)]

        if self.moving:
            self.move()
        else:
            self.set_state('agachado')

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def set_position(self, pos):
        self.rect.topleft = pos

    def move_to(self):
        self.moving = True
        self.set_state('run')

    def move(self):
        if self.target_pos:
            target_x, target_y = self.target_pos
            current_x, current_y = self.rect.topleft
            speed = 1  # Velocidade de movimento

            if abs(current_x - target_x) > speed:
                if current_x < target_x:
                    current_x += speed
                else:
                    current_x -= speed
            else:
                current_x = target_x

            if abs(current_y - target_y) > speed:
                if current_y < target_y:
                    current_y += speed
                else:
                    current_y -= speed
            else:
                current_y = target_y

            self.rect.topleft = (current_x, current_y)

            if (current_x, current_y) == self.target_pos:
                self.moving = False
                self.set_state('agachado')