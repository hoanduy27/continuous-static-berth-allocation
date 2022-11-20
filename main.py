from solver import *
from instance import *
import sys 


def solve(infile, outfile):
    problem = Problem.from_file(infile)
    solver = LP(problem)
    solution = solver()
    cost = solution.objective_value
    mooring_times = [u_i.solution_value for u_i in solver.u]
    berth_positions = [v_i.solution_value for v_i in solver.v]


    with open(outfile, 'w') as f:
        f.write('% Vessel index, mooring time $u_i$, starting berth position occupied $v_i$\n')
        f.writelines([
            '\t'.join([str(index), str(u_i), str(v_i)]) + '\n'
            for index, (u_i, v_i) in enumerate(zip(mooring_times, berth_positions))
        ])
        f.write(f'\nCost: {cost}')

    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        solve(infile, outfile)
    else:
        print("usage: %s <infile> <out file>" % sys.argv[0])

    