# StateSpaceGridLib

## Introduction

StateSpaceGridLib (henceforth referred to as SSG) is a library that uses the Python programming language. It is loosely based around replicating the
functionality of [GridWare](https://www.queensu.ca/psychology/adolescent-dynamics-lab/state-space-grids), an application created by Tom Hollenstein, Alex Lamey, and colleagues. Before using this library, it is advised to be familiar with the concept of [State Space Grids](https://link.springer.com/book/10.1007/978-1-4614-5007-8), and more broadly, the dynamic systems approach to development. 

Briefly, state space grids were developed by Marc Lewis and colleagues (Lewis, Lamey & Douglas, 1999) as a way to represent synchronous ordinal time series on a 2-D grid, based on dynamic systems principles. It has most commonly been used as a graphical approach to depict an aspect of the trajectory of a dyad across time, for example, how emotional affect during an interaction between a parent and child changes across a 5-minute observational task. As such, the minimum number of variables to create a state space grid are two 'state' variables and one variable to represent timestamps throughout the duration of the interaction. Each interaction is referred to as a 'trajectory'. 

In this context, we provide tools to:

1. Display state space grids visually
2. Handle data files from different formats (e.g. .csv files, .xls files, trj files)
3. Obtain measures of dyadic trajectories across time (e.g. dispersion, range, transitions) 

The first step to using this library is to install it with pip

pip install git+https://github.com/DyadicSolutions/StateSpaceGridLib

Once it has been installed, you can start to make use of the library within a Python script. (See [here](https://www.python.org/about/gettingstarted/) or [here](https://www.w3schools.com/python/python_intro.asp) for an introduction to Python programming). Python templates for this library can be found in [Examples](#examples), providing a basic starting point for using the different tools offered. 

## Examples

Templates 1 to 4 are all demonstrations for different approaches to handling data and getting it into a form that the SSG library can use.
Templates 5 onwards are focused on showcasing the different features of SSG.
For Templates 1 and 2, the csv data files provided display the recommended data file structure that can be used with the corresponding Python script without any changes required. It is perfectly fine for your data file structure to be completely different, though that would require some changes to the Python scripts. 

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
# Template 1
# script for obtaining measures of state space grid and displaying the grid itself

import state_space_grid as ssg 
import pandas as pd 

if __name__=="__main__":    
    # read in the contents of a csv data file called example1.csv
    raw_data = pd.read_csv('example1.csv')
    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    trajectory = ssg.Trajectory(raw_data["Parent Affect"].dropna().tolist(),raw_data["Child Affect"].dropna().tolist(),raw_data["Onset"].dropna().tolist(), id=0)
    # pass the trajectory to the Grid object constructor
    # the constructor takes a list of trajectories, so here we put the trajectory inside square brackets, making it a list of length 1
    grid=ssg.Grid([trajectory])

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
   
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
456,2.0,4,4
456,2.5,2,4
456,3.0,1,5
456,3.5,3,5
456,4.0,2,3
456,4.5,3,4
456,5.0,,
```
```python
# Template 2
# script for obtaining measures of state space grid and displaying the grid itself for two different trajectories read from the same file

import state_space_grid as ssg 
import pandas as pd 

if __name__=="__main__":    
    # read in the contents of a csv data file called example1.csv
    raw_data = pd.read_csv('example1.csv')
    # split the data into two different sets, dependent on the value of ID in each row
    data_traj_1 = raw_data.loc[raw_data["ID"]==123]
    data_traj_2 = raw_data.loc[raw_data["ID"]==456]

    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    trajectory1 = ssg.Trajectory(data_traj_1["Parent Affect"].dropna().tolist(),data_traj_1["Child Affect"].dropna().tolist(),data_traj_1["Onset"].dropna().tolist(), id=data_traj_1["ID"].tolist()[0])
    trajectory2 = ssg.Trajectory(data_traj_2["Parent Affect"].dropna().tolist(),data_traj_2["Child Affect"].dropna().tolist(),data_traj_2["Onset"].dropna().tolist(), id=data_traj_2["ID"].tolist()[0])
    # pass the trajectories to the Grid object constructor
    # the constructor takes a list of trajectories, so here we put both trajectories inside square brackets, making a list of length 2
    grid=ssg.Grid([trajectory1,trajectory2])

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
    
    # alternatively if we want to calculate measures individually for each trajectory and then deposit these in a data file:
    # calculate measures
    measures_1 = ssg.Grid([trajectory1]).get_measures()
    measures_2 = ssg.Grid([trajectory2]).get_measures()
    # make a list `rows', using the python function vars to convert the measures
    # from a class to a dictionary (a form which pandas knows how to deal with)
    rows = [vars(measures_1), vars(measures_2), vars(measure)]
    # put the rows into a pandas DataFrame
    df = pd.DataFrame(rows)
    # use the DataFrame function to_csv to output the data to a csv file. 
    # index=False tells it to not include a row index in the leftmost column
    df.to_csv("test_output.csv", index=False)
   
      
```
Displayed below is an alternative solution to the one shown above. It gets the ID values directly from the csv data, and makes no assumptions about the number of IDs (and hence number of trajectories) in the dataset.
Instead trajectory objects (and the trajectory data that those objects are made with) are stored in lists, with new IDs added to the end of the list.
This solution will work for csv data with an ID column as above, containing results for any number of IDs.
```python
# Template 2.5
# Script for obtaining measures of state space grid and displaying the grid itself for an arbitrary number of different trajectories read from the same file
# This script will work for any number of trajectories held in the same file, not just 2.

import state_space_grid as ssg 
import pandas as pd 

if __name__=="__main__":    
    # read in the contents of a csv data file called example1.csv
    raw_data = pd.read_csv('example1.csv')
    # Identify all unique IDs in the data file
    id_values = raw_data["ID"].unique()
    # create a list to hold each DataFrame (pandas term for a table) split up by ID value
    split_data = []
    # add DataFrames to the list - one per ID value
    for id in id_values:
        split_data.append(raw_data.loc[raw_data["ID"]==id])

    # make a list to hold trajectories
    trajectories = []
    # add Trajectory objects to the list
    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    for data in split_data:
        trajectories.append(ssg.Trajectory(data["Parent Affect"].dropna().tolist(),data["Child Affect"].dropna().tolist(),data["Onset"].dropna().tolist(), id=data["ID"].tolist()[0]))

    # pass the trajectory list to the Grid object constructor
    grid=ssg.Grid(trajectories)

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
    
    # alternatively if we want to calculate measures individually for each trajectory and then deposit these in a data file:
    # calculate measures
    individual_measures = []
    for trajectory in trajectories:
        individual_measures.append(ssg.Grid([trajectory]).get_measures())
    rows = []
    # add each of the measures to the list `rows', using the python function vars to convert them
    # from a class to a dictionary (a form which pandas knows how to deal with)
    for m in individual_measures:
        rows.append(vars(m))
    rows.append(measure)
    # put the rows into a pandas DataFrame
    df = pd.DataFrame(rows)
    # use the DataFrame function to_csv to output the data to a csv file. 
    # index=False tells it to not include a row index in the leftmost column
    df.to_csv("test_output.csv", index=False)
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
# Template 3
# script for obtaining measures of state space grid and displaying the grid itself

import state_space_grid as ssg 
import pandas as pd 

if __name__=="__main__":    
    
    # read in trajectory data using from_legacy_trj.
    # the function takes a file name, and a tuple containing the column numbers of your two variables. 
    # there is an implicit assumption that "Onset" is column 0. 
    # by default, if you were to not provide anything to the function aside from the filename, it would take the variables in columns 1 and 2 for the x and y data.
    trajectory = ssg.Trajectory.from_legacy_trj("example1.trj",(2,3))
    # pass the trajectory to the Grid object constructor
    # the constructor takes a list of trajectories, so here we put the trajectory inside square brackets, making it a list of length 1
    grid=ssg.Grid([trajectory])

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
   
      
```

### Template 4 for importing multiple trajectories (e.g. participants in a study with each dyad in a separate file) 
Earlier in the examples (templates 2, 2.5) there is an example case where all the data for multiple trajectories is contained within one csv file.
There may be a case where instead, the data is in lots of files with one file per trajectory.
Here we show an approach for dealing with this case, in a similar style to template 2.5.
```python
# Template 4
# Script for obtaining measures of state space grid and displaying the grid itself for an arbitrary number of different trajectories read from different files
# This script will work for any number of files held in the same folder/directory.

import state_space_grid as ssg 
import pandas as pd 
import glob

if __name__=="__main__":    
    # get a list of all csv datafiles in the folder
    # here we are assuming that the script is being run in the same folder as the csv files.
    datafiles = glob.glob("*.csv")
    # make a list to store the data from the files
    data_list = []
    # read in each datafile found by glob.glob and add to the data list
    for file in datafiles:
        data_list.append(pd.read_csv(file))
    # make a list to hold trajectories
    trajectories = []
    # add Trajectory objects to the list
    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    for data in data_list:
        trajectories.append(ssg.Trajectory(data["Parent Affect"].dropna().tolist(),data["Child Affect"].dropna().tolist(),data["Onset"].dropna().tolist(), id=data["ID"].tolist()[0]))

    # pass the trajectory list to the Grid object constructor
    grid=ssg.Grid(trajectories)

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
   
      
```

### Template 5 for handling non-numeric data in SSG
This template showcases SSG's approach for displaying data which is on a non-numeric scale (categoric data, by GridWare's definitions).
It is almost as simple to handle this form of data as for numeric data. 
The one difference is that SSG needs to know what order these data points come in. For example ["small","medium","large"] or ["Poor","Acceptable","Exceeds Expectations","Outstanding"].
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
# Template 5
# script for obtaining measures of state space grid and displaying the grid itself
# data is categoric/non-numeric

import state_space_grid as ssg 
import pandas as pd 

if __name__=="__main__":    
    # read in the contents of a csv data file called example1.csv
    raw_data = pd.read_csv('example1.csv')
    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    trajectory = ssg.Trajectory(raw_data["Parent Affect"].dropna().tolist(),raw_data["Child Affect"].dropna().tolist(),raw_data["Onset"].dropna().tolist(), id=0)

    # first define the ordering for our variables:
    ordering = ["HOSTILE","NEGATIVE","NEUTRAL","POSITIVE"]
    # All extra data to do with defining extra things needed for calculations goes in a GridQuantization object
    # in this case we need to tell it what the ordering for x and y objects is.
    quantization = ssg.GridQuantization(x_order=ordering, y_order=ordering)
    # pass the trajectory to the Grid object constructor
    # the constructor takes a list of trajectories, so here we put the trajectory inside square brackets, making it a list of length 1
    grid=ssg.Grid([trajectory])

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
   
```
### Template 6 for demonstrating GridQuantization objects in SSG
As introduced in template 5, SSG defines an object called a GridQuantization. 
This is effectively used to store options and information about the data being inputted.
If options in GridQuantization objects are not given, SSG will try to work out what fits best from the data provided.
As seen in templates 1-4, one can go completely without a GridQuantization object, and SSG will make it's best guess at _everything_.

```csv
Onset,Parent Affect,Child Affect
0.0,10,20
0.5,10,20
1.0,30,30
1.5,20,40
2.0,10,40
2.5,20,30
3.0,40,50
3.5,50,50
4.0,50,30
4.5,30,10
5.0
```
```python
# Template 6
# script for obtaining measures of state space grid and displaying the grid itself
# here we make use of all the options that GridQuantization has to provide 
# (apart from x_order and y_order, which already got their introduction in template 5)

import state_space_grid as ssg 
import pandas as pd 

if __name__=="__main__":    
    # read in the contents of a csv data file called example1.csv
    raw_data = pd.read_csv('example1.csv')
    # pass the columns of the csv file to the Trajectory object constructor
    # make sure to get rid of any NaN (Not a Number) values with dropna() and convert to a list with tolist()
    trajectory = ssg.Trajectory(raw_data["Parent Affect"].dropna().tolist(),raw_data["Child Affect"].dropna().tolist(),raw_data["Onset"].dropna().tolist(), id=0)
    # all extra data to do with defining extra things needed for calculations goes in a GridQuantization object
    # there are separate fields for each of the x and y axis to allow for the chance of differing scales of measurement.
    quantization = ssg.GridQuantization(cell_size_x=10, cell_size_y=10, x_min=10, x_max=100, y_min=10, y_max=100)
    # pass the trajectory to the Grid object constructor
    # the constructor takes a list of trajectories, so here we put the trajectory inside square brackets, making it a list of length 1
    grid=ssg.Grid([trajectory])

    # to print measures for this grid 

    measure=grid.get_measures()
    print(measure)

    # to get the image visualization of the grid - this will show up on your screen in a separate window 

    grid.draw()
   
      
```
## Todos

- General code cleanliness
- More unit tests :)

## Library API Reference

The main features of StateSpaceGrid are [Trajectory](#trajectory) objects, [Grid](#grid) objects and
the associated [GridStyle](#gridstyle) and [GridQuantization](#gridquantization) objects which hold any extra data needed for drawing grids and calculating measures.

[Trajectory](#trajectory) objects hold the input data as a set of lists, along with a single ID number.

[Grid](#grid) objects hold trajectory objects and are the interface through which you
can display grids and calculate measures.

See [test_end_to_end.py](unit_tests/test_end_to_end.py), or the [examples](#examples) section of this readme for a brief example of the code in action.

### Trajectory

```python
Trajectory(data_x, data_y, data_t, style=TrajectoryStyle(), id=None)
```
Data in StateSpaceGridLib is organised via Trajectories. These objects take in data for the x axis of the grid, data for the y axis of the grid, and time data for the transitions between states (ie. the time data specifies the time at which each state starts, as well as the end time of the last state).
* `data_x`

   A list of state values for the x axis. The length of this list is expected to be the same as for the y data.

* `data_y`

   A list of state values for the y axis. The length of this list is expected to be the same as for the x data.
* `data_t`

   Time data: a list of length 1 longer than the x or y data, specifying the start time of each event in the data_x/data_y lists as well as the end point of the final event.
* `style`
   [TrajectoryStyle](#trajectorystyle) object containing options for the display of the trajectory on a grid in MatPLotLib.

* `id`

   An integer id number for the Trajectory object. If left blank, this defaults to the global number of trajectory objects at time of creation. 
```python
Trajectory.get_num_visits()
```
Return number of "visits", defined as the number of state transitions plus 1 (the initial starting state) minus the number of transitions to the same state as where the transition is from (ie. `(x1, y1) -> (x2, y2)` where `x1 = x2` and `y1 = y2`).
```python
Trajectory.get_cell_range()
```
Return number of unique cells visited.
```python
Trajectory.get_states(x_ordering=None, y_ordering=None, merge_repeated_states=True)
```
Return formatted state data.
* `x_ordering`

   An optional list defining the ordering of the x data scale. If it is a numerical scale, this can be left blank.
   
   eg. `["low", "medium", "high"]`
* `y_ordering`

   An optional list defining the ordering of the y data scale. If it is a numerical scale, this can be left blank.
   
   eg. `["low", "medium", "high"]`
* `merge_repeated_states`

   Boolean flag to control whether or not adjacent events with repeated states should be merged. This defaults to True.
```python
Trajectory.calculate_dispersion(total_cells)
```
Return dispersion for trajectory.
* `total_cells`

   Total number of cells in the state space grid.

```python
Trajectory.from_legacy_trj(filename, params=(1,2))
```
Return a trajectory object initialised from a GridWare trajectory file.
* `filename`

   The path to the trajectory file.
* `params`

   A tuple containing the two column names of the parameters of interest.
   
### TrajectoryStyle
```python
TrajectoryStyle(colour=None, alpha=1.0, connection_style="arc3,rad=0.0", arrow_style="-|>")
```
* `colour`

   Colour for the nodes in the trajectory when it is drawn on a grid. 
   This can either be in the form of a colour name (eg. "red) or as a 6 digit hexadecimal value (eg. "#ffffff"). See [here](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html) for more information.
* `alpha`

   Transparency for the nodes in the trajectory when drawn on a grid on a scale from 0 (completely transparent) to 1 (opaque).
* `connection_style`

   Style of curve connecting nodes on the trajectory graph. See https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.FancyArrowPatch.html#matplotlib.patches.FancyArrowPatch for more information on the options.
* `arrow_style`

   Style of arrow on edges connecting nodes on the trajectory graph. See https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.ArrowStyle.html#matplotlib.patches.ArrowStyle for more information on the options.
   
### Grid
```python
Grid(trajectory_list, quantization=GridQuantization())
```
Data now formatted as [Trajectory](#trajectory) objects can be collated within a `Grid` object for visualisation and the calculation of grid measures.
* `trajectory_list`
   
   A list of [Trajectory](#trajectory) objects containing the input data.

* `quantization`

   A [GridQuantization](#gridquantization) object containing data relevant to the calculation of grid measures. If left blank, this defaults to the default settings in [GridQuantization](#gridquantization).
```python
Grid.draw(save_as=None, style=GridStyle())
```
   Draw visualisation of state space grid.
* `save_as`

   If provided, this is the name of the png file that the image of the grid is saved as.  If left blank, the grid will be displayed in a new window using whichever gui library matplotlib has access to.
* `style`

   [GridStyle](#gridstyle) object containing options for the display of the grid in MatPLotLib.
```python
Grid.get_measures()
```
Calculate cumulative measures from all trajectories provided to the grid and return as a `GridMeasures` object.
### GridStyle
```python
GridStyle(title="", label_font_size=14, tick_font_size=14, title_font_size=14, x_label=None, y_label=None, rotate_xlabels=False, checker_light=(220/256, 220/256, 220/256), checker_dark=(1, 1, 1), connection_style="arc3,rad=0.0", arrow_style="-|>")
```
Object containing visualisation customisation.
* `title`

   Grid title
* `label_font_size`

   Axis label font size
* `tick_font_size`

   Axis tick font size
* `title_font_size`

   Title font size
* `x_label`

   X axis label
* `y_label`

   Y axis label
* `rotate_xlabels`

   Rotate x axis tick labels by 90°.
* `checker_light`

   Colour of light squares on state space grid.
   
* `checker_dark`

   Colour of dark squares on state space grid.

### GridQuantization
```python
GridQuantization(cell_size_x=None, cell_size_y=None, x_order=None, y_order=None, x_min=None, x_max=None, y_min=None, y_max=None)
```
Object containing extra data relevant to grid measure calculation and visualisation.
* `cell_size_x`
    
   Width of a cell in the x axis. If left blank, a best guess will be calculated from the data available.
* `cell_size_y`
   
   Height of a cell in the y axis. If left blank, a best guess will be calculated from the data available.
* `x_order`

   An optional list defining the ordering of the x data scale.
   
   eg. `["low", "medium", "high"]` 
   
   If it is a numerical scale, this can be left blank.
* `y_order`

   An optional list defining the ordering of the y data scale.
   
   eg. `["low", "medium", "high"]`
   
    If it is a numerical scale, this can be left blank.
* `x_min`

   The lowest value in the x measurement scale. If left blank this is the lowest value in the data given.
* `x_max`

   The highest value in the x measurement scale. If left blank, this is the highest value in the data given.
* `y_min`

   The lowest value in the y measurement scale. If left blank this is the lowest value in the data given.
* `y_max`

   The highest value in the y measurement scale. If left blank, this is the highest value in the data given.
### GridMeasures
```python
GridMeasures()    
```
Data container for all measure data. Individual values can be read off, or the entire thing may be printed as is.
```python
GridMeasures.trajectory_ids
```
IDs of all trajectories in grid.
```python
GridMeasures.mean_duration
```
Mean total duration of the trajectories
```python
GridMeasures.mean_number_of_events
```
Mean number of events in the trajectories
```python
GridMeasures.mean_number_of_visits
```
Mean number of visits in the trajectories.

A visit is defined as being an entrance and then an exit of a cell.
```python
GridMeasures.mean_cell_range
```
Mean number of different cells reached by the trajectories.
```python
GridMeasures.overall_cell_range
```
Total number of cells visited cumulatively by the trajectories. 
```python
GridMeasures.mean_duration_per_event
```
Mean duration per event

Defined as mean of trajectory duration divided by number of trajectory events.
```python
GridMeasures.mean_duration_per_visit
```
Mean duration per visit

Defined as mean of trajectory duration divided by number of trajectory visits.
```python
GridMeasures.mean_duration_per_cell
```
Mean duration spent in each cell

Defined as mean of trajectory duration divided by trajectory cell range.
```python
GridMeasures.dispersion
```
Mean of trajectory dispersion across all trajectories. Dispersion for a single trajectory is calculated by the formula
$$\text{dispersion}=1-\frac{n(\sum_{i}{(\frac{d_i}{D})^2})-1}{n-1}$$
where $D$ is the total duration of the trajectory, $d_i$ is the duration in cell $i$, and $n$ is the number of cells in the entire grid.
```python
GridMeasures.visited_entropy
```
Entropy of visits, defined as 
$$\sum_{i}{\frac{P_i}{\ln(P_i)}}$$
where $P_i$ is the probablity of visiting cell $i$, defined as
$$P_i = \frac{\text{Number of visits to cell i}}{\text{total number of visits}}$$

