**README for GitHub Repository: "AI-Fundamentals"**

# AI Fundamentals

Welcome to my GitHub repository "AI-Fundamentals"! This repository contains several AI applications designed to learn the basics of artificial intelligence. The different projects cover various aspects of AI, ranging from graph search algorithms to solving the 8-Queens problem, implementing a knowledge base for the Wumpus game, and creating a feedforward neural network for handwriting recognition.

## Projects

### 1. Graph Search Algorithms

In the first project, all fundamental graph search algorithms are implemented:

- A* (A Star)
- DFS (Depth-First Search)
- BFS (Breadth-First Search)
- UCS (Uniform Cost Search)

These algorithms are excellent for understanding the basics of pathfinding in graphs. You can find detailed information and application examples in the corresponding project directory.
The Pygame visualization enhances the learning experience by providing a graphical representation of the algorithms in action. 
Both Euclidean and Manhattan distance heuristics are implemented for A* algorithm, giving users the flexibility to choose the appropriate heuristic for their specific scenarios.

![astart_visualization](https://github.com/ligabeast/ai/assets/114762651/13674899-027d-46a1-b053-314bfeb6c5ff)


### 2. 8-Queens Problem with Genetic Algorithm and Pygame Visualization

In the second project, the 8-Queens problem is solved using a genetic algorithm and visualized with Pygame. The visualization can be started by pressing the spacebar. To optimize runtime and explore different scenarios, various parameters can be adjusted by modifying global variables at the top of the code:

```python
boardLength = 8
# Priority > Initial 
initialPopulation = 20
priorityQueueSize = 50
mutation = 0.3
# Higher -> Select better parent
selectionFactor = 10
maxIteration = 100
stopScore = 0
```

These parameters allow users to customize the genetic algorithm's behavior, making it a versatile tool for experimenting with different optimization strategies.

Additionally, the genetic algorithm is designed to handle an increased board dimension efficiently. You can experiment with significantly larger board dimensions, and the runtime remains stable, showcasing the scalability of the algorithm.

For detailed instructions and application examples, please refer to the corresponding project directory.

![8queen](https://github.com/ligabeast/ai/assets/114762651/4713cf50-a454-49c7-81e2-8cf21a0a0731)



### 3. Knowledge Base for the Wumpus Game

The third project contains a knowledge base for the Wumpus game. Two different variants are implemented:

- Forward Chaining
- Resolution

The following actions are defined:
```python
WALK = 0
TURNLEFT = 1
TURNRIGHT = 2
GRAB = 3
SHOOT = 4
CLIMB = 5
```
![wumpusKB](https://github.com/ligabeast/ai/assets/114762651/63a2f2c5-98a8-4909-ae34-ae81b84bd3b8)

These actions can be utilized to interact with the Wumpus environment, and the knowledge base facilitates decision-making based on the current state and perceptions.

For detailed instructions and application examples, please refer to the corresponding project directory.

### 4. Feedforward Neural Network for Handwriting Recognition

#### Model Configuration:

To observe how the model behaves concerning the error rate, users can modify the following global variables at the top of the code:

```python
input_nodes = 784  # 28*28 pixels
hidden_nodes = 200  # voodoo magic number
output_nodes = 10  # numbers from [0:9]
training_samples = 400
training_quantity = 500
test_quantity = 100

learning_rate = 0.15  # feel free to play around with
```

These variables allow users to customize the neural network's architecture and training parameters, providing a flexible environment for experimentation.

For detailed instructions and application examples, please refer to the corresponding project directory.

![image](https://github.com/ligabeast/ai/assets/114762651/97e84d4d-dbcf-466d-9ad6-71000e638e48)
