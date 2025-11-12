# Artificial Intelligence Lecture Notes

## Introduction to Artificial Intelligence

Artificial Intelligence, or AI, is the branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding.

### Evolution of AI

The field of AI has evolved significantly since its inception in the 1950s. Early AI research focused on symbolic reasoning and problem-solving. The Dartmouth Conference in 1956 is widely considered the birth of AI as a field. Over the decades, AI has progressed through several phases including expert systems, machine learning, and now deep learning and neural networks.

### State of the Art

Modern AI systems have achieved remarkable success in various domains. Deep learning has revolutionized image recognition, natural language processing, and game playing. Large language models can now generate human-like text, and AI systems have surpassed human performance in complex games like Go and chess.

## Different Types of Artificial Intelligence

### Narrow AI

Narrow AI, also known as Weak AI, is designed to perform specific tasks. Examples include voice assistants, recommendation systems, and image recognition software. These systems excel at their designated tasks but cannot generalize beyond their training.

### General AI

General AI, or Strong AI, refers to systems that possess human-like intelligence and can perform any intellectual task that a human can do. This type of AI does not yet exist and remains a long-term goal of AI research.

### Superintelligent AI

Superintelligent AI would surpass human intelligence in virtually every aspect. This remains theoretical and is a subject of ongoing research and debate in the AI community.

## Applications of AI

Artificial Intelligence has found applications across numerous industries. In healthcare, AI assists in medical diagnosis and drug discovery. In transportation, self-driving cars use AI for navigation and decision-making. Finance uses AI for fraud detection and algorithmic trading. E-commerce platforms employ AI for personalized recommendations and customer service chatbots.

## Subfields of AI

### Machine Learning

Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It includes supervised learning, unsupervised learning, and reinforcement learning.

### Natural Language Processing

Natural Language Processing, or NLP, focuses on enabling computers to understand, interpret, and generate human language. Applications include machine translation, sentiment analysis, and chatbots.

### Computer Vision

Computer Vision allows machines to interpret and understand visual information from the world. It is used in facial recognition, autonomous vehicles, and medical image analysis.

### Robotics

Robotics combines AI with mechanical engineering to create autonomous machines. Robots use AI for perception, planning, and control in various environments.

### Expert Systems

Expert Systems are AI programs that mimic the decision-making ability of human experts. They use knowledge bases and inference engines to solve problems in specific domains.

## Intelligent Agents

An intelligent agent is an autonomous entity that perceives its environment through sensors and acts upon that environment through actuators. Agents are designed to achieve specific goals or maximize a performance measure.

### Structure of Intelligent Agents

Intelligent agents consist of several key components. The agent function maps percept sequences to actions. The agent program implements this function. Agents maintain an internal state to track their environment and use a knowledge base to store information about the world.

### Types of Agents

Simple reflex agents respond directly to percepts without maintaining internal state. Model-based reflex agents maintain an internal model of the world. Goal-based agents consider future actions to achieve goals. Utility-based agents maximize utility functions. Learning agents can improve their performance over time.

## Environments

The environment in which an agent operates can be characterized along several dimensions. Fully observable environments provide complete information to the agent, while partially observable environments have hidden information. Deterministic environments have predictable outcomes, whereas stochastic environments involve randomness. Episodic environments consist of independent episodes, while sequential environments have long-term consequences.

## Problem Solving by Searching

Problem solving in AI often involves searching through a space of possible solutions. State space search represents problems as graphs where nodes are states and edges are actions. The goal is to find a path from the initial state to a goal state.

### Uninformed Search Methods

Uninformed search methods, also called blind search, do not use problem-specific knowledge. Breadth First Search explores all nodes at the current depth before moving to the next level. Depth First Search explores as far as possible along each branch before backtracking. Uniform Cost Search expands the node with the lowest path cost. Depth-limited search limits the depth of exploration. Iterative deepening depth-first search combines the benefits of BFS and DFS by repeatedly running DFS with increasing depth limits.

### Informed Search Methods

Informed search methods use heuristic functions to guide the search. Best First Search uses a heuristic to select the most promising node. A* Search combines the cost to reach a node with the estimated cost to the goal, ensuring optimal solutions when the heuristic is admissible.

## Local Search Algorithms

Local search algorithms operate on a single current state rather than multiple paths. Hill-climbing search moves to the best neighboring state but can get stuck in local maxima. Simulated annealing allows occasional moves to worse states to escape local optima. Genetic algorithms use principles of natural selection, including crossover and mutation, to evolve solutions over generations.

## Adversarial Search

Adversarial search deals with competitive environments where agents have opposing goals. Game trees represent possible moves in a game. The Minimax algorithm determines the optimal move by assuming both players play optimally. Alpha-Beta Pruning improves minimax efficiency by eliminating branches that cannot influence the final decision.

### Tic-Tac-Toe Example

In tic-tac-toe, the game tree represents all possible board configurations. Minimax evaluates each position from the perspective of the current player. Alpha-beta pruning can reduce the number of nodes evaluated by up to 99 percent in complex games.

## Logic and Reasoning

Logic provides a formal framework for representing knowledge and drawing conclusions. Propositional Logic uses propositions that are either true or false, connected by logical operators like AND, OR, and NOT. First Order Logic extends propositional logic with quantifiers and predicates, allowing representation of objects and relationships.

### Inference in First Order Logic

Inference involves deriving new knowledge from existing knowledge. Unification is the process of finding substitutions that make two expressions identical. Forward Chaining starts with known facts and applies rules to derive new facts. Backward Chaining starts with a goal and works backwards to find supporting facts. Resolution is a complete inference procedure that can prove any statement that follows from a knowledge base.

## Uncertain Knowledge and Reasoning

Real-world problems often involve uncertainty. Probability theory provides a framework for reasoning under uncertainty. Bayes Rule allows updating beliefs based on new evidence. Bayesian Belief Networks represent probabilistic relationships between variables using directed graphs. Approximate inference methods, such as sampling algorithms, are used when exact inference is computationally intractable.

## Planning

Planning involves finding a sequence of actions that achieves a goal. Classical planning assumes a deterministic, fully observable environment. Planning can be viewed as state-space search, where forward search starts from the initial state and backward search starts from the goal state.

### Planning Graphs

Planning graphs provide a compact representation of possible actions and their effects. They enable efficient algorithms like Graphplan that can find optimal plans.

### Hierarchical Planning

Hierarchical planning breaks complex problems into simpler subproblems. This abstraction allows planning at multiple levels of detail.

### Nondeterministic Planning

In nondeterministic domains, actions may have uncertain outcomes. Sensor-less planning operates without direct observation of the environment. Multiagent planning coordinates actions among multiple agents, requiring consideration of other agents' plans and goals.

