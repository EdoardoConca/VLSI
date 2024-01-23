
import numpy as np
import matplotlib.pyplot as plt
from z3 import *
from itertools import combinations
from timeit import default_timer as timer
from tqdm import tqdm
import time as system_time
import os
from utils_sat import *
import re
from matplotlib import patches
from matplotlib.patches import Rectangle
import matplotlib.colors as colors
import random
import warnings
warnings.filterwarnings('ignore')


def solverSAT(problem_number,instance_dir,out_dir, plot=False):

    instance_file = os.path.join(instance_dir, f'ins-{problem_number}' + '.txt')
    instance_filename = f'ins-{problem_number}'
    out_file = os.path.join(out_dir,instance_filename + '-out.txt')
    print('INSTANCE-' + str(problem_number))

    w, n, chips_w, chips_h, circuits, min_h, max_h = load_file(instance_file)

    identical_circuits = find_identical_circuits_with_count(chips_w, chips_h)
    
    print(chips_h,chips_w,circuits)

    for h in range(min_h, max_h):

        # VARIABLES

        cells = [[[Bool(f"cell_{i}_{j}_{k}") for k in range(n)] for j in range(w)] for i in range(h)]
        print("variables:", n * w * h)
        print("current h: ", h)
        
        # SOLVER

        solver = Solver()
        start_time = system_time.time()

        # CONSTRAINTS

        #C1 - Unique Circuit Placement
       
        for i in tqdm(range(h), desc='Constraint 1: Unique Circuit Placement', leave=False):
            for j in range(w):
                solver.add(exactly_one([cells[i][j][k] for k in range(n)]))

        #C2 - Valid Circuit Positioning
        
        for k in tqdm(range(n), desc='Constraint 2: Valid Circuit Positioning', leave=False):
            possible_cells = []
            for x in range(h - chips_h[k] + 1):
                for y in range(w - chips_w[k] + 1):
                    possible_cells.append(And([cells[x + i][y + j][k] for j in range(chips_w[k]) for i in range(chips_h[k])]))
            solver.add(at_least_one(possible_cells))

        
        # C3 - Priority Placement for Largest Circuit
        
        areas = [chips_h[i] * chips_w[i] for i in range(n)]  # calculate areas
        largest_c = np.argmax(areas)  # find the index of the largest area
        for i in tqdm(range(chips_h[largest_c]), desc='Constraint 3: set largest circuit first', leave=False):
            for j in range(chips_w[largest_c]):
                for k in range(n):
                    if k == largest_c:
                        solver.add(cells[i][j][k])
                    else:
                        solver.add(Not(cells[i][j][k]))
        
        #C4 - symmetry breaking 
        for _, (indices, count) in tqdm(identical_circuits.items(), desc='Constraint 4: symmetry breaking', leave=False):
            if count > 1:
                for i in range(1, count):
                    circuit_idx = indices[i]
                    previous_circuit_idx = indices[i-1]
                    for x in range(h):
                        for y in range(w):
                            # If the current circuit is placed in (x, y), the previous identical circuit must be placed somewhere before
                            previous_positions = [cells[prev_x][prev_y][previous_circuit_idx] for prev_x in range(h) for prev_y in range(y)] + \
                                                 [cells[prev_x][y][previous_circuit_idx] for prev_x in range(x)]
                            solver.add(Implies(cells[x][y][circuit_idx], Or(previous_positions)))

        
        # maximum time of execution
        timeout = 300000
        solver.set("timeout", timeout)


        # Check the solver and process the result
        print('Checking the model...')
        #RESOLUTION
        outcome = solver.check()
        
        if outcome == sat:
            elapsed_time = system_time.time() - start_time
            print("SATISFIABLE in {:.2f} seconds".format(elapsed_time))
            m = solver.model()
            p_x_sol, p_y_sol, rot_sol = model_to_coordinates(m, cells, w, h, n)
            circuits_pos = [(p_x_sol[i], p_y_sol[i]) for i in range(len(p_x_sol))]
            write_file(w,n,chips_w,chips_h,circuits_pos,rot_sol,h,elapsed_time,out_file)
            circuits = list(zip(chips_w, chips_h))
            print_circuit_info(circuits_pos, circuits,rot_sol)
            if plot:
                plot_solution_without_rotation(circuits_pos, chips_w, chips_h,w, h)
            return (w, h, circuits_pos, rot_sol, chips_w, chips_h, n,circuits, system_time.time() - start_time)
        else:
            print("UNSATISFIABLE")
            break

    print("Execution completed or timeout reached")
    return None,None,None,None,None,None,None,None


