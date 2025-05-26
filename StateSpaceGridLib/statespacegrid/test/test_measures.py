import unittest
import math

import statespacegrid.measure as measure
import statespacegrid.trajectory as trajectory

class TestMeasureCalculations(unittest.TestCase):

    def test_empty_input(self):
        with self.assertRaises(Exception) as context:
            measure.get_measures()
        self.assertTrue("You must provide at least 1 trajectory" in str(context.exception))

    def test_mismatched_states(self):
        traj1 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=[0, 1, 2],
            states=[("ok", 1), ("bad", 0), ("bad", 1), ("bad", 2), ("ok", 2), ("good", 2), ("good", 1), ("good", 0), ("ok", 0)],
            times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            )
        traj2 = trajectory.Trajectory(
            x_range=[0, 1, 2],
            y_range=["bad", "ok", "good"],
            states=[(1, "ok"), (0, "bad"), (1, "bad"), (2, "bad"), (2, "ok"), (2, "good"), (1, "good"), (0, "good"), (0, "ok")],
            times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            )

        with self.assertRaises(Exception) as context:
            measure.get_measures(traj1, traj2)
        self.assertTrue("The state spaces of all provided trajectories must match" in str(context.exception))

    def test_misordered_states(self):
        traj1 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=[0, 1, 2],
            states=[("ok", 1), ("bad", 0), ("bad", 1), ("bad", 2), ("ok", 2), ("good", 2), ("good", 1), ("good", 0), ("ok", 0)],
            times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            )

        traj2 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=[0, 2, 1],
            states=[("ok", 1), ("bad", 0), ("bad", 1), ("bad", 2), ("ok", 2), ("good", 2), ("good", 1), ("good", 0), ("ok", 0)],
            times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            )

        with self.assertRaises(Exception) as context:
            measure.get_measures(traj1, traj2)
        self.assertTrue("The order of states should be the same in all state spaces in the provided trajectories" in str(context.exception))

    def test_correct_values_single_trajectory(self):
        traj1 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=["bad", "ok", "good"],
            states=[("bad", "bad"), ("ok", "ok"), ("good", "good")],
            times=[1, 1.1, 1.5, 2]
        )

        self.assertTrue(measure.get_mean_state_range(traj1) == 3)
        self.assertTrue(measure.get_mean_trajectory_duration(traj1) == 1)
        self.assertTrue(measure.get_mean_number_of_events(traj1) == 3)
        self.assertTrue(measure.get_mean_number_of_visits(traj1) == 3)
        self.assertTrue(measure.get_mean_state_range(traj1) == 3)
        self.assertTrue(measure.get_total_state_range(traj1) == 3)
        self.assertTrue(math.isclose(measure.get_mean_event_duration(traj1), 1/3))
        self.assertTrue(math.isclose(measure.get_mean_visit_duration(traj1), 1/3))
        self.assertTrue(math.isclose(measure.get_mean_state_duration(traj1), 1/3))
        self.assertTrue(math.isclose(measure.get_mean_dispersion(traj1), 0.6525))

        traj2 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=["bad", "ok", "good"],
            states=[("bad", "good"), ("ok", "ok"), ("ok", "ok"), ("good", "bad"), ("bad", "good")],
            times=[0, 0.9, 1, 1.5, 1.7, 2]
        )

        self.assertTrue(measure.get_mean_state_range(traj2) == 3)
        self.assertTrue(measure.get_mean_trajectory_duration(traj2) == 2)
        self.assertTrue(measure.get_mean_number_of_events(traj2) == 5)
        self.assertTrue(measure.get_mean_number_of_visits(traj2) == 4)
        self.assertTrue(measure.get_mean_state_range(traj2) == 3)
        self.assertTrue(measure.get_total_state_range(traj2) == 3)
        self.assertTrue(math.isclose(measure.get_mean_event_duration(traj2), 0.4))
        self.assertTrue(math.isclose(measure.get_mean_visit_duration(traj2), 0.5))
        self.assertTrue(math.isclose(measure.get_mean_state_duration(traj2), 2/3))
        self.assertTrue(math.isclose(measure.get_mean_dispersion(traj2), 0.6075))

    def test_correct_values_multi_trajectory(self):
        traj1 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=["bad", "ok", "good"],
            states=[("bad", "bad"), ("ok", "ok"), ("good", "good")],
            times=[1, 1.1, 1.5, 2]
        )

        traj2 = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=["bad", "ok", "good"],
            states=[("bad", "good"), ("ok", "ok"), ("ok", "ok"), ("good", "bad"), ("bad", "good")],
            times=[0, 0.9, 1, 1.5, 1.7, 2]
        )

        self.assertTrue(measure.get_mean_state_range(traj1, traj2) == 3)
        self.assertTrue(math.isclose(measure.get_mean_trajectory_duration(traj1, traj2), 1.5))
        self.assertTrue(measure.get_mean_number_of_events(traj1, traj2) == 4)
        self.assertTrue(math.isclose(measure.get_mean_number_of_visits(traj1, traj2), 3.5))
        self.assertTrue(measure.get_mean_state_range(traj1, traj2) == 3)
        self.assertTrue(measure.get_total_state_range(traj1, traj2) == 5)
        self.assertTrue(math.isclose(measure.get_mean_event_duration(traj1, traj2), 0.3666666666666))
        self.assertTrue(math.isclose(measure.get_mean_visit_duration(traj1, traj2), 0.4166666666666))
        self.assertTrue(math.isclose(measure.get_mean_state_duration(traj1, traj2), 0.5))
        self.assertTrue(math.isclose(measure.get_mean_dispersion(traj1, traj2), 0.63))

if __name__ == "__main__":
    unittest.main()