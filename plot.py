from matplotlib import pyplot
import numpy as np
from operator import attrgetter

def is_coord_in_bounds(rows, cols, coord):
    return coord[0] >= 0 and coord[0] < rows and coord[1] >= 0 and coord[1] < cols

class Plot:
    # Current state of grid (with Coordinate objects) to be displayed with graphics
    grid = []
    # Grid of tile numbers (0 is goal, tiles surrounding goal are 1, and so on)
    grid_nums = []
    # Current time step of simulation
    step = 0

    # Constructor
    def __init__(self, grid, step):
        self.step = step
        self.grid = grid
        self.grid_nums = [[0 for i in range(len(grid[0]))]
                                            for j in range(len(grid))]
        # Initialize grid_nums with values
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                num = self.grid[row][col].get_num()
                self.grid_nums[row][col] = num

    # Update grid to the new one in the parameter
    # Update values in grid_num
    # Increment step because this method is called every time step (before visualize method)
    def set_grid(self, grid):
        self.step += 1
        self.grid = grid
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                num = self.grid[row][col].get_num()
                self.grid_nums[row][col] = num

    # Visualization method for first time step
    def visualize(self, finished_agents, agents):
        pyplot.figure(figsize=(10, 10))
        # Set up grid of coordinates with tile numbers on corresponding coordinates
        # Each tile number will have an associated color (coords with same tile number will be colored the same color for ease of visualization)
        pyplot.imshow(self.grid_nums)
        ax = pyplot.gca()
        # Set up row and column axis labels
        num_cols = len(self.grid[0])
        x_labels = range(num_cols)
        ax.set_xticklabels(x_labels, fontsize=14)
        ax.set_xticks(x_labels)
        num_rows = len(self.grid)
        y_labels = range(num_rows)
        ax.set_yticklabels(y_labels, fontsize=14)
        ax.set_yticks(y_labels)
        ax.set_xlabel('Column', fontsize=16)
        ax.set_ylabel('Row', fontsize=16)

        # Scale fontsize with size of grid
        agent_fontsize = 11
        grid_size = len(self.grid)
        if (grid_size >= 8):
            agent_fontsize = 9

        grid_nums_transposed = np.array(self.grid_nums).T
        for row in range(len(grid_nums_transposed)):
            for col in range(len(grid_nums_transposed[0])):
                num = grid_nums_transposed[row][col]
                # Tile Number
                pyplot.text(row + .25, col - .25, num,
                            fontweight=850, fontsize=11)
                if (self.grid[col][row].agent != None):
                    circle = pyplot.Circle(
                        (row - .05, col + .05), radius=.3, color='white')
                    # Make agent numbers more visible
                    pyplot.text(row - .3, col + .05, "Agent ",
                                fontweight=500, fontsize=agent_fontsize)
                    # Draw agents as white circles
                    pyplot.text(row - .14, col + .26, self.grid[col][row].agent.get_id(
                    ), fontweight=500, fontsize=agent_fontsize)
                    ax.add_patch(circle)
                # Draw obstacles as black squares covering the entire coordinate
                if (self.grid[col][row].obstacle == True):
                    square = pyplot.Rectangle(
                        (row - .51, col - .51), height=1.02, width=1.02, color='black')
                    ax.add_patch(square)
        # Save this snapshot of the simulation in the images folder
        pyplot.figtext(.025, .05, "step = " + str(self.step), fontsize=15)
        # Create list of agents that reached goal and agents that haven't reached goal
        x_pos = .025
        x_increment = .03
        offset = .185
        pyplot.figtext(x_pos, .95, "Remaining Agents: ", fontsize=15)
        x_pos += offset
        agents.sort(key=attrgetter('id'))
        for agent in agents:
            x_pos += x_increment
            pyplot.figtext(x_pos, .95, agent.get_id(), fontsize=11)
        x_pos = .025
        pyplot.figtext(x_pos, .92, "Finished Agents: ", fontsize=15)
        x_pos += offset
        for fagent in finished_agents:
            x_pos += x_increment
            pyplot.figtext(x_pos, .92, fagent.get_id(), fontsize=11)
        pyplot.savefig("images/step" + str(self.step) + ".png")

    # Main visualization method
    def visualize_simulate(self, finished_agents, agents, intermediate_targets):
        pyplot.figure(figsize=(10, 10))
        # Set up grid of coordinates with tile numbers on corresponding coordinates
        # Each tile number will have an associated color (coords with same tile number will be colored the same color for ease of visualization)
        pyplot.imshow(self.grid_nums)
        ax = pyplot.gca()
        # Set up row and column axis labels
        num_cols = len(self.grid[0])
        x_labels = range(num_cols)
        ax.set_xticklabels(x_labels, fontsize=14)
        ax.set_xticks(x_labels)
        num_rows = len(self.grid)
        y_labels = range(num_rows)
        ax.set_yticklabels(y_labels, fontsize=14)
        ax.set_yticks(y_labels)
        ax.set_xlabel('Column', fontsize=16)
        ax.set_ylabel('Row', fontsize=16)

        # Scale fontsize with size of grid
        agent_fontsize = 11
        grid_size = len(self.grid)
        if (grid_size >= 8):
            agent_fontsize = 9

        grid_nums_transposed = np.array(self.grid_nums).T
        for row in range(len(grid_nums_transposed)):
            for col in range(len(grid_nums_transposed[0])):
                num = grid_nums_transposed[row][col]
                # Tile Number
                pyplot.text(row + .25, col - .25, num,
                            fontweight=850, fontsize=11)
                # Draw agents as white circles
                if (self.grid[col][row].agent != None):
                    circle = pyplot.Circle(
                        (row - .05, col + .05), radius=.3, color='white')
                    pyplot.text(row - .3, col + .05, "Agent ",
                                fontweight=500, fontsize=agent_fontsize)
                    pyplot.text(row - .14, col + .26, self.grid[col][row].agent.get_id(
                    ), fontweight=500, fontsize=agent_fontsize)
                    ax.add_patch(circle)
                # Draw obstacles as black squares covering the entire coordinate
                if (self.grid[col][row].obstacle == True):
                    square = pyplot.Rectangle(
                        (row - .51, col - .51), height=1.02, width=1.02, color='black')
                    ax.add_patch(square)
                # Mark the intermediate target tiles
                if (self.grid[col][row].agent == None and [col, row] in intermediate_targets):
                    pyplot.text(row - .18, col + .15, "IT",
                                fontweight=400, fontsize=15, color='white')
        # Save this snapshot of the simulation in the images folder
        pyplot.figtext(.025, .05, "step = " + str(self.step), fontsize=15)
        # Create list of agents that reached goal and agents that haven't reached goal
        x_pos = .025
        x_increment = .03
        offset = .185
        pyplot.figtext(x_pos, .95, "Remaining Agents: ", fontsize=15)
        x_pos += offset
        agents.sort(key=attrgetter('id'))
        for agent in agents:
            x_pos += x_increment
            pyplot.figtext(x_pos, .95, agent.get_id(), fontsize=11)
        x_pos = .025
        pyplot.figtext(x_pos, .92, "Finished Agents: ", fontsize=15)
        x_pos += offset
        for fagent in finished_agents:
            x_pos += x_increment
            pyplot.figtext(x_pos, .92, fagent.get_id(), fontsize=11)
        pyplot.savefig("images/step" + str(self.step) + ".png")
    
    # Add blank screens to indicate the end of simulation
    def blank_screen(self):
        pyplot.figure()
        self.step += 1
        pyplot.savefig("images/step" + str(self.step) + ".png")
        self.step += 1
        pyplot.savefig("images/step" + str(self.step) + ".png")
        self.step += 1
        pyplot.savefig("images/step" + str(self.step) + ".png")
