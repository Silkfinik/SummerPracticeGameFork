import pygame
import sys
import os
import json
from config import (screen, screen_width, screen_height, debug_mode, score, bar_color, bar_position, bar_height,
                    scale_factor, music_on, sound_on, key_bindings)
from player import Player
from coin import Coin
from portal import Portal
from sprites import load_images
from sounds import load_sounds, play_sound, stop_sound, play_music, stop_music
from platform_loader import load_sprite_positions
from hud import draw_hud
from menu import (draw_menu, handle_menu_click, draw_settings_menu, handle_settings_click, change_key, draw_end_screen,
                  Get_high_graphics_on)
from background import draw_background, background_image
from start_screen import start_screen

clock = pygame.time.Clock()

# Показ стартового окна
if not start_screen():
    pygame.quit()
    sys.exit()

animations = load_images('sprites', scale_factor)
sounds = load_sounds('sounds')

level = 1

coin_counter = 0  # Счетчик монеток

def get_level():
    global level
    return level

levels = {
    1: "map_danik",
    2: "map_vika",
    3: "map_kirill",
    4: "map_stas"
}


if music_on:
    play_music(os.path.join('sounds', 'background_music.mp3'))

player_cords = 0
player_death_line = 0

def reset_player(player):
    global level
    level = 1
    create_map()


def load_all_sprites(directory, scale_factor=3):
    sprites_coin = {}
    supported_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    for img_file in os.listdir(directory):
        img_path = os.path.join(directory, img_file)
        _, ext = os.path.splitext(img_file)
        if ext.lower() in supported_extensions:
            try:
                image = pygame.image.load(img_path).convert_alpha()
                if scale_factor != 1:
                    width, height = image.get_size()
                    image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
                sprites_coin[os.path.splitext(img_file)[0]] = image
            except pygame.error as e:
                print(f"Could not load image {img_file}: {e}")

    return sprites_coin


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
portals = pygame.sprite.Group()  # Группа для порталов
platforms_passive_group = pygame.sprite.Group()
coins = pygame.sprite.Group()  # Группа для монеток
player = Player(animations, sounds, 0, 0, screen_width, screen_height, 2)


def create_map():
    global player
    global player_cords
    global player_death_line
    all_sprites.empty()
    platforms.empty()
    platforms_passive_group.empty()
    coins.empty()  # Очищаем группу монеток
    portals.empty()  # Очищаем группу порталов

    with open(f"maps/{levels[level]}.json", 'r') as f:
        data = json.load(f)
    player_cords = data['player_spawn']
    player_death_line = data["death_line"]["y_d"]
    f.close()

    load_sprite_positions(f'{levels[level]}.json', platforms, screen_height, platforms_passive_group, levels[level])
    player = Player(animations, sounds, player_cords["x"], player_cords["y"], screen_width, screen_height, 2)

    all_sprites.add(platforms)
    all_sprites.add(platforms_passive_group)
    all_sprites.add(player)

    # Загружаем все спрайты из директории
    all_sprites_dict = load_all_sprites('img/coin_sprites', 3)

    # Проверка загруженных спрайтов
    if not all_sprites_dict:
        print("Error: No sprites loaded.")
        return

    # Добавляем монетки на карту
    coin_animations = [all_sprites_dict[key] for key in sorted(all_sprites_dict.keys()) if 'coin' in key.lower()]  # Преобразуем в список

    for coin_data in data.get("coins", []):
        coin = Coin(coin_data["x"], coin_data["y"], coin_animations)
        coins.add(coin)
        all_sprites.add(coin)

    # Загружаем изображение портала
    portal_image = pygame.image.load('img/portal_open.png').convert_alpha()
    width, height = portal_image.get_size()
    portal_image = pygame.transform.scale(portal_image, (int(width * 3), int(height * 3)))

    # Добавляем порталы на карту
    for portal_data in data.get("portals", []):
        portal = Portal(portal_data["x"], portal_data["y"], portal_image)
        portals.add(portal)
        all_sprites.add(portal)

    all_sprites.remove(*platforms_passive_group)
    if Get_high_graphics_on():
        all_sprites.remove(player)
        all_sprites.add(*platforms_passive_group)
        all_sprites.add(player)


create_map()

running = True
paused = False
menu_active = False
settings_active = False
end_game_active = False  # Новый флаг для экрана конца игры
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
            elif event.key == pygame.K_q and end_game_active:
                running = False  # Закрытие игры при нажатии "Q" на экране конца игры
            elif event.key == pygame.K_g:  # Проверка нажатия клавиши 'g'
                level += 1
                if level != 5:
                    create_map()
                else:
                    end_game_active = True  # Активируем экран конца игры
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active:
                result = handle_menu_click(event.pos, player)
                if result == "settings":
                    menu_active = False
                    settings_active = True
                elif result == "restart":
                    reset_player(player)  # Перезапуск уровня
                    menu_active = False  # Закрытие меню
                elif result == "graphics":
                    all_sprites.remove(*platforms_passive_group)
                    if Get_high_graphics_on():
                        all_sprites.remove(player)
                        all_sprites.add(*platforms_passive_group)
                        all_sprites.add(player)



            elif settings_active:
                result = handle_settings_click(event.pos, key_changing)
                if result == "menu":
                    settings_active = False
                    menu_active = True
                else:
                    key_changing = result

    if player.rect.bottom >= player_death_line:
        level = 1
        create_map()

    if end_game_active:
        draw_end_screen(screen, coin_counter)
        continue

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

    # Обновляем монетки и порталы
    coins.update()
    portals.update()

    # Проверяем столкновение игрока с монетками
    collected_coins = pygame.sprite.spritecollide(player, coins, dokill=True)
    coin_counter += len(collected_coins)

    # Проверяем столкновение игрока с порталом
    if pygame.sprite.spritecollideany(player, portals):
        level += 1
        if level != 5:
            create_map()
        else:
            end_game_active = True  # Активируем экран конца игры

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
