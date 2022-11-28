# Practical Astrodynamics: time correction data
This script provides a way to load (or retrieve from the internet) correction data for moving
between time standards.

The [load_time_correction_data](https://github.com/JasperJeuken/PracticalAstrodynamicsTime/blob/main/main.py#L5-L65)
function can be used to load information for both the
[UT1](https://en.wikipedia.org/wiki/Universal_Time) time standard and the GPS time standard
([International Atomic Time](https://en.wikipedia.org/wiki/International_Atomic_Time)).

## How it works
The tool retrieves time correction data for moving from several time standards to [UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time).
The user should specify which time standard should be looked up (see [Inputs](#inputs)). The script initially looks for a local file with time correction information. If it does not exist, 
it accesses US Naval Observatory data, retrieves it, and saves it into a file. The data is then read
into Python and returned in a standardised format (see [Outputs](#outputs)).

## Inputs
The script takes as an input the name of the time standard to convert to UTC from. Currently,
the standards `GPS` and `UT1` are supported. These names can be provided as a string to the function using the
`standard` keyword argument.

## Outputs
The function returns three items:
1. `list[int]`: list containing whole number parts of the Julian dates corresponding to the data list
2. `list[float]`: list containing fractional parts of the Julian dates above
3. `list[float`: time correction value in seconds (`={standard} - UTC`)

Note that all lists are of the same length, and each index corresponds to a data point with a time and value.

## How to use
1. Import or copy the function `load_time_correction_data` from [main.py](main.py).
2. Call the function specifying correction data for which time standard you want ('GPS' or 'UT1').
3. The function returns 

## Example
An example is provided at the bottom of [main.py](main.py) that uses the tool to retrieve GPS time
correction information and plots the correction value against the returned Julian dates correspdnding to it.

The code is also given below:
```python
import matplotlib.pyplot as plt

# Use the function to retrieve time correction data (choose a time standard)
corr_jds, corr_frs, corr_data = load_time_correction_data(standard='GPS')  # alternatively: GPS

# Plot the data against the provided Julian date
fig, ax = plt.subplots()
ax.plot(corr_jds, corr_data)
plt.show()
```