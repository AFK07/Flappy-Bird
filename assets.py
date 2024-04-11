import os
import pygame 

# will be used to load images, where the keys will be the filenames and the values will be the corresponding image surfaces
sprites = {}

def load_sprites():

    # os.path.join is the function to join the directory
    path = os.path.join("assets", "sprites") 
    # constructs a path to the directory containing the images.
    
    # istdir is a function from the os module in python that returns a list containing the names of the entries in a specified directory
    for file in os.listdir(path):

        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))
        # loads each image file using pygame.iage.load() and stores the resulting image surface in the images directory

def get_sprite(name):           # retrieves images from the images directory
    return sprites[name]