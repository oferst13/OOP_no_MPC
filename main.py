import copy
from scipy import integrate
import funx
from tank import Tank
from pipe import Pipe
from node import Node
import cfg
import numpy as np
from timer import Timer

runtime = Timer()
runtime.start()
demands = np.array([])
for demand in cfg.demands_3h:
    demands = np.append(demands, np.ones(int(cfg.demand_dt / cfg.dt)) * (demand * (cfg.dt / cfg.demand_dt)))
demand_PD = demands * cfg.PD / 100

tank1 = Tank('tank1', 30, 0, 9000, 180)
tank2 = Tank('tank2', 35, 0, 10000, 190)
tank3 = Tank('tank3', 25, 0, 8500, 150)
tank4 = Tank('tank4', 50, 0, 14000, 650)

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

tot_Q = np.zeros(cfg.sim_len, dtype=np.longfloat)
# Create forecast - currently real rain only!
forecast_rain = funx.set_rain_input('09-10.csv', cfg.rain_dt, cfg.sim_len)
for tank in Tank.all_tanks:
    tank.set_inflow_forecast(forecast_rain)  # happens once a forecast is made
    tank.set_daily_demands(demand_PD)  # happens only once

# starting main sim loop

for i in range(cfg.sim_len):
    if sum(forecast_rain[int(i // (cfg.rain_dt / cfg.dt)):-1]) + Tank.get_tot_storage() == 0:
        break  # this should break forecast run only!
    for tank in Tank.all_tanks:
        current_rain_volume = tank.inflow_forecast[int(i // (cfg.rain_dt / cfg.dt))] * (cfg.dt / cfg.rain_dt)
        tank.tank_fill(current_rain_volume, i)
        tank.rw_use(tank.daily_demands[i % tank.daily_demands.shape[0]], i)
    if i < 1 or (Pipe.get_tot_Q(i - 1) + Tank.get_tot_overflow(i)) < 1e-4:
        continue
    for node in Node.all_nodes:
        node.handle_flow(i)
        for pipe in node.giving_to:
            pipe.calc_q_outlet(i)
mass_balance_err = 100 * (abs(integrate.simps(pipe6.outlet_Q * cfg.dt, cfg.t[:-1]) - Tank.get_cum_overflow())) / Tank.get_cum_overflow()
print(f"Mass Balance Error: {mass_balance_err:0.2f}%")
runtime.stop()
print('d')
