# Shortest Path Algorithms Visualizer

## Background: A* Search Algorithm
The A* algorithm is a popular and powerful pathfinding algorithm that improves upon Dijkstra's algorithm by incorporating heuristic information to guide its search. It is widely used in various applications, including navigation systems and AI.

A* takes into account both the cost of reaching a node from the start and an estimate of the cost to the goal, known as the heuristic function. By considering this heuristic information, A* can prioritize the exploration of paths that are more likely to lead to the goal, resulting in more efficient and informed decision-making.

In contrast, Dijkstra's algorithm explores all possible paths equally, without considering the goal. This advantage of A* makes it particularly effective in scenarios where there is a need for finding the shortest path quickly and optimally, as it significantly reduces the number of unnecessary node expansions and improves overall performance.

**For example if we wanted to compute the shortest route from Denver to NYC:**


![alt text](https://github.com/zhijiazhang/sps-algorithms-visualizer/blob/main/pics/denverToNYC.png?raw=true)
