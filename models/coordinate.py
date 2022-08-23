from models import agent

class Coordinate:
    # The tile number of the coordinate (0 for goal coord, 1 for tiles surrounding goal coord and so on)
    num = -1
    # Coordinates on grid in format [ROW, COLUMN]
    coords = [-1, -1]
    # Pointer to agent if agent is on this coordinate on the grid (None if no agent on this coordinate)
    agent = None
    # True if this coordinte is an obstacle, False otherwise
    obstacle = False

    # Constructor
    def __init__(self, num, coords, agent, obs):
        self.num = num
        self.coords = coords
        self.agent = agent
        self.obstacle = obs
    
    # Remove agent if is_remove is true by setting pointer to None
    # Add agent if is_remove is false by setting pointer to agent parameter
    def update_agent(self, agent, is_remove):
        if (is_remove):
            self.agent = None
        else:
            self.agent = agent
    
    # Returns tile number of the coordinate
    def get_num(self):
        return self.num