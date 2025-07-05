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

def draw(*trajs: Trajectory):
    validate_trajectories(*trajs)


    print("draw")