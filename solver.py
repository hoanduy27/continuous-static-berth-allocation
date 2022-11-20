import cplex 
from docplex.mp.model import Model 
from instance import *

class Solver(object):
    def __init__(self, problem: Problem):
        self.problem = problem

class LP(Solver):
    def __init__(self, *args, **kwargs):
        super(LP, self).__init__(*args, **kwargs)
        self.model = Model()

    def make_problem(self):
        # Mooring time: Including domain constraint
        self.u = self.model.continuous_var_list(
            self.problem.num_vessels, 
            lb=list(map(lambda vessel: vessel.arrival_time, self.problem.vessels)),
            ub=list(map(lambda vessel: self.problem.plan_time - vessel.processing_time, self.problem.vessels))
        )

        # Berth position: Including domain constraint
        self.v = self.model.continuous_var_list(
            self.problem.num_vessels, 
            lb=0,
            ub=list(map(lambda vessel: self.problem.berth_size - vessel.size, self.problem.vessels))
        )

        # Departure
        self.c = self.model.continuous_var_list(
            self.problem.num_vessels, 
            lb=0, 
            ub=cplex.infinity
        )
        sigma = self.model.binary_var_matrix(
            self.problem.num_vessels, self.problem.num_vessels,
        )
        delta = self.model.binary_var_matrix(self.problem.num_vessels, self.problem.num_vessels)
        gamma = self.model.binary_var_matrix(self.problem.num_vessels, self.problem.num_breaks)


        # CONSTRAINTS
        ## Vessel constraints
        self.model.add_constraints(
            (self.u[j] - self.u[i] - self.problem.vessels[i].processing_time - (sigma[(i,j)] - 1)*self.problem.plan_time >= 0 
            for i,j in sigma if i!=j) 
        )
        self.model.add_constraints(
            (self.v[j] - self.v[i] - self.problem.vessels[i].size - (delta[(i,j)] - 1)*self.problem.berth_size >= 0 
            for i,j in delta if i!=j) 
        )

        ## Overlapping constraints
        self.model.add_constraints(
            (sigma[(i,j)] + sigma[(j,i)] <= 1  
            for i,j in sigma if i!=j) 
        )

        self.model.add_constraints(
            (delta[(i,j)] + delta[(j,i)] <= 1  
            for i,j in delta if i!=j) 
        )

        self.model.add_constraints(
            (sigma[(i,j)] + sigma[(j,i)] + delta[(i,j)] + delta[(j,i)] >= 1  
            for i,j in delta if i!=j) 
        )

        ## Departure constraint
        self.model.add_constraints(
            (self.problem.vessels[i].processing_time + self.u[i] == self.c[i] 
            for i in range(self.problem.num_vessels)) 
        )

        ## Decision variable domain (gamma)
        self.model.add_constraints(
            (self.problem.breaks[k].pos * gamma[(i,k)] <=  self.v[i] + self.problem.vessels[i].size 
            for i,k in gamma)
        )

        ## Intermidiate variable constraints
        self.model.add_constraints(
            (self.problem.breaks[k].pos - self.v[i] + self.problem.berth_size * gamma[(i,k)] >=0 
            for i,k in gamma)
        )

        ## Breaks constraints
        for i,k in gamma:
            self.model.add_if_then(
                gamma[(i,k)] == 1,
                self.v[i] >= self.problem.breaks[k].pos, 
            )
            self.model.add_if_then(
                gamma[(i,k)] == 1,
                self.v[i] - self.problem.breaks[k].pos - gamma[(i,k)] * self.problem.berth_size <= 0
            )

            self.model.add_if_then(
                gamma[(i,k)] == 0,
                self.v[i] + self.problem.vessels[i].size <= self.problem.breaks[k].pos,
            )

            self.model.add_if_then(
                gamma[(i,k)] == 0,
                self.v[i] + self.problem.vessels[i].size - self.problem.breaks[k].pos * gamma[(i,k)] >= 0
            )

 
        self.model.minimize(
            sum([self.problem.vessels[i].weight * (self.c[i] - self.problem.vessels[i].arrival_time) for i in range(self.problem.num_vessels)])
        )

        
    def __call__(self):
        self.make_problem()
        # print(self.u)
        sol = self.model.solve()
        # print(self.model.solve_details)
        return sol

if __name__ == "__main__":

    vessels = [
        Vessel(10, 10, 10, 1),
        Vessel(15, 5, 9, 2),
        Vessel(6, 0, 5, 1),
        Vessel(20, 2, 10, 3),
        Vessel(5, 15, 5, 1),
        Vessel(15, 12, 8, 1),
        Vessel(7, 8, 10, 3),
    ]
    breaks = [
        Break(20), Break(32)
    ]
    prob = Problem(40, 30, breaks, vessels)

    # print(prob)

    solver = LP(prob)

    sol = solver()
    print("Mooring time")
    print([var.solution_value for var in solver.u])
    print("Starting berth pos")
    print([var.solution_value for var in solver.v])

    print("Opt value: ", sol.objective_value)