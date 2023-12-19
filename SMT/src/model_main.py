import os
from z3 import *
import time
from itertools import combinations
import numpy as np

from utils.types_SMT import CorrectSolution, Solution, StatusEnum

def compute_length(x, y, w):
    # Compute the maximum length based on x, y, and w
    max_l = sum(y)
    block_width = w // max(x)
    max_l = -(max_l // - block_width)
    max_l = max(y) if max_l < max(y) else max_l
    return max_l

def open_data(filename):
    # Read instance data from a file
    with open(filename, 'r') as in_file:
        lines = in_file.read().splitlines()

        # Extract data from the file
        w = int(lines[0])
        n = int(lines[1])
        x = [int(line.split(' ')[0]) for line in lines[2:2+n]]
        y = [int(line.split(' ')[1]) for line in lines[2:2+n]]

        # Calculate the maximum length (height) of the plate
        max_l = compute_length(x, y, w)

        # Calculate the magnitude of width for coordinate differentiation
        len_w = len(str(w))
        magnitude_w = 10 ** len_w

        return w, n, x, y, max_l, magnitude_w

def z3_maximum(vector):
    # Find the maximum value in a vector using Z3 expressions
    maximum = vector[0]
    for value in vector[1:]:
        maximum = If(value > maximum, value, maximum)
    return maximum

def z3_cumulative(start, duration, resources, total):
    # Define Z3 cumulative constraints based on start, duration, and resource requirements
    decomposition = []
    for u in resources:
        decomposition.append(sum([
            If(And(start[i] <= u, u < start[i] + duration[i]), resources[i], 0)
            for i in range(len(start))]) <= total)
    return decomposition

def write_output(w, n, x, y, pos_x, pos_y, length, output_file, elapsed_time):
    # Write the solution output to a file
    solution = Solution()
    solution.input_name = output_file
    solution.width = w
    solution.n_circuits = n
    solution.circuits = [[x[i], y[i]] for i in range(n)]
    solution.height = length
    solution.solve_time = elapsed_time
    solution.rotation = rotation
    solution.coords = {
        "pos_x": pos_x,
        "pos_y": pos_y
    }
    solution.status = StatusEnum.SMT
    return solution

def build_model(w, n, x, y, logic="LIA"):
    l_lower = max(max(y), math.ceil(sum([x[i] * y[i] for i in range(n)]) / w))
    l_upper = sum(y)
    lines = []

    # Set logic
    lines.append(f'(set-logic {logic})')

    # Declare variables
    lines += [f'(declare-fun pos_x{i} () Int)' for i in range(n)]
    lines += [f'(declare-fun pos_y{i} () Int)' for i in range(n)]
    lines += [f'(declare-fun l () Int)']

    # Define the length as the maximum y-coordinate among the circuits
    lines += [f'(assert (and (>= pos_x{i} 0) (<= pos_x{i}{w-min(x)})))' for i in range(n)]
    lines += [f'(assert (and (>= pos_y{i} 0) (<= pos_y{i}{l_upper-min(y)})))' for i in range(n)]
    lines.append(f'(assert (and (>= l {l_lower}) (<= l {l_upper})))')

    # Define non-overlapping constraints
    for i  in range(n):
        for j in range(n):
            if i<j:
                lines.append(f'(assert (or (<= (+ pos_x{i} {x[i]}) pos_x{j})'
                             f'(<= (+ pos_y{i} {y[i]}) pos_y{j})'
                             f'(>= (- pos_x{i} {x[j]}) pos_x{j})'
                             f'(>= (- pos_y{i} {y[j]}) pos_y{j})))')
                
    #Define bounding box constraints
    lines += [f'(assert (and (<= (+ pos_x{i} {x[i]}) {w})(<= (+ pos_y{i} {y[i]}) l)))' for i in range(n)]

    #Define cumulative constraints
    for yi in y:
        sum_var = [f'(ite (and (<= pos_y{i} {yi}) (< {yi} (+ pos_y{i} {y[i]}))) {y[i]} 0)' for i in range(n)]
        lines.append(f'(assert (<= (+ {" ".join(sum_var)}) {w}))')

    for xi in x:
        sum_var = [f'(ite (and (<= pos_x{i} {xi}) (< {xi} (+ pos_x{i} {x[i]}))) {x[i]} 0)' for i in range(n)]
        lines.append(f'(assert (<= (+ {" ".join(sum_var)}) l))')

    # Define symmetry constraints
    for i in range(n):
        for j in range(n):
            if i<j:
                lines.append(f'(assert (ite (and (= {x[i]} {x[j]}) (= {y[i]} {y[j]}))'
                             f'(and (<= pos_x{i} pos_x{j}) (<= pos_y{i} pos_y{j})) true))')

    #Symmetry breaking for insertion of max area circuit in (0,0)
    area = [x[i]*y[i] for i in range(n)]
    max_area = area.index(max(area))
    lines.append(f'(assert (= pos_x{max_area} 0))')
    lines.append(f'(assert (= pos_y{max_area} 0))')

    lines.append('(check-sat)')
    for i in range(n):
        lines.append(f'(get-value (pos_x{i}))')
        lines.append(f'(get-value (pos_y{i}))')
    lines.append('(get-value (l))')

    return l_lower, l_upper


def solve(solver, model_type):
    solution = {'solution':{}, 'l_var':None}

    res = solver.solve()
    if not res:
        print("Unsat, search interrupted")
        return None
    
    last_model = solver.get_model()
    var_list = [v[0] for v in last_model]
    l_ind = [str(v) for v in var_list].index('l')
    l_var = var_list[l_ind]
    l, pos_x, pos_y, rot =  last_model[l_ind], [], [], []
    solution['solution'] = {}
def solver(input_file, output_dir):
    instance_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, instance_name + '-out.txt')

    # Load instance data using the open_data function
    w, n, x, y, max_l, w_mag = open_data(input_file)

    # Variables
    pos_x = [Int("pos_x_%s" % str(i + 1)) for i in range(n)]
    pos_y = [Int("pos_y_%s" % str(i + 1)) for i in range(n)]

    # Define the length as the maximum y-coordinate among the circuits
    length = z3_maximum([pos_y[i] + y[i] for i in range(n)])

    # Define Z3 constraints for the plate bounds, coordinate differentiation, cumulative constraints, maximum width,
    # maximum height, overlapping, symmetries, and moving circuits to the left.
    plate_x = [pos_x[i] >= 0 for i in range(n)]
    plate_y = [pos_y[i] >= 0 for i in range(n)]
    alldifferent = [Distinct([w_mag * pos_y[i] + pos_x[i]]) for i in range(n)]
    cumulative_x = z3_cumulative(pos_x, x, y, max_l)
    cumulative_y = z3_cumulative(pos_y, y, x, w)
    max_w = [z3_maximum([pos_x[i] + x[i] for i in range(n)]) <= w]
    max_h = [z3_maximum([pos_y[i] + y[i] for i in range(n)]) <= max_l]
    overlapping = []
    for (i, j) in combinations(range(n), 2):
        overlapping.append(Or(pos_x[i] + x[i] <= pos_x[j], pos_x[j] + x[j] <= pos_x[i],
                              pos_y[i] + y[i] <= pos_y[j], pos_y[j] + y[j] <= pos_y[j]))
    symmetry = [And(pos_x[np.argmax(np.asarray(y))] == 0, pos_y[np.argmax(np.asarray(y))] == 0)]
    move_left = [sum([If(pos_x[i] <= w // 2, x[i] * y[i], 0) for i in range(n)]) >=
                 sum([If(pos_x[i] > w // 2, x[i] * y[i], 0) for i in range(n)])]

    # Optimizer
    optimizer = Optimize()
    optimizer.add(plate_x + plate_y + alldifferent + overlapping + cumulative_x + cumulative_y +
                  max_w + max_h + symmetry + move_left)
    optimizer.minimize(length)

    # Execution time
    timeout = 300000
    optimizer.set("timeout", timeout)

    # Solving
    print(f'{output_file}:', end='\t', flush=True)
    starting_time = time.time()

    p_x, p_y = [], []
    if optimizer.check() == sat:
        model = optimizer.model()
        elapsed_time = time.time() - starting_time
        print(f'{elapsed_time * 1000:.1f} ms')
        # Get variable values
        for i in range(n):
            p_x.append(model.evaluate(pos_x[i]).as_string())
            p_y.append(model.evaluate(pos_y[i]).as_string())
        solution_len = model.evaluate(length).as_string()

        write_output(w, n, x, y, p_x, p_y, solution_len, output_file, elapsed_time)
    else:
        elapsed_time = time.time() - starting_time
        print(f'{elapsed_time*1000:.1f} ms')
        print("No Solution")

def main():
    input_file = "../../data/instances/ins-1.txt"
    output_dir = "../out"
    solver(input_file, output_dir)

if __name__ == '__main__':
    main()