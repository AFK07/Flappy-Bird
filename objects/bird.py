# ### class object for bird
# import pygame.sprite

# import assets   #   error with this aswell
# import configs
# from layer import Layer # error in this line
# from objects.column import Column
# from objects.floor import Floor

# class Bird(pygame.sprite.Sprite):
#     def __init__(self, *groups):
#         self._layer = Layer.player
    
#         self.images = [
#             assets.get_sprite("down"),
#             assets.get_sprite("mid"),
#             assets.get_sprite("up")              # different images 
#         ]

#         self.image = self.images[0]
#         self.rect = self.image.get_rect(topleft=(-50, 50))    # positions it quite to the right side

#         self.mask = pygame.mask.from_surface(self.image)

#         self.flap = 0

#         super().__init__(*groups)


#     def update(self):
#         self.images.insert(0, self.images.pop())
#         self.image = self.images[0]

#         self.flap += configs.gravity            # gravity constantly increases
#         self.rect.y += self.flap

#         if self.rect.x < 50:
#             self.rect.x += 2                    # untill the bird's position hasnt reached the given input(for now 50) from the starting point

#     def handle_event(self, event):
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#             self.flap = 0
#             self.flap -= 6                      # when space is clicked, it will raise its position. speed depends on fps
        
#     def check_collision(self, sprites):
#         for sprite in sprites:
#             if ((type(sprite) is Column or type(sprite) is Floor) and sprite.mask.overlap(self.mask, (
#                     self.rect.x - sprite.rect.x, 
#                     self.rect.y - sprite.rect.y)) or
#                     self.rect.bottom < 0):
#                                                 # masking allows pixel perfection collision detection
#                                                 # this statement identifies the positions of the bird and columns
#                 return True
#         return False