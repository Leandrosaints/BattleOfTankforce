import math

import pygame
import random
import ctypes
from config import *
from hud import HUD
from get_name_input import IntroInput, draw_text_button, draw_text
from dados_json import *
from functionEss import  *
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

# Função para manter a janela sempre no topo da barra de tarefas
x_pos = 0
y_pos = screen_height - HEIGHT - 40
ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], 0, x_pos, y_pos, 0, 0, 0x0001)
clock = pygame.time.Clock()
game_over = False

background = pygame.image.load('img/bg_3.jpg').convert_alpha()
background_width = background.get_width()
num_repeats = (WIDTH // background_width) + 1

# Imagenso
tank_img = pygame.image.load("img/tank.png").convert_alpha()
tank_img = pygame.transform.scale(tank_img, (50, 20))
tank_width, tank_height = tank_img.get_size()
tank_pos = [50, HEIGHT // 2 - tank_height // 3]
tank_speed = 3
tank_health = 3
shield_active =True# False
shield_duration = 3
shield_timer = 0
tank_speed_duration = 3
aero_active = True
enemy_img = pygame.image.load("img/Enemy/enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (50, 20))

item_images = {
    'health': pygame.image.load("img/itens/healt.png").convert_alpha(),
    'shield': pygame.image.load("img/itens/escudo.png").convert_alpha(),
    'upgrade': pygame.image.load("img/itens/laser.png").convert_alpha(),
    'aero': pygame.image.load("img/itens/icon_aero.png").convert_alpha(),  # Imagem do item de helicóptero
}

heli_img = pygame.image.load("img/F16.png").convert_alpha()
img_aero = pygame.transform.scale(heli_img, (70, 18))
bomb_img = pygame.image.load("img/itens/misseis.png").convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (10, 20))

get_name = IntroInput()

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
        pygame.draw.rect(surface, (255, 0, 0),
                         (self.x + 10, self.y - health_bar_height - 2, health_bar_length, health_bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (
        self.x + 10, self.y - health_bar_height - 2, health_bar_length * health_ratio, health_bar_height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def drop_item(self):
        if random.random() < 0.5:  # Chance de 50% para dropar um item
            item_type = random.choice(list(item_images.keys()))
            items.append(Item((self.x, self.y), item_type, item_images))

def game_over_screen():
    global game_over, score
    game_over = True
    font = pygame.font.SysFont(None, 25)

    while game_over:
        screen.fill(BLACK)
        draw_text('Game Over!', font, RED, screen, WIDTH // 2 - 50, HEIGHT // 2)
        draw_text('Press R to Restart or Q to Quit', font, RED, screen, WIDTH // 2 - 120, HEIGHT // 2 - 20)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Sai do jogo completamente
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()  # Função para reiniciar o jogo
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # Sai do jogo completamente


def restart_game():
    global game_over, score, enemies, bullets, items, tank_pos, enemy_bullets, particles, shield_duration,score
    global shield_active,shield_timer, aero_active, explosions,helicopters, bombs, tank_health, tank_speed

    # Reinicializar variáveis principais
    game_over = False
    score = 0
    particles = []
    bullets = []
    enemy_bullets = []
    enemies = []
    items = []
    helicopters = []
    bombs = []
    explosions = []
    tank_health = 3
    tank_speed = 3
    score = 0
    # Redefinir a posição inicial da nave
    tank_pos = [50, HEIGHT // 2 - tank_height // 3]

    # Reiniciar estados e temporizadores
    shield_active = False
    shield_timer = 0
    shield_duration = 3
    aero_active = True

    # Outras variáveis globais que possam ser afetadas pelo estado do jogo podem ser redefinidas aqui, se necessário.


def pause():
    paused = True
    font = pygame.font.SysFont(None, 30)
    draw_text('Paused. Press P to continue.', font, RED, screen, WIDTH // 2 - 100, HEIGHT // 2 - 10)
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        clock.tick(5)

# Lista de partículas, tiros, inimigos, itens coletáveis, helicópteros e bombas
particles = []
bullets = []
enemy_bullets = []
enemies = []
items = []
helicopters = []
bombs = []
explosions = []
explosion_radius_increment = 2
max_explosion_radius = 50  # Tamanho máximo da explosão
score = 0
def draw_explosions():
    for explosion in explosions[:]:
        pygame.draw.circle(screen, RED, explosion["pos"], explosion["radius"], 2)
        explosion["radius"] += explosion_radius_increment
        if explosion["radius"] > max_explosion_radius:
            check_explosion_hits(explosion)
            explosions.remove(explosion)

# Função para verificar se a explosão atingiu algum alienígena
def check_explosion_hits(explosion):
    global score
    for enemy in enemies[:]:
        enemy_center = (enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
        distance = pygame.math.Vector2(enemy_center).distance_to(explosion["pos"])
        if distance <= explosion["radius"]:

            enemies.remove(enemy)
            score += 1
            # Atualize o placar ou qualquer outra lógica aqui
# Fonte para o texto do score e game over
font = pygame.font.SysFont(None, 15)

def main():
    enemy_timer = 0
    enemy_count = 0
    waiting_for_items = False
    item_wait_timer = 0
    global game_over,score, shield_active, tank_health,tank_speed_duration, tank_speed, explosions, shield_duration, aero_active
    hud = HUD(tank_health, shield_active,shield_duration, abilities_icons=[item_images['aero']], aero=aero_active)
    caminho_json = 'pontuacoes.json'
    nome_jogador = get_name.get_player_name(screen)
    verificar_ou_criar_json(caminho_json)
    level_text = LevelTransitionText(
        text="Next Stage",
        start_pos=(50, HEIGHT // 2 -12 ),# Começa fora da tela na parte inferior
        center_pos=(WIDTH // 2, HEIGHT // 2-20),
        font=pygame.font.SysFont(None, 50),
        color=(255, 255, 255),
        speed=5
    )


    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_LCTRL:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_p:

                    pause()
                elif event.key == pygame.K_SPACE:
                    bullets.append(Bullet((tank_pos[0] + tank_width, tank_pos[1] + tank_height // 2)))
                elif event.key == pygame.K_h and aero_active:  # Tecla para chamar o helicóptero
                    helicopters.append(Bombardeiro(helicopters, bombs, 5))
                    aero_active = False

        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] and tank_pos[0] > 0:
            tank_pos[0] -= tank_speed
            moving = True
        if keys[pygame.K_RIGHT] and tank_pos[0] < WIDTH - tank_width:
            tank_pos[0] += tank_speed
            moving = True

        if shield_duration <= 0:
            shield_active = False
        """ if shield_active:
            #shield_timer -= 1
            #shield_duration -= 1
            if shield_duration <= 0:
                shield_active = False"""

        screen.fill((0, 0, 0))
        for i in range(num_repeats):
            screen.blit(background, (i * background_width, 0))

        screen.blit(tank_img, tank_pos)


        # Gerar partículas se o tanque estiver se movendo
        if moving:
            particles.append(Particle((tank_pos[0] + tank_width // 2 - 20, tank_pos[1] + tank_height)))
        for particle in particles:
            particle.update()
            particle.draw(screen)

        for bullet in bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.x > WIDTH:
                bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        particles.extend([Particle((bullet.x, bullet.y)) for _ in range(5)])
                        bullets.remove(bullet)
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemy.drop_item()  # Adiciona um item quando o inimigo é destruído
                            score += 1
                            enemies.remove(enemy)
                        break

        for bullet in enemy_bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.x < 0:
                enemy_bullets.remove(bullet)
            elif bullet.get_rect().colliderect(pygame.Rect(tank_pos[0], tank_pos[1], tank_width, tank_height)):

                enemy_bullets.remove(bullet)

                shield_duration -= 1
                    #print(shield_duration)


                if not shield_active:
                    tank_health -= 0.5
                if tank_health <= 0:
                    game_over = True

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
                    items.append(Item((item_x, 0), item_type, item_images))
                waiting_for_items = False
                enemy_count = 0  # Permitir novos inimigos após a coleta de itens

        for item in items[:]:
            # item.update()
            item.draw(screen)
            if item.y > HEIGHT:
                items.remove(item)
            elif item.get_rect().colliderect(pygame.Rect(tank_pos[0], tank_pos[1], tank_width, tank_height)):
                items.remove(item)
                if item.type == 'health':
                    tank_health += 0.5
                    if tank_health >=3:
                        tank_health =3
                elif item.type == 'shield':
                    shield_active = True
                    shield_duration = 3
                elif item.type == 'upgrade':
                    tank_speed += 1
                    if tank_speed >=5:
                        tank_speed_duration -= 0.5
                    if tank_speed_duration <= 0:
                        tank_speed = 3

                elif item.type == 'aero':
                    aero_active = True
        hud.update(tank_health, shield_duration, aero_active)
        hud.draw(screen)
        for enemy in enemies:
            enemy.update()
            enemy.draw(screen)
        for heli in helicopters[:]:
            heli.update()
            heli.draw(screen, img_aero)

        for bomb in bombs[:]:
            bomb.update(bombs, enemies, explosions)
            bomb.draw(screen, bomb_img)
        if score >= 10:
            # No loop principal do jogo
            if not level_text.is_done():
                level_text.update()
                level_text.draw(screen)

        draw_text(f'Score: {score}', font, RED, screen, 20, 30)
        atualizar_pontuacao(caminho_json, nome_jogador,score)
        draw_explosions()
        # Mostrar mensagem de Game Over se o jogo terminar
        if game_over:
            game_over_screen()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
