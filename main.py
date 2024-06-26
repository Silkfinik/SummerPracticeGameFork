import pygame
import sys
import os
from sprites import Player, load_images
from sounds import load_sounds, play_sound, stop_sound, play_music, stop_music

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера для звуков

# Размеры окна
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

pygame.display.set_caption("Sound Integration")

# Основной цикл
clock = pygame.time.Clock()

# Путь к директории с анимациями спрайтов и звуками
sprite_dir = 'sprites'
sound_dir = 'sounds'

# Загрузка изображений спрайта и звуков
animations = load_images(sprite_dir)
sounds = load_sounds(sound_dir)

# Воспроизведение фоновой музыки
play_music(os.path.join(sound_dir, 'background_music.mp3'))

# Создание игрока
player = Player(animations, sounds, 100, screen_height - 100)

# Группа спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Загрузка изображения фона
background_image = pygame.image.load('img/background1.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Основной игровой цикл
running = True
while running:
    dt = clock.tick(60) / 1000  # Время, прошедшее с последнего кадра (в секундах)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left()
        play_sound(sounds, 'walk')  # Воспроизведение звука ходьбы
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right()
        play_sound(sounds, 'walk')  # Воспроизведение звука ходьбы
    else:
        stop_sound(sounds, 'walk')  # Остановка звука ходьбы при отпускании клавиши
        if player.on_ground:
            player.change_animation(f"idle_idle_{player.direction}")

    if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
        player.jump()
        play_sound(sounds, 'jump')  # Воспроизведение звука прыжка

    # Обновление всех спрайтов
    all_sprites.update(dt)

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
