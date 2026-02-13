import pygame.sprite

import assets
import configs
from layer import Layer

class EndMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.ui
        self.image = assets.get_sprite("over")    
        self.rect = self.image.get_rect(center = (configs.screen_width / 2, 
                                                  configs.screen_height / 2)) # centre alignment
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)