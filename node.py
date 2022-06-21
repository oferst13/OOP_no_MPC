import numpy as np
import cfg


class Node:
    all_nodes = []

    def __init__(self, name, receiving_from=[], giving_to=[]):
        self.name = name
        self.receiving_from = receiving_from
        self.giving_to = giving_to
        Node.all_nodes.append(self)

    def pass_flow(self, timestep):
        inflow: float = 0
        for pipe in self.receiving_from:
            inflow += pipe.outlet_Q[timestep]
        for pipe in self.giving_to:
            pipe.inlet_Q[timestep] = inflow / len(self.giving_to)

