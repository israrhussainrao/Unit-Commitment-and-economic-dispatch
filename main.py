# Name: Israr Hussain
# Std No: 20620032
# Subject: Power System Protection and Control
# Instructor: Professor Dr. Reza Sirjani
# Unit Commitment and Economic Dispatch Python Code for 24 hours of Load Demand


import pandas
import itertools
import numpy as np
from numpy import poly1d
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from scipy.misc import derivative
import prettytable

Units = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']
Units_Data = {
    'min_pw': ['3', '1.3', '1.65', '1.30', '2.25', '0.5', '2.50', '1.10', '2.75', '0.75'],
    'max_pw': ['10', '40', '6', '4.2', '7', '2', '7.5', '3.75', '8.5', '2.5'],
    'a': ['113', '160', '147', '150', '234', '515', '131', '171', '128', '452'],
    'b': ['9.023', '7.654', '8.752', '8.431', '9.223', '7.054', '9.121', '7.762', '8.162', '8.149'],
    'c': ['0.00082','0.0004','0.0006','0.00042','0.00054','0.000175','0.0006','0.0004','0.000725','0.0002']}

Unit_Data_Table = DataFrame(Units_Data, index=Units)
Unit_Data_Table.index.names = ['Units']



Generator_units = [{
    "index": 1, "max_pow": 1000, "min_pow": 300, "a": 113, "b": 9.023, "c": 0.00082, "power_cost": 0
}, {
    "index": 2, "max_pow": 4000, "min_pow": 130, "a": 160, "b": 7.654, "c": 0.0004, "power_cost": 0
}, {
    "index": 3, "max_pow": 600, "min_pow": 165, "a": 147, "b": 8.752, "c": 0.0006, "power_cost": 0
}, {
    "index": 4, "max_pow": 420, "min_pow": 130, "a": 150, "b": 8.431, "c": 0.00042, "power_cost": 0
}, {
    "index": 5, "max_pow": 700, "min_pow": 225, "a": 234, "b": 9.223, "c": 0.00054, "power_cost": 0
}, {
    "index": 6, "max_pow": 200, "min_pow": 50, "a": 515, "b": 7.054, "c": 0.000175, "power_cost": 0
}, {
    "index": 7, "max_pow": 750, "min_pow": 250, "a": 131, "b": 9.121, "c": 0.0006, "power_cost": 0
}, {
    "index": 8, "max_pow": 375, "min_pow": 110, "a": 171, "b": 7.762, "c": 0.0004, "power_cost": 0
}, {
    "index": 9, "max_pow": 850, "min_pow": 275, "a": 128, "b": 8.162, "c": 0.000725, "power_cost": 0
}, {
    "index": 10, "max_pow": 250, "min_pow": 75, "a": 452, "b": 8.149, "c": 0.0002, "power_cost": 0
}]

MAX_HOUR = 24

LAMBDA_MAX = 0.5# we iterate lambda value to reach near to this value.
Error_MAX = 0.01
P_DEL_MAX = 1.0
#Unit_Data_Table

for index, generator_data in Unit_Data_Table.iterrows():
  Incremental_Cost_function = []
  equation = np.poly1d([float(generator_data['c']),float(generator_data['b']), float(generator_data['a'])])
  print(index+' =\n', equation)
  Incremental_Cost = equation.deriv()
  print(f"Incremental Cost = {Incremental_Cost}")
  print('-----------------------')
  Incremental_Cost_function.append(Incremental_Cost)


class Generator:
    def __init__(self, index=0, max_pow=0, min_pow=0, a=0, b=0, c=0, power_cost=0, curr_generation=0):
        self.index = index
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.a = a
        self.b = b
        self.c = c
        self.flapc = 0
        self.power_cost = power_cost
        self.curr_generation = curr_generation

    def Cost(self,
             power):  # its a cost function in order to calculate cost after calculating generated power of ON generators.
        return self.a + self.b * power + self.c * power * power


class Suitable_state:
    def __init__(self, power_cost=0, f_cost=0,prev_state=None, is_feasible=False, avl_generators={}):
        self.power_cost = power_cost
        self.f_cost = f_cost
        self.prev_state = prev_state
        self.is_feasible = False
        self.avl_generators = {}


def EconomicDispatch(gvn_gens, p_demand):
    lmb = LAMBDA_MAX
    error = Error_MAX
    p_del = P_DEL_MAX
    p_total = 0
    sum_c = 0
    Generator_units = gvn_gens

    while p_del > error:
        p_total = 0.0
        sum = 0.0
        for i, generator in enumerate(gvn_gens):

            Generator_units[i].curr_generation = (lmb - generator.b) / (2 * generator.c)

            if Generator_units[i].curr_generation > generator.max_pow:
                Generator_units[i].curr_generation = generator.max_pow

            if Generator_units[i].curr_generation < generator.min_pow:
                Generator_units[i].curr_generation = generator.min_pow

            p_total = Generator_units[i].curr_generation + p_total
            sum = (sum + 1.0) / (2.0 * generator.c)

        p_del = p_demand - p_total
        lmb = lmb + p_del / sum

    _state = Suitable_state(power_cost=0, f_cost=0, prev_state=None, is_feasible=None, avl_generators={})
    _state.load = p_demand
    for i, units in enumerate(Generator_units):
        _state.power_cost = _state.power_cost + gvn_gens[i].Cost(units.curr_generation)
        _state.avl_generators[i] = units.curr_generation
    return _state


