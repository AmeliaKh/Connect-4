import pygame

# This module takes care of the graphical interface: drawing the shapes and
# printing the text that together make the game window.

# display constants (these are not crucial to the game or pygame)
fontsize = 24
cell_size = 60
offset_canvas = 60
top_offset = 24
bottom_spacing = 64

# colour constants
BLACK  = (13,161,146)   #lines = dark blue
WHITE  = (13,161,146)
RED    = (242,235,211)  #token = cream
BLUE   = (105,97,87)    #token = brown
YELLOW = (19,189,172)   #background = bluish

def setup_display(field_width, field_height):
    window_width = 2 * offset_canvas + field_width * cell_size
    window_height = 2 * offset_canvas + top_offset + bottom_spacing + field_height * cell_size
    display = pygame.display.set_mode((window_width, window_height), 0, 32)
    pygame.display.set_caption('Connect FOUR')
    gamefont = pygame.font.Font(None, fontsize)
    return (display, gamefont)

def draw_arrow(display, column):
    top_point = (offset_canvas + cell_size / 2 + cell_size * column,
                 offset_canvas -40)
    bottom_point = (offset_canvas + cell_size / 2 + cell_size * column,
                    offset_canvas + top_offset * 3 / 4 -30)
    left_point = (offset_canvas + 3 * cell_size / 8 + cell_size * column -10,
                  offset_canvas + top_offset / 2 -35)
    right_point = (offset_canvas + 5 * cell_size / 8 + cell_size * column +10,
                   offset_canvas + top_offset / 2 -35)
    pygame.draw.line(display, BLACK, left_point, bottom_point, 6)
    pygame.draw.line(display, BLACK, right_point, bottom_point, 6)
    pygame.draw.line(display, BLACK, top_point, bottom_point, 6)


def draw_board(game_display,
        field_state, field_width, field_height, score_red, score_blue,
        selected_index, game_running, player_turn, red_turn, winner):
    (display, gamefont) = game_display
    display.fill(YELLOW)

    # draw border
    pygame.draw.rect(display, BLACK,
            (offset_canvas-20,
             offset_canvas + top_offset-20,
             field_width * cell_size+40,
             field_height * cell_size +40
            ),
            10)

    # draw all tokens and circles
    for j in range(field_height):
        for i in range(field_width):
            xc = offset_canvas + cell_size / 2 + i * cell_size
            yc = offset_canvas + top_offset + cell_size / 2 + (field_height - j - 1) * cell_size
            if field_state[i][j] == 1:
                pygame.draw.circle(display, RED, (int(xc), int(yc)), int(cell_size * 2 / 5), 0)
            if field_state[i][j] == 2:
                pygame.draw.circle(display, BLUE, (int(xc), int(yc)), int(cell_size * 2 / 5), 0)
            pygame.draw.circle(display, BLACK, (int(xc), int(yc)), int(cell_size * 2 / 5)+1, 2)

    # display players' score
    red_score_surf = gamefont.render('WHITE: ' + str(score_red), False, RED)
    blue_score_surf = gamefont.render('BROWN: ' + str(score_blue), False, BLUE)
    score_x = offset_canvas
    score_y = 2 * offset_canvas + top_offset + field_height * cell_size
    display.blit(red_score_surf, (score_x, score_y))
    display.blit(blue_score_surf, (score_x, score_y + fontsize))

    # potentially display arrow
    if selected_index >= 0 and game_running and player_turn:
        draw_arrow(display, selected_index)
    # is it the AI player's turn?
    if game_running:
        if red_turn:
            thinking_surf = gamefont.render("White playing...", False, RED)
        else:
            thinking_surf = gamefont.render("Brown playing...", False, BLUE)
        display.blit(thinking_surf, (offset_canvas + 3 * cell_size, 2 * offset_canvas + top_offset + field_height * cell_size))

    if not(game_running):
        draw_winners(display, gamefont, winner)

def draw_winners(display, gamefont, winner):
    if winner == 0:
        win_surf = gamefont.render("DRAW!", False, BLACK)
    elif winner == 1:
        win_surf = gamefont.render("WHITE WINS!", False, RED)
    else:
        win_surf = gamefont.render("BROWN WINS!", False, BLUE)
    display.blit(win_surf, (offset_canvas, offset_canvas / 2))

# check whether a column is selected
def cursor_check(field_width, field_height):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    if (mouse_x >= offset_canvas \
       and mouse_x < offset_canvas + field_width * cell_size \
       and mouse_y >= offset_canvas + top_offset \
       and mouse_y <= offset_canvas + top_offset + field_height * cell_size):
        # The player clicked on a column, not outside
        return int((mouse_x - offset_canvas) / cell_size)
    else:
        # `-1` is the indicator that nothing has been selected
        return -1

