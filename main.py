from solver import *
from instance import *
import sys 
import time
import math
import os

def solve(infile, outfile):
    if os.path.exists(outfile):
        exit(f"{outfile} already exists")
    problem = Problem.from_file(infile)
    if problem.num_vessels > 18 or problem.num_breaks > 18:
        exit(f"Skip {infile}")
    print(f"Running {infile}")
    solver = LP(problem)
    begin_s = time.time()
    solution = solver()
    end_s = time.time()
    cost = solution.objective_value
    mooring_times = [int(round(u_i.solution_value, 0)) for u_i in solver.u]
    berth_positions = [int(round(v_i.solution_value, 0)) for v_i in solver.v]


    with open(outfile, 'w') as f:
        f.write('% Vessel index, mooring time $u_i$, starting berth position occupied $v_i$\n')
        f.writelines([
            '\t'.join([str(index), str(u_i), str(v_i)]) + '\n'
            for index, (u_i, v_i) in enumerate(zip(mooring_times, berth_positions))
        ])
        f.write(f'\nOur cost = {int(round(cost, 0))}\n')
        f.write(f'Time = {end_s - begin_s}')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        solve(infile, outfile)
    else:
        print("usage: %s <infile> <out file>" % sys.argv[0])

    