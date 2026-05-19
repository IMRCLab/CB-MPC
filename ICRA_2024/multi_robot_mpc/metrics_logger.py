import pickle
import os
import yaml

class MetricsLogger:
    def __init__(self):
        self.metrics_data = {}

    def log_metrics(self, run_description, trial_num, state_cache, map, initial_state, final_state, total_comp_time, max_comp_time, traj_length, makespan, avg_rob_dist, c_avg, success, execution_collision, max_time_reached):
        # Log the metrics for a specific algorithm trial
        if run_description not in self.metrics_data:
            self.metrics_data[run_description] = {}
        if trial_num not in self.metrics_data[run_description]:
            self.metrics_data[run_description][trial_num] = {
                "state_cache": {},
                "initial_state": [],
                "final_state": [],
                "map": [],
                "avg_comp_time": [],
                "max_comp_time": [],
                "c_avg": [],
                "traj_length": [],
                "makespan": [],
                "avg_rob_dist": [],
                "success": [],
                "execution_collision": [],
                "max_time_reached": []
            }
        self.metrics_data[run_description][trial_num]["state_cache"] = state_cache
        self.metrics_data[run_description][trial_num]["initial_state"] = initial_state
        self.metrics_data[run_description][trial_num]["final_state"] = final_state
        self.metrics_data[run_description][trial_num]["map"] = map
        self.metrics_data[run_description][trial_num]["total_comp_time"] = total_comp_time
        self.metrics_data[run_description][trial_num]["max_comp_time"] = max_comp_time
        self.metrics_data[run_description][trial_num]["traj_length"] = traj_length
        self.metrics_data[run_description][trial_num]["makespan"] = makespan
        self.metrics_data[run_description][trial_num]["avg_rob_dist"] = avg_rob_dist
        self.metrics_data[run_description][trial_num]["success"] = success
        self.metrics_data[run_description][trial_num]["c_avg"] = c_avg
        self.metrics_data[run_description][trial_num]["execution_collision"] = execution_collision
        self.metrics_data[run_description][trial_num]["max_time_reached"] = max_time_reached

    def print_metrics_summary(self):
        # Returns the collected metrics data
        for algorithm_name, trials in self.metrics_data.items():
            for trial_num, metrics in trials.items():
                total_computation_time = metrics["total_comp_time"]
                max_computation_time = metrics["max_comp_time"]
                traj_length = metrics["traj_length"]
                makespan = metrics["makespan"]
                success = metrics["success"]
                execution_collision = metrics["execution_collision"]
                max_time_reached = metrics["max_time_reached"]

                if(success):
                    print("Total Comp Time:")
                    print(total_computation_time)
                    print("Traj Length:")
                    print(traj_length)
                    print("Makespan:")
                    print(makespan)
                    print("Success:")
                    print(bool(success))
                    print("===================")
                else:
                    print("Success:")
                    print(bool(success))
                    print("Collision:")
                    print(execution_collision)
                    print("Timeout:")
                    print(max_time_reached)
                    print("===================")

    def save_metrics_data(self, base_folder="results"):
        # Create the base folder if it doesn't exist
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        for run_description, trials in self.metrics_data.items():
            run_folder = os.path.join(base_folder, run_description)
            # Create a folder for each run description if it doesn't exist
            if not os.path.exists(run_folder):
                os.makedirs(run_folder)

            for trial_num, metrics in trials.items():
                file_name = f"trial_{trial_num}.pkl"
                file_path = os.path.join(run_folder, file_name)
                with open(file_path, 'wb') as file:
                    pickle.dump(metrics, file)

    def save_state_cache(self, state_cache, filename):
        result = []

        for agent_id, traj in state_cache.items():
            agent_entry = {"states": []}

            for state in traj:
                # convert numpy -> python list
                agent_entry["states"].append(state.tolist())

            result.append(agent_entry)

        data = {"result": result}

        with open(filename, "w") as f:
            yaml.dump(data, f, default_flow_style=False)


