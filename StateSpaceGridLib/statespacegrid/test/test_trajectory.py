import unittest

import statespacegrid.trajectory as trajectory

class TestTrajectoryConstruction(unittest.TestCase):

    def test_default_construction(self):
        traj = trajectory.Trajectory()
        self.assertEqual(traj.state_space, trajectory.StateSpace([1,2,3,4], [1,2,3,4]))
        self.assertEqual(traj.states, [])
        self.assertEqual(traj.times, [0.0])

    def test_state_space_definition(self):
        traj = trajectory.Trajectory(x_range=[0,1,2,3], y_range=[4,5,6,7])
        self.assertEqual(traj.state_space.x_range, [0,1,2,3])
        self.assertEqual(traj.state_space.y_range, [4,5,6,7])

    def test_normal_use(self):
        traj = trajectory.Trajectory(
            x_range=["bad", "ok", "good"],
            y_range=[0, 1, 2],
            states=[("ok", 1), ("bad", 0), ("bad", 1), ("bad", 2), ("ok", 2), ("good", 2), ("good", 1), ("good", 0), ("ok", 0)],
            times=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            )


    def test_bad_inputs(self):

        with self.assertRaises(Exception) as context:
            trajectory.Trajectory(times=[])
        self.assertTrue("The number of states should be equal to the number of timestamps minus 1" in str(context.exception))

        with self.assertRaises(Exception) as context:
            trajectory.Trajectory(times=[0,1,2])
        self.assertTrue("The number of states should be equal to the number of timestamps minus 1" in str(context.exception))

        with self.assertRaises(Exception) as context:
            trajectory.Trajectory(times=["a"])
        self.assertTrue("Times are expected as integers or floats" in str(context.exception))

        with self.assertRaises(Exception) as context:
            trajectory.Trajectory(times=[0,1,2,3], states=[(1,1), (2)])
        self.assertTrue("The states should be supplied as a list of (x_value, y_value) tuple or list pairs" in str(context.exception))

        with self.assertRaises(Exception) as context:
            trajectory.Trajectory(times=[0,1,2,3], states=[[1,1], [2]])
        self.assertTrue("The states should be supplied as a list of (x_value, y_value) pairs" in str(context.exception))

        with self.assertRaises(Exception) as context:
            trajectory.Trajectory(times=[0,1], states=[(0,10)])
        self.assertTrue("All provided state points should fall within the ranges provided in x_range and y_range" in str(context.exception))


if __name__ == "__main__":
    unittest.main()