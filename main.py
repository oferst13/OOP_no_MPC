import copy
from tank import Tank
from pipe import Pipe
from node import Node
import cfg
import numpy as np


tank1 = Tank('tank1', 30, 0, 9000)
tank2 = Tank('tank2', 35, 0, 10000)
tank3 = Tank('tank3', 25, 0, 8500)
tank4 = Tank('tank4', 50, 0, 14000)

outlet1 = Pipe('outlet1', 250, 0.4, 0.02)
outlet2 = Pipe('outlet2', 330, 0.4, 0.015)
outlet3 = Pipe('outlet3', 220, 0.4, 0.02)
outlet4 = Pipe('outlet4', 350, 0.4, 0.007)

pipe1 = Pipe('pipe1', 400, 0.4, 0.0063)

node111 = Node('node111', [outlet1], [pipe1])
print(node111.giving_to[0].slope)


