# adventure_functions.py
import os
import pygame
import Configure_The_Simulation as config

def draw_room(screen, row, col):
    left = col * config.ROOM_WIDTH
    right = left + config.ROOM_WIDTH
    top = row * config.ROOM_HEIGHT
    bottom = top + config.ROOM_HEIGHT
    mid_x = (left + right) // 2
    mid_y = (top + bottom) // 2

     #Top wall
    if row == 0:
        pygame.draw.line(screen, config.WALL_COLOR, (left, top), (right, top), config.WALL_THICK)
    else:
        pygame.draw.line(screen, config.WALL_COLOR, (left, top), (mid_x - config.DOOR_SIZE // 2, top), config.WALL_THICK)
        pygame.draw.line(screen, config.WALL_COLOR, (mid_x + config.DOOR_SIZE // 2, top), (right, top), config.WALL_THICK)

    # Bottom wall
    if row == config.GRID_ROWS - 1:
        pygame.draw.line(screen, config.WALL_COLOR, (left, bottom), (right, bottom), config.WALL_THICK)
    else:
        pygame.draw.line(screen, config.WALL_COLOR, (left, bottom), (mid_x - config.DOOR_SIZE // 2, bottom), config.WALL_THICK)
        pygame.draw.line(screen, config.WALL_COLOR, (mid_x + config.DOOR_SIZE // 2, bottom), (right, bottom), config.WALL_THICK)

    # Left wall
    if col == 0:
        pygame.draw.line(screen, config.WALL_COLOR, (left, top), (left, bottom), config.WALL_THICK)
    else:
        pygame.draw.line(screen, config.WALL_COLOR, (left, top), (left, mid_y - config.DOOR_SIZE // 2), config.WALL_THICK)
        pygame.draw.line(screen, config.WALL_COLOR, (left, mid_y + config.DOOR_SIZE // 2), (left, bottom), config.WALL_THICK)

    # Right wall
    #if col == config.GRID_COLS - 1:
        #pygame.draw.line(screen, config.WALL_COLOR, (right, top), (right, bottom), config.WALL_THICK)
    #else:
        #pygame.draw.line(screen, config.WALL_COLOR, (right, top), (right, mid_y - config.DOOR_SIZE // 2), config.WALL_THICK)
        #pygame.draw.line(screen, config.WALL_COLOR, (right, mid_y + config.DOOR_SIZE // 2), (right, bottom), config.WALL_THICK)
    #Puter
    #pygame.draw.rect(screen, (0, 255, 0), (left + 40, top + 40, 40, 30))  # Example computer rectangle


def computer_rect(screen):
    left = 30
    top = 30
    width = 40
    height = 40
    computer_rectangle = pygame.Rect(left, top, width, height)
    pygame.draw.rect(screen, (194, 194, 194), computer_rectangle)  # Draw the computer rectangle
    return computer_rectangle
        


def is_blocked(x, y):
    """Return True if the player is hitting a wall (excluding doors)"""
    for row in range(config.GRID_ROWS):
        for col in range(config.GRID_COLS):
            left = col * config.ROOM_WIDTH
            right = left + config.ROOM_WIDTH
            top = row * config.ROOM_HEIGHT
            bottom = top + config.ROOM_HEIGHT
            mid_x = (left + right) // 2
            mid_y = (top + bottom) // 2

            if left <= x <= right and top <= y <= bottom:
                if x - config.PLAYER_RADIUS < left:
                    #if col == 0 or not (mid_y - config.DOOR_SIZE//2 <= y <= mid_y + config.DOOR_SIZE//2):
                        return True
                if x + config.PLAYER_RADIUS > right:
                    #if col == config.GRID_COLS - 1 or not (mid_y - config.DOOR_SIZE//2 <= y <= mid_y + config.DOOR_SIZE//2):
                        return True
                if y - config.PLAYER_RADIUS < top:
                    #if row == 0 or not (mid_x - config.DOOR_SIZE//2 <= x <= mid_x + config.DOOR_SIZE//2):
                        return True
                if y + config.PLAYER_RADIUS > bottom:
                    #if row == config.GRID_ROWS - 1 or not (mid_x - config.DOOR_SIZE//2 <= x <= mid_x + config.DOOR_SIZE//2):
                        return True
                return False

    return True


'''def draw_obstacle(screen):

    #draws a simple box
    left = 10
    top = 10
    right = 20
    bottom = 20
    pygame.draw.line(screen, config.BOX_COLOR, (left, top), (right, top), config.Box_Thick)
    pygame.draw.line(screen, config.BOX_COLOR, (left, bottom), (right, bottom), config.Box_Thick)
    pygame.draw.line(screen, config.BOX_COLOR, (right, top), (right, bottom), config.Box_Thick)
    pygame.draw.line(screen, config.BOX_COLOR, (left, top), (left, bottom), config.Box_Thick)'''


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


def mini_game(screen):
    while show_mini_game() == True:
        pygame.draw.line(screen, (255, 0, 0), (0, 0), (700, 700), 5)
      


            
def count_objectives(screen):
    dict_objectives = {"objectives_left": 4}
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

    #if mini_game() == False:
    #    dict_objectives["objectives_left"] -= 144
        

    waiting = True
    while waiting:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                waiting = False
    


        