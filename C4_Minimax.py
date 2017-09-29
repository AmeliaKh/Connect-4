#ai win = 1
#ai lose = -1
#ai draw = 0

opponent = 1
b_ai = 2
impossibly_high = 2000
impossibly_low = -2000

# estimate of a field quality
def state_score(game):
    # EVALUATE_score considers a board more valuable if there are open ended rows
    (white_open, brown_open) = game.evaluate_score()
    (white_score, brown_score) = game.score()
    return brown_open - white_score * 3 - white_open*2 + brown_open

def minimax(game,ply):
    best_col = possible_moves(game)[0]
    best_outcome = impossibly_low

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)

        outcome = min_play(possible_game,ply + 1)           #min_play returns worst outcome for ai/best outcome for opponent

        if outcome >= best_outcome:
            best_outcome = outcome
            best_col = col

    return best_col

def max_play(game, ply):
    best_outcome = impossibly_low

    if game.over():
        return state_score(game)

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)

        if ply >= 3:
                outcome = state_score(possible_game)
        else:
            outcome = min_play(possible_game,ply + 1)

        if outcome >= best_outcome:
            best_outcome = outcome

    return best_outcome


def min_play(game,ply):
    worst_outcome = impossibly_high

    if game.over():
        return state_score(game)

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)
        if ply >= 3:
                outcome = state_score(possible_game)
        else:
            outcome = max_play(possible_game, ply + 1)      #max _play returns best outcome for ai/worst outcome for opponent
        if outcome <= worst_outcome:
            worst_outcome = outcome

    return worst_outcome


def simulate_game(game, col):
    copied_game = game.copy()
    copied_game.attempt_insert(col)
    return copied_game


def possible_moves(game):
    possible_moves_list = []
    for col in [4,5,3,6,2,7,1,8,0]:
        if game.col_heights[col]<game.field_height:
            possible_moves_list.append(col)
    return possible_moves_list

def AIcheck(game):
    ply = 1
    if sum(game.col_heights) <= 2:
        optmove = 4
    elif sum(game.col_heights) <= 4:
        if game.col_heights[3] > 0:
            optmove = 5
        else:
            optmove = 3
    else:
        optmove = minimax(game, ply)

    return optmove
