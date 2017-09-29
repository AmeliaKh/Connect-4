import ConnectFourMinimaxAI
import HeuristicsBROWN_deep
import ConnectFourEngine2


if __name__ == '__main__':
    # Initialise the game engine
    # Modify these parameters to tweak the game
    app = ConnectFourEngine2.ConnectFour(
        #red = white     blue = brown
            set_rewards=[0.000002, 0.0001, 0, 0, 0, 0, 0, 0, 0], # needed when playing with white2
            set_white_player = None,
            set_brown_player = None,
            )
    # start the game engine
    app.game_loop()