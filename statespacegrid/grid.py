"""Module containing functionality for visualising state space grids

Typical usage example:

    traj = trajectory.Trajectory(
                x_range=["bad", "ok", "good"],
                y_range=[0, 1, 2],
                states=[("ok", 1), ("bad", 0), ("bad", 1), ("bad", 2), ("ok", 2), ("good", 2), ("good", 1), ("good", 0), ("ok", 0)],
                times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                )

    grid.draw(measure)
"""

from statespacegrid.trajectory import Trajectory, validate_trajectories

from matplotlib import patches, pyplot
from dataclasses import dataclass
from typing import List
from collections import defaultdict

@dataclass
class DataPoint:
    """
    Class to hold visit data prior to it being converted into a circle in the diagram.
    Useful to have in order to allow for further adjustment in cases of overlapping events.

    Attributes:
        x: The position of the point on the x axis
        y: The position of the point on the y axis
        radius: The radius of the point
    """
    x: float
    y: float
    radius: float

    def to_circle(self) -> patches.Circle:
        """Convert point into a matplotlib circle"""
        return patches.Circle((self.x, self.y), self.radius, zorder=2)


def _group_trajectory_points_by_state(trajectory_points_list: List[List[DataPoint]]) -> defaultdict:
    """
    Group all trajectory data points into buckets for each state in the state space
    so that we know how many overlaps we have
    """
    data_points_grouped_by_state = defaultdict(list)
    for traj_points in trajectory_points_list:
        for point in traj_points:
            data_points_grouped_by_state[(point.x, point.y)].append(point)
    return data_points_grouped_by_state


def _adjust_trajectory_points_list(trajectory_points_list: List[List[DataPoint]]):
    """
    Adjust data points in list so they no longer overlap.
    Function both adjusts the radius so that it fits inside the state box
    and moves points within the state box so they do not sit on top of each other
    """
    data_points_grouped_by_state = _group_trajectory_points_by_state(trajectory_points_list)
    normalisation_factor = max(map(lambda points: sum(2*point.radius for point in points), data_points_grouped_by_state.values()))
    for state, points in data_points_grouped_by_state.items():
        for point in points:
            point.radius /= normalisation_factor
        if len(points) > 1:
            """
            2 or more data points means we will have to adjust
            Arrange points along the diagonal
            """
            half_length = sum(map(lambda point: point.radius, points))
            center = (state[0]-(half_length), state[1]-(half_length))
            for point in points:
                center = (center[0]+point.radius, center[1]+point.radius)
                point.x = center[0]
                point.y = center[1]
                center = (center[0]+point.radius, center[1]+point.radius)


def _get_trajectory_points(*trajs: Trajectory) -> List[List[DataPoint]]:
    """Calculate a set of DataPoint objects for all of the visits in all of the trajectories"""
    return [
        [DataPoint(traj.state_space.get_x_index(visit[0]), traj.state_space.get_y_index(visit[1]), time)
         for visit, time in zip(traj.get_visits(), traj.get_visit_durations())
         ] for traj in trajs]


def _get_adjusted_trajectory_points(*trajs: Trajectory) -> List[List[DataPoint]]:
    """Calculate a set of non-overlapping DataPoint objects for all of the visits in all of the trajectories"""
    trajectory_points_list = _get_trajectory_points(*trajs)
    _adjust_trajectory_points_list(trajectory_points_list)
    return trajectory_points_list


def draw(*trajs: Trajectory):
    """Create a visualisation of the provided points on a state space grid"""
    validate_trajectories(*trajs)

    fig, ax = pyplot.subplots()

    trajectory_points_list = _get_adjusted_trajectory_points(*trajs)

    for trajectory_points in trajectory_points_list:
        # Add lines
        for point1, point2 in zip(trajectory_points, trajectory_points[1:]):
            ax.plot((point1.x, point2.x), (point1.y, point2.y), "-ok", mfc='C0', mec='C0', zorder = 1)
        # Add circles
        for point in trajectory_points:
            ax.add_patch(point.to_circle())

    # Set grid size
    ax.set_xlim((-0.5, len(trajs[0].state_space.x_range)-0.5))
    ax.set_ylim((-0.5, len(trajs[0].state_space.y_range)-0.5))

    # Set grid state labels
    ax.set_xticks([i for i in range(len(trajs[0].state_space.x_range))], labels=trajs[0].state_space.x_range)
    ax.set_yticks([i for i in range(len(trajs[0].state_space.y_range))], labels=trajs[0].state_space.y_range)

    # Add gridlines
    ax.set_xticks([i-0.5 for i in range(len(trajs[0].state_space.x_range)+1)], minor=True)
    ax.set_yticks([i-0.5 for i in range(len(trajs[0].state_space.y_range)+1)], minor=True)
    ax.grid(which="minor")


    fig.savefig("ssg.png")
