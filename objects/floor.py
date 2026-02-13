# import pygame.sprite

# import assets
# import configs
# from layer import Layer

# class Floor(pygame.sprite.Sprite):
#     def __init__(self, index, *groups):
#         self._layer = Layer.floor
#         self.image = assets.get_sprite("floor")    # i am just using random images i have in the folder at the moment
#         self.rect = self.image.get_rect(bottomleft = (configs.screen_width * index, configs.screen_height))

#         self.mask = pygame.mask.from_surface(self.image)



#         super().__init__(*groups)

#     def update(self):
#         self.rect.x -= 2

#         if self.rect.right <= 0:
#             self.rect.x = configs.screen_width