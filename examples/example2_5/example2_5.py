# Example 2.5
# script for obtaining measures of state space grid and displaying the grid itself for any number of different trajectories read from the same file
# script also outputs the measures for each trajectory individually as well as both trajectories together into a data file

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd

if __name__=="__main__":
    # read in the contents of a csv data file called example2_5.csv
    raw_data = pd.read_csv('example2_5.csv')
    # split the data into two different sets, dependent on the value of ID in each row
    data_trajs = [data_traj for _, data_traj in raw_data.groupby("ID")]

    # the set of possible state values is [1, 2, 3, 4, 5]
    ranges = [i for i in range(1,6)]

    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    trajectories = [
        statespacegrid.trajectory.Trajectory(
            x_range=ranges,
            y_range=ranges,
            states=list(zip(
                data_traj["Parent Affect"].dropna().tolist(),
                data_traj["Child Affect"].dropna().tolist()
            )),
            times=data_traj["Onset"].dropna().tolist()
        )
        for data_traj in data_trajs
    ]

    individual_measures = [statespacegrid.measure.get_measures(traj) for traj in trajectories]
    for measure in individual_measures:
        print(measure)
    combined_measures = statespacegrid.measure.get_measures(*trajectories)
    print(combined_measures)

    # make a list `rows', using the python function vars to convert the measures
    # from a class to a dictionary (a form which pandas knows how to deal with)
    rows = [vars(measure) for measure in individual_measures]
    rows.append(vars(combined_measures))
    # put the rows into a pandas DataFrame
    df = pd.DataFrame(rows)
    # use the DataFrame function to_csv to output the data to a csv file.
    # index=False tells it to not include a row index in the leftmost column
    df.to_csv("test_output.csv", index=False)

    # display the grid showing both trajectories together
    statespacegrid.grid.draw(*trajectories, xlabel="Parent Affect", ylabel="Child Affect", title="Plot showing two trajectories")

