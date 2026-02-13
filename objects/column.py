### Column
# contains the pass functions

import random
import pygame.sprite
import assets
import configs
from layer import Layer

class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = Layer.obstacle
        self.gap = 100

        self.image = assets.get_sprite("pipe-green")
        self.sprite_rect = self.image.get_rect()                                    # You can use self.image to access the sprite image

        self.pipe_bottom = self.image
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprite_rect.height + self.gap))

        self.pipe_top = pygame.transform.flip(self.image, True, True)               # flips the images
        self.pipe_top_rect = self.pipe_bottom.get_rect(topleft=(0, 0))              #play with this to understand around


        self.image = pygame.surface.Surface((self.sprite_rect.width, 
                                             self.sprite_rect.height * 2 + self.gap),
                                             pygame.SRCALPHA)                       # srcalpha is a transparency support, need to play around with this
        # self.image.fill("red")                      # Not really necessary

        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)


        sprite_floor_height = assets.get_sprite("floor").get_rect().height
        min_y = 100
        max_y = configs.screen_height - sprite_floor_height - 100

        
        self.rect = self.image.get_rect(midleft=(configs.screen_width, 
                                                 random.uniform(min_y, max_y)))             # remember, midleft = (x, y)
                                                                                            # 
        self.mask = pygame.mask.from_surface(self.image)

        self.passed = False                         # checking whether the bird/player passed through the column gaps


    def update(self):
        self.rect.x -= 2

        if self.rect.right <= 0:
            self.kill()

        # self.rect = self.image.get_rect(topleft=(0, max_y))
        # task to increase the y axis length of column. thats why i decreased the hight of the dimension itself

    def is_passed(self):
        if self.rect.x < 50 and not self.passed:
            # self.rect.x < 50 : checks if the column's x coordinates is less than 50, which means the column has moved passed the bird
            # not self.passed : checks if its false, indicating the bird has not yet passed through the column
            self.passed = True
            return True
        return False