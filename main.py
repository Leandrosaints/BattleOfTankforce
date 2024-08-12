import pygame
import random
from config import *
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
# Função para manter a janela sempre no topo da barra de tarefas
x_pos = 0
y_pos = screen_height - HEIGHT - 40
ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], 0, x_pos, y_pos, 0, 0, 0x0001)
clock = pygame.time.Clock()
game_over = False
import pygame
import random
from config import *
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
# Função para manter a janela sempre no topo da barra de tarefas
x_pos = 0
y_pos = screen_height - HEIGHT - 40
ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], 0, x_pos, y_pos, 0, 0, 0x0001)
clock = pygame.time.Clock()

background = pygame.image.load('img/bg.jpg').convert_alpha()
background_width = background.get_width()
num_repeats = (WIDTH // background_width) + 1

# Imagens
tank_img = pygame.image.load("img/tank.png").convert_alpha()
tank_img = pygame.transform.scale(tank_img, (50, 20))
tank_width, tank_height = tank_img.get_size()
tank_pos = [50, HEIGHT // 2 - tank_height // 2]
tank_speed = 3
tank_health = 3
shield_active = False
shield_duration = 300
shield_timer = 0

enemy_img = pygame.image.load("img/Enemy/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 20))

item_images = {
    'health': pygame.image.load("img/itens/healt.png").convert_alpha(),
    'shield': pygame.image.load("img/itens/escudo.png").convert_alpha(),
    'upgrade': pygame.image.load("img/itens/misseis.png").convert_alpha(),
}

# Classe de Partícula
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.size = random.randint(1, 4)
        self.color = (169, 169, 169)
        self.lifetime = random.randint(20, 40)
        self.x_vel = random.uniform(-1, 1)
        self.y_vel = random.uniform(-1, 1)

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.lifetime -= 1
        self.size -= 0.1

    def draw(self, surface):
        if self.size > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

# Classe de Tiro
class Bullet:
    def __init__(self, pos, speed=5):
        self.x, self.y = pos
        self.speed = speed
        self.size = 5
        self.color = (255, 0, 0)

    def update(self):
        self.x += self.speed
        particles.append(Particle((self.x, self.y)))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

# Classe de Inimigo
class Enemy:
    def __init__(self, pos, speed=1, health=3):
        self.x, self.y = pos
        self.speed = speed
        self.health = health
        self.img = enemy_img
        self.width, self.height = self.img.get_size()
        self.shoot_timer = random.randint(30, 120)
        self.moving_to_point = True
        self.move_point = (random.randint(WIDTH // 2, WIDTH - 50), HEIGHT // 2)

        #self.move_point = (random.randint(WIDTH // 2, WIDTH - 50), random.randint(50, HEIGHT - 50))

    def update(self):
        if self.moving_to_point:
            if abs(self.x - self.move_point[0]) > self.speed:
                self.x += self.speed if self.x < self.move_point[0] else -self.speed
            if abs(self.y - self.move_point[1]) > self.speed:
                self.y += self.speed if self.y < self.move_point[1] else -self.speed
            if abs(self.x - self.move_point[0]) <= self.speed and abs(self.y - self.move_point[1]) <= self.speed:
                self.moving_to_point = False
        else:
            if self.shoot_timer <= 0:
                enemy_bullets.append(Bullet((self.x, self.y + self.height // 2 - 5), -2))
                self.shoot_timer = random.randint(30, 120)
            else:
                self.shoot_timer -= 1


    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        health_bar_length = 30
        health_bar_height = 3
        health_ratio = self.health / 3
        pygame.draw.rect(surface, (255, 0, 0), (self.x + 10, self.y - health_bar_height - 2, health_bar_length, health_bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.x + 10, self.y - health_bar_height - 2, health_bar_length * health_ratio, health_bar_height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Classe de Item Coletável
class Item:
    def __init__(self, pos, item_type):
        self.x, self.y = pos
        self.type = item_type
        self.img = item_images[item_type]
        self.img_scale = pygame.transform.scale(self.img, (15,15))
        self.width, self.height = (10, 10)
        self.speed = 2

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.img_scale, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Lista de partículas, tiros, inimigos e itens coletáveis
particles = []
bullets = []
enemy_bullets = []
enemies = []
items = []

def main():
    global game_over, shield_active, shield_timer, tank_health, tank_speed

    enemy_timer = 0
    enemy_count = 0
    waiting_for_items = False
    item_wait_timer = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet((tank_pos[0] + tank_width, tank_pos[1] + tank_height // 2 - 5)))

        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] and tank_pos[0] > 0:
            tank_pos[0] -= tank_speed
            moving = True
        if keys[pygame.K_RIGHT] and tank_pos[0] < WIDTH - tank_width:
            tank_pos[0] += tank_speed
            moving = True
        if keys[pygame.K_UP] and tank_pos[1] > 0:
            tank_pos[1] -= tank_speed
            moving = True
        if keys[pygame.K_DOWN] and tank_pos[1] < HEIGHT - tank_height:
            tank_pos[1] += tank_speed
            moving = True

        if moving:
            particles.append(Particle((tank_pos[0] + tank_width // 2 - 20, tank_pos[1] + tank_height)))

        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)

        for bullet in bullets[:]:
            bullet.update()
            if bullet.x > WIDTH:
                bullets.remove(bullet)

        for bullet in enemy_bullets[:]:
            bullet.update()
            if bullet.x < 0:
                enemy_bullets.remove(bullet)
            if bullet.get_rect().colliderect(pygame.Rect(tank_pos[0], tank_pos[1], tank_width, tank_height)):
                if shield_active:
                    enemy_bullets.remove(bullet)
                else:
                    tank_health -= 1
                    enemy_bullets.remove(bullet)
                    if tank_health <= 0:
                        game_over = True

        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        if not waiting_for_items:
            if enemy_count < 5:
                if enemy_timer <= 0:
                    enemy_y = HEIGHT // 2 - 5
                    enemies.append(Enemy((WIDTH, enemy_y)))
                    enemy_count += 1
                    enemy_timer = 60
                else:
                    enemy_timer -= 1
            else:
                if not enemies:
                    waiting_for_items = True
                    item_wait_timer = 300  # Tempo de espera para coleta de itens (5 segundos)

        if waiting_for_items:
            if item_wait_timer > 0:
                item_wait_timer -= 1
            else:
                if random.random() < 0.1:
                    item_type = random.choice(list(item_images.keys()))
                    item_x = random.randint(0, WIDTH - 10)
                    items.append(Item((item_x, 0), item_type))
                waiting_for_items = False
                enemy_count = 0  # Permitir novos inimigos após a coleta de itens

        for enemy in enemies[:]:
            enemy.update()
            for bullet in bullets[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    enemy.health -= 1
                    bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        enemy_count -= 1
                        particles.extend([Particle((enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)) for _ in range(10)])

        for item in items[:]:
            item.update()
            if item.get_rect().colliderect(pygame.Rect(tank_pos[0], tank_pos[1], tank_width, tank_height)):
                if item.type == 'health':
                    tank_health = min(tank_health + 1, 3)
                elif item.type == 'shield':
                    shield_active = True
                    shield_timer = shield_duration
                elif item.type == 'upgrade':
                    tank_speed += 1
                items.remove(item)

        screen.blit(background, (0, 0))
        for i in range(num_repeats):
            screen.blit(background, (i * background_width, 0))

        screen.blit(tank_img, tank_pos)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for item in items:
            item.draw(screen)
        for particle in particles:
            particle.draw(screen)

        pygame.draw.rect(screen, (0, 255, 0), (10, 10, 30 * tank_health, 10))
        if shield_active:
            pygame.draw.rect(screen, (0, 0, 255), (10, 30, 30, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()