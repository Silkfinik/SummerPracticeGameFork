import sys
import pygame
from sprite_placer import run_sprite_placer
from config import font, screen_width, screen_height, difficulty_levels

def draw_start_screen(screen, button_rect, hover):
    """
    Отрисовка стартового экрана с кнопкой начала игры.

    :param screen: Экран Pygame.
    :param button_rect: Прямоугольник кнопки начала игры.
    :param hover: Флаг наведения на кнопку.
    """
    screen.fill((0, 0, 0))  # Заполняем экран черным цветом
    text = font.render("Start Game", True, (255, 255, 255))

    if hover:
        text = pygame.transform.scale(text, (int(text.get_width() * 1.1), int(text.get_height() * 1.1)))

    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    # Добавляем сообщение о сочетании клавиш
    info_text = font.render("Press Ctrl+B to launch the level editor", True, (255, 255, 255))
    info_rect = info_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    screen.blit(info_text, info_rect)

def draw_difficulty_screen(screen, buttons, hover_index):
    """
    Отрисовка экрана выбора уровня сложности.

    :param screen: Экран Pygame.
    :param buttons: Словарь с кнопками уровней сложности и их координатами.
    :param hover_index: Индекс кнопки, на которую наведена мышь.
    """
    screen.fill((0, 0, 0))  # Заполняем экран черным цветом
    title_text = font.render("Select Difficulty", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

    for i, (difficulty, rect) in enumerate(buttons.items()):
        text = font.render(difficulty.capitalize(), True, (255, 255, 255))
        if i == hover_index:
            text = pygame.transform.scale(text, (int(text.get_width() * 1.1), int(text.get_height() * 1.1)))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_death_screen(screen):
    """
    Отрисовка экрана смерти.

    :param screen: Экран Pygame.
    """
    screen.fill((0, 0, 0))  # Заполняем экран черным цветом
    death_text = font.render("You died", True, (255, 0, 0))
    restart_text = font.render("Press ENTER to restart", True, (255, 255, 255))
    quit_text = font.render("Press Q to quit", True, (255, 255, 255))

    death_text_rect = death_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    restart_text_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2))
    quit_text_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    screen.blit(death_text, death_text_rect)
    screen.blit(restart_text, restart_text_rect)
    screen.blit(quit_text, quit_text_rect)

def start_screen():
    """
    Запуск экрана начала игры и выбор уровня сложности.

    :return: Выбранный уровень сложности.
    """
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Start Screen")

    button_width, button_height = 200, 50
    button_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 - button_height // 2,
                              button_width, button_height)

    running = True
    selecting_difficulty = False
    hover_index = 0
    difficulty_buttons = {}
    for i, difficulty in enumerate(difficulty_levels.keys()):
        rect = pygame.Rect(screen_width // 2 - button_width // 2,
                           screen_height // 2 - button_height // 2 - 70 + (i + 1) * (button_height + 10),
                           button_width, button_height)
        difficulty_buttons[difficulty] = rect

    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos) if not selecting_difficulty else False

        if selecting_difficulty:
            hover_index = -1  # Сброс наведения
            for i, rect in enumerate(difficulty_buttons.values()):
                if rect.collidepoint(mouse_pos):
                    hover_index = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hover and not selecting_difficulty:
                    selecting_difficulty = True
                elif selecting_difficulty:
                    for difficulty, rect in difficulty_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            return difficulty
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selecting_difficulty:
                    hover_index = (hover_index - 1) % len(difficulty_buttons)
                elif event.key == pygame.K_DOWN and selecting_difficulty:
                    hover_index = (hover_index + 1) % len(difficulty_buttons)
                elif event.key == pygame.K_RETURN and selecting_difficulty:
                    selected_difficulty = list(difficulty_buttons.keys())[hover_index]
                    return selected_difficulty
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if not selecting_difficulty:
                        selecting_difficulty = True
                elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    run_sprite_placer()
                elif selecting_difficulty:
                    if event.key == pygame.K_e:
                        return "easy"
                    elif event.key == pygame.K_m:
                        return "medium"
                    elif event.key == pygame.K_h:
                        return "hard"

        if not selecting_difficulty:
            draw_start_screen(screen, button_rect, hover)
        else:
            draw_difficulty_screen(screen, difficulty_buttons, hover_index)
        pygame.display.flip()

    return None  # Возвращаем None, если окно закрыто

if __name__ == "__main__":
    start_screen()
