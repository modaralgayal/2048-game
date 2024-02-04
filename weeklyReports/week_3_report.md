# Week 3

* The expectiminimax algorithm is now implemented and tested in the game. The best_next_move acts as a player instead of a real player. The function takes a board as an argument and returns the next best move based on the depth given to the function.

* I have made the possibility of testing all possibilities with and without pruning. Pruning is now implemented to that if only the n most valuable tiles are taken into consideration in the expectiminimax testing in order to speed up the gameplay.

* I implemented increasing the depth as the amount of tiles becomes smaller, so that the gameplay is not dramatically slow in the beginning. With less tiles it is okay to increase the depth in order for the AI to make "smarter" decisions.

* What is left to do is improve the pruning and depth relationship. Right now a tile of 4096 is guaranteed but the algorithm has room for improvement. I am aiming to get a guaranteed 8192 from each run.