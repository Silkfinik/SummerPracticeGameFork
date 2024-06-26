import pygame
import sys
from sprites import Player, load_images

# Инициализация Pygame
pygame.init()

# Размеры окна
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

pygame.display.set_caption("Анимация спрайтов")

# Основной цикл
clock = pygame.time.Clock()

# Путь к директории с анимациями спрайтовa
sprite_dir = 'sprites'

# Загрузка изображений спрайта
animations = load_images(sprite_dir)

# Создание игрока
player = Player(animations, 100, screen_height - 100)

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
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right()
    else:
        if player.on_ground:
            player.change_animation(f"idle_idle_{player.direction}")

    if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
        player.jump()

    # Обновление всех спрайтов
    all_sprites.update(dt)

    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
