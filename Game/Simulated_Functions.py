# Simulated_Functions.py
import os
import pygame
import Configure_The_Simulation as config
import random

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
MUSIC_DIR = os.path.join(ASSETS_DIR, "Music")
IMG_DIR   = os.path.join(ASSETS_DIR, "Images")

enemy_image_vertical = None
enemy_image_horizontal = None

def get_outer_walls():
    """Return ONLY the outer boundary walls."""
    return [
        pygame.Rect(0, 0, config.WIDTH, config.wall_thickness),  # Top
        pygame.Rect(0, config.HEIGHT - config.wall_thickness, config.WIDTH, config.wall_thickness),  # Bottom
        pygame.Rect(0, 0, config.wall_thickness, config.HEIGHT),  # Left
        pygame.Rect(config.WIDTH - config.wall_thickness, 0, config.wall_thickness, config.HEIGHT)  # Right
    ]

def get_default_inner_walls():
    """Return ONLY the default inner walls (not including borders)."""
    return [
        pygame.Rect(80, 0, 20, 200),
        pygame.Rect(200, 400, 20, 200),
        pygame.Rect(320, 0, 20, 200),
        pygame.Rect(440, 400, 20, 200),
        pygame.Rect(400, 300, 200, 20),
        pygame.Rect(0, 300, 200, 20)
    ]

def asset_path(*parts):
    """Build full path inside assets folder."""
    return os.path.join(ASSETS_DIR, *parts)


def draw_layout(screen, wall_color, wall_thickness):
    """Return default walls WITHOUT drawing them."""

    walls = []

    # Outer walls
    walls.append(pygame.Rect(0, 0, config.WIDTH, wall_thickness))  # Top
    walls.append(pygame.Rect(0, config.HEIGHT - wall_thickness, config.WIDTH, wall_thickness))  # Bottom
    walls.append(pygame.Rect(0, 0, wall_thickness, config.HEIGHT))  # Left
    walls.append(pygame.Rect(config.WIDTH - wall_thickness, 0, wall_thickness, config.HEIGHT))  # Right

    # Inner walls
    inner = [
        pygame.Rect(80, 0, 20, 200),
        pygame.Rect(200, 400, 20, 200),
        pygame.Rect(320, 0, 20, 200),
        pygame.Rect(440, 400, 20, 200),
        pygame.Rect(400, 300, 200, 20),
        pygame.Rect(0, 300, 200, 20)
    ]

    walls.extend(inner)
    return walls



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
    """Draw sprite centered at (x, y); returns player rect for collision."""
    if _player_image:
        rect = _player_image.get_rect(center=(int(x), int(y)))
        screen.blit(_player_image, rect)
        return rect

    # fallback circle with rect
    rect = pygame.Rect(
        int(x - config.PLAYER_RADIUS),
        int(y - config.PLAYER_RADIUS),
        config.PLAYER_RADIUS * 2,
        config.PLAYER_RADIUS * 2
    )
    pygame.draw.circle(screen, config.PLAYER_COLOR, rect.center, config.PLAYER_RADIUS)
    pygame.draw.circle(screen, (0, 0, 0), rect.center, config.PLAYER_RADIUS, 2)
    return rect

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

            
def count_objectives(screen, remaining):
    font = pygame.font.Font(None, 25)
    objective_text = font.render(f"Computers Left: {remaining}", True, (255, 255, 255))
    ob_text_rect = objective_text.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))

    box_width = ob_text_rect.width + 40
    box_height = ob_text_rect.height + 40
    box_surface = pygame.Surface((box_width, box_height))
    box_surface.set_alpha(180)
    box_surface.fill((0, 0, 0))
    box_rect = box_surface.get_rect(center=ob_text_rect.center)

    screen.blit(box_surface, box_rect)
    screen.blit(objective_text, ob_text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                waiting = False
    
class Enemy:
    def __init__(self, x, y, movement="vertical", speed=200, size=(55,55)):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.axis = movement           # "vertical" or "horizontal"
        self.sprite_axis = movement    # used for image selection
        self.direction = 1             # 1 or -1

    def update(self, dt, walls):
        """Move enemy along its axis and reverse if hitting walls."""
        if self.axis == "vertical":
            new_y = self.y + self.speed * self.direction * dt
            future = pygame.Rect(self.x, new_y, self.size[0], self.size[1])
            if any(future.colliderect(w) for w in walls):
                self.direction *= -1
            else:
                self.y = new_y
        else:  # horizontal
            new_x = self.x + self.speed * self.direction * dt
            future = pygame.Rect(new_x, self.y, self.size[0], self.size[1])
            if any(future.colliderect(w) for w in walls):
                self.direction *= -1
            else:
                self.x = new_x

    def draw(self, screen):
        """Draw enemy using its image or fallback rectangle."""
        global enemy_image_vertical, enemy_image_horizontal
        if self.sprite_axis == "vertical" and enemy_image_vertical:
            screen.blit(enemy_image_vertical, (self.x, self.y))
        elif self.sprite_axis == "horizontal" and enemy_image_horizontal:
            screen.blit(enemy_image_horizontal, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 50, 50), pygame.Rect(self.x, self.y, self.size[0], self.size[1]))

    @staticmethod
    def load_images(vertical_path, horizontal_path, size):
        """Load enemy images safely."""
        global enemy_image_vertical, enemy_image_horizontal

        if os.path.exists(vertical_path):
            img = pygame.image.load(vertical_path).convert_alpha()
            enemy_image_vertical = pygame.transform.smoothscale(img, size)
        else:
            print(f"[Warning] Vertical enemy image not found: {vertical_path}")

        if os.path.exists(horizontal_path):
            img = pygame.image.load(horizontal_path).convert_alpha()
            enemy_image_horizontal = pygame.transform.smoothscale(img, size)
        else:
            print(f"[Warning] Horizontal enemy image not found: {horizontal_path}")