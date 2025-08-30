# Example 2
# script for obtaining measures of state space grid and displaying the grid itself for two different trajectories read from the same file
# script also outputs the measures for each trajectory individually as well as both trajectories together into a data file

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd

if __name__=="__main__":
    # read in the contents of a csv data file called example2.csv
    raw_data = pd.read_csv('example2.csv')
    # split the data into two different sets, dependent on the value of ID in each row
    data_traj_1 = raw_data.loc[raw_data["ID"]==123]
    data_traj_2 = raw_data.loc[raw_data["ID"]==456]

    # the set of possible state values is [1, 2, 3, 4, 5]
    ranges = [i for i in range(1,6)]

    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    trajectory1 = statespacegrid.trajectory.Trajectory(
        x_range = ranges,
        y_range=ranges,
        states=list(zip(
            data_traj_1["Parent Affect"].dropna().tolist(),
            data_traj_1["Child Affect"].dropna().tolist()
        )),
        times=data_traj_1["Onset"].dropna().tolist()
    )

    trajectory2 = statespacegrid.trajectory.Trajectory(
        x_range = ranges,
        y_range=ranges,
        states=list(zip(
            data_traj_2["Parent Affect"].dropna().tolist(),
            data_traj_2["Child Affect"].dropna().tolist()
        )),
        times=data_traj_2["Onset"].dropna().tolist()
    )

    measures_1 = statespacegrid.measure.get_measures(trajectory1)
    print(measures_1)
    measures_2 = statespacegrid.measure.get_measures(trajectory2)
    print(measures_2)
    combined_measures = statespacegrid.measure.get_measures(trajectory1, trajectory2)
    print(combined_measures)

    # make a list `rows', using the python function vars to convert the measures
    # from a class to a dictionary (a form which pandas knows how to deal with)
    rows = [vars(measures_1), vars(measures_2), vars(combined_measures)]
    # put the rows into a pandas DataFrame
    df = pd.DataFrame(rows)
    # use the DataFrame function to_csv to output the data to a csv file.
    # index=False tells it to not include a row index in the leftmost column
    df.to_csv("test_output.csv", index=False)

    # display the grid showing both trajectories together
    statespacegrid.grid.draw(trajectory1, trajectory2, xlabel="Parent Affect", ylabel="Child Affect", title="Plot showing two trajectories")
