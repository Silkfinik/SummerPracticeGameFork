import pygame

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Размеры окна
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h - 200
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Sound Integration")

# создание черной полосы внизу экрана
bar_height = 15
bar_color = (0, 0, 0)
bar_position = (0, screen_height - bar_height)

sprite_dir = 'sprites'
sound_dir = 'sounds'
font_path = 'default_font.ttf'

# Счетчик очков
score = 0

# Установка шрифта по умолчанию
font_size = 36
font = pygame.font.Font(font_path, font_size)

debug_mode = True  # Включаем режим отладки для отображения хитбоксов
