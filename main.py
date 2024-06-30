import pygame
import sys
import os
from config import screen, screen_width, screen_height, debug_mode, score, bar_color, bar_position, bar_height, scale_factor
from player import Player
from sprites import load_images
from sounds import load_sounds, play_sound, stop_sound, play_music, stop_music
from game_platform import Platform
from platform_loader import load_sprite_positions
from hud import draw_hud
from menu import draw_menu
from background import draw_background, background_image

# Основной цикл
clock = pygame.time.Clock()

# Загрузка изображений спрайта и звуков
animations = load_images('sprites', scale_factor)
sounds = load_sounds('sounds')

play_music(os.path.join('sounds', 'background_music.mp3'))

# Создание игрока
player = Player(animations, sounds, 100, screen_height - 100 - bar_height, screen_width, screen_height, scale_factor)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Создание пола (застилание платформами)
platforms = pygame.sprite.Group()
platform_image_path = 'img/platform.png'
platform_width = 200
platform_height = 50

platforms.add(Platform(platform_image_path, 0, screen_height - platform_height - bar_height, screen_width, platform_height))
all_sprites.add(platforms)

# Загрузка карты из json файла
load_sprite_positions('map.json', platforms, screen_height)
all_sprites.add(platforms)

running = True
paused = False
menu_active = False
was_sprinting = False
was_walking = False

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_active = not menu_active
            elif event.key == pygame.K_q and menu_active:
                running = False

    if menu_active:
        screen.fill((0, 0, 0))
        draw_menu(screen)
        pygame.display.flip()
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

    draw_background(screen, background_image, screen_width)
    all_sprites.draw(screen)

    if debug_mode:
        for sprite in all_sprites:
            if hasattr(sprite, 'rect'):
                pygame.draw.rect(screen, (255, 0, 0), sprite.rect, 1)

    draw_hud(screen)

    pygame.draw.rect(screen, bar_color, (bar_position[0], bar_position[1], screen_width, bar_height))

    pygame.display.flip()

pygame.quit()
sys.exit()
