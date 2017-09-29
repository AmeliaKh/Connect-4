impossibly_high = 20000
impossibly_low = -20000

alpha_win = 1
alpha_lose = -1
alpha_draw = 0

w_ai = 1
opponent = 2

# estimate of a field quality
def state_score(game):
    #EVALUATE_score considers a board more valuable if there are open ended rows
    (white_open, brown_open) = game.evaluate_score()
    (white_score, brown_score) = game.score()
    return white_score - brown_score * 3 - brown_open*2 + white_open

def alpha_beta_pruning(game):
    iterations = 1
    max_depth = 1                           #start at max_depth of 2
    max = 4
    column_order = [4,5,3,6,2,7,1,8,0]      #this changes with each iteration

    while max_depth <= max:
        alpha = impossibly_low
        best_col = possible_moves(game)[0]
        # If only one move available: take it
        if len(possible_moves(game)) == 1:
            return possible_moves(game)[0]

        for col in possible_moves(game,column_order):
            possible_game = simulate_game(game, col)

            if possible_game.winner_is()==w_ai:
                return col
            else:
                outcome = min_play(possible_game, alpha,iterations+1,max_depth)
                if outcome == alpha_win:
                    return col

                elif outcome == alpha_lose and max_depth <=2:
                    max = 2

                if outcome > alpha:
                    best_col = col
                    alpha = outcome
        if max_depth <= 6:
            max_depth += 1
            column_order.insert(0, column_order.pop(column_order.index(best_col)))
            # this happens when using iterative deepening because the best column from the last iteration should be investigated first to improve the efficiency of the alpha beta search
        else:
            max_depth += 100

    return best_col


def max_play(game,beta,iterations,max_depth):
    alpha = impossibly_low

    if game.over():
        return state_score(game)

    if len(possible_moves(game)) == 1:
        return possible_moves(game)[0]

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)

        if possible_game.winner_is() == w_ai:
            return alpha_win

        else:
            if iterations >= max_depth:
                outcome = state_score(possible_game)

            else:
                outcome = min_play(possible_game,alpha,iterations+1,max_depth)
            if outcome >= beta:                                                     #max outcome will be >= to this.. so if other node has lower max outcome there is no point searching down this node as it won't be chosen by min
                return outcome
            elif outcome > alpha:
                alpha = outcome

    return alpha


def min_play(game,alpha,iterations,max_depth):
    beta = impossibly_high

    if game.over():
        return state_score(game)

    if len(possible_moves(game)) == 1:
        print('NO option!!')
        return possible_moves(game)[0]

    for col in possible_moves(game):
        possible_game = simulate_game(game, col)

        if possible_game.winner_is() == opponent:
            return alpha_lose

        else:
            if iterations >= max_depth:
                outcome = state_score(possible_game)
            else:
                outcome = max_play(possible_game,beta,iterations+1,max_depth)       # max_play returns best outcome for ai/worst outcome for opponent
            if outcome <= alpha:                                                    # min outcome of this parent node will be <= this outcome (can't be more)... so if min of another node is better than this value - don't bother searching any more as you know this node won't be chosen
                return outcome
            elif outcome < beta:                                                    #if this outcome is better than min of other nodes AND it is worse than the other child nodes of this node...
                beta = outcome
    return beta


def simulate_game(game, col):
    copied_game = game.copy()
    copied_game.attempt_insert(col)
    return copied_game


def possible_moves(game, column_order = [4,5,3,6,2,7,1,8,0]):
    possible_moves_list = []
    for col in column_order:
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