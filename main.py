import pygame
import sys
import os
import json
from player import Player
from sprites import load_images
from sounds import load_sounds, play_sound, stop_sound, play_music, stop_music
from game_platform import Platform

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

debug_mode = True  # Включаем режим отладки для отображения хитбоксов

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

# Основной цикл
clock = pygame.time.Clock()

# Путь к директории с анимациями спрайтов и звуками
sprite_dir = 'sprites'
sound_dir = 'sounds'
font_path = 'default_font.ttf'

# Загрузка изображений спрайта и звуков, с изменением размера изображений
scale_factor = 5
animations = load_images(sprite_dir, scale_factor)
sounds = load_sounds(sound_dir)

print("Loaded animations:", animations.keys())

play_music(os.path.join(sound_dir, 'background_music.mp3'))

# Создание игрока
player = Player(animations, sounds, 100, screen_height - 100 - bar_height, screen_width, screen_height)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Создание пола (застилание платформами)
platforms = pygame.sprite.Group()
platform_image_path = 'img/platform.png'
platform_width = 200
platform_height = 50

width_counter = 0
platforms.add(Platform(platform_image_path, 0, screen_height - platform_height - bar_height, screen_width, platform_height))
all_sprites.add(platforms)

# Загрузка изображения фона
def load_and_scale_background(image_path, screen_width, screen_height):
    image = pygame.image.load(image_path).convert_alpha()
    image_width, image_height = image.get_size()

    # Вычисляем новый размер для масштабирования по высоте
    scale_factor = screen_height / image_height
    new_width = int(image_width * scale_factor)
    scaled_image = pygame.transform.scale(image, (new_width, screen_height))

    return scaled_image

background_image_path = 'img/sky_blue.png'
background_image = load_and_scale_background(background_image_path, screen_width, screen_height)

# Счетчик очков
score = 0

# Установка шрифта по умолчанию
font_size = 36
font = pygame.font.Font(font_path, font_size)

def draw_hud():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# Класс для платформ с масштабированием
class ScaledPlatform(Platform):
    def __init__(self, image_path, x, y, original_size, canvas_size, screen_height):
        super().__init__(image_path, x, y)
        image = pygame.image.load(image_path).convert_alpha()
        original_width, original_height = original_size
        canvas_width, canvas_height = canvas_size

        # Масштабирование платформы по высоте экрана
        scale_factor = screen_height / canvas_height
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(x * scale_factor), int(y * scale_factor))

# Функция для загрузки и размещения платформ из .json файла
def load_sprite_positions(json_file, platforms_group, screen_height):
    with open(json_file, 'r') as f:
        data = json.load(f)
    placed_sprites = data["placed_sprites"]
    canvas_size = data["canvas_size"]
    for item in placed_sprites:
        sprite_name = item['sprite']
        x, y = item['x'], item['y']
        original_size = item['original_size']
        sprite_image_path = os.path.join(sprite_dir, sprite_name)
        # Создание объекта ScaledPlatform
        platform = ScaledPlatform(sprite_image_path, x, y, original_size, (canvas_size["width"], canvas_size["height"]), screen_height)
        platforms_group.add(platform)

# Основной игровой цикл
running = True
paused = False
was_sprinting = False
was_walking = False

# Загрузка карты из json файла
json_file_path = 'map.json'  # Укажите правильный путь к вашему json файлу
load_sprite_positions(json_file_path, platforms, screen_height)
all_sprites.add(platforms)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                paused = not paused

    if paused:
        continue

    keys = pygame.key.get_pressed()
    sprinting = keys[pygame.K_LSHIFT]
    is_moving = False

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left(platforms, sprinting)
        is_moving = True
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right(platforms, sprinting)
        is_moving = True
    else:
        if player.is_walking:
            stop_sound(sounds, 'walk')
            stop_sound(sounds, 'sprint')
            player.is_walking = False
        if player.on_ground:
            player.change_animation(f"idle_{player.direction}")
        player.reset_animation_speed()

    if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
        if player.on_ground:
            player.jump(sprinting)
            stop_sound(sounds, 'walk')
            stop_sound(sounds, 'sprint')
            play_sound(sounds, 'jump')

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    if is_moving and player.on_ground:
        if sprinting:
            if not was_sprinting:
                stop_sound(sounds, 'walk')
                play_sound(sounds, 'sprint', -1)
                was_sprinting = True
            was_walking = False
        else:
            if was_sprinting:
                stop_sound(sounds, 'sprint')
                play_sound(sounds, 'walk', -1)
                was_sprinting = False
            elif not was_walking:
                play_sound(sounds, 'walk', -1)
                was_walking = True
        player.is_walking = True
    else:
        was_sprinting = False
        was_walking = False

    player.update(dt, platforms)
    platforms.update()

    for x in range(0, screen_width, background_image.get_width()):
        screen.blit(background_image, (x, 0))

    all_sprites.draw(screen)

    # Отрисовка хитбоксов
    if debug_mode:
        for sprite in all_sprites:
            if hasattr(sprite, 'rect'):
                pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 1)

    draw_hud()

    pygame.draw.rect(screen, bar_color, (bar_position[0], bar_position[1], screen_width, bar_height))

    pygame.display.flip()

pygame.quit()
sys.exit()
