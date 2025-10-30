def count_objectives(screen):
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