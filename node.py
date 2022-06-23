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
                inflow += (tank.overflows[timestep] + tank.releases[timestep]) / cfg.dt
        else:
            for pipe in self.receiving_from:
                inflow += pipe.outlet_Q[timestep]
        for pipe in self.giving_to:
            pipe.inlet_Q[timestep] = inflow / len(self.giving_to)

