from scipy import integrate
from tank import Tank
from pipe import Pipe
from node import Node
import cfg
import numpy as np
import math
from timer import Timer


class Scenario:
    def __init__(self, last_outflow, max_flow):
        self.last_outflow = last_outflow
        self.max_flow = max_flow
        self.release_hour = math.ceil(Tank.get_last_overflow() * (cfg.dt / 3600))
        self.obj_Q = None
        self.fitness = None

    def calc_obj_Q(self):
        self.obj_Q = outfall.get_outflow_volume() / Tank.get_last_overflow()

    def calc_fitness(self):
        to_min: float = 0
        for i in range(self.last_outflow):
            to_min += abs(outfall.get_flow(i) - self.obj_Q)
        self.fitness = to_min


def set_rain_input(rainfile, rain_dt, duration):
    rain = np.zeros(int(duration / (rain_dt/cfg.dt)))
    rain_input = np.genfromtxt(rainfile, delimiter=',')
    rain[:len(rain_input)] = rain_input
    return rain


def calc_mass_balance():
    mass_balance = 100 * (abs(outfall.get_outflow_volume() - Tank.get_cum_outflow())) / (Tank.get_cum_outflow())
    return mass_balance


def run_model():
    for i in range(cfg.sim_len):
        if sum(forecast_rain[int(i // (cfg.rain_dt / cfg.dt)):-1]) + Tank.get_tot_storage() == 0:
            break  # this should break forecast run only!
        for tank in Tank.all_tanks:
            tank.tank_fill(i)
            tank.set_release(i)
            tank.rw_use(i)
        if i < 1 or (Pipe.get_tot_Q(i - 1) + Tank.get_tot_outflow(i)) < 1e-3:
            continue
        for node in Node.all_nodes:
            node.handle_flow(i)
            for pipe in node.giving_to:
                pipe.calc_q_outlet(i)


runtime = Timer()
runtime.start()
demands = np.array([])
for demand in cfg.demands_3h:
    demands = np.append(demands, np.ones(int(cfg.demand_dt / cfg.dt)) * (demand * (cfg.dt / cfg.demand_dt)))
demand_PD = demands * cfg.PD / 100

tank1_dict = {'name': 'tank1', 'n_tanks': 30, 'init_storage': 0, 'roof': 9000, 'dwellers': 180}
tank2_dict = {'name': 'tank2', 'n_tanks': 35, 'init_storage': 0, 'roof': 10000, 'dwellers': 180}
tank3_dict = {'name': 'tank3', 'n_tanks': 25, 'init_storage': 0, 'roof': 8500, 'dwellers': 180}
tank4_dict = {'name': 'tank4', 'n_tanks': 50, 'init_storage': 0, 'roof': 14000, 'dwellers': 180}
#tank1 = Tank('tank1', 30, 0, 9000, 180)
#tank2 = Tank('tank2', 35, 0, 10000, 190)
#tank3 = Tank('tank3', 25, 0, 8500, 150)
#tank4 = Tank('tank4', 50, 0, 14000, 650)
tank1 = Tank(tank1_dict)
tank2 = Tank(tank2_dict)
tank3 = Tank(tank3_dict)
tank4 = Tank(tank4_dict)

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

tank1_out = Node('tank1_out', [tank1], [outlet1], tank_node=True)
tank2_out = Node('tank1_out', [tank2], [outlet2], tank_node=True)
tank3_out = Node('tank1_out', [tank3], [outlet3], tank_node=True)
tank4_out = Node('tank1_out', [tank4], [outlet4], tank_node=True)

node111 = Node('node111', [outlet1], [pipe1])
node11 = Node('node11', [pipe1, outlet2], [pipe2])
node12 = Node('node12', [outlet3], [pipe3])
node1 = Node('node1', [pipe2, pipe3], [pipe4])
node21 = Node('node21', [outlet4], [pipe5])
node2 = Node('node2', [pipe4, pipe5], [pipe6])
outfall = Node('outfall', [pipe6])

# Create forecast - currently real rain only!
forecast_rain = set_rain_input('09-10.csv', cfg.rain_dt, cfg.sim_len)
for tank in Tank.all_tanks:
    tank.set_daily_demands(demand_PD)  # happens only once

# starting main sim loop
for tank in Tank.all_tanks:
    tank.set_inflow_forecast(forecast_rain)  # happens once a forecast is made


run_model()

baseline = Scenario(Tank.get_last_overflow(), outfall.get_max_Q())
mass_balance_err = calc_mass_balance()
print(f"Mass Balance Error: {mass_balance_err:0.2f}%")
zero_Q = outfall.get_zero_Q()
last_overflow = Tank.get_last_overflow()
obj_Q = integrate.simps(pipe6.outlet_Q[:zero_Q], cfg.t[:zero_Q]) / (last_overflow)
baseline.calc_obj_Q()
baseline.calc_fitness()

runtime.stop()

print('d')

