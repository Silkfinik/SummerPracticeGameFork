import pygame
import sys
import os
from config import screen, screen_width, screen_height, debug_mode, score, bar_color, bar_position, bar_height, scale_factor, music_on, sound_on, key_bindings
from player import Player
from sprites import load_images
from sounds import load_sounds, play_sound, stop_sound, play_music, stop_music
from game_platform import Platform
from platform_loader import load_sprite_positions
from hud import draw_hud
from menu import draw_menu, handle_menu_click, draw_settings_menu, handle_settings_click, change_key
from background import draw_background, background_image

clock = pygame.time.Clock()

animations = load_images('sprites', scale_factor)
sounds = load_sounds('sounds')

if music_on:
    play_music(os.path.join('sounds', 'background_music.mp3'))

player = Player(animations, sounds, 100, screen_height - 100 - bar_height, screen_width, screen_height, 2)

all_sprites = pygame.sprite.Group()

platforms = pygame.sprite.Group()
platforms_passive_group = pygame.sprite.Group()

all_sprites.add(platforms)

load_sprite_positions('map.json', platforms, screen_height, platforms_passive_group)
all_sprites.add(platforms)
all_sprites.add(platforms_passive_group)
all_sprites.add(player)

running = True
paused = False
menu_active = False
settings_active = False
was_sprinting = False
was_walking = False
key_changing = None  # Для отслеживания изменения клавиши

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if menu_active:
                if event.key == pygame.K_ESCAPE:
                    menu_active = False
                elif event.key == pygame.K_q:
                    running = False
            elif settings_active:
                if event.key == pygame.K_ESCAPE:
                    settings_active = False
                    menu_active = True
                else:
                    key_changing = change_key(event, key_changing, key_bindings)
            elif event.key == pygame.K_ESCAPE:
                menu_active = not menu_active

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active:
                result = handle_menu_click(event.pos, player)
                if result == "settings":
                    menu_active = False
                    settings_active = True
            elif settings_active:
                result = handle_settings_click(event.pos, key_changing)
                if result == "menu":
                    settings_active = False
                    menu_active = True
                else:
                    key_changing = result

    if menu_active:
        screen.fill((0, 0, 0))
        draw_menu(screen)
        pygame.display.flip()
        continue

    if settings_active:
        screen.fill((0, 0, 0))
        draw_settings_menu(screen, key_bindings, key_changing)
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    sprinting = keys[key_bindings["sprint"]]
    is_moving = False

    if keys[key_bindings["left"]]:
        player.move_left(platforms, sprinting)
        is_moving = True
    elif keys[key_bindings["right"]]:
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

    if keys[key_bindings["jump"]]:
        if player.on_ground:
            player.jump(sprinting)
            stop_sound(sounds, 'walk')
            stop_sound(sounds, 'sprint')
            if player.sounds_on:  # Проверка состояния звуков
                play_sound(sounds, 'jump')

    if is_moving and player.on_ground:
        if sprinting:
            if not was_sprinting:
                stop_sound(sounds, 'walk')
                if player.sounds_on:  # Проверка состояния звуков
                    play_sound(sounds, 'sprint', -1)
                was_sprinting = True
            was_walking = False
        else:
            if was_sprinting:
                stop_sound(sounds, 'sprint')
                if player.sounds_on:  # Проверка состояния звуков
                    play_sound(sounds, 'walk', -1)
                was_sprinting = False
            elif not was_walking:
                if player.sounds_on:  # Проверка состояния звуков
                    play_sound(sounds, 'walk', -1)
                was_walking = True
        player.is_walking = True
    else:
        was_sprinting = False
        was_walking = False

    platforms_passive_group.update()
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
