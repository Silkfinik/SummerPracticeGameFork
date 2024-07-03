import os
import json
import pygame

# Словарь уровней с соответствующими именами карт
levels = {
    1: "map_danik",
    2: "map_vika",
    3: "map_kirill",
    4: "map_stas"
}

class Map_Object(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, original_size):
        """
        Инициализация объекта ScaledPlatform.

        :param image_path: Путь к изображению платформы.
        :param x: Координата X расположения платформы.
        :param y: Координата Y расположения платформы.
        :param original_size: Исходный размер платформы.
        """
        super().__init__()
        image = pygame.image.load(image_path).convert_alpha()
        original_width, original_height = original_size
        self.image = pygame.transform.scale(image, (original_width, original_height))
        self.rect = self.image.get_rect(topleft=(x, y))

def load_sprite_positions(json_file, platforms_group, screen_height, platforms_passive_group, dir1):
    """
    Загрузка позиций спрайтов из JSON файла и создание платформ.

    :param json_file: Имя JSON файла.
    :param platforms_group: Группа активных платформ.
    :param screen_height: Высота экрана.
    :param platforms_passive_group: Группа пассивных платформ.
    :param dir1: Директория, содержащая изображения спрайтов.
    """
    with open(os.path.join('maps', json_file), 'r') as f:
        data = json.load(f)
    placed_sprites = data["placed_sprites"]
    canvas_size = data["canvas_size"]

    for item in placed_sprites:
        sprite_name = item['sprite']
        x, y = item['x'], item['y']
        original_size = item['current_size']
        active = item.get('active', True)  # По умолчанию True, если ключ 'active' отсутствует
        sprite_image_path = os.path.join('img', dir1, 'used_sprites', sprite_name)  # Путь к используемым спрайтам

        # Создание объекта ScaledPlatform
        platform = Map_Object(sprite_image_path, x, y, original_size)

        if active:
            platforms_group.add(platform)
        else:
            platforms_passive_group.add(platform)
