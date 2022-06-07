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
pipe2 = Pipe('pipe2', 500, 0.6, 0.002)
pipe3 = Pipe('pipe3', 400, 0.4, 0.0013)
pipe4 = Pipe('pipe4', 400, 0.8, 0.0088)
pipe5 = Pipe('pipe5', 300, 0.4, 0.005)
pipe6 = Pipe('pipe6', 200, 0.8, 0.01)

node111 = Node('node111', [outlet1], [pipe1])
node11 = Node('node11', [pipe1, outlet2], [pipe2])
node1 = Node('node1', [pipe2, pipe3], [pipe4])
node12 = Node('node12', [outlet3], [pipe3])
node2 = Node('node2', [pipe4, pipe5], [pipe6])
node21 = Node('node21', [outlet4], [pipe5])
outfall = Node('outfall', [pipe6])

print(outfall.giving_to)


