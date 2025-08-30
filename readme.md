# StateSpaceGridLib

## Introduction

StateSpaceGridLib (henceforth referred to as SSG) is a library that uses the Python programming language to provide a streamlined approach to large-scale analysis of dyadic systems. Before using this library, it is advised to be familiar with the concept of [State Space Grids](https://link.springer.com/book/10.1007/978-1-4614-5007-8), and more broadly, the dynamic systems approach to development.

Briefly, state space grids were developed by Marc Lewis and colleagues (Lewis, Lamey & Douglas, 1999) as a way to represent synchronous ordinal time series on a 2-D grid, based on dynamic systems principles. It has most commonly been used as a graphical approach to depict an aspect of the trajectory of a dyad across time, for example, how emotional affect during an interaction between a parent and child changes across a 5-minute observational task. As such, the minimum number of variables to create a state space grid are two 'state' variables and one variable to represent timestamps throughout the duration of the interaction. Each interaction is referred to as a 'trajectory'.

In this context, we provide tools to, from within Python code:

1. Obtain measures of dyadic trajectories across time (e.g. dispersion, range, transitions)
2. Display state space grids visually

The first step to using this library is to install it with pip

pip install git+https://github.com/DyadicSolutions/StateSpaceGridLib

Once it has been installed, you can start to make use of the library within a Python script. (See [here](https://www.python.org/about/gettingstarted/) or [here](https://www.w3schools.com/python/python_intro.asp) for an introduction to Python programming). Python templates for this library can be found in [Examples](#examples), providing a basic starting point for using the different tools offered.

## Examples

Templates 1 to 5 are all demonstrations for different approaches to handling data and getting it into a form that the SSG library can use.
For Templates 1 and 2, the csv data files provided display the recommended data file structure that can be used with the corresponding Python script without any changes required. It is perfectly fine for your data file structure to be completely different, though that would require some deviations from the Python code in the example scripts.

Each example given here also exists as a standalone set of files in folder "examples"

### Template 1 for importing csv file to be used (only contains one trajectory, e.g. only one dyad from a study)
Your data file should include, at a minimum, the timestamp variable and the time series data (two state variables).

In this example, we import a csv file that contains data on parent affect (first state variable) and child affect (second state variable) coded on a scale of 1-5 (1 being high negative, 5 being high positive), in 30-second bins over 5 minutes (timestamp variable with 11 values covering the range 0-5 minutes).
```csv
Onset,Parent Affect,Child Affect
0.0,1,2
0.5,1,2
1.0,3,3
1.5,2,4
2.0,1,4
2.5,2,3
3.0,4,5
3.5,5,5
4.0,5,3
4.5,3,1
5.0
```
```python
# Example 1
# script for obtaining measures of state space grid and displaying the grid itself

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd

if __name__=="__main__":
   # read in the contents of a csv data file called example1.csv
   raw_data = pd.read_csv('example1.csv')
   # pass the columns of the csv file to the Trajectory object constructor
   # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
   traj = statespacegrid.trajectory.Trajectory(
     x_range=[i for i in range(1,6)],
     y_range=[i for i in range(1,6)],
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
```

### Template 2 for importing csv file to be used (contains more than one trajectory, e.g. multiple dyads from a study/multiple participant IDs)
This second template is an extension of the first template. In this case we have a data file which contains data for two different trajectories.
The sample csv below shows a suggestion of how the data could be laid out for ease of handling in the python script.
The ID column with its repeated ID values is a very useful feature when read in by the script, as it lets the code know exactly which ID each row belongs to.
With this property, we are able to use some of the built-in cleverness in the python library pandas to easily split the data in two.
As an extension, below the template script is a version of that script which, given the same data layout in a csv file, can read in any amount of trajectory data with no extra knowledge needed about how many trajectories there are in the data file.
This is to provide an example of the approach which should be used when using SSG on large volumes of collated data.
Both scripts, after calculating the cumulative measures of all trajectories on the same grid, then calculate measures for each trajectory individually and deposits all measures calculated into a new csv file.
```csv
ID,Onset,Parent Affect,Child Affect
123,0.0,1,2
123,0.5,1,2
123,1.0,3,3
123,1.5,2,4
123,2.0,1,4
123,2.5,2,3
123,3.0,4,5
123,3.5,5,5
123,4.0,5,3
123,4.5,3,1
123,5.0,,
456,0.0,2,2
456,0.5,1,3
456,1.0,3,3
456,1.5,4,4
456,2.0,5,4
456,2.5,2,4
456,3.0,1,5
456,3.5,3,5
456,4.0,2,3
456,4.5,3,4
456,5.0,,
```
```python
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

```
Displayed below is an alternative solution to the one shown above. It gets the ID values directly from the csv data, and makes no assumptions about the number of IDs (and hence number of trajectories) in the dataset.
Instead trajectory objects (and the trajectory data that those objects are made with) are stored in lists, with new IDs added to the end of the list.
This solution will work for csv data with an ID column as above, containing results for any number of IDs.
```python
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

```

### Template 3 for making use of trj files from Gridware with SSG

For more information on trj files, refer to the [Gridware manual](https://www.queensu.ca/psychology/sites/psycwww/files/uploaded_files/Faculty/Tom%20Hollenstein/GridWare/GridWare1.1_Manual.pdf)
SSG contains a tool for taking trj files, and turning them directly into trajectory objects in the python code.
```tsv
Onset	variable 1	variable 2	variable 3
0.00	1	3	2
0.65	2	2	3
1.51	3	1	4
3.21	4	2	3
8.36	3	3	2
9.45	2	4	1
10.39	1	3	2
11.53	2	2	3
13.32	3	1	4
14.00
```
```python
# Example 3
# script for obtaining measures of state space grid and displaying the grid itself using .traj input files

import statespacegrid.trajectory
import statespacegrid.measure
import statespacegrid.grid
import pandas as pd

if __name__=="__main__":
   # read in the contents of a traj data file called example3.traj
   # .traj files are basically csv files, but suing tabs instead of commas to separate variables
   raw_data = pd.read_csv('example3.traj', sep="\t")
   # pass the columns of the traj file to the Trajectory object constructor
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
```

### Template 4 for importing multiple trajectories (e.g. participants in a study with each dyad in a separate file)
Earlier in the examples (templates 2, 2.5) there is an example case where all the data for multiple trajectories is contained within one csv file.
There may be a case where instead, the data is in lots of files with one file per trajectory.
Here we show an approach for dealing with this case, in a similar style to template 2.5.
```python
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
```

### Template 5 for handling non-numeric data in SSG
This template showcases SSG's approach for displaying data which is on a non-numeric scale.
The process is essentially identical to all the preceding cases, simply with a slightly different range.
```csv
Onset,Parent Affect,Child Affect
0.0,HOSTILE,NEGATIVE
0.5,HOSTILE,NEGATIVE
1.0,NEUTRAL,NEUTRAL
1.5,NEGATIVE,POSITIVE
2.0,HOSTILE,POSITIVE
2.5,NEGATIVE,NEUTRAL
3.0,POSITIVE,POSITIVE
3.5,POSITIVE,POSITIVE
4.0,POSITIVE,NEUTRAL
4.5,NEUTRAL,HOSTILE
5.0
```
```python
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

```