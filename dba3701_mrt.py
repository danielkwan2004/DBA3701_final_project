import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Define nodes
station_codes = pd.read_csv('mrt_lrt_stations.csv')
# exclude all the stations that LINE_COLOR is not grey
nodes = station_codes[station_codes['LINE_COLOR'] != 'Grey']['ALPHANUMERIC_CODE'].unique().tolist()
nodes.insert(nodes.index('EW33') + 1, 'CG0') # insert CG0 because tanah merah has no CG code but it is an interchange to go to expo/CG
print(len(nodes))

# Define arcs, costs, and capacities
# each node is connected to the next node in the same line, and also to the interchanges
# the nodes have values e.g. NS1, NS2, NS3. NS1 has an arc to NS2, NS2 has an arc to NS3 but NS1 has no arc to NS3.
arcs = []
for i in range(len(nodes) - 1):
    if nodes[i][:2] == nodes[i + 1][:2]:
        arcs.append((nodes[i], nodes[i + 1]))
# print(arcs)
interchanges = [('NS1', 'EW24'), ('NS9', 'TE2'),
                ('NS17', 'CC15'), ('NS21', 'DT11'), ('NS22', 'TE14'), 
               ('NS24', 'NE6'), ('NS24', 'CC1'), ('NS25', 'EW13'), 
               ('NS26', 'EW14'), ('NS27', 'TE20'), ('NS27', 'CE2'),
               ('CC22', 'EW21'), ('EW16', 'NE3'), ('EW16', 'TE17'), 
               ('EW12', 'DT14'), ('EW8', 'CC9'), ('EW4', 'CG0'), 
               ('EW2', 'DT32'), ('CG1', 'DT35'), ('CC19', 'DT9'),
               ('DT10', 'TE11'), ('NE7', 'DT12'), ('DT15', 'CC4'),
               ('DT16', 'CE1'), ('DT19', 'NE4'), ('DT26', 'CC10'),
               ('CC29', 'NE1'), ('CC17', 'TE9'), ('CC13', 'NE12'),
               ('CC1', 'NE6'), ('CE2', 'TE20'), ('NE3', 'TE17'), 
               ]
for interchange in interchanges:
    arcs.append(interchange)
# since all arcs are bidirectional, need to include the other direction as well.
for arc in arcs.copy():
    arcs.append((arc[1], arc[0]))
# print(arcs)

# arcs include the connected train stations AND the interchanges e.g. tampines has green and blue

# Costs for each arc 
# taken from the dataset that has the timings between stations,
# including transfer timings

station_timings_coost = pd.read_csv('station_costs.csv')
costs = {
    (1, 2): 4,
    (1, 3): 4,
    (2, 3): 2,    
    (2, 4): 2,
    (3, 4): 1,
    (3, 5): 3,
    (2, 5): 6,
    (4, 5): 2
}

# # Capacities for each arc
# capacities = {
#     (1, 2): 15,
#     (1, 3): 8,
#     (2, 3): GRB.INFINITY,
#     (2, 4): 4,
#     (3, 4): 15,
#     (3, 5): 5,
#     (2, 5): 10,
#     (4, 5): GRB.INFINITY
# }

# # Supply and demand at each node 
# supply = {
#     1: GRB.INFINITY,  # supply node
#     2: 0,
#     3: 0,
#     4: 0,  # demand node
#     5: GRB.INFINITY  # demand node
# }

# # Create the model
# m = gp.Model('maximize_profit')

# # Create flow variables
# flow = m.addVars(arcs,ub=[capacities[arc] for arc in arcs])
# selling_amount = m.addVar(name="selling_amount")

# # Flow conservation constraints at nodes 
# for i in supply:
#     if (i == 1):
#         m.addConstr(flow.sum(i, '*') == selling_amount)
#     elif (i == 5):
#         m.addConstr(flow.sum('*', i) == selling_amount)
#     else:
#         m.addConstr(flow.sum(i, '*') - flow.sum('*', i) == 0)

# # Set Objective
# m.setObjective(selling_amount*11 - gp.quicksum(costs[arc]*flow[arc] for arc in arcs), GRB.MAXIMIZE)

# # Optimize the model
# m.optimize()

# # Print the solution
# print("---------------------------------")
# print("Optimal flow and cost:")
# print(selling_amount.VarName, selling_amount)
# print(f"Total profit: {m.objVal}")
