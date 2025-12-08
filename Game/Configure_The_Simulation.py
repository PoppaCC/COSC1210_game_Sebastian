# config.py
from Simulated_Functions import asset_path

# Grid and Room Settings
ROOM_WIDTH = 600
ROOM_HEIGHT = 600
wall_color = (100, 100, 100)
wall_thickness = 20


# Player Settings
PLAYER_RADIUS = 10
PLAYER_SPEED = 200

# Screen Size
WIDTH = ROOM_WIDTH
HEIGHT = ROOM_HEIGHT

# Colors (R, G, B)
BG_COLOR = (119, 85, 138)
PLAYER_COLOR = (100, 200, 255)
BOX_COLOR = (194,194,194)

# Frames Per Second
FPS = 60

# Player appearance 
PLAYER_IMAGE_PATH = asset_path("Images", "Character2.png.png")        # transparent PNG, e.g. 48x48
PLAYER_IMAGE_SIZE = (55, 55)             # w, h in pixels
PLAYER_RADIUS = 24                       # half of width; used by your collision

# Player Health and Objectives
MAX_HEALTH = {3}
Objectives_left = 4

