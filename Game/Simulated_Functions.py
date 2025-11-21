# adventure_functions.py
import os
import pygame
import Configure_The_Simulation as config
import random

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "Music")
IMG_DIR   = os.path.join(ASSETS_DIR, "Images")

def asset_path(*parts):
    """Build full path inside assets folder."""
    return os.path.join(ASSETS_DIR, *parts)


def draw_layout(screen, wall_color, wall_thickness):
    # Draw the layout of the room with walls and obstacles
    screen.fill((50, 50, 50))  # Fill background with dark gray

    # Draw walls
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 0, config.WIDTH, wall_thickness))  # Top wall
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, config.HEIGHT - wall_thickness, config.WIDTH, wall_thickness))  # Bottom wall
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 0, wall_thickness, config.HEIGHT))  # Left wall
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(config.WIDTH - wall_thickness, 0, wall_thickness, config.HEIGHT))  # Right wall

#INNER OBSTACLES
    # 4. Left side pillar
    wall_1_rect = pygame.draw.rect(screen, config.wall_color, pygame.Rect(80, 0, 20, 200))




def computer_rect(screen):
    left = 30
    top = 30
    width = 40
    height = 40
    computer_rectangle = pygame.Rect(left, top, width, height)
    pygame.draw.rect(screen, (194, 194, 194), computer_rectangle)  # Draw the computer rectangle
    return computer_rectangle
        


def is_blocked(x, y):
    if x - config.PLAYER_RADIUS < 0: return True
    if x + config.PLAYER_RADIUS > config.WIDTH: return True
    if y - config.PLAYER_RADIUS < 0: return True
    if y + config.PLAYER_RADIUS > config.HEIGHT: return True
    return False






_player_image = None
_warned_once = False


def load_player_image():
    """Call once at startup after pygame.init()."""

    global _player_image, _warned_once
    _player_image = None  # default

    path = getattr(config, "PLAYER_IMAGE_PATH", None)
    size = getattr(config, "PLAYER_IMAGE_SIZE", None)

    if path and os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        _player_image = img
    else:
        if not _warned_once:
            print("No player image found or PLAYER_IMAGE_PATH not set; using circle.")
            _warned_once = True

def draw_player(screen, x, y):
    """Draw sprite centered at (x, y); fall back to circle if no image."""
    if _player_image:
        player_rect = _player_image.get_rect(center=(int(x), int(y)))
        screen.blit(_player_image, player_rect.topleft)
        return player_rect
    else:
        pygame.draw.circle(screen, config.PLAYER_COLOR, (int(x), int(y)), config.PLAYER_RADIUS)
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), config.PLAYER_RADIUS, 2)
        return player_rect

def show_game_over(screen):
    """Draw a Game Over box in the center of the screen."""
    font = pygame.font.Font(None, 72)  # default font, large size
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))

    # Draw a semi-transparent dark box behind the text
    box_width = text_rect.width + 40
    box_height = text_rect.height + 40
    box_surface = pygame.Surface((box_width, box_height))
    box_surface.set_alpha(180)  # transparency
    box_surface.fill((0, 0, 0))
    box_rect = box_surface.get_rect(center=text_rect.center)

    # Blit box then text
    screen.blit(box_surface, box_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Pause to let player see the message
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

# Pulls up a black screen over the whole screen for the mini-game
def show_mini_game(screen):
    #sets the dimensions and color of the mini-game screen
    mini_game_width = 700
    mini_game_height = 700
    mini_game_surface = pygame.Surface((mini_game_width, mini_game_height))
    mini_game_surface.fill((0, 0, 0))  # Creates black background
    mini_game_rect = mini_game_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2)) # Sets location of the black box

    screen.blit(mini_game_surface, mini_game_rect) # Puts the black box on the screen
    pygame.display.flip() # Updates the display to show the mini-game screen

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.KEYDOWN: # Waits for a key press to exit the mini-game screen.
                waiting = False


#def mini_game(screen):
    #while show_mini_game(screen) == True:
        #is_blocked() == False
        #draw_player() == False

      


            
def count_objectives(screen):
    #dict_objectives = {"objectives_left": 4}
    font = pygame.font.Font(None, 25)  # default font, large size
    objective_text = font.render("Objectives Left: 4", True, (255, 255, 255)) # Renders text in the game with (color) 
    ob_text_rect = objective_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2)) #Center, defines where the center of the rectangle will lie and the second half finds the center of the game screen based on it's dimensions

    objective_box_width = ob_text_rect.width + 40 
    objective_box_height = ob_text_rect.height + 40
    objective_box_surface = pygame.Surface((objective_box_width, objective_box_height))
    objective_box_surface.set_alpha(180)
    objective_box_surface.fill((0, 0, 0))
    objective_box_rect = objective_box_surface.get_rect(center=ob_text_rect.center)

    screen.blit(objective_box_surface, objective_box_rect)
    screen.blit(objective_text, ob_text_rect)
    pygame.display.flip()
        
    waiting = True
    while waiting:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                waiting = False
    


        '''# Enemy Systems    
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 150
        self.color = (255, 0, 0)
        self.size = 24
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move = move

    
def spawn_enemies(num_enemies):
    """Return a list of new enemies."""
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(10, config.WIDTH - 30)
        y = random.randint(10, config.HEIGHT - 30)
        enemies.append(Enemy(x, y))
    return enemies

def draw_enemy(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

def move(self):
        """Simple random bouncing movement."""
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Bounce off walls (stay inside screen)
        if self.x < self.size or self.x > config.WIDTH - self.size:
            self.direction = (-self.direction[0], self.direction[1])
        if self.y < self.size or self.y > config.HEIGHT - self.size:
            self.direction = (self.direction[0], -self.direction[1])
'''