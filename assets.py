import os
import pygame 

# Dictionaries to store loaded surfaces and sounds
sprites = {}
audios = {}

def load_sprites():
    """
    Loads images from the 'sprites' directory.
    Uses convert_alpha() for better performance and handles extensions.
    """
    # Uses the 'sprites' folder located in your root directory
    path = os.path.join("sprites") 
    
    if not os.path.exists(path):
        print(f"Error: The directory {path} does not exist.")
        return

    for file in os.listdir(path):
        # Only load valid image files
        if file.endswith(('.png', '.jpg', '.jpeg')):
            name = file.split('.')[0]
            # convert_alpha() optimizes the surface for faster drawing in pygame
            sprites[name] = pygame.image.load(os.path.join(path, file)).convert_alpha()

def get_sprite(name):
    """Retrieves an image from the sprites dictionary"""
    return sprites.get(name)

def load_audios():
    """Loads audio files as Sound objects from the 'audios' directory."""
    # Uses the 'audios' folder located in your root directory
    path = os.path.join("audios")
    
    if not os.path.exists(path):
        print(f"Error: The directory {path} does not exist.")
        return

    for file in os.listdir(path):
        # Only load valid audio files
        if file.endswith(('.wav', '.mp3', '.ogg')):
            name = file.split('.')[0]
            audios[name] = pygame.mixer.Sound(os.path.join(path, file))

def play_audio(name):
    """Plays the sound associated with the given name if it exists"""
    if name in audios:
        audios[name].play()