alpha_win = 1
alpha_lose = -1
alpha_draw = 0

impossibly_high = 2000
impossibly_low = -2000
ply_depth = 3
w_ai = 1
opponent = 2

# estimate of a field quality
def state_score(game):
    #EVALUATE_score considers a board more valuable if there are open ended rows
    (white_open, brown_open) = game.evaluate_score()
    (white_score, brown_score) = game.score()
    return white_score - brown_score * 3 - brown_open*2 + white_open


def alpha_beta_pruning(game):
    alpha = impossibly_low
    ply = 1
    best_col = possible_moves(game)[0]

    for col in possible_moves(game):

        possible_game = simulate_game(game, col)
        if possible_game.winner_is() == w_ai:
            return col
        else:
            outcome = min_play(possible_game,ply+1, alpha)

            if outcome > alpha:
                best_col = col
                alpha = outcome
    return best_col

def max_play(game, ply,beta):
    #alpha is the running best alternative for max
    alpha = impossibly_low
    if game.over():
        return state_score(game)

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)
        if possible_game.winner_is() == w_ai:
            return alpha_win

        else:
            if ply >= ply_depth:
                outcome = state_score(possible_game)
            else:
                outcome = min_play(possible_game,ply + 1,alpha)     #min_play returns worst outcome for ai/best outcome for opponent
            if outcome >= beta:                                     #the rest of this parent node's outcomes will be >= to this.. so if another parent node has a lower max outcome there is no point searching further down this node as it won't be chosen by min
                return outcome
            elif outcome > alpha:
                alpha = outcome

    return alpha


def min_play(game,ply,alpha):
    beta = impossibly_high
    if game.over():
        return state_score(game)

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)

        if possible_game.winner_is() == opponent:
            return alpha_lose

        else:
            if ply >= ply_depth:
                outcome = state_score(possible_game)
            else:
                outcome = max_play(possible_game, ply + 1,beta)     #max_play returns best outcome for ai/worst outcome for opponent
            if outcome <= alpha:                                    #min outcome of this parent node will be <= this outcome (can't be more)... so if min of another node is better than this value - don't bother searching any more as you know this node won't be chosen!
                return outcome
            elif outcome < beta:                                    #if this outcome is better than min of other nodes AND it is worse than the other child nodes of this node...
                beta = outcome
    return beta


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
    if sum(game.col_heights) <= 1:
        optmove = 4
    elif sum(game.col_heights) <= 2:
        if game.col_heights[3] > 0:
            optmove = 5
        else:
            optmove = 3
    else:
        optmove = alpha_beta_pruning(game)

    return optmove
