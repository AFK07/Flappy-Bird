# import pygame.sprite

# import assets
# import configs
# from layer import Layer
# ### score
# class Score(pygame.sprite.Sprite):
#     def __init__(self, *groups):
#         self._layer = Layer.ui
#         self.value = 0                          # initialises the score value to 0
#         self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA) # transparency 
#         # creates a new surface image for score    
#         self.__create()                         

#         super().__init__(*groups)

#     def __create(self):
#         self.str_value = str(self.value)        # converts integer value score to a string 

#         self.images =[]
#         self.width = 0                          # initialises an empty list to store individual digit images and a variable to kekep track of the total width of the score image

#         for str_value_char in self.str_value:
#             img = assets.get_sprite(str_value_char)
#             self.images.append(img)
#             self.width += img.get_width()
#                                                 # for each character, it retrieves the corresponding images from the asset and appends it to images list
#                                                 # updates the total width of the score image based on the width of the added image
#         self.height = self.images[0].get_height()# calculates the height of the score image based on the heightof the first centre image
#         self.image = pygame.surface.Surface((self.width, 
#                                              self.height), 
#                                             pygame.SRCALPHA)
#                                                 #creates new surface for the score image 
#         self.rect = self.image.get_rect(center=(configs.screen_width / 2, 50))
#                                                 # basically positioning, centre and 50 pixel top from centre
#         x =0
#         for img in self.images:
#             self.image.blit(img, (x, 0))        # stacks horizontally
#             x += img.get_width()

#     def update(self):
#         self.__create() 