import pygame
import sys
import os
from sprites import Player, load_images
from sounds import load_sounds, play_sound, stop_sound, play_music, stop_music
from game_platform import Platform

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

debug_mode = True  # Включение отладочного режима

# Размеры окна
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h - 200
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Sound Integration")

# Основной цикл
clock = pygame.time.Clock()

# Путь к директории с анимациями спрайтов и звуками
sprite_dir = 'sprites'
sound_dir = 'sounds'

# Загрузка изображений спрайта и звуков, с изменением размера изображений
scale_factor = 0.6
animations = load_images(sprite_dir, scale_factor)
sounds = load_sounds(sound_dir)

# Воспроизведение фоновой музыки
# play_music(os.path.join(sound_dir, 'background_music.mp3'))

# Создание игрока
player = Player(animations, sounds, 100, screen_height - 100, screen_width, screen_height)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Создание платформ
platforms = pygame.sprite.Group()
platform_image_path = 'img/platform.png'
platform_width = 200
platform_height = 50
platforms.add(Platform(platform_image_path, 200, screen_height - platform_height, platform_width, platform_height))

# Добавляем платформы в общую группу спрайтов для отрисовки
all_sprites.add(platforms)

# Загрузка изображения фона
background_image = pygame.image.load('img/background1.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Основной игровой цикл
running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left()
        play_sound(sounds, 'walk')
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right()
        play_sound(sounds, 'walk')
    else:
        stop_sound(sounds, 'walk')
        if player.on_ground:
            player.change_animation(f"idle_idle_{player.direction}")

    if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
        player.jump()
        if player.on_ground:
            play_sound(sounds, 'jump')
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    # Обновление игрока и платформ
    player.update(dt, platforms)
    platforms.update()

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    # Отрисовка границ прямоугольников в отладочном режиме
    if debug_mode:
        for sprite in all_sprites:
            pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()