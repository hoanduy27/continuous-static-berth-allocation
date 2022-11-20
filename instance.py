from typing import List
import cplex 
from docplex.mp.model import Model


class Vessel:
    def __init__(self, index, size, arrival_time, processing_time, weight):
        self.index = index
        self.size = size
        self.arrival_time = arrival_time
        self.processing_time = processing_time
        self.weight = weight

    def __str__(self):
        return f"Vessel(index=%s, size=%s, arrival_time=%s, processing_time=%s, weight=%s)" % (self.index, self.size, self.arrival_time, self.processing_time, self.weight)

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
    def __init__(
        self, 
        berth_size: int, 
        plan_time: int, 
        breaks: List[Break], 
        vessels: List[Vessel]
    ):
        self.berth_size = berth_size
        self.plan_time = plan_time
        self.breaks = breaks
        self.vessels = vessels

    def assert_input(self):
        assert all([brk.pos > 0 and brk.pos < self.berth_size for brk in self.breaks])

    @property
    def num_breaks(self):
        return len(self.breaks)

    @property
    def num_vessels(self):
        return len(self.vessels)

    def __str__(self):
        return f"Problem(\n\tberth_size=%s,\n\tplan_time=%s,\n\tbreaks=%s,\n\tvessels=%s\n)" % (self.berth_size, self.plan_time, self.breaks, self.vessels)
        
    def __repr__(self) -> str:
        return self.__str__()

    @classmethod 
    def from_file(cls, infile):
        TIME = 'Time allocation'
        BERTH_SIZE = "Berth length"
        BERTH_BREAKS =  "Berth breaks"
        VESSELS = "Vessel_index"

        with open(infile, 'r') as f:
            breaks = []
            vessels = []
            reader_state = None
            for line in f:
                if TIME in line:
                    reader_state = TIME
                    continue
                elif BERTH_SIZE in line:
                    reader_state = BERTH_SIZE
                    continue
                elif BERTH_BREAKS in line:
                    reader_state = BERTH_BREAKS
                    continue
                elif VESSELS in line:
                    reader_state = VESSELS
                    continue
                elif line != '\n':
                    if reader_state == TIME:
                        plan_time = float(line.strip())
                    
                    elif reader_state == BERTH_SIZE:
                        berth_size = float(line.strip())

                    elif reader_state == BERTH_BREAKS:
                        pos = float(line.strip())
                        breaks.append(Break(pos))
                    
                    else:
                        vessel_info = line.strip().split('\t')
                        if len(vessel_info) == 4:
                            index, size, arrival_time, processing_time, weight = vessel_info + [1]
                        elif len(vessel_info) == 5:
                            index, size, arrival_time, processing_time, weight = vessel_info
                        else:
                            raise ValueError
                        
                        vessels.append(Vessel(index, float(size), float(arrival_time), float(processing_time), float(weight)))
        
        return Problem(berth_size, plan_time, breaks, vessels)

       
