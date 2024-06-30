import pygame
import os

def load_images(sprite_dir, scale_factor=1):
    animations = {}
    supported_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    def load_frames_from_directory(directory):
        frames = []
        max_width, max_height = 0, 0

        # Находим максимальные размеры кадров
        for img_file in sorted(os.listdir(directory)):
            img_path = os.path.join(directory, img_file)
            _, ext = os.path.splitext(img_file)
            if ext.lower() in supported_extensions:
                try:
                    image = pygame.image.load(img_path).convert_alpha()
                    width, height = image.get_size()
                    max_width = max(max_width, width)
                    max_height = max(max_height, height)
                except pygame.error:
                    pass

        # Приводим все кадры к одному размеру
        for img_file in sorted(os.listdir(directory)):
            img_path = os.path.join(directory, img_file)
            _, ext = os.path.splitext(img_file)
            if ext.lower() in supported_extensions:
                try:
                    image = pygame.image.load(img_path).convert_alpha()
                    width, height = image.get_size()
                    new_image = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
                    new_image.blit(image, ((max_width - width) // 2, (max_height - height) // 2))
                    new_image = pygame.transform.scale(new_image, (int(max_width * scale_factor), int(max_height * scale_factor)))
                    frames.append(new_image)
                except pygame.error:
                    pass

        return frames

    def load_animation_paths(base_dir, prefix=""):
        for entry in os.listdir(base_dir):
            entry_path = os.path.join(base_dir, entry)
            if os.path.isdir(entry_path):
                new_prefix = f"{prefix}_{entry}" if prefix else entry
                load_animation_paths(entry_path, new_prefix)
            else:
                # Пропускаем файлы в корневом каталоге
                continue

        # Загружаем кадры из текущего каталога, если это каталог с изображениями
        if prefix and os.path.isdir(base_dir):
            frames = load_frames_from_directory(base_dir)
            if frames:
                animations[prefix] = frames

    # Проверка существования директории
    if not os.path.exists(sprite_dir):
        raise FileNotFoundError(f"Directory '{sprite_dir}' does not exist.")

    load_animation_paths(sprite_dir)
    return animations

# Пример использования:
pygame.init()
sprite_dir = 'sprites'  # Укажите правильный путь к вашему каталогу с анимациями
scale_factor = 1  # Масштабирование, если необходимо
animations = load_images(sprite_dir, scale_factor)

# Выводим названия загруженных анимаций
print("Loaded animations:", animations.keys())