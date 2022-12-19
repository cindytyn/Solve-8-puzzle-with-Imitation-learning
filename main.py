from collections import deque
import copy
import random
from queue import PriorityQueue
import pandas as pd

import numpy as np

global_dataset_list = []
# global_solutions_list = []

def manhattan_distance(state, goal):
  # Create a dictionary to store the positions of the tiles in the current state
  positions = {}

  # For each row in the state,
  for i, row in enumerate(state):
    # For each tile in the row,
    for j, tile in enumerate(row):
      # If the tile is not the blank space, store its position in the dictionary
      if tile != 0:
        positions[tile] = (i, j)

  # Initialize the total Manhattan distance to 0
  distance = 0

  # For each tile in the goal state,
  for i, row in enumerate(goal):
    for j, tile in enumerate(row):
      # If the tile is not the blank space,
      if tile != 0:
        # Get the position of the tile in the current state from the dictionary
        x, y = positions[tile]

        # Add the Manhattan distance for this tile to the total distance
        distance += abs(i - x) + abs(j - y)

  # Return the total distance
  return distance


def get_actions(state):
  # Find the position of the blank space in the grid
  x, y = find_blank_space(state)
  # print(x, y)

  # Initialize a list to store the possible actions
  actions = []

  # If the blank space is not in the first row, we can move it up
  if x > 0:
    actions.append('UP')

  # If the blank space is not in the last row, we can move it down
  if x < 2:
    actions.append('DOWN')

  # If the blank space is not in the first column, we can move it left
  if y > 0:
    actions.append('LEFT')

  # If the blank space is not in the last column, we can move it right
  if y < 2:
    actions.append('RIGHT')

  # Return the list of possible actions
  return actions


def find_blank_space(state):
  # For each row in the state,
  for i, row in enumerate(state):
    # For each tile in the row,
    for j, tile in enumerate(row):
      # If the tile is the blank space, return its position
      if tile == 0:
        return (i, j)

  # If we have reached this point, it means that the blank space was not found
  return None

def apply_action(state, action):
  # Find the position of the blank space in the grid
  x, y = find_blank_space(state)

  # Create a copy of the current state
  new_state = copy.deepcopy(state)

  # Based on the action, move the blank space in the specified direction
  if action == 'UP':
    new_state[x][y], new_state[x-1][y] = state[x-1][y], state[x][y]
  elif action == 'DOWN':
    new_state[x][y], new_state[x+1][y] = state[x+1][y], state[x][y]
  elif action == 'LEFT':
    new_state[x][y], new_state[x][y-1] = state[x][y-1], state[x][y]
  elif action == 'RIGHT':
    new_state[x][y], new_state[x][y+1] = state[x][y+1], state[x][y]

  # Return the new state
  return new_state


def get_neighbors(state):
  actions = get_actions(state)

  neighbors=[]

  for action in actions:
    new_state = apply_action(state, action)
    neighbors.append(new_state)

  return neighbors

def get_action(current_state, neighbor_state):
  # actions = ["UP", "DOWN", "LEFT", "RIGHT"]
  actions = get_actions(current_state)
  for action in actions:
      new_state = apply_action(current_state, action)
      if new_state == neighbor_state:
          return action
  return None



