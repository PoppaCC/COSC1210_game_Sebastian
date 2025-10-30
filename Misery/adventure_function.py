
import os
import pygame
import Config



def draw_room(screen, row, col):
    left = col * Config.ROOM_WIDTH
    right = left + Config.ROOM_WIDTH
    top = row * Config.ROOM_HEIGHT
    bottom = top + Config.ROOM_HEIGHT
    mid_x = (left + right) // 2
    mid_y = (top + bottom) // 2

      #Top wall
    if row == 0:
        pygame.draw.line(screen, Config.WALL_COLOR, (left, top), (right, top), Config.WALL_THICK)
    else:
        pygame.draw.line(screen, Config.WALL_COLOR, (left, top), (mid_x - Config.DOOR_SIZE // 2, top), Config.WALL_THICK)
        pygame.draw.line(screen, Config.WALL_COLOR, (mid_x + Config.DOOR_SIZE // 2, top), (right, top), Config.WALL_THICK)

    # Bottom wall
    if row == Config.GRID_ROWS - 1:
        pygame.draw.line(screen, Config.WALL_COLOR, (left, bottom), (right, bottom), Config.WALL_THICK)
    else:
        pygame.draw.line(screen, Config.WALL_COLOR, (left, bottom), (mid_x - Config.DOOR_SIZE // 2, bottom), Config.WALL_THICK)
        pygame.draw.line(screen, Config.WALL_COLOR, (mid_x + Config.DOOR_SIZE // 2, bottom), (right, bottom), Config.WALL_THICK)

    # Left wall
    if col == 0:
        pygame.draw.line(screen, Config.WALL_COLOR, (left, top), (left, bottom), Config.WALL_THICK)
    else:
        pygame.draw.line(screen, Config.WALL_COLOR, (left, top), (left, mid_y - Config.DOOR_SIZE // 2), Config.WALL_THICK)
        pygame.draw.line(screen, Config.WALL_COLOR, (left, mid_y + Config.DOOR_SIZE // 2), (left, bottom), Config.WALL_THICK)

    # Right wall
    if col == Config.GRID_COLS - 1:
        pygame.draw.line(screen, Config.WALL_COLOR, (right, top), (right, bottom), Config.WALL_THICK)
    else:
        pygame.draw.line(screen, Config.WALL_COLOR, (right, top), (right, mid_y - Config.DOOR_SIZE // 2), Config.WALL_THICK)
        pygame.draw.line(screen, Config.WALL_COLOR, (right, mid_y + Config.DOOR_SIZE // 2), (right, bottom), Config.WALL_THICK)

_player_image = None
_warned_once = False

def load_player_image():
    global _player_image, _warned_once
    _player_image = None  # default

    path = getattr(Config, "PLAYER_IMAGE_PATH", None)
    size = getattr(Config, "PLAYER_IMAGE_SIZE", None)

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
    if _player_image:
        rect = _player_image.get_rect(center=(int(x), int(y)))
        screen.blit(_player_image, rect.topleft)
    else:
        pygame.draw.circle(screen, Config.PLAYER_COLOR, (int(x), int(y)), Config.PLAYER_RADIUS)
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), Config.PLAYER_RADIUS, 2)

def show_game_over(screen):
    """Draw a Game Over box in the center of the screen."""
    font = pygame.font.Font(None, 72)  # default font, large size
    text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))

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
