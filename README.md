# SocialMAPF

## About the Project

## Installation

1. Make sure you have installed <a href="https://www.python.org/downloads/">Python</a> on your system
2. Install NumPy
```
pip install numpy
```
3. Install Matplotlib
```
pip install matplotlib
```
4. Follow <a href="https://phoenixnap.com/kb/ffmpeg-windows">these steps</a> to install <a href="https://ffmpeg.org/download.html">FFmpeg</a> on your system
5. Clone the repository
```
git clone https://github.com/Arya333/SocialMAPF.git
```

## Usage

In ```main.py``` the following code runs the simulation:
```python
simulator = Simulate(grid, agents, goal_coord, 0, max_sim_steps, finished_agents)
start = time.time()
simulator.run_simulation()
```

Also in ```main.py``` the following code uses FFmpeg to create a video of the simulation from images generated in ```plot.py```:
```python
pro = os.system("ffmpeg -r 1 -f image2 -i ./images/step%d.png -s 1000x1000 -y simulation.avi")
os.system("ffmpeg -i simulation.avi -c:v libx264 -preset slow -crf 19 -c:a libvo_aacenc -b:a 128k -y simulation.mp4")
os.system("ffmpeg -i simulation.mp4 -crf 10 -vf \"minterpolate=fps=10:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1\" out.mp4")
```
The first line converts a series of images (time steps of the simulation) in the ```images``` folder into an AVI video file. The second line creates an MP4 video file from the AVI file. The last line motion interpolates the MP4 file to make smoother transitions in the simulation. Parameters in these commands can be changed or added to alter the simulation video.

To run a simulation, run ```main.py```

## Configuration

First, set up the grid with the size of the grid (number of rows and columns) and how many agents should be in the grid.
```python
'''
USER INPUT: number of rows for grid
            number of columns for grid
            number of agents
'''
num_rows = 10
num_cols = 10
num_agents = 20
```

Then, either randomize the goal coordinate or select your own goal coordinate as a list of size 2 (x & y value). The velocities in ```vels``` are used by the auction algorithm to determine which agent moves to the goal coordinate based on priority. Entries in ```vels``` can be changed so long as the size of the list is the same as ```num_agents```.

```python
# Velocity for each agent is its id in this case
# Velocity is the attribute used in auction algorithm to determine which agent moves to the goal
vels = [i for i in range(1, 1 + num_agents)]
# USER INPUT: goal coordinate
goal_coord = list(np.random.randint(1, num_rows, 2))
```

## Examples

## Acknowledgements

## Contributing
