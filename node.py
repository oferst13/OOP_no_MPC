import copy

import numpy as np
import cfg


class Node:
    all_nodes = []

    def __init__(self, name, receiving_from=[], giving_to=[], tank_node=False):
        self.name = name
        self.receiving_from = receiving_from
        self.giving_to = giving_to
        self.tank_node = tank_node
        Node.all_nodes.append(self)

    def handle_flow(self, timestep):
        inflow: float = 0
        if self.tank_node:
            for tank in self.receiving_from:
                inflow += (tank.overflows[timestep] + tank.release_volume[timestep]) / cfg.dt
        else:
            for pipe in self.receiving_from:
                inflow += pipe.outlet_Q[timestep]
        for pipe in self.giving_to:
            pipe.inlet_Q[timestep] = inflow / len(self.giving_to)

    def get_zero_Q(self):
        last_Q_list = []
        for pipe in self.receiving_from:
            last_Q_list.append(np.max(np.nonzero(pipe.outlet_Q)))
        return max(last_Q_list) + 1

    def get_max_Q(self): # this works only with 1 pipe for now
        max_Q = 0.0
        for pipe in self.receiving_from:
            max_Q += np.max(pipe.outlet_Q)
        return max_Q