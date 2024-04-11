import pygame
import random     
from enum import IntEnum, auto                  # layers
import configs as configs                       # configuraiton settings for the game                  
import assets as assets
import pygame.sprite


class Background(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        super().__init__(*groups)
        self._layer = Layer.background          # make sure to understand how the layers work on each class functions
        self.image = assets.get_sprite("background")   # gets the image for the background from the assets using the image name
        self.rect = self.image.get_rect(topleft=(configs.screen_width * index, -50)) #sets the position of the image. Right now, top left of the screen
    
    def update(self):
        self.rect.x -= 1                        # speed of the image slide

        if self.rect.right <= 0:
            self.rect.x = configs.screen_width



class Floor(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        self._layer = Layer.floor
        self.image = assets.get_sprite("floor")    # i am just using random images i have in the folder at the moment
        self.rect = self.image.get_rect(bottomleft = (configs.screen_width * index, configs.screen_height))

        self.mask = pygame.mask.from_surface(self.image)



        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2

        if self.rect.right <= 0:
            self.rect.x = configs.screen_width


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
        if self.rect.x < 50 and self.passed:
            self.passed = True
            return True
        return False



class Layer(IntEnum):
    background = auto()
    obstacle = auto()
    floor = auto()
    player = auto()
    ui = auto()



class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.player

        self.images = [
            assets.get_sprite("down"),
            assets.get_sprite("mid"),
            assets.get_sprite("up")              # different images 
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(-50, 50))    # positions it quite to the right side

        self.mask = pygame.mask.from_surface(self.image)

        self.flap = 0

        super().__init__(*groups)


    def update(self):
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]

        self.flap += configs.gravity            # gravity constantly increases
        self.rect.y += self.flap

        if self.rect.x < 50:
            self.rect.x += 2                    # untill the bird's position hasnt reached the given input(for now 50) from the starting point

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.flap = 0
            self.flap -= 6                      # when space is clicked, it will raise its position. speed depends on fps
        
    def check_collision(self, sprites):
        for sprite in sprites:
            if ((type(sprite) is Column or type(sprite) is Floor) and sprite.mask.overlap(self.mask, (
                    self.rect.x - sprite.rect.x, 
                    self.rect.y - sprite.rect.y)) or
                    self.rect.bottom < 0):
                                                # masking allows pixel perfection collision detection
                                                # this statement identifies the positions of the bird and columns
                return True
        return False




pygame.init()                                   # initialises pygame          

screen = pygame.display.set_mode((configs.screen_width, 
                                  configs.screen_height)) # dimensions are fetched from configs.py file


clock = pygame.time.Clock()                     # controls the frame rate of the game
running = True                                  # controls the main game loop
gameover = False
score = 0

column_create_event = pygame.USEREVENT          # a constant that represent a custom event type
# used to create a custm event identifier that you can later use to trugger and handle custom event in your pygame program
assets.load_sprites()                           # loads the images from assets
sprites = pygame.sprite.LayeredUpdates()        # to hold all sprites in the game


Background(0, sprites)
Background(1, sprites)                          # creates the instance of class Background

Floor(0, sprites)
Floor(1, sprites)

bird = Bird(sprites)
# Column(sprites)

pygame.time.set_timer(column_create_event, 1500)# the counter that calls column_create_event

while running:                                  # runs until the running variable is set to False
    for event in pygame.event.get():            # this loop waits for any keys clicked by the user
        if event.type == pygame.QUIT:           # incase the user clicks the quit button
            running = False                     # applied if user quits
        if event.type == column_create_event:
            Column(sprites)                     # as seen in the above code, as long as the game runs, this statement repeatedly generates columns 
                                                # depending on the counter timer(currently 1500 milliseconds)
        bird.handle_event(event)                # calls up the flap function

    screen.fill(0)                              # window colour
    
    sprites.draw(screen)                        # renders the images
    
    if not gameover:
        sprites.update()


    if bird.check_collision(sprites):           # checks collisions
        gameover = True

    # for sprite in sprites:
    #     if type(sprite) is Column and sprite.is_passed():
    #         score += 1
    # print(score)

    pygame.display.flip()                       # updates the content of the display
    
    clock.tick(configs.fps)                     # limits the frame rate

pygame.quit()                                   # closing function