# Shortest Path Algorithms Visualizer

## Background: A* Search Algorithm
The A* algorithm is a popular and powerful pathfinding algorithm that improves upon Dijkstra's algorithm by incorporating heuristic information to guide its search. It is widely used in various applications, including navigation systems and AI.

A* takes into account both the cost of reaching a node from the start and an estimate of the cost to the goal, known as the heuristic function. By considering this heuristic information, A* can prioritize the exploration of paths that are more likely to lead to the goal, resulting in more efficient and informed decision-making.

In contrast, Dijkstra's algorithm explores all possible paths equally, without considering the goal. This advantage of A* makes it particularly effective in scenarios where there is a need for finding the shortest path quickly and optimally, as it significantly reduces the number of unnecessary node expansions and improves overall performance.

**Let's say we were interested in computing the shortest path possible going from Denver to New York. If we used Dijkstra's Algorithm, yes we would eventually compute the shortest path, but before that we would've found the shortest path to Las Vegas, Los Angeles, Dallas etc. Why are we doing all this extra work that we don't care about?**

![alt text](https://github.com/zhijiazhang/sps-algorithms-visualizer/blob/main/pics/denverToNYC.png?raw=true)

**A\* algorithm takes care of this. At a high level, instead of searching toward unnecessary directions, the algorithm makes it's decisions based on heuristics. This results in the algorithm only searching towards New York, which makes it much more efficient than Dijkstra's. Depicted below, from Denver there are 4 possible directions A\* could go in. It will choose to go towards Henderson because that path is going towards New York, while the other 3 are going in the opposite direction.**


<img src="https://github.com/zhijiazhang/sps-algorithms-visualizer/blob/main/pics/denver.png?raw=true"  width="350" height="350">

## Demo