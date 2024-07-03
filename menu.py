import os
import pygame
from config import font, screen_width, screen_height, music_on, sound_on, key_bindings
from sounds import play_music, stop_music  # Добавлен импорт stop_music

# Константы
square_size = 20
padding = 10
offset_down = 7  # Смещение вниз на 7 пикселей
high_graphics_on = True

# Вычисление позиций для центрирования всех элементов
menu_text = font.render("Menu", True, (255, 255, 255))
quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
music_text = font.render("Music", True, (255, 255, 255))
sound_text = font.render("Sound", True, (255, 255, 255))
settings_text = font.render("Settings", True, (255, 255, 255))
restart_text = font.render("Restart", True, (255, 255, 255))
graphics_text = font.render("Graphics: ", True, (255, 255, 255))

menu_text_pos = (screen_width // 2 - menu_text.get_width() // 2, screen_height // 2 - 5 * (menu_text.get_height() + padding))
music_text_pos = (screen_width // 2 - (music_text.get_width() + square_size + padding) // 2, menu_text_pos[1] + menu_text.get_height() + padding)
sound_text_pos = (screen_width // 2 - (sound_text.get_width() + square_size + padding) // 2, music_text_pos[1] + music_text.get_height() + padding)
settings_text_pos = (screen_width // 2 - settings_text.get_width() // 2, sound_text_pos[1] + sound_text.get_height() + padding)
restart_text_pos = (screen_width // 2 - restart_text.get_width() // 2, settings_text_pos[1] + settings_text.get_height() + padding)
graphics_text_pos = (screen_width // 2 - graphics_text.get_width() // 2, restart_text_pos[1] + restart_text.get_height() + padding)
quit_text_pos = (screen_width // 2 - quit_text.get_width() // 2, graphics_text_pos[1] + graphics_text.get_height() + padding)

music_square_pos = (music_text_pos[0] + music_text.get_width() + padding, music_text_pos[1] + offset_down)
sound_square_pos = (sound_text_pos[0] + sound_text.get_width() + padding, sound_text_pos[1] + offset_down)
graphics_square_pos = (graphics_text_pos[0] + graphics_text.get_width(), graphics_text_pos[1] + offset_down)

def draw_menu(screen):
    """
    Отрисовка меню на экране.
    
    :param screen: Объект экрана Pygame.
    """
    global high_graphics_on

    screen.blit(menu_text, menu_text_pos)
    screen.blit(music_text, music_text_pos)
    screen.blit(sound_text, sound_text_pos)
    screen.blit(settings_text, settings_text_pos)
    screen.blit(restart_text, restart_text_pos)
    screen.blit(graphics_text, graphics_text_pos)
    screen.blit(quit_text, quit_text_pos)

    pygame.draw.rect(screen, (255, 255, 255), (*music_square_pos, square_size, square_size), 2)
    pygame.draw.rect(screen, (255, 255, 255), (*sound_square_pos, square_size, square_size), 2)

    if music_on:
        pygame.draw.rect(screen, (0, 255, 0), (*music_square_pos, square_size, square_size))
    if sound_on:
        pygame.draw.rect(screen, (0, 255, 0), (*sound_square_pos, square_size, square_size))

    graphics_state_text = font.render("ultra" if high_graphics_on else "potato", True, (0, 255, 0))
    graphics_state_text_pos = (graphics_square_pos[0], graphics_text_pos[1])
    screen.blit(graphics_state_text, graphics_state_text_pos)

def handle_menu_click(pos, player):
    """
    Обработка кликов по элементам меню.
    
    :param pos: Позиция клика мыши.
    :param player: Объект игрока.
    :return: Строка с результатом действия (например, "settings", "restart") или None.
    """
    global music_on, sound_on, high_graphics_on
    x, y = pos
    if music_square_pos[0] <= x <= music_square_pos[0] + square_size and music_square_pos[1] <= y <= music_square_pos[1] + square_size:
        music_on = not music_on
        if music_on:
            play_music(os.path.join('sounds', 'background_music.mp3'))
        else:
            stop_music()
    elif sound_square_pos[0] <= x <= sound_square_pos[0] + square_size and sound_square_pos[1] <= y <= sound_square_pos[1] + square_size:
        sound_on = not sound_on
        player.sounds_on = sound_on
        if not sound_on:
            for sound in player.sounds.values():
                sound.stop()
        print(f"Sound {'enabled' if sound_on else 'disabled'}")
    elif settings_text_pos[0] <= x <= settings_text_pos[0] + settings_text.get_width() and settings_text_pos[1] <= y <= settings_text_pos[1] + settings_text.get_height():
        return "settings"
    elif restart_text_pos[0] <= x <= restart_text_pos[0] + restart_text.get_width() and restart_text_pos[1] <= y <= restart_text_pos[1] + restart_text.get_height():
        return "restart"
    elif graphics_text_pos[0] <= x <= graphics_text_pos[0] + graphics_text.get_width() and graphics_text_pos[1] <= y <= graphics_text_pos[1] + graphics_text.get_height():
        high_graphics_on = not high_graphics_on
        print("High Graphics " + str(high_graphics_on))
        return "graphics"
    return None

def Get_high_graphics_on():
    """
    Получение состояния высоких графических настроек.
    
    :return: Булево значение состояния высоких графических настроек.
    """
    global high_graphics_on
    print("getter " + str(high_graphics_on))
    return high_graphics_on

def draw_settings_menu(screen, key_bindings, key_changing):
    """
    Отрисовка меню настроек управления.
    
    :param screen: Объект экрана Pygame.
    :param key_bindings: Словарь с текущими настройками клавиш.
    :param key_changing: Текущая изменяемая клавиша.
    """
    settings_text = font.render("Settings", True, (255, 255, 255))
    back_text = font.render("Back to Menu", True, (255, 255, 255))

    screen.blit(settings_text, (screen_width // 2 - settings_text.get_width() // 2, screen_height // 2 - settings_text.get_height() // 2 - 120))

    actions = ["left", "right", "jump", "sprint"]
    for i, action in enumerate(actions):
        action_text = font.render(action.capitalize(), True, (255, 255, 255))
        key_text = font.render("Enter your key" if key_changing == action else pygame.key.name(key_bindings[action]), True, (255, 255, 255))
        screen.blit(action_text, (screen_width // 2 - action_text.get_width() // 2 - 60, screen_height // 2 - action_text.get_height() // 2 - 40 + i * 40))
        screen.blit(key_text, (screen_width // 2 + 40, screen_height // 2 - key_text.get_height() // 2 - 40 + i * 40))

    screen.blit(back_text, (screen_width // 2 - back_text.get_width() // 2, screen_height // 2 - back_text.get_height() // 2 + 120))

def handle_settings_click(pos, key_changing):
    """
    Обработка кликов по элементам меню настроек.
    
    :param pos: Позиция клика мыши.
    :param key_changing: Текущая изменяемая клавиша.
    :return: Действие или None.
    """
    back_text = font.render("Back to Menu", True, (255, 255, 255))
    back_text_pos = (screen_width // 2 - back_text.get_width() // 2, screen_height // 2 - back_text.get_height() // 2 + 120)
    actions = ["left", "right", "jump", "sprint"]
    for i, action in enumerate(actions):
        key_text_pos = (screen_width // 2 + 40, screen_height // 2 - font.size("Enter your key")[1] // 2 - 40 + i * 40)
        if key_text_pos[0] <= pos[0] <= key_text_pos[0] + font.size(pygame.key.name(key_bindings[action]))[0] and key_text_pos[1] <= pos[1] <= key_text_pos[1] + font.size("Enter your key")[1]:
            return action

    x, y = pos
    if back_text_pos[0] <= x <= back_text_pos[0] + back_text.get_width() and back_text_pos[1] <= y <= back_text_pos[1] + back_text.get_height():
        return "menu"
    return None

def change_key(event, key_changing, key_bindings):
    """
    Изменение назначения клавиши управления.

    :param event: Событие Pygame.
    :param key_changing: Текущая изменяемая клавиша.
    :param key_bindings: Словарь с текущими настройками клавиш.
    :return: Новая изменяемая клавиша или None.
    """
    if key_changing:
        key_bindings[key_changing] = event.key
        return None
    return key_changing

def draw_end_screen(screen, coin_counter):
    """
    Отрисовка экрана окончания игры.

    :param screen: Объект экрана Pygame.
    :param coin_counter: Количество собранных монет.
    """
    end_text = font.render("Congratulations, You Won!", True, (255, 255, 255))
    score_text = font.render(f"You collected {coin_counter} out of 13 coins", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))

    end_text_pos = (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 2 * (end_text.get_height() + padding))
    score_text_pos = (screen_width // 2 - score_text.get_width() // 2, end_text_pos[1] + end_text.get_height() + padding)
    quit_text_pos = (screen_width // 2 - quit_text.get_width() // 2, score_text_pos[1] + score_text.get_height() + padding)

    screen.fill((0, 0, 0))
    screen.blit(end_text, end_text_pos)
    screen.blit(score_text, score_text_pos)
    screen.blit(quit_text, quit_text_pos)

    pygame.display.flip()