generator_unit = Generator_units
MAX_GEN = len(generator_unit)
Generator_units = []
for i in range(MAX_GEN):
    Generator_units.append(Generator(
        index=generator_unit[i]['index'],
        max_pow=generator_unit[i]['max_pow'],
        min_pow=generator_unit[i]['min_pow'],
        a=generator_unit[i]['a'],
        b=generator_unit[i]['b'],
        c=generator_unit[i]['c'],
        power_cost=generator_unit[i]['power_cost']))

# input the load for 24 hours
load = Load_demand = [2796, 2643, 2655, 2450, 2459, 2492, 2447, 2532, 2502, 2708, 3069, 2882, 3128, 2802, 2957, 3002,
                      2775,
                      2934, 2850, 3005, 3381, 3296, 3375, 3222]

Generator_values = {
    'Power_min': [],
    'Power_max': [],
    'Gen_Power1': [],
    'Gen_Power2': [],
    'Gen_Power5': [],
    'Gen_Power6': [],
    'Gen_Power7': [],
    'Gen_Power8': [],
    'Gen_Power9': [],
    'Gen_Power10': [],
    'power_cost': []
}

values_table = DataFrame(Generator_values)
binary_combination = list(itertools.product([0, 1], repeat=10))
combination = DataFrame(binary_combination, columns=Units)
Data_table = pandas.concat([combination, values_table])

for generator in Generator_units:
    generator.flapc = generator.Cost(generator.max_pow) / generator.max_pow

# sort generators using the flapc attribute
Generator_units.sort(key=lambda x: x.flapc)
gen_index = [el.index for el in Generator_units]

all_states = [[Suitable_state(is_feasible=False) for x in range(MAX_HOUR)] for y in range(MAX_GEN)]
s_costs = [[0 for x in range(MAX_GEN)] for y in range(MAX_GEN)]

# calculating the p_cost of each state and the generator's generating values
for hour in range(MAX_HOUR):
    for i, gen in enumerate(Generator_units):
        max_capacity = sum(x.max_pow for x in Generator_units[0:(i + 1)])
        if load[hour] <= max_capacity:
            all_states[i][hour] = EconomicDispatch(Generator_units[0:(i + 1)], load[hour])
            all_states[i][hour].is_feasible = True

# finding the transition cost
for i in range(MAX_GEN):
    for j in range(MAX_GEN):
        if i >= j:
            s_costs[i][j] = 0
        else:
            for k in range(i + 1, j):
                s_costs[i][j] = s_costs[i][j] + Generator_units[k].power_cost

# finding the F cost for the first hour
for i in range(MAX_GEN):
    all_states[i][0].f_cost = all_states[i][0].p_cost
    for k in range(0, i):
        all_states[i][0].f_cost = all_states[i][0].f_cost + Generator_units[i].power_cost

for hour in range(1, MAX_HOUR):

    for i in range(MAX_GEN):

        # finding the first feasible state in the previous hour
        first_feasible = 0
        for first_feasible in range(MAX_GEN):
            if all_states[first_feasible][hour - 1].is_feasible == True:
                break

        min_cost = all_states[first_feasible][hour - 1].f_cost + s_costs[first_feasible][i]
        min_index = first_feasible

        # finding the minimum of all the feasible states
        for next_feasible in range(min_index, MAX_GEN):
            if all_states[next_feasible][hour - 1].is_feasible and min_cost > all_states[next_feasible][
                hour - 1].f_cost + s_costs[next_feasible][i]:
                min_cost = all_states[next_feasible][hour - 1].f_cost + s_costs[next_feasible][i]
                min_index = next_feasible

        all_states[i][hour].f_cost = all_states[i][hour].p_cost + min_cost
        all_states[i][hour].prev_state = min_index

# find first feasible state at 24th hour
feasible_state = 0;
for feasible_state in range(MAX_GEN):
    if all_states[first_feasible][MAX_HOUR - 1].is_feasible == True:
        feasible_state = first_feasible

# Store the final state for 24th hr by finding minimum of all states
final_states = [Suitable_state() for x in range(MAX_HOUR)]
final_states[MAX_HOUR - 1] = all_states[feasible_state][MAX_HOUR - 1];

for i in range(feasible_state, MAX_GEN):
    if final_states[MAX_HOUR - 1].f_cost > all_states[i][MAX_HOUR - 1].f_cost and all_states[i][
        MAX_HOUR - 1].is_feasible:
        final_states[MAX_HOUR - 1] = all_states[i][MAX_HOUR - 1]

# backtracking the states for the previous hours
for i in range(MAX_HOUR - 2, -1, -1):
    final_states[i] = all_states[final_states[i + 1].prev_state][i]

columns = ['Hour', 'load', 'P cost', 'F cost']
for i in range(0, MAX_GEN):
    columns.append("Generator - " + str(gen_index[i]))
table = prettytable.PrettyTable(columns)

for i, state in enumerate(final_states):
    row = [i + 1, state.load, state.p_cost, state.f_cost]
    for j in range(MAX_GEN):
        if j in state.avl_generators:
            row.append(state.avl_generators[j])
        else:
            row.append(0)
    table.add_row(row)

print(table)


