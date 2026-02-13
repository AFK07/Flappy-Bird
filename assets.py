import os
import pygame 

sprites = {}
audios = {}

def load_sprites():
    # Use 'sprites' directly as it is in your root directory
    path = os.path.join("sprites") 
    for file in os.listdir(path):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            name = file.split('.')[0]
            sprites[name] = pygame.image.load(os.path.join(path, file)).convert_alpha()

def get_sprite(name):
    return sprites[name]

def load_audios():
    # Use 'audios' directly as it is in your root directory
    path = os.path.join("audios")
    for file in os.listdir(path):
        if file.endswith(('.wav', '.mp3', '.ogg')):
            name = file.split('.')[0]
            audios[name] = pygame.mixer.Sound(os.path.join(path, file))

def play_audio(name):
    if name in audios:
        audios[name].play()