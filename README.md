# 2048-game [AI solver included]

[Definition Document](./Definition.md)

[Testing Document](./testingDocument.md)

### Weekly Reports

[Week 1](./weeklyReports/week_1_report.md)

[Week 2](./weeklyReports/week_2_report.md)

[Week 3](./weeklyReports/week_3_report.md)

[Week 4](./weeklyReports/week_4_report.md)

### Usage Instructions

- Clone the repository
- navigate to `./2048-game`
- If you want to play the game by yourself run `poetry run invoke start`
- If you want the AI to solve it for you `poetry run invoke startAi`
- To run tests navigate to `./2048-game/src` and run `poetry run invoke test`
- When the game is over, Press enter to restart it.


### Short Description

- Although the algorithm might sometimes fail in the early stages of the game, if you run it more that 1 times it will prove that it is capable of making it very far in the game. The Expectiminimax algorithm takes into account that there is a random element to the game and tries its best to mitigate the outcome.