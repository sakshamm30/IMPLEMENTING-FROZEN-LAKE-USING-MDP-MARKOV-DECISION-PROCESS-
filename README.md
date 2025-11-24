# IMPLEMENTING-FROZEN-LAKE-USING-MDP-MARKOV-DECISION-PROCESS-
IMPLEMENTING FROZEN LAKE USING MDP (MARKOV DECISION PROCESS) GROUP PROJECT 
This project models the game Frozen Lake as an MDP, where the agent's goal is to navigate a slippery grid world to a target without falling into holes. The states represent the grid locations, actions are the movement directions, and rewards are received upon reaching the goal. Value Iteration or Policy Iteration is applied to find the optimal policy that maximizes the expected cumulative reward.
❄️ Breakdown of MDP Components in Frozen Lake
To elaborate, the core components are:
• States (S): Each tile on the grid (e.g., (0,0) to (3,3) for a 4 \times 4 map).
• Actions (A): Move Up, Down, Left, or Right.
• Transition Probability (P_{a}(s, s')): Due to the slippery nature, taking an action a from state s may land the agent in an adjacent state s' with a certain probability (e.g., 1/3 for the intended direction, and 1/3 for each of the two perpendicular directions).
• Reward (R_{a}(s, s')): Typically +1 for reaching the goal and 0 or -1 for falling into a hole or moving to a non-terminal state.
