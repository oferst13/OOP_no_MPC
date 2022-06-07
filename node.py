import numpy as np
import cfg


class Node:
    def __init__(self, name, receiving_from=[], giving_to=[]):
        self.name = name
        self.receiving_from = receiving_from
        self.giving_to = giving_to
    def get_outlet_q(self):
        pass