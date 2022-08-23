from models import coordinate

class Agent:
    # Unique id to differentiate each agent from each other
    id = -1
    # Attribute used in auction algorithm to determine agent that goes to goal
    velocity = 0
    # The current coordinates on the grid of the agent
    curr_coords = [-1, -1]
    # List of all coordinates agent has been to in order (index is time step)
    trajectory = []
    # The tile number of the coordinate the agent is on
    coord_num = -1
    # Whether the agent has reached the goal or not
    reached_goal = False

    # Constructor
    def __init__(self, agent_id, vel, coords, coord_num, trajectory):
        self.id = agent_id
        self.velocity = vel
        self.curr_coords = coords
        self.coord_num = coord_num
        self.trajectory = trajectory
        self.reached_goal = False

    # Change curr_coords of agent to new_coords and decrement coord_num because
    # it is assumed that agent only moves to tile numbers that are smaller by 1
    # This is not always the case (as seen in intermediate target phase)
    def update_coords(self, new_coords):
        self.curr_coords = new_coords
        self.coord_num -= 1
    
    # Add the current coordinate to the trajectory list
    def add_to_path(self):
        self.trajectory.append(self.curr_coords)

    # Return the tile number of coordinate the agent is currently on
    def get_coord_num(self):
        return self.coord_num
    
    # Return agent's id
    def get_id(self):
        return self.id
    
    # Return agent's current coordinates on the grid
    def get_curr_coords(self):
        return self.curr_coords

    # When agent reaches goal, set reached_goal to True
    def reached(self):
        self.reached_goal = True
    
    # Printable representation of agent object
    # FORMAT: { ID CURR_COORDS COORD_NUM VEL } 
    def __repr__(self):
        return "{ " + str(self.id) + " " + str(self.curr_coords) + " " + str(self.coord_num) + " " + str(self.velocity) + " }"
