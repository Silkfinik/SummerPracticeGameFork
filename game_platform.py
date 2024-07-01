import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=None, height=None):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()

        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass
