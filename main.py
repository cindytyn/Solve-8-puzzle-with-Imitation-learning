import sys
import copy
import random
from dataprocess import *
from collections import deque

#########################################################################################
def star_search_with_imitation_learning(initial_board, goal_board):
    # Create a queue for storing the states to be explored
    queue = deque([initial_board])

    # Create a set for storing the visited states
    visited_states = set()

    # Create a dictionary for storing the actions taken from each state
    actions = {}

    # Keep track of the number of iterations
    iterations = 0

    while queue:
        # Get the next state to explore
        current_state = queue.popleft()

        # If the state is the goal, we have found a solution
        if current_state == goal_board:
            return actions

        # Otherwise, add the current state to the visited set
        visited_states.add(current_state)

        # Get the possible actions from the current state
        possible_actions = get_possible_actions(current_state)

        # For each possible action, create a new state and add it to the queue
        for action in possible_actions:
            new_state = apply_action(current_state, action)
            if new_state not in visited_states:
                queue.append(new_state)
                actions[new_state] = action

        # Update the number of iterations
        iterations += 1

    # If we have reached this point, it means that no solution was found
    return None

def get_possible_actions(state):
  # define a list to store the possible actions
  actions = []

  # Get the current position of the agent
  agent_x, agent_y = get_agent_position(state)

  # check if any of the possible actions can be taken from the current state
  if is_valid_move(state, agent_x, agent_y - 1):
    actions.append("move_up")
  if is_valid_move(state, agent_x, agent_y + 1):
    actions.append("move_down")
  if is_valid_move(state, agent_x - 1, agent_y):
    actions.append("move_left")
  if is_valid_move(state, agent_x + 1, agent_y):
    actions.append("move_right")

  # return the list of possible actions
  return actions

def get_agent_position(state):
  # Loop through the grid to find the position of the agent
  for x in range(state.grid_width):
    for y in range(state.grid_height):
      if state.grid[x][y] == state.AGENT:
        return x, y

def is_valid_move(state, agent_x, agent_y):
  # Check if the given coordinates are within the bounds of the grid
  if agent_x < 0 or agent_x >= state.grid_width or agent_y < 0 or agent_y >= state.grid_height:
    return False

  # Check if the position is occupied by a wall
  if state.grid[agent_x][agent_y] == state.WALL:
    return False

  # If the position is within the bounds of the grid and not occupied by a wall, it is a valid move
  return True

def apply_action(current_state, action):
  # Create a new state object by copying the current state
#   new_state = State(current_state.grid, current_state.grid_width, current_state.grid_height)
  new_state = copy.copy(current_state)

  # Get the current position of the agent
  agent_x, agent_y = get_agent_position(new_state)

  # Update the position of the agent based on the action
  if action == 'move_up':
    agent_y -= 1
  elif action == 'move_down':
    agent_y += 1
  elif action == 'move_left':
    agent_x -= 1
  elif action == 'move_right':
    agent_x += 1

  # Update the grid in the new state to reflect the new position of the agent
  new_state.grid[agent_x][agent_y] = new_state.AGENT

  # Return the new state
  return new_state

def generate_random_state():
  # create a list of all possible numbers in the puzzle
  numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]

  # shuffle the list of numbers to generate a random state
  random.shuffle(numbers)

  # create a new state object using the shuffled numbers
  state = State(numbers)

  # return the initial state
  return state

# generate a random initial state
initial_state = generate_random_state()

# define the goal state for the 8 puzzle
goal_state = State([1, 2, 3, 4, 5, 6, 7, 8, 0])

# use a* search to find the optimal path from the initial state to the goal state
path = star_search_with_imitation_learning(initial_state, goal_state)

if __name__ == "__main__":
    print("CMPT417 Final Project")
    (puzzle,size) = read_instance('s_t01.txt')
    print(puzzle)
    print(size)
