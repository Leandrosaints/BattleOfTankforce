import pygame
import os

class SoldierAnimation:
    def __init__(self, idle_folder, run_folder, shoot_folder, animation_speed=0.1):
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.time_elapsed = 0
        self.state = 'idle'

        # Carregue as animações de imagens separadas
        self.animations = {
            'idle': self.load_frames(idle_folder),
            'run': self.load_frames(run_folder),
            'shoot': self.load_frames(shoot_folder)
        }
        self.image = self.animations[self.state][0]

    def load_frames(self, folder):
        frames = []
        # Liste e ordene os arquivos na pasta
        for filename in sorted(os.listdir(folder), key=lambda x: int(x.split('_')[1].split('.')[0])):
            if filename.endswith('.png'):
                frame_path = os.path.join(folder, filename)
                frame = pygame.image.load(frame_path).convert_alpha()
                frames.append(frame)
        return frames

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.current_frame = 0
            self.time_elapsed = 0

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed > self.animation_speed:
            self.time_elapsed = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]

    def draw(self, surface, pos):
        surface.blit(self.image, pos)

# Inicialize o pygame


# Defina o tamanho da tela


# Pastas das animações
idle_folder = 'img/soldier/idle'
run_folder = 'img/soldier/run'
shoot_folder = 'img/soldier/shoot'

# Crie uma instância da animação do soldado
#soldier = SoldierAnimation(idle_folder, run_folder, shoot_folder)

# Variável para controlar o tempo

"""
# Loop principal do jogo
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time em segundos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                soldier.set_state('run')
            #elif event.key == pygame.K_s:
                #soldier.set_state('shoot')
            elif event.key == pygame.K_i:
                soldier.set_state('idle')

    soldier.update(dt)

    screen.fill((0, 0, 0))
    soldier.draw(screen, (400, 300))
    pygame.display.flip()

pygame.quit()"""
