"""Module that generates specifiable windows from time-series data."""
import numpy as np
import numpy.typing as npt


def create_array_window(
    data: npt.NDArray[np.float64], input_length: int, output_length: int
) -> npt.NDArray[np.float64]:
    """Creates a 3 dimensional array of windows out of a single time series.

    Args:
        data: Time series of the shape (n,m), with n observations and m attributes.
        input_length: Length of the input window.
        output_length: Length of the output window.

    Returns:
        window: Time series transformed into an 3 dimensional windowing array,
        (x,y,z) with x: windows, y: time points, z: attributes
    """
    window = data.reshape((data.shape[0], 1, data.shape[1]))
    i = 0
    total_width = input_length + output_length
    for i in range(total_width - 1):
        new_column = np.roll((window[:, i, :]), -1, axis=0).reshape(
            window.shape[0], 1, window.shape[2]
        )
        window = np.append(window, new_column, 1)
    # Drop all rows that include missing data
    window = np.delete(
        window, [window.shape[0] - i for i in range(1, total_width)], axis=0
    )
    return window


def create_window_dataset(
    data_list: list[npt.NDArray[np.float64]], input_length: int, output_length: int
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Creates dataset in the form of a 3 dimensional array of windows.

    Args:
        data_list: 3D array of time series in the shape (x,y,z),
            with x observations y timestamps and m attributes.
        input_length: Length of the input window.
        output_length: Length of the output window.

    Returns:
        X: Input data of the shape (x,y,z),
            with x: windows, y: time points, z: attributes
        y: Output data of the shape (x,y,z),
            with x: windows, y: time points, z: attributes
    """
    windows = np.concatenate(
        [create_array_window(data, input_length, output_length) for data in data_list],
        axis=0,
    )
    X = windows[:, :input_length]
    y = windows[:, input_length:]
    return X, y
