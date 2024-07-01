import pygame
from config import font, screen_width, screen_height


def draw_start_screen(screen, button_rect, hover):
    screen.fill((0, 0, 0))  # Заполняем экран черным цветом
    text = font.render("Start Game", True, (255, 255, 255))

    if hover:
        text = pygame.transform.scale(text, (int(text.get_width() * 1.1), int(text.get_height() * 1.1)))

    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


def start_screen():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Start Screen")

    button_width, button_height = 200, 50
    button_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 - button_height // 2,
                              button_width, button_height)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hover:
                    running = False  # Выходим из цикла, чтобы начать игру

        draw_start_screen(screen, button_rect, hover)
        pygame.display.flip()

    return True  # Возвращаем True, чтобы показать, что игра должна начаться


if __name__ == "__main__":
    start_screen()
