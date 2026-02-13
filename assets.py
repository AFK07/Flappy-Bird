import os
import pygame 

# Global dictionaries to store game media
sprites = {}
audios = {}

def load_sprites():
    """
    Loads images from the 'sprites' directory located in the root folder.
    Keys are filenames without extensions, values are pygame Surfaces.
    """
    # Based on your tree output, 'sprites' is in the root directory
    path = os.path.join("sprites") 
    
    for file in os.listdir(path):
        # Only load files that look like images
        if file.endswith(('.png', '.jpg', '.jpeg')):
            name = file.split('.')[0]
            sprites[name] = pygame.image.load(os.path.join(path, file)).convert_alpha()

def get_sprite(name):
    """Retrieves a loaded image surface by its name"""
    return sprites[name]

def load_audios():
    """
    Loads sound files from the 'audios' directory in the root folder.
    Keys are filenames without extensions, values are pygame Sound objects.
    """
    # Based on your tree output, 'audios' is in the root directory
    path = os.path.join("audios")
    
    for file in os.listdir(path):
        # Only load common audio formats
        if file.endswith(('.wav', '.mp3', '.ogg')):
            name = file.split('.')[0]
            audios[name] = pygame.mixer.Sound(os.path.join(path, file))

def play_audio(name):
    """Plays a loaded audio file by its name"""
    if name in audios:
        audios[name].play()