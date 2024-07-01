import pygame
import os
from config import sound_on

def load_sounds(sound_dir):
    sounds = {}
    for sound_file in os.listdir(sound_dir):
        if sound_file.endswith('.wav') or sound_file.endswith('.mp3'):
            sound_path = os.path.join(sound_dir, sound_file)
            sound_name = os.path.splitext(sound_file)[0]
            sounds[sound_name] = pygame.mixer.Sound(sound_path)
    return sounds

def play_sound(sounds, sound_name, loops=0):
    if sound_on and sound_name in sounds:
        sounds[sound_name].play(loops=loops)
        print(f"Playing sound: {sound_name}")
    elif sound_name not in sounds:
        print(f"Sound '{sound_name}' not found in loaded sounds.")
    else:
        print(f"Sound is disabled. Not playing: {sound_name}")

def stop_sound(sounds, sound_name):
    if sound_name in sounds:
        sounds[sound_name].stop()
    else:
        print(f"Sound '{sound_name}' not found in loaded sounds.")

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()
