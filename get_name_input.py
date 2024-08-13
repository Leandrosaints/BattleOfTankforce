import pygame
from config import BLACK, WIDTH, HEIGHT, WHITE, BLUE
from dados_json import load_ranking_from_json
def display_ranking(screen):
    font = pygame.font.SysFont(None, 30)
    start_x = -200  # Ponto inicial fora da tela (primeiro nome)
    y_position =HEIGHT // 2 - 18
    ranking_list = load_ranking_from_json()
    done = False

    while not done:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_r):
                    done = True
        draw_text('press R for return', font, BLUE, screen,WIDTH//2, HEIGHT // 2 - 14)
        # Desenhar o ranking lado a lado
        current_x = start_x
        for i, (name, score) in enumerate(ranking_list):
            text = f"{i + 1}. {name}: {score}"
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (current_x, y_position))
            current_x += text_surface.get_width() + 50  # Move para a próxima posição com espaçamento

        start_x += 3  # Velocidade do deslizamento
        if current_x >WIDTH:
            done = True  # Sai do loop quando o texto passar completamente pela tela

        pygame.display.flip()
        pygame.time.delay(50)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_text_button(screen, text, x, y, width, height, font, action=None):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, button_rect, 2)  # Borda preta
    draw_text(text, font, BLUE, screen, x,  height // 2 - 12)  # Desenha o texto sobre o botão
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if button_rect.collidepoint(mouse):
        if click[0] == 1 and action is not None:
            action()
    return button_rect.collidepoint(mouse)
def get_player_name(screen):
    font = pygame.font.SysFont(None, 30)
    input_box = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 - 18, 140, 30)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    active = False
    done = False

    # Texto "Veja os Ranks ou digite seu nome para iniciar"

    # Posição do texto
    #instruction_text_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while not done:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive



            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Renderizar o texto da caixa de entrada
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        if draw_text_button(screen, 'Rank', 270, HEIGHT // 2 - 14, 200, 50, font,  action=lambda:display_ranking(screen)):

            ...
        draw_text('ou digite seu nome para iniciar >>>', font, WHITE, screen, 330,
                  HEIGHT // 2 - 14)  # font.render('Veja os Ranks ou digite seu nome para iniciar', True, pygame.Color('white'))

        # Desenhar o texto de instrução
        #screen.blit(instruction_text)

        pygame.display.flip()

    return text