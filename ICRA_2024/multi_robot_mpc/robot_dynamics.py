import numpy as np
import casadi as ca

class DoubleIntegrator2D:
    def f(self, x, u):
        return ca.vertcat(x[2], x[3], u[0], u[1])

    def f_np(self, x, u):
        return np.array([x[2], x[3], u[0], u[1]])

    def state_bounds(self, opti, X, params):
        x, y, vx, vy = X[:,0], X[:,1], X[:,2], X[:,3]

        opti.subject_to(opti.bounded(-5, x, 12))
        opti.subject_to(opti.bounded(-5, y, 12))

        opti.subject_to(opti.bounded(params.min_vel[0], vx, params.max_vel[0]))
        opti.subject_to(opti.bounded(params.min_vel[1], vy, params.max_vel[1]))

    def control_bounds(self, opti, U, params):
        ax, ay = U[:,0], U[:,1]

        opti.subject_to(opti.bounded(params.min_acc[0], ax, params.max_acc[0]))
        opti.subject_to(opti.bounded(params.min_acc[1], ay, params.max_acc[1]))

class UnicycleFirstOrder:
    def f(self, x, u):
        return ca.vertcat(
            u[0] * ca.cos(x[2]),
            u[0] * ca.sin(x[2]),
            u[1]
        )
    def f_np(self, x, u):
        return np.array([
            u[0] * np.cos(x[2]),
            u[0] * np.sin(x[2]),
            u[1]
        ])
    
    def state_bounds(self, opti, X, params):
        x, y, theta = X[:,0], X[:,1], X[:,2]

        opti.subject_to(opti.bounded(-5, x, 12))
        opti.subject_to(opti.bounded(-5, y, 12))

    def control_bounds(self, opti, U, params):
        v, omega = U[:,0], U[:,1]

        opti.subject_to(opti.bounded(params.min_speed, v, params.max_speed))
        opti.subject_to(opti.bounded(params.min_angular_vel, omega, params.max_angular_vel))