# Connect-4

[![DEMO691d58afa75a74d6.gif](https://gifyu.com/images/DEMO691d58afa75a74d6.gif)](https://gifyu.com/image/wOvq)

I have developed three AIs: Minimax, α-β and Deep. Deep is optimised by iterative deepening in addition to α-β pruning. I recorded my data by playing each AI against another AI with both of their first two moves being generated randomly in order to get a large range of different outcomes. When recording this data the graphics were turned off to increase the program’s speed and prevent crashing.

The graphs show that as the number of plies searched through by each AI increases, the average time spent choosing a move increases exponentially. Also, the spread of the average time taken increases with the plies. The data also shows that there is a strong positive correlation between the proportion of wins by an AI and the number of plies. However, my evaluation function is not perfect which may explain why the AI with a higher ply doesn’t always win.

To play the game run ConnectFourAIvsHuman.py
