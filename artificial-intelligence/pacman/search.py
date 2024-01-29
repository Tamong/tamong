# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def genericSearch(problem, i):
    """Search deepest node first (dfs) if i is 1 else it searches the shallowest node first (bfs)."""

    if i is 1:
        open = util.Stack()  # Stores states that need to be expanded for dfs.
        currentPath = util.Stack()  # Stores path of expanded states for dfs.
    else:
        open = util.Queue()  # Stores states that need to be expanded for bfs.
        currentPath = util.Queue()  # Stores path of expanded states for bfs.

    closed = []  # Stores states that have been expanded.
    finalPath = []  # Store final path of states.

    open.push(problem.getStartState())
    currState = open.pop()  # Current State.
    while not problem.isGoalState(currState):  # Search until goal state.
        if currState not in closed:  # New state found.
            closed.append(currState)  # Add state to closed.
            for successor in problem.getSuccessors(
                currState
            ):  # Adding successors of current state.
                open.push(successor[0])  # Add to open.
                currentPath.push(finalPath + [successor[1]])  # Store path.

        currState = open.pop()  # Update current State.
        finalPath = currentPath.pop()  # Add to final path.
    return finalPath


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # STUDENTS: JIMMY HARVIN, PHILIP WALLIS

    # Initialize node (location, path, cost)
    node = problem.getStartState(), [], 0

    # return if node is a goal state
    if problem.isGoalState(node[0]):
        return node[1]

    # initialize LIFO stack and visited set
    stack = util.Stack()
    stack.push((node))
    visited = []

    # While the stack is not empty
    while not stack.isEmpty():
        node = stack.pop()

        if problem.isGoalState(node[0]):
            return node[1]

        # If the node is not visited
        if node[0] not in visited:
            # Mark as visited
            visited.append(node[0])

            # For each successor of the node
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                # If the successor is not visited
                if successor[0] not in visited:
                    # Push the successor to the stack
                    stack.push((successor[0], node[1] + [successor[1]]))


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # STUDENTS: JIMMY HARVIN, PHILIP WALLIS

    # From textbook page 82

    # Initial node (location, path, cost)
    node = problem.getStartState(), [], 0

    # return if node is a goal state
    if problem.isGoalState(node[0]):
        return node[1]

    # initialize FIFO queue and visited set
    queue = util.Queue()
    queue.push((node))
    visited = []

    # While the queue is not empty
    while not queue.isEmpty():
        node = queue.pop()

        # If the node is not visited
        if node[0] not in visited:
            # Add to visited and check if it is a goal state
            visited.append(node[0])
            if problem.isGoalState(node[0]):
                return node[1]

            # For each successor, add to queue
            for successor in problem.getSuccessors(node[0]):
                successorAction = node[1] + [successor[1]]
                queue.push((successor[0], successorAction))


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # STUDENTS: JIMMY HARVIN, PHILIP WALLIS

    # From textbook page 84

    # Initial node (location, path, cost)
    node = problem.getStartState(), [], 0

    # return if node is a goal state
    if problem.isGoalState(node[0]):
        return node[1]

    # initialize priority queue and visited set
    pqueue = util.PriorityQueue()
    pqueue.push((node), 0)  # 0 is priority
    visited = []

    # While the pqueue is not empty
    while not pqueue.isEmpty():
        node = pqueue.pop()

        # If the node is not visited
        if node[0] not in visited:
            # Add to visited and check if it is a goal state
            visited.append(node[0])
            if problem.isGoalState(node[0]):
                return node[1]

            for successor in problem.getSuccessors(node[0]):
                successorAction = node[1] + [successor[1]]
                successorCost = node[2] + successor[2]
                # cost will be the priority
                pqueue.push(
                    (successor[0], successorAction, successorCost), successorCost
                )


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    open = (
        util.PriorityQueue()
    )  # Stores states that need to be expanded for Uniform Cost Search.
    currPath = util.PriorityQueue()  # Stores path of expanded states.
    closed = []  # Stores states that have been expanded.
    finalPath = []  # Store final path of states.

    open.push(problem.getStartState(), 0)
    currState = open.pop()  # Current State.
    while not problem.isGoalState(currState):  # Search until goal state.
        if currState not in closed:  # New state found.
            closed.append(currState)  # Add state to closed.

            for successor in problem.getSuccessors(
                currState
            ):  # To calculate costs of successors of current state.
                pathCost = problem.getCostOfActions(
                    finalPath + [successor[1]]
                )  # Cost of selecting successor.
                if heuristic is not None:  # Add heuristic if A* search.
                    pathCost += heuristic(successor[0], problem)
                if (
                    successor[0] not in closed
                ):  # If successor is a new state add to open queue and store path.
                    open.push(successor[0], pathCost)
                    currPath.push(finalPath + [successor[1]], pathCost)

        currState = open.pop()  # Update current state.
        finalPath = currPath.pop()  # Add to final path.

    return finalPath


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
