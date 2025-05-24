"""Module containing definitions of trajectory measures, and a dataclass to store all the measures for a trajectory

Measures are the various properties calculated from a trajectory or set of trajectories. They are as follows:

- mean trajectory duration: The mean duration of all trajectories provided to get_measures or get_mean_duration
- mean number of events: The mean number of events in the trajectories provided to get_measures or get_mean_num_events
- mean number of visits: The mean number of events in a state across all trajectories provided to get_measures or get_mean_num_visits. Consecutive events in the same state count as a single visit
- mean state range: The mean number of unique states visited by the trajectories provided to get_measures or get_mean_state_range
- total state range: The total number of unique states visited across all trajectories provided to get_measures or get_total_state_range
- mean event duration: The mean duration of an event for a single trajectory, averaged across all trajectories provided to get_measures or get_mean_event_duration
- mean visit duration: The mean duration of a visit to a state for a single trajectory, averaged across all trajectories provided to get_measures or get_mean_visit_duration. Consecutive events in the same state count as a single visit
- mean state duration: The mean time spent in a state for a single trajectory, averaged across all trajectories provided to get_measures or get_mean_state_duration. This does not include states not visited in the state space.
- mean dispersion: Mean dispersion of a trajectory, averaged across all trajectories provided to get_measures or get_mean_dispersion.

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
from itertools import chain
import statistics
from collections import defaultdict

from statespacegrid.trajectory import Trajectory

@dataclass()
class Measures:
    mean_trajectory_duration: float
    mean_number_of_events: float
    mean_number_of_visits: float
    mean_cell_range: float
    total_cell_range: int
    mean_event_duration: float
    mean_visit_duration: float
    mean_state_duration: float
    mean_dispersion: float

def validate_trajectories(*trajs: Trajectory):
    """Checks that state spaces are consistent across all provided trajectories"""

    if len(trajs) == 0:
        raise ValueError("You must provide at least 1 trajectory")

    x_ranges = set(chain(*(traj.state_space.x_range for traj in trajs)))
    if not all(map(lambda traj: set(traj.state_space.x_range) == x_ranges, trajs)):
        raise ValueError("The state spaces of all provided trajectories must match")

    y_ranges = set(chain(*(traj.state_space.y_range for traj in trajs)))
    if not all(map(lambda traj: set(traj.state_space.y_range) == y_ranges, trajs)):
        raise ValueError("The state spaces of all provided trajectories must match")

    first_traj_x_range = trajs[0].state_space.x_range
    if not all(map(lambda traj: all(len(set(comp)) == 1 for comp in zip(first_traj_x_range, traj.state_space.x_range)), trajs[1:])):
        raise ValueError("The order of states should be the same in all state spaces in the provided trajectories")

    first_traj_y_range = trajs[0].state_space.y_range
    if not all(map(lambda traj: all(len(set(comp)) == 1 for comp in zip(first_traj_y_range, traj.state_space.y_range)), trajs[1:])):
        raise ValueError("The order of states should be the same in all state spaces in the provided trajectories")

def _get_mean_trajectory_duration(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: traj.times[-1] - traj.times[0], trajs))

def get_mean_trajectory_duration(*trajs: Trajectory) -> float:
    validate_trajectories(*trajs)
    return _get_mean_trajectory_duration(*trajs)

def _get_mean_number_of_events(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: len(traj.states), trajs))

def get_mean_number_of_events(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_number_of_events(*trajs)

def _get_mean_number_of_visits(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: len(traj.get_visits()), trajs))

def get_mean_number_of_visits(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_number_of_visits(*trajs)

def _get_mean_cell_range(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: len(set(traj.states)), trajs))

def get_mean_cell_range(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_cell_range(*trajs)

def _get_total_cell_range(*trajs: Trajectory) -> int:
    return len({state for traj in trajs for state in traj})

def get_total_cell_range(*trajs: Trajectory) -> int:
	validate_trajectories(*trajs)
	return _get_total_cell_range(*trajs)

def _get_mean_event_duration(*trajs: Trajectory) -> float:
    return statistics.mean(
         map(
              lambda traj: statistics.mean(
                map(lambda time_pairs: time_pairs[1] - time_pairs[0], zip(traj.times, traj.times[1:]))),
              trajs
            )
        )

def get_mean_event_duration(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_event_duration(*trajs)

def _get_mean_visit_duration(*trajs: Trajectory) -> float:
    return statistics.mean(
         map(
              lambda traj: statistics.mean(
                   map(lambda time_pairs: time_pairs[1] - time_pairs[0], zip(traj.get_visit_times(), traj.get_visit_times()[1:]))),
              trajs
            )
        )

def get_mean_visit_duration(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_visit_duration(*trajs)

def __get_state_durations(traj: Trajectory) -> defaultdict:
    state_durations = defaultdict(float)
    for t_start, t_end, state in zip(traj.times, traj.times[1:], traj.states):
        state_durations[state] += t_end - t_start
    return state_durations

def _get_mean_state_duration(*trajs: Trajectory) -> float:
    return statistics.mean(
         map(lambda traj: statistics.mean(__get_state_durations(traj).values()), trajs)
    )

def get_mean_state_duration(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_state_duration(*trajs)

def __get_dispersion(traj: Trajectory) -> float:
    state_space_size = len(traj.state_space.x_range) * len(traj.state_space.y_range)
    return 1 - ((
         state_space_size * (
              sum(
                   map(lambda d: pow(d/(traj.times[-1] - traj.times[0]), 2), __get_state_durations(traj).values())
                   )
                ) - 1) / (state_space_size - 1))

def _get_mean_dispersion(*trajs: Trajectory) -> float:
    return statistics.mean(map(__get_dispersion, trajs))

def get_mean_dispersion(*trajs: Trajectory) -> float:
	validate_trajectories(*trajs)
	return _get_mean_dispersion(*trajs)

def get_measures(*trajs: Trajectory) -> Measures:
    validate_trajectories(*trajs)
    return Measures(
        mean_trajectory_duration = _get_mean_trajectory_duration(*trajs),
        mean_number_of_events = _get_mean_number_of_events(*trajs),
        mean_number_of_visits=_get_mean_number_of_visits(*trajs),
        mean_cell_range=_get_mean_cell_range(*trajs),
        total_cell_range=_get_total_cell_range(*trajs),
        mean_event_duration=_get_mean_event_duration(*trajs),
        mean_visit_duration=_get_mean_visit_duration(*trajs),
        mean_state_duration=_get_mean_state_duration(*trajs),
        mean_dispersion=_get_mean_dispersion(*trajs)
    )