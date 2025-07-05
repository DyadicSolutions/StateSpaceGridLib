"""Module containing definitions of trajectory measures, and a dataclass to store all the measures for a trajectory

Measures are the various properties calculated from a trajectory or set of trajectories. They are as follows:

- mean trajectory duration: The mean duration of all trajectories provided to get_measures or get_mean_trajectory_duration
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
import statistics
from collections import defaultdict

from statespacegrid.trajectory import Trajectory, validate_trajectories

@dataclass()
class Measures:
    """
    Measures class to hold all measures for a trajectory or collection of trajectories.

    Attributes:
        mean_trajectory_duration: The mean duration of all trajectories provided
        mean_number_of_events: The mean number of events in the trajectories provided to get_measures or get_mean_num_events
        mean_number_of_visits: The mean number of events in a state across all trajectories provided. Consecutive events in the same state count as a single visit
        mean_state_range: The mean number of unique states visited by the trajectories provided
        total_state_range: The total number of unique states visited across all trajectories provided
        mean_event_duration: The mean duration of an event for a single trajectory, averaged across all trajectories provided
        mean_visit_duration: The mean duration of a visit to a state for a single trajectory, averaged across all trajectories provided. Consecutive events in the same state count as a single visit
        mean_state_duration: The mean time spent in a state for a single trajectory, averaged across all trajectories provided. This does not include states not visited in the state space.
        mean_dispersion: Mean dispersion of a trajectory, averaged across all trajectories provided
    """
    mean_trajectory_duration: float
    mean_number_of_events: float
    mean_number_of_visits: float
    mean_state_range: float
    total_state_range: int
    mean_event_duration: float
    mean_visit_duration: float
    mean_state_duration: float
    mean_dispersion: float

def _get_mean_trajectory_duration(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: traj.times[-1] - traj.times[0], trajs))

def get_mean_trajectory_duration(*trajs: Trajectory) -> float:
    """Get the mean duration of all trajectories"""
    validate_trajectories(*trajs)
    return _get_mean_trajectory_duration(*trajs)

def _get_mean_number_of_events(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: len(traj.states), trajs))

def get_mean_number_of_events(*trajs: Trajectory) -> float:
    """Get the mean number of events in the trajectories"""
    validate_trajectories(*trajs)
    return _get_mean_number_of_events(*trajs)

def _get_mean_number_of_visits(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: len(traj.get_visits()), trajs))

def get_mean_number_of_visits(*trajs: Trajectory) -> float:
    """Get the mean number of events in a state across all trajectories.
    Consecutive events in the same state count as a single visit"""
    validate_trajectories(*trajs)
    return _get_mean_number_of_visits(*trajs)

def _get_mean_state_range(*trajs: Trajectory) -> float:
    return statistics.mean(map(lambda traj: len(set(traj.states)), trajs))

def get_mean_state_range(*trajs: Trajectory) -> float:
    """Get the mean number of unique states visited by the trajectories"""
    validate_trajectories(*trajs)
    return _get_mean_state_range(*trajs)

def _get_total_state_range(*trajs: Trajectory) -> int:
    return len({state for traj in trajs for state in traj.states})

def get_total_state_range(*trajs: Trajectory) -> int:
    """Get the total number of unique states visited across all trajectories"""
    validate_trajectories(*trajs)
    return _get_total_state_range(*trajs)

def _get_mean_event_duration(*trajs: Trajectory) -> float:
    return statistics.mean(
         map(
              lambda traj: statistics.mean(
                map(lambda time_pairs: time_pairs[1] - time_pairs[0], zip(traj.times, traj.times[1:]))),
              trajs
            )
        )

def get_mean_event_duration(*trajs: Trajectory) -> float:
    """Get the mean duration of an event for a single trajectory, averaged across all trajectories"""
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
    """Get the mean duration of a visit to a state for a single trajectory, averaged across all trajectories.
    Consecutive events in the same state count as a single visit"""
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
    """Get the mean time spent in a state for a single trajectory, averaged across all trajectories.
    This does not include states not visited in the state space."""
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
    """Get the dispersion of a trajectory, averaged across all trajectories."""
    validate_trajectories(*trajs)
    return _get_mean_dispersion(*trajs)

def get_measures(*trajs: Trajectory) -> Measures:
    """Get all measures, packaged in a Measures object"""
    validate_trajectories(*trajs)
    return Measures(
        mean_trajectory_duration = _get_mean_trajectory_duration(*trajs),
        mean_number_of_events = _get_mean_number_of_events(*trajs),
        mean_number_of_visits = _get_mean_number_of_visits(*trajs),
        mean_state_range = _get_mean_state_range(*trajs),
        total_state_range = _get_total_state_range(*trajs),
        mean_event_duration = _get_mean_event_duration(*trajs),
        mean_visit_duration = _get_mean_visit_duration(*trajs),
        mean_state_duration = _get_mean_state_duration(*trajs),
        mean_dispersion = _get_mean_dispersion(*trajs)
    )