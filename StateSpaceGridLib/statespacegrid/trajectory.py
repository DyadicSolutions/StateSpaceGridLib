from dataclasses import dataclass
from typing import List

@dataclass()
class StateSpace:
    x_range: List
    y_range: List

class Trajectory:

    def __init__(self, x_range: List = [1,2,3,4], y_range: List = [1,2,3,4], states: List = [], times: List = [0.0]):
        self.state_space = StateSpace(x_range, y_range)

        self.states = states
        self.times = times

        self.__internal_validity_check()
    
    def __internal_validity_check(self):
        if not all(map(lambda state: len(state) == 2, self.states)):
            raise ValueError("The states should be supplied as a list of (x_value, y_value) pairs")
        if len(self.states) != len(self.times) -1:
            raise ValueError("The number of states should be equal to the number of timestamps minus 1")
        if not all(map(lambda time: isinstance(time, (int, float)), self.times)):
            raise ValueError("Times are expected as integers or floats")
        if not all(map(lambda state: state[0] in self.state_space.x_range and state[1] in self.state_space.y_range, self.states)):
            raise ValueError("All provided state points should fall within the ranges provided in x_range and y_range")

