import numpy as np
import cfg


class Pipe:

    def __init__(self, length, diameter, slope):
        self.length = length
        self.diameter = diameter
        self.slope = slope
        self.alpha = (0.501 / cfg.manning) * (diameter ** (1 / 6)) * (slope ** 0.5)

    def calc_q_outlet(self):
        pass

    def get_q_outlet(self):
        pass

