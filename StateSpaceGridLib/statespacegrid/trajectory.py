"""Module containing definitions of a Trajectory and the state space in which that trajectory applies.

Trajectories are the building blocks of StateSpaceGridLib.
These objects describe the path of a dyad through a state space.

Typical usage example:

    traj = trajectory.Trajectory(
                x_range=["bad", "ok", "good"],
                y_range=[0, 1, 2],
                states=[("ok", 1), ("bad", 0), ("bad", 1), ("bad", 2), ("ok", 2), ("good", 2), ("good", 1), ("good", 0), ("ok", 0)],
                times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                )

    print(measure.get_measures(traj))

"""
from dataclasses import dataclass
from typing import List, Tuple

@dataclass()
class StateSpace:
    x_range: List
    y_range: List

class Trajectory:
    """
    Trajectory class to hold a single trajectory plus an idea of the state space it lies in.

    Attributes:
        state_space: An object holding all possible state values in the x and y axes
        states: A list of (x, y) pairs where x and y are members of state_space.x_range and
                state_space.y_range respectively
        times: A list of integers or floats giving the timestamps of the state transitions.
               These are fenceposts (ie. fall at either side of each state) so there should
               be N+1 of these, where N is the number of states
    """

    def __init__(self, x_range: List = [1,2,3,4], y_range: List = [1,2,3,4], states: List = [], times: List = [0.0]):
        self.state_space = StateSpace(x_range, y_range)

        self.states = states
        self.times = times

        self.__internal_validity_check()

    def __internal_validity_check(self):
        """Checks all values in object to ensure trajectory is valid"""
        if not all(map(lambda state: isinstance(state, (tuple, list)), self.states)):
            raise ValueError("The states should be supplied as a list of (x_value, y_value) tuple or list pairs")
        if not all(map(lambda state: len(state) == 2, self.states)):
            raise ValueError("The states should be supplied as a list of (x_value, y_value) pairs")
        if len(self.states) != len(self.times) -1:
            raise ValueError("The number of states should be equal to the number of timestamps minus 1")
        if not all(map(lambda time: isinstance(time, (int, float)), self.times)):
            raise ValueError("Times are expected as integers or floats")
        if not all(map(lambda state: state[0] in self.state_space.x_range and state[1] in self.state_space.y_range, self.states)):
            raise ValueError("All provided state points should fall within the ranges provided in x_range and y_range")
        if not all(map(lambda time_pair: time_pair[0] < time_pair[1], zip(self.times, self.times[1:]))):
            raise ValueError("Times should appear in ascending order")

    def get_visits(self) -> List[Tuple]:
        """Returns a list of all visits to states. A visit is defined as 1 or more consecutive events in the same state"""
        return [self.states[0]] + [state_pair[1] for state_pair in zip(self.states, self.states[1:]) if state_pair[0] != state_pair[1]]

    def get_visit_times(self) -> List[int | float]:
        """Returns a list of times for all visits to states. A visit is defined as 1 or more consecutive events in the same state"""
        return [self.times[0]] + [self.times[i] for i in range(1, len(self.times)) if i == len(self.states) or self.states[i-1] != self.states[i]]
