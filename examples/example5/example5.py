# Example 5
# script for obtaining measures of state space grid and displaying the grid itself

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd

if __name__=="__main__":
   # read in the contents of a csv data file called example5.csv
   raw_data = pd.read_csv('example5.csv')
   # pass the columns of the csv file to the Trajectory object constructor
   # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
   ranges = ["HOSTILE", "NEGATIVE", "NEUTRAL", "POSITIVE"]
   traj = statespacegrid.trajectory.Trajectory(
     x_range=ranges,
     y_range=ranges,
     states=list(zip(
        raw_data["Parent Affect"].dropna().tolist(),
        raw_data["Child Affect"].dropna().tolist()
     )),
     times = raw_data["Onset"].dropna().tolist()
   )

   # get the measures for the trajectory
   measures = statespacegrid.measure.get_measures(traj)
   # print the measures for the trajectory
   print(measures)

   # draw the grid in a new window
   statespacegrid.grid.draw(traj)
