import os
import random
import pygame
from config import HEIGHT, WIDTH, GREEN, RED

class SoldierAnimation:
    def __init__(self, idle_folder, run_folder, screen, flip_img):
        self.state = 'idle'
        self.flip_images = flip_img
        self.idle_images = self.load_images(idle_folder)
        self.run_images = self.load_images(run_folder)
        self.current_images = self.idle_images
        self.index = 0
        self.image = self.current_images[self.index]
        self.rect = self.image.get_rect()
        self.health = 3  # Vida total do soldado
        self.max_health = self.health  # Vida máxima do soldado
        self.moving = False
        self.screen = screen


        self.target_pos = (random.randint(WIDTH // 4, 3 * WIDTH // 4), HEIGHT // 2 - 5)
        self.shoot_timer = random.randint(30, 120)
        self.bullets = []

    def load_images(self, folder):
        images = []
        for filename in sorted(os.listdir(folder)):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            img = pygame.transform.scale(img, (25, 25))
            if self.flip_images:
                img = pygame.transform.flip(img, True, False)
            images.append(img)
        return images

    def set_state(self, state):
        if state != self.state:
            self.state = state
            if state == 'idle':
                self.current_images = self.idle_images
            elif state == 'run':
                self.current_images = self.run_images
            elif state == 'agachado':

                self.ima = pygame.image.load('img/soldier_2/shoot/sprite_3.png').convert_alpha()
                self.image = pygame.transform.scale(self.ima, (25, 25))

                if self.flip_images:
                    self.ima1 = pygame.image.load('img/soldier_1/shoot/sprite_3.png').convert_alpha()
                    self.image = pygame.transform.scale(self.ima1, (25, 25))
                    self.image = pygame.transform.flip(self.image  , True, False)
            self.index = 0

    def update(self):
        self.index += 0.3
        if int(self.index) >= len(self.current_images):
            self.index = 0
        self.image = self.current_images[int(self.index)]

        if self.moving:
            self.move()

    def draw(self, screen, visible):
        if visible:
            for bullet in self.bullets:
                bullet.draw(screen)

            self.screen.blit(self.image, self.rect.topleft)
            # Barra de fundo (saúde total)
            self.draw_health_bar(screen)

    def draw_health_bar(self, surface):
        health_bar_length = self.rect.width
        health_bar_height = 3
        health_ratio = self.health / 3  # Assumindo que a saúde máxima é 3
        pygame.draw.rect(surface, (255, 0, 0),
                         (self.rect.x + 10, self.rect.y - health_bar_height - 2, health_bar_length, health_bar_height))
        pygame.draw.rect(surface, (0, 255, 0),
                         (self.rect.x + 10, self.rect.y - health_bar_height - 2, health_bar_length * health_ratio,
                          health_bar_height))

    def set_position(self, pos):
        self.rect.topleft = pos

    def move_to(self):
        self.moving = True
        self.set_state('run')
    def get_rect(self):
        return pygame.Rect(self.rect.right, self.rect.centery, self.rect.width, self.rect.height)
    def move(self):
        if self.target_pos:
            target_x, target_y = self.target_pos
            current_x, current_y = self.rect.topleft
            speed = 1  # Velocidade de movimento

            if self.flip_images:
                # Movendo da direita para a esquerda
                if abs(current_x - target_x) > speed:
                    if current_x > target_x:
                        current_x -= speed
                    else:
                        current_x += speed
                else:
                    current_x = target_x
            else:
                # Movendo da esquerda para a direita
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

    def shoot(self, speed, ):
        bullet = Bullet((self.rect.right, self.rect.centery), speed=speed)
        self.bullets.append(bullet)

    def update_bullets(self, enemies=None, rect=None, rect_two=None, shield=None, health=None):
        for bullet in self.bullets[:]:
            bullet.update()

            # Remove o bullet se sair dos limites da tela
            if bullet.get_rect().right > WIDTH or bullet.get_rect().left < 0:
                self.bullets.remove(bullet)

            #elif self.flip_images:
                # Verifica colisão com inimigos
            elif enemies is not None:
                for enemy in enemies[:]:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        self.bullets.remove(bullet)
                        enemy.health -= 0.1
                        if enemy.health <= 0:
                            #enemy.drop_item()
                            enemies.remove(enemy)
                        break
                            # Verifica colisão com um rect específico (por exemplo, o tanque)
                    '''elif rect is not None:
                    if bullet.get_rect().colliderect(pygame.Rect(rect)):
                        self.bullets.remove(bullet)
                        # Reduz o shield e health se forem fornecidos
                        if shield is not None:
                            shield -= 0.1

                        if health is not None:
                            if shield is None or shield <= 0:  # Só reduz a saúde se o escudo não estiver ativo
                                health -= 0.1
                            if health <= 0:
                                # Lógica de game over aqui, ou outro tratamento
                                print("Game Over")'''





        # Retorna valores atualizados de shield e health se forem usados
        return shield, health

        #return False, shield_duration, tank_health  # Continua o jogo


class Bullet:
    def __init__(self, pos, speed):
        self.x, self.y = pos
        self.speed = speed
        self.size = 2
        self.color = (255, 0, 0)

    def update(self):
        self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
