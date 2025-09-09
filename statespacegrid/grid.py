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

from matplotlib import patches, pyplot, colors, figure, axes
from dataclasses import dataclass
from typing import List, Optional, Tuple
from collections import defaultdict
from math import cos, sin, pi
from random import random

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

    def to_circle(self, colour, first = False) -> patches.Circle:
        """Convert point into a matplotlib circle"""
        if first:
            return patches.Circle((self.x, self.y), self.radius, zorder=2, edgecolor=colour, facecolor='none', alpha = 0.7)
        else:
            return patches.Circle((self.x, self.y), self.radius, zorder=2, color=colour, alpha = 0.7)


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
    Adjust data points in list so they are less likely to overlap.
    Function both adjusts the radius so that it fits inside the state box
    and moves points within the state box so they do not sit in the centre
    """
    if len(trajectory_points_list[0]) == 0:
        return
    data_points_grouped_by_state = _group_trajectory_points_by_state(trajectory_points_list)
    normalisation_factor = max(map(lambda points: sum(2*point.radius for point in points), data_points_grouped_by_state.values()))
    for state, points in data_points_grouped_by_state.items():
        for point in points:
            point.radius /= normalisation_factor
        center = state
        for i, point in enumerate(points):
            random_angle = (random() + i) * 2 * pi / len(points)
            max_offset = 0.5 - point.radius
            actual_offset = ((1+random())/2) * max_offset

            point.x = center[0] + (actual_offset * cos(random_angle))
            point.y = center[1] + (actual_offset * sin(random_angle))


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


def draw(*trajs: Trajectory, filename: Optional[str]=None, display=True, colours: Optional[List[str]]=None,
         xlabel: Optional[str]=None, ylabel: Optional[str]=None, title: Optional[str]=None,
         fig: Optional[figure.Figure]=None, ax: Optional[axes.Axes]=None) -> Tuple[figure.Figure, axes.Axes]:
    """
    Create a matplotlib visualisation of the provided points on a state space grid

    Keyword Arguments:
    filename: File path for output grid visualisation. If not provided,
              will simply return a matplotlib Axes, Figure pair
    display: Display grid in new window if True.
             This has the side effect of invalidating the returned figure
    colours: List of colours for trajectories. If not provided,
             a grid with multiple trajectories will assign each
             trajectory a new colour randomly. Uses matplotlib
             colors interface
    xlabel: Axis label for the x axis
    ylabel: Axis label for the y axis
    title: Title for the plot

    Returns:
    matplotlib figure for grid (valid only if display=False)
    matplotlib axes (valid only if display=False)
    """
    validate_trajectories(*trajs)

    if fig == None and ax == None:
        fig, ax = pyplot.subplots()

    trajectory_points_list = _get_adjusted_trajectory_points(*trajs)

    # Figure out the different trajectory colours
    colours_to_set = []
    if colours is not None:
        if len(colours) != len(trajs):
            raise ValueError("The number of colours provided should match the number of trajectories")
        colours_to_set=colours
    else:
        colour_list = list(colors.TABLEAU_COLORS.keys())
        colours_to_set = [colour_list[i%len(colour_list)] for i in range(len(trajs))]

    for trajectory_points, trajectory_colour in zip(trajectory_points_list, colours_to_set):
        # Add lines
        for point1, point2 in zip(trajectory_points, trajectory_points[1:]):
            ax.plot((point1.x, point2.x), (point1.y, point2.y), "-ok", mfc='k', mec='k', zorder = 1)
            ax.arrow(point1.x, point1.y, (point2.x-point1.x)/2, (point2.y-point1.y)/2, head_width = 0.05, length_includes_head = True, fc='k')
        # Add circles
        for i, point in enumerate(trajectory_points):
            ax.add_patch(point.to_circle(trajectory_colour, i==0))

    # Set grid size
    ax.set_xlim((-0.5, len(trajs[0].state_space.x_range)-0.5))
    ax.set_ylim((-0.5, len(trajs[0].state_space.y_range)-0.5))

    # Set grid state labels
    ax.set_xticks([i for i in range(len(trajs[0].state_space.x_range))], labels=trajs[0].state_space.x_range)
    ax.set_yticks([i for i in range(len(trajs[0].state_space.y_range))], labels=trajs[0].state_space.y_range)

    # Add gridlines
    ax.set_xticks([i-0.5 for i in range(len(trajs[0].state_space.x_range)+1)], minor=True)
    ax.set_yticks([i-0.5 for i in range(len(trajs[0].state_space.y_range)+1)], minor=True)
    ax.grid(visible=True, which="minor")

    # Add axis labels
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # Add figure title
    if title is not None:
        ax.set_title(title)

    if filename is not None:
        fig.savefig(filename)

    if display:
        pyplot.show(block=True)

    return fig, ax
