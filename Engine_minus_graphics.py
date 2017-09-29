# import all of the necessary libraries
import sys
import copy
import time

import pdb
# import helper libraries
import ConnectFourGraphics

white = 1
brown = 2
blank = 0

    #takes col and row and returns colour of token at index

    #takes col and row and returns colour of token in inputted direction
def other_token(token):
    if token == white:
        return brown
    else:
        return white


class ConnectFour:


    # The `__init__` method is called to initialise the `ConnectFour` game.
    # It is called automatically when a call `app = ConnectFour()` is made.
    def __init__(self,
            set_width = 9, set_height = 8,
            set_rewards =  [0.000002,0.0001,1,1,1,1,1,1,1], #[0, 1, 2, 4, 8, 16, 32, 64, 128],
            set_winscore = 1,
            set_white_player = None,
            set_brown_player = None,
            set_ai_delay = 10
            ):

        ## game constants
        self.field_width = set_width
        self.field_height = set_height
        self.rewards = set_rewards

        self.score_win = set_winscore

        ### PLAYER SETTINGS ###
        self.white_player = set_white_player
        self.brown_player = set_brown_player
        self.ai_delay = set_ai_delay

        ## state of the game (board, scoreboard, etc.)
        self.field_state =  [[0, 0, 0, 0, 0, 0, 0, 0], # each mini list represents a column
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]]
        #same as:

        self.col_heights = [0] * self.field_width
        self.score_white = 0
        self.score_brown = 0
        self.winner = 0
        self.game_running = True
        self.white_turn = True
        if self.white_player is None:
            self.player_turn = True
        else:
            self.player_turn = False

        ## interface
        self.selected_index = -1

    def copy(self):
        newself = ConnectFour()
        newself.field_state = copy.deepcopy(self.field_state)
        newself.col_heights = copy.deepcopy(self.col_heights)
        newself.field_width = copy.deepcopy(self.field_width)
        newself.field_height = copy.deepcopy(self.field_height)
        newself.white_turn = self.white_turn
        return newself


    def draw(self):
        # A wrapper around the `ConnectFourGraphics.draw_board` function that picks all
        # the right components of `self`.
        ConnectFourGraphics.draw_board(self.DISPLAY,
                self.field_state, self.field_width, self.field_height,
                self.score_white, self.score_brown,
                self.selected_index, self.game_running,
                self.player_turn, self.white_turn, self.winner)


    # current player attempts to insert into a column
    def attempt_insert(self, col):
        # is it possible to insert into this column?
        if self.col_heights[col] < self.field_height:
            row = self.col_heights[col] #the row is the height of the column + 1 (but as heights don't start at 0, dont need to add one)

            # add a token in the selected column
            if self.white_turn:
                self.field_state[col][row] = 1
                if self.brown_player is None:    #if white is playing check if brown is an ai -- brown is an ai if self.brown_player is NOT None
                    self.player_turn = True     #if brown is HUMAN then set player_turn to True -> can play human turn
                else:
                    self.player_turn = False
            else:
                self.field_state[col][row] = 2
                if self.white_player is None:
                    self.player_turn = True
                else:
                    self.player_turn = False
            self.col_heights[col] += 1

            # who is playing next?
            self.white_turn = not(self.white_turn)

            # is the game over?
            if self.over():
                self.set_winner()

        # else do nothing: this forces the player to choose again

    def game_loop(self):
        n_moves_w = -2     #number of moves made by white (start as -2 to ignore first two random moves!
        n_moves_b = -2
        time_w = 0  #total time taken by white... and brown
        time_b = 0
        while self.game_running:
            # Let the AI play if it's its turn
            if not self.player_turn:
                if self.white_turn:
                    start_time = time.time()
                    move = self.white_player(self)
                    time_w += (time.time()-start_time)
                    n_moves_w+=1
                    print('White move: ', move)
                else:
                    start_time = time.time()
                    move = self.brown_player(self)
                    time_b += (time.time()-start_time)
                    n_moves_b +=1
                    print('Brown move: ',move)
                self.attempt_insert(move)
                if sum(self.col_heights) >= 6:
                    if self.over():
                        self.set_winner()





        if self.score_brown>self.score_white:
            winner = 'b'
        elif self.score_brown<self.score_white:
            winner = 'w'
        else: winner = 'none!'
        print('SCORES  WHITE:  ', self.score_white, ' BROWN:  ', self.score_brown)
        print('AVERAGE TIME TAKEN  WHITE:  ',(time_w/n_moves_w),' BROWN:  ',(time_b/n_moves_b))

        file = open("times_wins.txt", "a")
        file.write("winner:")
        file.write(winner)
        file.write("  time w : b --   ")

        file.write(str(round((time_w/n_moves_w),4)))
        file.write(' : ')
        file.write(str(round((time_b/n_moves_b),4)))
        file.write('              ')



        file.close()


    def calculate_points(self,n_of_tokens_in_row):
        return self.rewards[n_of_tokens_in_row - 2]

    def score_list(self,list):
        #take list and score it using REWARDS!! ONLY considers 3 in a rows good if there is no gap between them!!
        white_ = 0
        brown_ =0
        n_of_browns_in_row = 1
        n_of_whites_in_row = 1
        for (index, token) in enumerate(list):
            if index+1<len(list):
                next_token = list[index+1]
                if token == 0:
                    pass

                elif next_token == token:
                    if token == 1:
                        n_of_whites_in_row+=1

                    if token == 2:
                        n_of_browns_in_row +=1

                elif next_token != token and (n_of_browns_in_row>1 or n_of_whites_in_row>1):
                    if token == 1:
                        white_ += self.rewards2[n_of_whites_in_row - 1]
                        n_of_whites_in_row = 1
                    elif token == 2:
                        brown_ += self.rewards[n_of_browns_in_row - 1]
                        n_of_browns_in_row = 1

            #if index is going off screen (ie not a token and not on board) if there is a row of browns or whites: add its score!
            elif n_of_browns_in_row>1 or n_of_whites_in_row>1:
                if token == 1:
                    white_+= self.rewards2[n_of_whites_in_row - 1]
                    n_of_whites_in_row = 1
                elif token == 2:
                    brown_+= self.rewards[n_of_browns_in_row - 1]
                    n_of_browns_in_row = 1

        return(white_,brown_)

    def score_list2(self,list):
        #JUST CHECKS FOR  - 4 - IN A ROW
        white_ = 0
        brown_ = 0
        for start_index in range(len(list)-4+1):
            token = list[start_index+1]
            if token!= 0:
                items = [list[start_index],list[start_index+1], list[start_index+2],list[start_index+3]]
                if all(x == token for x in items):
                    if token == 1:
                        white_+= 1
                    else: brown_ +=1

        return (white_,brown_)

    def score(self):
        #ONLY gives points for - 4 - in a row!!
        final_white = 0
        final_brown=0
        #Check rows
        for row in range(self.field_height):
            row_list = self.make_row_list(row)
            if sum(row_list) >=4:
                white1,brown1 = self.score_list2(row_list)
                final_white += white1
                final_brown += brown1

        #Check columns
        for col in self.field_state:
            if sum(col) >= 4:
                white2,brown2 = self.score_list2(col)
                final_white +=white2
                final_brown +=brown2

        right_diagonal_start_col = [0]*self.field_height+[x for x in range(1,8)]
        right_diagonal_start_row = [x for x in range(7,0,-1)]+[0]*self.field_height
        right_diagonal_zipped = zip(right_diagonal_start_col,right_diagonal_start_row)

        left_diagonal_start_col = [8]*self.field_height+[x for x in range(7,-1,-1)]
        left_diagonal_start_row = [x for x in range(7,-1,-1)]+[0]*self.field_height
        left_diagonal_zipped = zip(left_diagonal_start_col,left_diagonal_start_row)

        #Check right diagonals
        for coordinates in right_diagonal_zipped:
            right_diagonal_list = self.make_diagonal_right_list(coordinates)
            white3,brown3 = self.score_list2(right_diagonal_list)
            final_white+=white3
            final_brown+=brown3
            # coordinates is just the coordinate of each of the starting points of each diagonal
            # -> the make_diagonal method takes each start point and generates a list of tokens in the diagonal
            # -> the score_list method then updates white and brown scores based on pairs in the diagonal


        #Check left diagonals
        for coordinates in left_diagonal_zipped:
            left_diagonal_list = self.make_diagonal_left_list(coordinates)
            white4,brown4 = self.score_list2(left_diagonal_list)
            final_white+=white4
            final_brown+=brown4

        #returns whitescore,brownscore
        return (final_white, final_brown)


        '''
        #count number of whites and browns
        white = 0     #whites are 1
        brown = 0    #browns are 2

        for col in range(self.field_width):
            white += field[col].count(1)
            brown += field[col].count(2)
        '''
        #1. Do Horizontal:
        #   for each column for each token: check colour, if white: check if there is a white next to it: if so add 1 to number_of_tokens_in_row
        #                                                                                          else: add check its score value and add to score_white
        #   make a method which returns colour of token in inputted direction
    def eval(self,list):
        #returns score of lists containing a potential winning row -> more points for rows containing 3s than 2s and more for 4s than 3s!
        white_ = 0
        brown_ = 0
        for start_index in range(len(list)-4+1):
            #ONLY WORKS FOR WHITE!!
            #For each row of 4 tokens -> if all tokens are white or none -> count up how many whites there are
            #                                                          -> score using rewards at the top
            items = [list[start_index], list[start_index + 1], list[start_index + 2], list[start_index + 3]]
            if sum(items) >=2:
                if all(token == white or token == blank for token in items):
                    whites = sum(token == white for token in items)
                    white_ += self.calculate_points(whites)

                elif all(token == brown or token == blank for token in items) and sum(items)>=4:
                    browns = sum(token == brown for token in items)
                    brown_ += self.calculate_points(browns)

        return (white_,brown_)

    def evaluate_score(self):
        #SCORES board using REWARDS AT THE TOP -> Can be used to give points depending on how many in a row (ie not just 4) + to evaluate how good a board is!!
        final_open_white = 0
        final_open_brown = 0
        # Check rows
        for row in range(self.field_height):
            row_list = self.make_row_list(row)
            if sum(row_list) >= 2:
                white1, brown1 = self.eval(row_list)
                final_open_white += white1
                final_open_brown += brown1

        # Check columns
        for col in self.field_state:
            if sum(col) >= 2:
                white2, brown2 = self.eval(col)
                final_open_white += white2
                final_open_brown += brown2

        right_diagonal_start_col = [0] * self.field_height + [x for x in range(1, 8)]
        right_diagonal_start_row = [x for x in range(7, 0, -1)] + [0] * self.field_height
        right_diagonal_zipped = zip(right_diagonal_start_col, right_diagonal_start_row)

        left_diagonal_start_col = [8] * self.field_height + [x for x in range(7, -1, -1)]
        left_diagonal_start_row = [x for x in range(7, -1, -1)] + [0] * self.field_height
        left_diagonal_zipped = zip(left_diagonal_start_col, left_diagonal_start_row)

        # Check right diagonals
        for coordinates in right_diagonal_zipped:
            right_diagonal_list = self.make_diagonal_right_list(coordinates)
            white3, brown3 = self.eval(right_diagonal_list)
            final_open_white += white3
            final_open_brown += brown3
            # coordinates is just the coordinate of each of the starting points of each diagonal
            # -> the make_diagonal method takes each start point and generates a list of tokens in the diagonal
            # -> the score_list method then updates white and browns scores based on pairs in the diagonal

        # Check left diagonals
        for coordinates in left_diagonal_zipped:
            left_diagonal_list = self.make_diagonal_left_list(coordinates)
            white4, brown4 = self.eval(left_diagonal_list)
            final_open_white += white4
            final_open_brown += brown4

        return (final_open_white, final_open_brown)

    def make_row_list(self,row):
        row_list = []
        for col in range(self.field_width):
            row_list.append(self.field_state[col][row])
        return row_list

    def make_diagonal_right_list(self,coordinates):
        starting_col,starting_row = coordinates
        diagonal_list = []
        #find diagonal
        diagonal_list.append(self.field_state[starting_col][starting_row])
        for offset in range(1,self.field_width):
            if starting_row+offset<self.field_height and starting_col+offset<self.field_width:
                diagonal_list.append(self.field_state[starting_col+offset][starting_row+offset])
        return diagonal_list

    def make_diagonal_left_list(self,coordinates):
        starting_col,starting_row = coordinates
        diagonal_list = []
        diagonal_list.append(self.field_state[starting_col][starting_row])
        for offset in range(1,self.field_width):
            if starting_row+offset<self.field_height and starting_col-offset>=0:
                diagonal_list.append(self.field_state[starting_col-offset][starting_row+offset])
        return diagonal_list



    def refresh_scores(self):
        (white_, brown_) = self.score()
        self.score_white = white_
        self.score_brown = brown_


    def full_check(self):
        return all([ height == self.field_height for height in self.col_heights ])

    # is the game finished?
    # return True if that is the case otherwise return False
    def winner_is(self):
        #if board is full or score of white or brown is more than score needed to win:
        self.refresh_scores()
        if self.score_white >= 1:
            return 1
        elif self.score_brown >= 1:
            return 2
        return 0 #Either draw or game is not over yet

    def set_winner(self):
        if self.score_white >=1:
            self.winner = 1 #white wins

        elif self.score_brown >=1:
            self.winner = 2 #brown wins

        else: self.winner = 0
        self.game_running = False

    def over(self):
        self.refresh_scores()
        if self.full_check() or self.score_white >= 1 or self.score_brown >= 1:   #if gameboard is full or a player has won...
            return True
        return False #not won yet