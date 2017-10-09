# Connect-4

[![DEMO691d58afa75a74d6.gif](https://gifyu.com/images/DEMO691d58afa75a74d6.gif)](https://gifyu.com/image/M6Q9)

I have developed three AIs: Minimax, α-β and Deep. The third one is called Deep as it is optimised by iterative deepening in addition to α-β pruning. I recorded my data by playing each AI against another AI with both of their first two moves being generated randomly in order to get a large range of different outcomes. Any game where this has lead to an AI winning unfairly has been discarded. Also, when recording this data I turned off the graphics to increase the program’s speed and prevent the program crashing.

From the graphs it is clear that as the number of plies searched through by each AI increases, the average time spent choosing a move increases exponentially. Also, the spread of the average time taken increases with the plies. The data also shows that there is a strong positive correlation between the proportion of wins by an AI and the number of plies. However, my evaluation function is not perfect which may explain why the AI with a higher ply doesn’t always win.

In a tournament I would use the Deep AI with a ply of 4. This is because the Deep AI is much faster than the α-β and Minimax algorithms which would make it better for competitive games. I would use a max depth of 4 as the data recorded suggests that a larger ply of 5 would not significantly increase the Deep AI’s winning rate while more than halving its speed.

