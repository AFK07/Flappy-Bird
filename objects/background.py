# import pygame.sprite
# import assets
# import configs
# from layer import Layer

# class Background(pygame.sprite.Sprite):
#     def __init__(self, index, *groups):
#         super().__init__(*groups)
#         self._layer = Layer.background          # make sure to understand how the layers work on each class functions
#         self.image = assets.geet_sprite("background")   # gets the image for the background from the assets using the image name
#         self.rect = self.imag.get_rect(topleft=(configs.screen_width * index, -50)) #sets the position of the image. Right now, top left of the screen
    
#     def update(self):
#         self.rect.x -= 1                        # speed of the image slide

#         if self.rect.right <= 0:
#             self.rect.x = configs.screen_width
