import os
import json
import pygame


levels = {
    1: "map_danik",
    2: "map_vika",
    3: "map_kirill",
    4: "map_stas"
}

class ScaledPlatform(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, original_size, canvas_size, screen_height):
        super().__init__()
        image = pygame.image.load(image_path).convert_alpha()
        original_width, original_height = original_size
        canvas_width, canvas_height = canvas_size

        # Масштабирование платформы по высоте экрана
        scale_factor = 1
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(x * scale_factor), int(y * scale_factor))


def load_sprite_positions(json_file, platforms_group, screen_height, platforms_passive_group, dir1):
    with open('maps/' + json_file, 'r') as f:
        data = json.load(f)
    placed_sprites = data["placed_sprites"]
    canvas_size = data["canvas_size"]

    for item in placed_sprites:
        sprite_name = item['sprite']
        x, y = item['x'], item['y']
        original_size = item['current_size']
        active = item.get('active', True)  # Default to True if 'active' key is not present
        sprite_image_path = os.path.join('img', f'{dir1}', 'used_sprites', sprite_name)  # Новый путь к используемым спрайтам

        # Создание объекта ScaledPlatform
        platform = ScaledPlatform(sprite_image_path, x, y, original_size, (canvas_size["width"], canvas_size["height"]),
                                  screen_height)

        if active:
            platforms_group.add(platform)
        else:
            platforms_passive_group.add(platform)
