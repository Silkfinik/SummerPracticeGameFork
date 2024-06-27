import pygame
import os

def load_images(sprite_dir, scale_factor=1):
    animations = {}
    supported_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

    def load_frames_from_directory(directory):
        frames = []
        for img_file in sorted(os.listdir(directory)):
            img_path = os.path.join(directory, img_file)
            _, ext = os.path.splitext(img_file)
            if ext.lower() in supported_extensions:
                try:
                    image = pygame.image.load(img_path).convert_alpha()
                    width, height = image.get_size()
                    image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
                    frames.append(image)
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
                frames = load_frames_from_directory(base_dir)
                if frames:
                    animations[prefix] = frames

    load_animation_paths(sprite_dir)
    return animations
