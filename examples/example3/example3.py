# Example 3
# script for obtaining measures of state space grid and displaying the grid itself using .traj input files

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd

if __name__=="__main__":
   # read in the contents of a trj data file called example3.trj
   # .trj files are basically csv files, but using tabs instead of commas to separate variables
   # we specify that the separator is a tab to read_csv with sep="\t"
   raw_data = pd.read_csv('example3.trj', sep="\t")
   # pass the columns of the trj file to the Trajectory object constructor
   # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
   traj = statespacegrid.trajectory.Trajectory(
     x_range=[i for i in range(1,6)],
     y_range=[i for i in range(1,6)],
     states=list(zip(
        raw_data["variable 1"].dropna().tolist(),
        raw_data["variable 2"].dropna().tolist()
     )),
     times = raw_data["Onset"].dropna().tolist()
   )

   # get the measures for the trajectory
   measures = statespacegrid.measure.get_measures(traj)
   # print the measures for the trajectory
   print(measures)

   # draw the grid in a new window
   statespacegrid.grid.draw(traj)