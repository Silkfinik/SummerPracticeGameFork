import pygame
from config import screen_width, screen_height

def load_and_scale_background(image_path, screen_width, screen_height):
    """
    Загрузка и масштабирование фона по высоте экрана.

    :param image_path: Путь к изображению фона.
    :param screen_width: Ширина экрана.
    :param screen_height: Высота экрана.
    :return: Масштабированное изображение фона.
    """
    image = pygame.image.load(image_path).convert_alpha()
    image_width, image_height = image.get_size()

    # Вычисляем коэффициент масштабирования по высоте
    scale_factor = screen_height / image_height
    new_width = int(image_width * scale_factor)
    scaled_image = pygame.transform.scale(image, (new_width, screen_height))

    return scaled_image

# Путь к изображению фона
background_image_path = 'img/sky_blue.png'
background_image = load_and_scale_background(background_image_path, screen_width, screen_height)

def draw_background(screen, background_image, screen_width):
    """
    Отрисовка фона на экране.

    :param screen: Объект экрана Pygame.
    :param background_image: Изображение фона.
    :param screen_width: Ширина экрана.
    """
    for x in range(0, screen_width, background_image.get_width()):
        screen.blit(background_image, (x, 0))
