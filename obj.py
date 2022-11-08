class Vessel:
    def __init__(self, arrival_time, size, processing_time, weight):
        self.arrival_time = arrival_time
        self.size = size
        self.processing_time = processing_time
        self.weight = weight

    def __str__(self):
        return f"Vessel(arrival_time=%s, size=%s, processing_time=%s, weight=%s)" % (self.arrival_time, self.size, self.processing_time, self.weight)

    def __repr__(self) -> str:
        return self.__str__()

class Break:
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return f"Break(pos=%s)" % (self.pos)

    def __repr__(self) -> str:
        return self.__str__()

class Problem:
    def __init__(self, berth_size, plan_time, breaks, vessels):
        self.berth_size = berth_size
        self.plan_time = plan_time
        self.breaks = breaks
        self.vessels = vessels

    def assert_input(self):
        assert all([brk.pos > 0 and brk.pos < self.berth_size for brk in self.breaks])

    @property
    def num_breaks(self):
        return len(self.breaks)

    def __str__(self):
        return f"Problem(\n\tberth_size=%s,\n\tplan_time=%s,\n\tbreaks=%s,\n\tvessels=%s\n)" % (self.berth_size, self.plan_time, self.breaks, self.vessels)
        
    def __repr__(self) -> str:
        return self.__str__()


class Solution(object):
    def __init__(self, problem):
        self.problem = problem

class GRASP(Solution):
    def __init__(self, *args, **kwargs):
        super(GRASP.__init__(*args, **kwargs), self)




vessels = [
    Vessel(10, 10, 10, 1),
    Vessel(10, 10, 10, 2),
]
breaks = [
    Break(10), Break(20)
]
prob = Problem(30, 100, breaks, vessels)
print(prob)