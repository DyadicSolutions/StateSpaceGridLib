import pytest
from state_space_grid import trajectory


@pytest.mark.parametrize("x0", [0, 1, 3.7])
@pytest.mark.parametrize("y0", [0, 1, 3.7])
@pytest.mark.parametrize("t1", [1, 3.7])
@pytest.mark.parametrize("grid_points", [2, 5])  # nb. 1 == div/0
def test_calculate_dispersion_single_point(x0, y0, t1, grid_points):
    traj = trajectory.Trajectory(
        data_x=[x0],
        data_y=[y0],
        data_t=[0, t1],
    )
    result = traj.calculate_dispersion(grid_points)
    assert result == 0


@pytest.mark.parametrize("n_times", [2, 3, 4, 5])
def test_calculate_dispersion_uniform_distribution(n_times):
    """
    I think that dispersion is 0 if each cell is only hit once?
    -------
    """
    x_data = []
    y_data = []
    for i in range(n_times):
        for j in range(n_times):
            x_data.append(i)
            y_data.append(j)

    traj = trajectory.Trajectory(
        data_x=x_data,
        data_y=y_data,
        data_t=list(range(n_times**2 + 1)),
    )
    result = traj.calculate_dispersion(n_times**2)
    assert result == 1.0


def test_calculate_dispersion_two_points():
    traj = trajectory.Trajectory(
        data_x=[1, 5],
        data_y=[1, 5],
        data_t=[0, 1, 3],
    )
    result = traj.calculate_dispersion(99)
    expected = 0.44897959
    assert abs(result - expected) < 1e-3, f"got {result}, expected about {expected}"


@pytest.mark.parametrize(
    "data_t,grid_size,expected",
    [
        # hardcoded dispersion values as regression test
        (list(range(10)), 100, 0.897867),
        (list(range(10)), 973, 0.889803),
        ([0, 1, 5, 7, 10, 11, 29, 75, 89, 99], 100, 0.724931),
        ([0, 1, 5, 7, 10, 11, 29, 75, 89, 99], 256, 0.720496),
        ([i * 10 for i in range(10)], 100, 0.897867),
    ],
)
@pytest.mark.parametrize(
    "dummy_y_vals",  # y vals should not affect the answer for distinct x vals
    [list(range(9)), [0 for _ in range(9)]],
)
def test_calculate_dispersion_distinct_x_regression(
    data_t,
    grid_size,
    expected,
    dummy_y_vals,
):
    """
    data x always separate, so dispersion depends upon data_t and grid size
    and data_y should not affect the result.
    """
    traj = trajectory.Trajectory(
        data_x=list(range(9)),
        data_y=dummy_y_vals,
        data_t=data_t,
    )
    result = traj.calculate_dispersion(grid_size)
    assert abs(result - expected) < 1e-4, f"got {result}, expected about {expected}"
