import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        """
        Инициализация объекта Portal.

        :param x: Координата X расположения портала.
        :param y: Координата Y расположения портала.
        :param image: Изображение портала.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
