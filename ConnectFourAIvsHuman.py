import ConnectFourEngine
import C4_AlphaBeta
import C4_Deep
import C4_Minimax
import Engine_minus_graphics

if __name__ == '__main__':

# the Deep AI and Alpha Beta AI should only be white players and the Minimax AI should only be a brown player

    app = ConnectFourEngine.ConnectFour(
            set_rewards=[0.000002, 0.0001, 0, 0, 0, 0, 0, 0, 0], # needed when playing with Deep
            set_white_player = C4_Deep.AIcheck,
            set_brown_player = None,
            )
    app.game_loop()
