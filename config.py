# config.py
import pygame
import json

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Загрузка размеров карты из файла JSON

map_width = 1500
map_height = 750

# Получение размеров экрана
screen_height = map_height
screen_width = map_width

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Sound Integration")
scale_factor = 1

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

debug_mode = False  # Включаем режим отладки для отображения хитбоксов

# Добавляем переменные для отслеживания состояния звука и музыки
music_on = True
sound_on = True

# Настройки клавиш управления
key_bindings = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_SPACE,
    "sprint": pygame.K_LSHIFT
}

# Добавляем переменные для уровней сложности
difficulty_levels = {
    "easy": 3,
    "medium": 2,
    "hard": 1
}

# Переменные для здоровья и временного счетчика монет
current_difficulty = None
current_health = None
temp_coin = 0

# Путь к спрайту сердечка
heart_sprite_path = 'unused_sprites/items/heart.png'