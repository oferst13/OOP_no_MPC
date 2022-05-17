import numpy as np
from collections import namedtuple
import cfg


def tank_fill(tank_storage, rain, tank_size):
    overflows = np.zeros_like(tank_size, dtype=float)
    for tank_num, tank in enumerate(tank_size):
        tank_storage[tank_num] = tank_storage[tank_num] + rain[tank_num]
        if tank_storage[tank_num] > tank:
            overflows[tank_num] = tank_storage[tank_num] - tank
            tank_storage[tank_num] = tank
    fill_res = namedtuple("tank_overflows", ["tank_storage", "overflows"])
    return fill_res(tank_storage, overflows)


def rw_use(tank_storage, demand):
    use = demand
    tank_storage = tank_storage - demand
    if len(tank_storage[tank_storage < 0]) > 0:
        neg_vals = np.where(tank_storage < 0)
        for val in neg_vals:
            tank_storage[val] += demand[val]
            use[val] = tank_storage[val]
            tank_storage[val] = 0
    use_res = namedtuple("water_use", ["tank_storage", "rainW_use"])
    return use_res(tank_storage, use)


def q_calc(q_in, pipe_n, timestep):
    inlet_A = (q_in / cfg.pipe_alphas[pipe_n]) ** (1 / cfg.beta)
    constant = cfg.pipe_alphas[pipe_n] * cfg.beta * (cfg.dt / cfg.pipes_L[pipe_n])
    out_A = pipe_out_A[pipe_n, timestep - 1] - constant * (((inlet_A + cfg.pipe_out_A[pipe_n, timestep - 1]) / 2) ** (cfg.beta - 1)) * \
            (pipe_out_A[pipe_n, timestep - 1] - inlet_A)
    out_Q = pipe_alphas[pipe_n] * (out_A ** beta)
    kinematic_res = namedtuple("q_result", ["outlet_A", "outlet_Q"])
    return kinematic_res(out_A, out_Q)


def model(pipe_flow, outlet_flow, timestep, alphas, last_pipe_out_A, pipe_length, beta, dt):
    # Pipe1
    pipe_flow[0, i, 0] = outlet_flow[0, timestep]
    kinematic_result = q_calc(pipe_flow[0, timestep, 0], 0, timestep, alphas, last_pipe_out_A, pipe_length, beta, dt)
    pipe_out_A[0, i] = kinematic_result.outlet_A
    pipe_Q[0, i, 1] = kinematic_result.outlet_Q
    # Pipe2
    pipe_Q[1, i, 0] = outlet_Q[1, i] + pipe_Q[0, i, 1]
    kinematic_result = funx.q_calc(pipe_Q[1, i, 0], 1, timestep, alphas, last_pipe_out_A, pipes_L, beta, dt)
    pipe_out_A[1, i] = kinematic_result.outlet_A
    pipe_Q[1, i, 1] = kinematic_result.outlet_Q
    # Pipe3
    pipe_Q[2, i, 0] = outlet_Q[2, i]
    kinematic_result = funx.q_calc(pipe_Q[2, i, 0], 2, timestep, alphas, pipe_out_A, pipes_L, beta, dt)
    pipe_out_A[2, i] = kinematic_result.outlet_A
    pipe_Q[2, i, 1] = kinematic_result.outlet_Q
    # Pipe4
    pipe_Q[3, i, 0] = pipe_Q[1, i, 1] + pipe_Q[2, i, 1]
    kinematic_result = funx.q_calc(pipe_Q[3, i, 0], 3, i, alphas, pipe_out_A, pipes_L, beta, dt)
    pipe_out_A[3, i] = kinematic_result.outlet_A
    pipe_Q[3, i, 1] = kinematic_result.outlet_Q
    # Pipe5
    pipe_Q[4, i, 0] = outlet_Q[3, i]
    kinematic_result = funx.q_calc(pipe_Q[4, i, 0], 4, i, alphas, pipe_out_A, pipes_L, beta, dt)
    pipe_out_A[4, i] = kinematic_result.outlet_A
    pipe_Q[4, i, 1] = kinematic_result.outlet_Q
    # Pipe6
    pipe_Q[5, i, 0] = pipe_Q[3, i, 1] + pipe_Q[4, i, 1]
    kinematic_result = funx.q_calc(pipe_Q[5, i, 0], 5, i, alphas, pipe_out_A, pipes_L, beta, dt)
    pipe_out_A[5, i] = kinematic_result.outlet_A
    pipe_Q[5, i, 1] = kinematic_result.outlet_Q