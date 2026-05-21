from cb_mpc import CB_MPC
from task_generator import Task_Generator
import numpy as np
from cbs import Environment
from cbs import CBS
from utils import *
import time
import yaml
from pathlib import Path

if __name__ == "__main__":

    cost_func_params = {
        'Q':  np.array([[5.0, 0.0, 0.0, 0.0], 
                        [0.0, 5.0, 0.0, 0.0], 
                        [2.0, 0.0, 0.0, 0.0], 
                        [0.0, 2.0, 0.0, 0.0]]),
        'R': np.array([[5.5, 0.0], [0.0, 5.5]]),
        'P': np.array([[15.0, 0.0], [0.0, 15.0]]),
        'Qc': 8,
        'kappa': 3 
    }
    mpc_params = {
        'dt': 0.1,
        'N' : 10,
        'vx_lim': 5.0,
        'vy_lim': 5.0,
        'ax_lim': 2.0,
        'ay_lim': 2.0,
        'total_sim_timestep': 500,
        'obs_sim_timestep': 200,
        'epsilon_o': 0.1,
        'epsilon_r': 0.1,
        'safety_margin': 0.1,
        'goal_tolerence': 0.5
    }

    num_trials = 1
    path = "../instances/test.yaml"
    scenario = Path(path).stem 
    # read your input file
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    robots = data["robots"]
    num_agents = len(data["robots"])
    # set the map as grid
    map_min = data["environment"]["min"]
    map_max = data["environment"]["max"] 
    map_size = (
        int(round((map_max[0] - map_min[0]))),
        int(round((map_max[1] - map_min[1])))
    )
    # obstacles
    static_obs = []
    dynamic_obs = []
    obs = {"static": static_obs, "dynamic": dynamic_obs}
    obstacle = {
        "type": "box",
        "x": 2.0,
        "y": 3.0,
        "radius": 0.5,
        "width": 1.5,
        "height": 2.0
    }
    for o in data["environment"]["obstacles"]:
        obstacle = {"type": o["type"]}
        if o["type"] == "box":
            obstacle["x"] = o["center"][0]
            obstacle["y"] = o["center"][1]
            obstacle["width"] = o["size"][0]
            obstacle["height"] = o["size"][1]

        elif o["type"] == "sphere":

            obstacle["x"] = o["center"][0]
            obstacle["y"] = o["center"][1]
            obstacle["radius"] = o["radius"]
        static_obs.append(obstacle)

    num_obstacles = len(static_obs)
    # read initial, final states
    initial_states = [robot["start"]
        for robot in data["robots"]]
    final_states = [robot["goal"]
        for robot in data["robots"]]
    # update mpc params
    mpc_params['num_agents'] = num_agents
    mpc_params['rob_dia'] = 0.50 # robot diameter
    mpc_params['rob_radius'] = 0.25

    for trial in range(0, num_trials):
        mpc_params["num_agents"] = num_agents
        map = generate_map(map_size, num_obstacles)
        while True:
            task_gen = Task_Generator(num_agents, map, mpc_params["rob_dia"])
            env = Environment(map, map_size, initial_states, final_states)
            cbs = CBS(env)
            cbs_timeout = 10 # in seconds
            start_time = time.time()
            solution = None
            
            try:
                print("CBS Search Running")
                solution = cbs.search(cbs_timeout)
            except TimeoutError:
                print("CBS search timeout exceeded...")
                break
            
            if solution:
                print('Discrete Solution Found')
                ref = discretize_waypoints(solution, mpc_params["dt"], mpc_params["N"])
                print('MPC Running')
                mpc = CB_MPC(initial_states, final_states, cost_func_params, obs, mpc_params, scenario, trial, map, ref)
                mpc.simulate()
                print("Finished CB-MPC")
                
            else:
                print("CBS Solution not found")
        
            break  # Break out of the loop if CBS search was successful
        



   