def a_star_search(start, goal, heuristic):
  # create an empty set to store visited nodes
  visited = set()

  # create a priority queue to store nodes that have been visited but not yet expanded
  # the priority queue will be sorted by the total cost of the path to the node,
  # which is the sum of the cost to reach the node from the start and the heuristic
  # estimate of the cost to reach the goal from the node
  queue = PriorityQueue()

  # add the start node to the queue, with a cost of 0
  queue.put((0, start))

  # create a dictionary to store the previous node for each node that is visited
  # this will be used to reconstruct the path from the start to the goal
  previous = {str(start): start}

  # create a dictionary to store the cost of the path from the start to each node
  # this will be used to determine the total cost of the path to each node
  cost_from_start = {str(start): 0}


  data = []
  solution = []
  actions = []

  # while the queue is not empty, continue searching for the goal
  while not queue.empty():
    # get the node with the lowest total cost from the queue
    current_cost, current_node = queue.get()

    # if the current node is the goal, we are done
    solution.append((previous[str(current_node)], current_node))
    if current_node == goal:
      # print("GOAL!!!")
      # print(current_node)
      break

    # if the current node has already been visited, skip it
    if str(current_node) in visited:
      continue

    # mark the current node as visited
    visited.add(str(current_node))

    # get the neighbors of the current node;
    # current_node_copy = copy.deepcopy(current_node)
    # neighbors = get_neighbors(current_node_copy)
    neighbors = get_neighbors(current_node)

    # for each neighbor of the current node...
    for neighbor in neighbors:
      # calculate the cost of the path from the start to the neighbor
      # by adding the cost to reach the current node to the edge cost
      # to reach the neighbor from the current node
      neighbor_cost = current_cost + 1

      # if the neighbor has not been visited, or if the current path
      # to the neighbor is shorter than the previous path to the neighbor,
      # update the cost and previous node for the neighbor
      if str(neighbor) not in cost_from_start or neighbor_cost < cost_from_start[str(neighbor)]:
        cost_from_start[str(neighbor)] = neighbor_cost
        total_cost = neighbor_cost + heuristic(neighbor, goal)
        queue.put((total_cost, neighbor))
        previous[str(neighbor)] = current_node

        # print("C1:",current_node)
        # print("N1:",neighbor)

        # store the action taken to reach the neighbor
        action = get_action(current_node, neighbor)
        actions.append(action)

        # print("===============================================")

        # print("C:",current_node)
        # print("N:",neighbor)

        # print("===============================================")

        # add the current and next states, along with the action, to the data list
        data.append((current_node, neighbor, action))

        # print(data)

      # print(neighbor)

  # print(data)
  df = pd.DataFrame(data, columns=["current_state", "next_state", "action"])
  df2 = pd.DataFrame(solution, columns=["previous_state", "current_state"])
  return df, df2

def is_solvable(state):
    # Convert the state to a 1-dimensional array of tiles
    tiles = [tile for row in state for tile in row]

    # Compute the parity of the permutation of the tiles
    parity = sum([tiles.index(i) for i in range(1, 9)]) % 2

    # If the parity is even, the puzzle is solvable
    return parity == 0

def generate_random_8_puzzle_state():
  # Create a list with the numbers 0-8
  numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]

  # Shuffle the list to generate a random permutation
  random.shuffle(numbers)

  state = [numbers[0:3], numbers[3:6], numbers[6:9]]

  if not is_solvable(state):
        generate_random_8_puzzle_state()

  # Return the permuted list as a 2D array (3x3 matrix)
  return state



if __name__ == "__main__":

  global_solutions_df = pd.DataFrame()

  # define the goal state for the 8 puzzle
  goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

  for i in range(5):
    state = generate_random_8_puzzle_state()
    # if str(state) not in global_dataset_dict.keys():
    #   global_dataset_dict[str(state)] = state
    if state not in global_dataset_list:
      global_dataset_list.append(state)
    else:
      continue

    path_df, solution_df = a_star_search(state, goal_state, manhattan_distance)

    global_solutions_df = global_solutions_df.append(solution_df)

    print(i)

  # global_df_dataset = pd.DataFrame({'Puzzles': global_dataset_list})

  

  # with pd.option_context('display.max_rows', None,
  #                      'display.max_columns', None,
  #                      'display.precision', 3,
  #                      ):
  #   print(global_df_dataset)

  # global_df_dataset.to_csv("dataset_df.csv")
  global_solutions_df.to_csv("dataset_solutions_df.csv")


#   initial_state = generate_random_8_puzzle_state()

#   print(initial_state)

#   # define the goal state for the 8 puzzle
#   goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

#   dist = manhattan_distance(initial_state,goal_state)

#   print(dist)


#   space = find_blank_space(initial_state)
#   print(space)



#   # # use a* search to find the optimal path from the initial state to the goal state
#   path_df, solution_df = a_star_search(initial_state, goal_state, manhattan_distance)
#   # display(path_df)


#   with pd.option_context('display.max_rows', None,
#                        'display.max_columns', None,
#                        'display.precision', 3,
#                        ):
#     print(path_df)

#   with pd.option_context('display.max_rows', None,
#                        'display.max_columns', None,
#                        'display.precision', 3,
#                        ):
#     print(solution_df)

# path_df.to_csv("path_df.csv")
# solution_df.to_csv("solution_df.csv")
