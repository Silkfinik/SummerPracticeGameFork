import pygame

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Конфигурация карты
map_width = 1500
map_height = 750

# Размеры экрана
screen_width = map_width
screen_height = map_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sound Integration")

# Масштабирование
scale_factor = 1

# Черная полоса внизу экрана
bar_height = 15
bar_color = (0, 0, 0)
bar_position = (0, screen_height - bar_height)

# Директории ресурсов
sprite_dir = 'sprites'
sound_dir = 'sounds'
font_path = 'default_font.ttf'

# Счетчик очков
score = 0

# Настройка шрифта
font_size = 36
font = pygame.font.Font(font_path, font_size)

# Режим отладки
debug_mode = False

# Настройки звука и музыки
music_on = True
sound_on = True

# Настройки клавиш управления
key_bindings = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_SPACE,
    "sprint": pygame.K_LSHIFT
}

# Уровни сложности
difficulty_levels = {
    "easy": 3,
    "medium": 2,
    "hard": 1
}

# Переменные состояния игры
current_difficulty = None
current_health = None
temp_coin = 0

# Путь к спрайту сердечка
heart_sprite_path = 'unused_sprites/items/heart.png'
