# Example 4
# script for obtaining measures of state space grid and displaying the grid itself for any number of different trajectories read from multiple files in the same folder
# script also outputs the measures for each trajectory individually as well as both trajectories together into a data file

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd
import glob

if __name__=="__main__":
    # Get the names of all files in the current folder
    # As in all the other examples, we are assuming the script is being run from the same folder as the files
    all_files = glob.glob("*.csv")

    # get all of the data from the csvs which appear in the list of all_files
    data_trajs = [pd.read_csv(filename) for filename in all_files]

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


