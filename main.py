import pygame
import pygame.sprite
import random     
from enum import IntEnum, auto

# Importing external modules
import configs as configs                       
import assets as assets                         

# --- Layer Definition ---
# Defines the draw order of sprites to ensure UI is always on top
class Layer(IntEnum):
    background = auto()
    obstacle = auto()
    floor = auto()
    player = auto()
    ui = auto()

# --- Sprite Classes ---

class Background(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        super().__init__(*groups)
        self._layer = Layer.background
        self.image = assets.get_sprite("background")
        self.rect = self.image.get_rect(topleft=(configs.screen_width * index, -50))
    
    def update(self):
        self.rect.x -= 1
        if self.rect.right <= 0:
            self.rect.x = configs.screen_width

class Floor(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        super().__init__(*groups)
        self._layer = Layer.floor
        self.image = assets.get_sprite("floor")
        self.rect = self.image.get_rect(bottomleft=(configs.screen_width * index, configs.screen_height))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.rect.x = configs.screen_width

class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = Layer.obstacle
        self.gap = 100
        self.image_base = assets.get_sprite("pipe-green")
        self.sprite_rect = self.image_base.get_rect()

        # Create bottom pipe
        self.pipe_bottom = self.image_base
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprite_rect.height + self.gap))
        
        # Create top pipe by flipping the base image
        self.pipe_top = pygame.transform.flip(self.image_base, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))

        # Assemble the column surface with transparency
        self.image = pygame.surface.Surface((self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap), pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        sprite_floor_height = assets.get_sprite("floor").get_rect().height
        min_y = 100
        max_y = configs.screen_height - sprite_floor_height - 100
        
        self.rect = self.image.get_rect(midleft=(configs.screen_width, random.uniform(min_y, max_y)))
        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False

    def update(self):
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        # Checks if bird has crossed the pipe's x-coordinate
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False

class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = Layer.player
        self.images = [assets.get_sprite("down"), assets.get_sprite("mid"), assets.get_sprite("up")]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(-50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.flap = 0

    def update(self):
        # Cycle through wings animation
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)

        # Apply gravity to vertical velocity
        self.flap += configs.gravity
        self.rect.y += self.flap

        # Initial entrance slide-in
        if self.rect.x < 50:
            self.rect.x += 2

    def handle_event(self, event):
        # Space key jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.jump()
        # Mouse click jump
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.jump()

    def jump(self):
        self.flap = -6
        assets.play_audio("wing")
        
    def check_collision(self, sprites):
        for sprite in sprites:
            if isinstance(sprite, (Column, Floor)):
                # Pixel-perfect collision using masks
                if sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)) or self.rect.bottom < 0 or self.rect.top > configs.screen_height:
                    return True
        return False

class StartMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = Layer.ui
        self.image = assets.get_sprite("start")    
        self.rect = self.image.get_rect(center=(configs.screen_width / 2, configs.screen_height / 2))

class EndMessage(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = Layer.ui
        self.image = assets.get_sprite("over")    
        self.rect = self.image.get_rect(center=(configs.screen_width / 2, configs.screen_height / 2))

class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._layer = Layer.ui
        self.value = 0
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)
        self.__create()

    def __create(self):
        self.str_value = str(self.value)
        self.images = [assets.get_sprite(char) for char in self.str_value]
        self.width = sum(img.get_width() for img in self.images)
        self.height = self.images[0].get_height()
        self.image = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.screen_width / 2, 50))
        
        x = 0
        for img in self.images:
            self.image.blit(img, (x, 0))
            x += img.get_width()

    def update(self):
        self.__create()

# --- Main Game Loop ---

pygame.init()
screen = pygame.display.set_mode((configs.screen_width, configs.screen_height))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

def create_sprites():
    # Initialize game environment
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    return Bird(sprites), StartMessage(sprites), Score(sprites)

bird, start_message, score = create_sprites()

running = True
gameover = False
gamestarted = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Spawn pipes only when game is active
        if event.type == column_create_event and gamestarted and not gameover:
            Column(sprites)

        # Handle Inputs (Space, Mouse, Escape)
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # Logic for starting the game
            if not gamestarted and not gameover:
                gamestarted = True
                start_message.kill()
                pygame.time.set_timer(column_create_event, 1500)
            
            # Logic for jumping while alive
            if gamestarted and not gameover:
                bird.handle_event(event)

            # Logic for restarting after game over
            if gameover:
                # Restart on Space, Escape, or Click
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE)) or event.type == pygame.MOUSEBUTTONDOWN:
                    gameover = False
                    gamestarted = False
                    sprites.empty()
                    bird, start_message, score = create_sprites()

    screen.fill(0)
    
    if gamestarted and not gameover:
        sprites.update()
        
        # Check collision only when game is active
        if bird.check_collision(sprites):
            gameover = True
            EndMessage(sprites)
            pygame.time.set_timer(column_create_event, 0)
            assets.play_audio("hit")

        # Update score logic
        for sprite in sprites:
            if isinstance(sprite, Column) and sprite.is_passed():
                score.value += 1
                assets.play_audio("point")

    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(configs.fps)

pygame.quit()