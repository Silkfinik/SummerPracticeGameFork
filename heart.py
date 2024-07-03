import pygame

class Heart(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        """
        Инициализация объекта Heart.

        :param image: Изображение сердца.
        :param x: Координата X расположения сердца.
        :param y: Координата Y расположения сердца.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
