from dataclasses import dataclass
import yaml
from robot_dynamics import DoubleIntegrator2D, UnicycleFirstOrder


@dataclass
class RobotParams:
    dynamics: str
    distance_weights: list[float]

    dim_state: int
    dim_action: int

    # Optional parameters
    max_vel: list[float] | None = None
    min_vel: list[float] | None = None

    max_acc: list[float] | None = None
    min_acc: list[float] | None = None

    max_speed: float | None = None
    min_speed: float | None = None

    max_angular_vel: float | None = None
    min_angular_vel: float | None = None

    shape_type: str | None = None
    radius: float | None = None
    size: list[float] | None = None


def load_robot_params(filename: str) -> RobotParams:
    with open(filename, "r") as f:
        cfg = yaml.safe_load(f)

    dynamics = cfg["dynamics"]

    params = {
        "dynamics": dynamics,
        "distance_weights": cfg["distance_weights"],
        "dim_state": cfg["dim_state"],
        "dim_action": cfg["dim_action"],
    }

    if dynamics == "unicycle_first_order":
        params.update({
            "max_speed": cfg["max_speed"],
            "min_speed": cfg["min_speed"],

            "max_angular_vel": cfg["max_angular_vel"],
            "min_angular_vel": cfg["min_angular_vel"],

            "shape_type": cfg["shape"]["type"],
            "size": cfg["shape"]["size"]
        })

    elif dynamics == "double_integrator_2d":
        params.update({
            "max_vel": cfg["max_vel"],
            "min_vel": cfg["min_vel"],

            "max_acc": cfg["max_acc"],
            "min_acc": cfg["min_acc"],

            "shape_type": cfg["shape"]["type"],
            "radius": cfg["shape"]["radius"]
        })

    return RobotParams(**params)

def create_dynamics(robot_params):
    if robot_params.dynamics == "double_integrator_2d":
        return DoubleIntegrator2D()

    elif robot_params.dynamics == "unicycle_first_order":
        return UnicycleFirstOrder()

    else:
        raise ValueError("Unknown dynamics")