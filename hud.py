import pygame
from config import BLUE, WHITE, RED


class HUD:
    def __init__(self,tank_health, shield_active,shield_duration, abilities_icons, aero):
        self.shield_duration = shield_duration
        self.tank_health = tank_health
        self.shield_active = shield_active
        self.abilities_icons = abilities_icons
        self.aero = aero
        self.width =30
        self.height =5
        self.margin = 5
        self.icon_size =10
        self.max_health = 3
        #bar_width = 30
        #bar_height = 5
        self.icon = pygame.image.load("img/itens/escudo.png").convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (15, 15))
        self.font = pygame.font.SysFont(None, 24)

    def draw_health_bar(self, screen):

        health_ratio = self.tank_health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.margin, self.margin, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.margin, self.margin, self.width * health_ratio, self.height))
        #health_text = self.font.render(f'HP: {self.tank_health}/{max_health}', True, (255, 255, 255))
        #self.screen.blit(health_text, (self.margin, self.margin + bar_height + 5))

    def draw_shield_status(self, screen):
        #shield_text = "Shield: ON" if self.shield_active else "Shield: OFF"

        health_ratio =  self.shield_duration / 3
        pygame.draw.rect(screen, RED, (self.margin, 15, self.width, self.height))
        pygame.draw.rect(screen, BLUE, (self.margin, 15, self.width * health_ratio, self.height))

    def draw_abilities(self, screen):
        for i, icon in enumerate(self.abilities_icons):
            if self.aero:
                screen.blit(pygame.transform.scale(icon, (10, 10)), (40, 2))

    def update(self, tank_health, shield_duration, aero_active):
        self.tank_health = tank_health
        self.shield_duration= shield_duration
        self.aero = aero_active

    def draw(self, screen):
        self.draw_health_bar(screen)
        self.draw_shield_status(screen)
        self.draw_abilities(screen)