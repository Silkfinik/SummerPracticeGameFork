import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, animations):
        """
        Инициализация объекта Coin.

        :param x: Координата X расположения монетки.
        :param y: Координата Y расположения монетки.
        :param animations: Список кадров анимации монетки.
        """
        super().__init__()
        self.animations = animations
        self.current_frame = 0
        self.image = self.animations[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1  # Скорость анимации в секундах
        self.last_update = pygame.time.get_ticks()
        self.id = None  # Уникальный идентификатор монетки

    def update(self):
        """
        Обновление анимации монетки.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.image = self.animations[self.current_frame]
