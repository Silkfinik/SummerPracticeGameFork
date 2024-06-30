import pygame
import json

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Загрузка размеров карты из файла JSON
with open('map.json', 'r') as f:
    map_data = json.load(f)
map_width = map_data["canvas_size"]["width"]
map_height = map_data["canvas_size"]["height"]

# Получение размеров экрана
screen_info = pygame.display.Info()
screen_height = screen_info.current_h - 80

# Вычисление коэффициента увеличения
scale_factor = screen_height / map_height
scaled_map_width = int(map_width * scale_factor)

screen_width = scaled_map_width
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

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
