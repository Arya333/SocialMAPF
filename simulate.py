from plot import Plot
from models.agent import Agent
from operator import attrgetter
import math, sys

# Checks if the provided coordinate is within the bounds of the grid
# Used in several methods in Simulate class
def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols

class Simulate:
    # Grid that the simulation is running on
    grid = []
    # List of all agents remaining in simulation
    agents = []
    # Goal coord of agents
    goal_coords = []
    # Current time step of simulation
    step = 0
    # Maximum number of steps allowed for simulation
    max_num_steps = 0
    # List of agents that reached goal
    finished_agents = []

    # List of coordinates that have a path to the goal coord
    # Some coords are removed from this list when creating mapping of ids to corresponding intermediate target
    intermediate_candidates = []
    # List of all coordinates in grid that have a path to the goal coord
    intermediate_candidates_2 = []
    # List of agent ids of agents that are completely stuck (obstacles all around, no true path to the goal coord)
    completely_stuck_agent_ids = []
    # Mapping of agent ids to intermediate targets for them to move to
    ids_to_intermediate_coords = {}

    # Constructor
    def __init__(self, grid, agents, goal, step, max_steps, finished_agents):
        self.grid = grid
        self.agents = agents
        self.goal_coords = goal
        self.step = step
        self.max_num_steps = max_steps
        self.finished_agents = finished_agents

    # Loops through every coordinate (that is not obstacle or goal) in the grid and
    # checks whether there is a path (that follows the 'rolling down the hill' principle) to the goal
    # If there is a path, add that coordinate to intermediate_candidates and intermediate_candidates_2
    def find_intermediate_candidates(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if (self.path_to_coord_exists(row, col, self.goal_coords[0], self.goal_coords[1]) and not self.grid[row][col].obstacle and not (row == self.goal_coords[0] and col == self.goal_coords[1])):
                    self.intermediate_candidates.append([row, col])
                    self.intermediate_candidates_2.append([row, col])
    
    # Recursive backtracking helper method for find_intermediate_candidates method
    # Checks if a coordinate has a path to the goal by following the 'rolling down the hill' principle by
    # only going moving to a tile with a lower tile number
    def path_to_coord_exists(self, row, col, goal_row, goal_col):
        if (row == goal_row and col == goal_col):
            return True
        up = [row - 1, col]
        down = [row + 1, col]
        left = [row, col - 1]
        right = [row, col + 1]
        moves = [up, down, left, right]
        for move in moves:
            check = False
            if (is_coord_in_bounds(len(self.grid), len(self.grid[0]), move) and not self.grid[move[0]][move[1]].obstacle and self.grid[move[0]][move[1]].get_num() < self.grid[row][col].get_num()):
                check = self.path_to_coord_exists(move[0], move[1], goal_row, goal_col)
            if (not check):
                continue
            else:
                return True
        return False
    
    # Returns true if there is a path btwn coord1 and coord2 (any path, not necessarily following 'rolling down the hill' principle)
    # Used to find if agent is completely stuck (obstacles surrounding it)
    def path_btwn_two_coords_exists(self, coord1, coord2):
        # visited is 2d array to avoid already visited coordinates in path
        visited = [[False for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        path_exists = self.path_btwn_two_coords_recursion(coord1[0], coord1[1], coord2, visited)
        return path_exists

    # Recursive helper method for path_btwn_two_coords_exists
    # Returns true if path exists btwn the 2 coordinates and false otherwise
    def path_btwn_two_coords_recursion(self, row, col, coord2, visited):
        if (is_coord_in_bounds(len(self.grid), len(self.grid[0]), [row, col]) and not self.grid[row][col].obstacle and not visited[row][col]):
            visited[row][col] = True
            if (row == coord2[0] and col == coord2[1]):
                return True
            up = self.path_btwn_two_coords_recursion(row - 1, col, coord2, visited)
            if (up):
                return True
            down = self.path_btwn_two_coords_recursion(row + 1, col, coord2, visited)
            if (down):
                return True
            left = self.path_btwn_two_coords_recursion(row, col - 1, coord2, visited)
            if (left):
                return True
            right = self.path_btwn_two_coords_recursion(row, col + 1, coord2, visited)
            if (right):
                return True
        return False

    # Iterates through list of all intermediate targets in grid and
    # checks if the agent has a path (not rolling down hill) to atleast one of these targets
    # Returns false if agent has a path and true if agent is completely stuck (no path to any intermediate target = obstacles surrounding agent)
    # Used to add agents to stuck_agent_ids list
    def is_agent_completely_stuck(self, agent):
        row = agent.get_curr_coords()[0]
        col = agent.get_curr_coords()[1]
        for coord in self.intermediate_candidates:
            if (self.path_btwn_two_coords_exists(coord, [row, col])):
                return False
        return True
    
    # Checks if an agent is stuck (all surrounding tiles have higher tile numbers)
    # Returns False if agent is not stuck and True if stuck
    # Used in cause_intermediate function to determine whether or not to begin intermediate target phase
    def is_agent_stuck(self, rows, cols, agent):
        row = agent.get_curr_coords()[0]
        col = agent.get_curr_coords()[1]
        up = [row - 1, col]
        down = [row + 1, col]
        left = [row, col - 1]
        right = [row, col + 1]
        if (is_coord_in_bounds(rows, cols, up) and (self.grid[up[0]][up[1]].get_num() < agent.get_coord_num()) and (self.grid[up[0]][up[1]].agent == None)):
            return False
        if (is_coord_in_bounds(rows, cols, down) and (self.grid[down[0]][down[1]].get_num() < agent.get_coord_num()) and (self.grid[down[0]][down[1]].agent == None)):
            return False 
        if (is_coord_in_bounds(rows, cols, left) and (self.grid[left[0]][left[1]].get_num() < agent.get_coord_num()) and (self.grid[left[0]][left[1]].agent == None)):
            return False
        if (is_coord_in_bounds(rows, cols, right) and (self.grid[right[0]][right[1]].get_num() < agent.get_coord_num()) and (self.grid[right[0]][right[1]].agent == None)):
            return False
        return True

    # Given an agent as parameter, find the closest coordinate to it in the intermediate_candidates list
    # Find the intermediate target coord with the minimum euclidian distance to agent's coords
    # Used in create_agent_intermediate_goal_mapping method
    def find_closest_intermediate_coord(self, agent):
        shortest_dist = sys.maxsize
        shortest_coords = []
        for coords in self.intermediate_candidates:
            dist = math.dist(agent.get_curr_coords(), coords)
            if (dist < shortest_dist):
                shortest_dist = dist
                shortest_coords = coords
        return shortest_coords
    
    # Given an agent as parameter, find the closest coordinate to it in the intermediate_candidates_2 list
    # Find the intermediate target coord with the minimum euclidian distance to agent's coords
    # Used in move_agent_towards_interm_coord method
    def find_closest_intermediate_coord2(self, new_coords):
        shortest_dist = sys.maxsize
        shortest_coords = []
        for coords in self.intermediate_candidates_2:
            dist = math.dist(new_coords, coords)
            if (dist < shortest_dist):
                shortest_dist = dist
                shortest_coords = coords
        return shortest_coords

    # Sets up the ids_to_intermediate_coords map and stuck_agent_ids list
    def create_agent_intermediate_goal_mapping(self):
        rows = len(self.grid)
        cols = len(self.grid[0])
        self.completely_stuck_agent_ids = []
        for agent in self.agents:
           # Adds completely stuck agents (surrounded by obstacles) to stuck_agent_ids list
           if (self.is_agent_completely_stuck(agent)):
                self.completely_stuck_agent_ids.append(agent.get_id())
           # Only create a mapping for agents that are temporarily stuck (not completely stuck)
           elif (self.is_agent_stuck(rows, cols, agent)):
                # Pair agent id to its closest available intermediate target coords
                # Remove the coords from the intermediate_candidates list so its not an option for other agents to go to
                id = agent.get_id()
                closest_coord = self.find_closest_intermediate_coord(agent)
                self.ids_to_intermediate_coords[id] = closest_coord
                self.intermediate_candidates.remove(closest_coord)
                #self.stuck_agent_ids.append(id)
        # Add remaining intermediate targets to intermediate_candidates from intermediate_candidates_2 list to make a complete list
        for coord in self.intermediate_candidates_2:
            if (not coord in self.intermediate_candidates):
                self.intermediate_candidates.append(coord)
    
    # Check if there are agents in the one tile and add these agents to a list
    # Sort this list by an attribute
    # The first agent that is in the list after being sorted is the highest priority agent that will move to the goal first
    # This is the auction algorithm
    def check_ones(self):
        agents_with_ones = []
        temp = False
        if (self.agents[0].get_coord_num() == 1):
            temp = True
        else:
            return None
        index = 0
        while (temp):
            if (index >= len(self.agents) or self.agents[index].get_coord_num() != 1):
                temp = False
                break
            else:
                agents_with_ones.append(self.agents[index])
                index += 1
        agents_with_ones.sort(key=attrgetter('velocity'), reverse=True)
        return agents_with_ones[0]
    
    # Choose an agent's next coordinate based on which move will reduce the euclidian distance between 
    # the agent's corresponding intermediate target (using the map) and the next coord
    def move_agent_towards_intermediate_coord(self, agent, up, down, left, right, rows, cols):
        curr_coords = agent.get_curr_coords()
        id = agent.get_id()
        interm_coord = self.ids_to_intermediate_coords[id]
        next_coords = [curr_coords[0], curr_coords[1]]
        moves = [up, down, left, right]
        order = []
        # Create a priority of which order to consider with the move with minimum distance first
        while (len(moves) > 0):
            min_dist = sys.maxsize
            coords_min_dist = []
            for move in moves:
                dist = math.dist(move, interm_coord)
                if (dist < min_dist):
                    min_dist = dist
                    coords_min_dist = move
            order.append(coords_min_dist)
            moves.remove(coords_min_dist)
        recent_coords = agent.trajectory[len(agent.trajectory) - 2]
        for move in order:
            # If move is in bounds, has no agent in its coord, isnt an obstacle, and wasn't recently explored, the move is set to next coord
            if (is_coord_in_bounds(rows, cols, move) and self.grid[move[0]][move[1]].agent == None 
                and not self.grid[move[0]][move[1]].obstacle and not (move[0] == recent_coords[0] and move[1] == recent_coords[1])):
                next_coords = move
                break
        # Optimization: set a new intermediate target for the agent based on the next move
        # This ensures agent doesn't get stuck in a never-ending loop
        new_interm_target = self.find_closest_intermediate_coord2(next_coords)
        self.ids_to_intermediate_coords[id] = new_interm_target
        return next_coords
    
    # Main algorithm for moving agents to goal
    # Works until all agents reached goal or the only remaining agents are the ones that are completely stuck (surrounded by obstacles)
    def simulate(self):
        plot = Plot(self.grid, self.step)
        while (self.step < self.max_num_steps):
            # Stop when agents list is empty (meaning all agents reached the goal)
            if (not self.agents):
                break
            # Stop when length of stuck_agent_ids list equals length of agents list 
            # This means only remaining agents are the ones completely stuck
            if (len(self.completely_stuck_agent_ids) == len(self.agents)):
                break
            
            self.step += 1
            self.agents.sort(key=attrgetter('coord_num'))
            rows = len(self.grid)
            cols = len(self.grid[0])
            # Re-create mapping and available intermediate targets for each time step
            self.create_agent_intermediate_goal_mapping()
            # Check if agents are in one tiles for special case
            # If so, use auction algorithm to determine which agent in one tile moves to goal first
            agent_ones = self.check_ones()
            if (agent_ones != None):
                curr_coords = agent_ones.get_curr_coords()
                self.grid[curr_coords[0]][curr_coords[1]].update_agent(agent_ones, True)
                self.grid[self.goal_coords[0]][self.goal_coords[1]].update_agent(agent_ones, False)
                agent_ones.update_coords(self.goal_coords)
                agent_ones.add_to_path()
                agent_ones.reached()
                self.finished_agents.append(agent_ones)
                self.grid[self.goal_coords[0]][self.goal_coords[1]].update_agent(agent_ones, True)
                index_remove = 0
                for a in self.agents:
                    if (a.get_id() == agent_ones.get_id()):
                        break
                    index_remove += 1
                del self.agents[index_remove]

            # Loop through agents and move them one at a time
            for agent in self.agents:
                if (agent.get_coord_num() != 1):
                    id = agent.get_id()
                    cur_row = agent.curr_coords[0]
                    cur_col = agent.curr_coords[1]
                    next_coords = [cur_row, cur_col]
                    up = [cur_row - 1, cur_col]
                    down = [cur_row + 1, cur_col]
                    left = [cur_row, cur_col - 1]
                    right = [cur_row, cur_col + 1]
                    moves = [up, down, left, right]
                    # Check if agent is in interm coords array
                    # If so, move agents to coord in interm coords array that has smaller tile number than itself
                    # This works because all coords in interm coord array have a path to the goal following 'rolling down the hill' principle
                    if (agent.get_curr_coords() in self.intermediate_candidates_2):
                        if (id in self.ids_to_intermediate_coords.keys()):
                            del self.ids_to_intermediate_coords[id]
                        for move in moves:
                            if (is_coord_in_bounds(rows, cols, move) and self.grid[move[0]][move[1]].agent == None and self.grid[move[0]][
                            move[1]].get_num() < agent.get_coord_num() and move in self.intermediate_candidates_2):
                                next_coords[0] = move[0]
                                next_coords[1] = move[1]
                                break
                    # If not in interm coords array, move agent towards associated interm coord
                    # Move based on which move will reduce euclidian distance (simple greedy algorithm)
                    elif (id in self.ids_to_intermediate_coords.keys()):
                        next_coords = self.move_agent_towards_intermediate_coord(agent, up, down, left, right, rows, cols)
                    # Use standard 'rolling down hill' algorithm for agents that aren't temporarily stuck and not in an intermediate target coordinate
                    else:
                        for move in moves:
                            if (is_coord_in_bounds(rows, cols, move) and self.grid[move[0]][move[1]].agent == None and self.grid[move[0]][
                            move[1]].get_num() < agent.get_coord_num()):
                                next_coords[0] = move[0]
                                next_coords[1] = move[1]

                    # Adding and removing agent pointers from coordinate object if the agent moved positions
                    if (next_coords[0] != cur_row or next_coords[1] != cur_col):
                        new_coord_row = next_coords[0]
                        new_coord_col = next_coords[1]
                        self.grid[new_coord_row][new_coord_col].update_agent(agent, False)
                        self.grid[cur_row][cur_col].update_agent(agent, True)
                        agent.update_coords(next_coords)
                        agent.coord_num = self.grid[new_coord_row][new_coord_col].get_num()
                    agent.add_to_path()
            plot.set_grid(self.grid)
            plot.visualize_simulate(self.finished_agents, self.agents, self.intermediate_candidates_2)
            print("step = " + str(self.step))
            print("Agents")
            print(self.agents)
            print("Interm Candidates")
            print(self.intermediate_candidates_2)
            print("Mapping")
            print(self.ids_to_intermediate_coords)
            print("")

    # Call to setup and run simulation
    def run_simulation(self):
        self.find_intermediate_candidates()
        self.create_agent_intermediate_goal_mapping()
        self.simulate()
        plot = Plot(self.grid, self.step)
        plot.blank_screen()