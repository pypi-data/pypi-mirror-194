# Organic Navigation Reference Data

The `onavdata` module provides easy access to both **reference datasets** and **user-specified datasets** for the design, development, and testing of navigation algorithms.  Additionally, useful **utilities** are included for working with common navigation sensors.

**Reference datasets** are well understood, documented, and purged of data logging artifacts.  A valuable set of reference datasets are included with `onavdata`.  They are well-understood yet realistic datasets, making them useful for testing a data processing script or candidate algorithm.

**User-specified datasets** are managed and made available via the same `onavdata` interface as the reference datasets, with the exception that these datasets are added by the user.  Thus, the transition from reference to experimental datasets is relatively smooth.

**Utilities** are included for facilitating common unit conversions or getting data columns for common navigation sensors.

The primary data structure used by `onavdata` is the [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/user_guide/dsintro.html#dataframe).  A basic familiarity with DataFrames is recommended (e.g. one-liners to down-sample, average, plot, or save to CSV).  All configuration or meta data files use the easily understood [TOML](https://toml.io/en/) format.

## Quick Start

### List Data Available
All data sets are referenced using their shortname.
```python
>> import onavdata
>> onavdata.print_shortnames()
	2011 UMN-UAV GPSFASER1
	2012 UMN-UAV FASER5
	2012 UMN-UAV GPSFASER3
	2012 UMN-UAV THOR60
	2012 UMN-UAV THOR75
	2012 UMN-UAV THOR77
	2012 UMN-UAV THOR79
	2021-04-27 HGuide n380 Car Drive Between Traffic Lights
	2021-04-27 HGuide n380 Car Hill Driving
	SIM-MEASURED-CAR NORTH FIXED-SPEED FIXED-HEADING
	SIM-MEASURED-CAR NORTH FIXED-SPEED VARY-HEADING
	SIM-MEASURED-CAR NORTH VARY-SPEED FIXED-HEADING
	SIM-MEASURED-CAR NORTH VARY-SPEED VARY-HEADING
	SIM-PERFECT-CAR NORTH FIXED-SPEED FIXED-HEADING
	SIM-PERFECT-CAR NORTH FIXED-SPEED VARY-HEADING
	SIM-PERFECT-CAR NORTH VARY-SPEED FIXED-HEADING
	SIM-PERFECT-CAR NORTH VARY-SPEED VARY-HEADING
```

### Load a Reference Data Set
An arbitrary data set can be loaded if no shortname is specified.  In this case the data from `2014 UMN-UAV THOR77` was returned.
```python
>> import onavdata
>> df = onavdata.get_data()
	get_data(): No shortname specified so choice will be arbitrary.  Returning: 2014 UMN-UAV THOR77
>> df.head()
		           AccelX (m/s^2)  AccelY (m/s^2)  AccelZ (m/s^2)       ...         AngleHeading (rad)  AnglePitch (rad)  AngleRoll (rad)
	TimeFromStart (s)                                                       ...
	0.00                     1.862795       -0.392167       -9.673463       ...                   1.004700          0.192806         0.006130
	0.02                     1.895476       -0.424848       -9.640783       ...                   1.004225          0.192856         0.006130
	0.04                     1.895476       -0.359487       -9.706145       ...                   1.003786          0.192888         0.006259
	0.06                     1.895476       -0.392167       -9.640783       ...                   1.003258          0.192990         0.006354
	0.08                     1.895476       -0.392167       -9.640783       ...                   1.002907          0.193056         0.006482

	[5 rows x 12 columns]
```


### Load User-Specified Datasets

#### Add Dataset Folder
The `examples/simple_data_load.py` file shows an example of adding a user-specified dataset using the `add_dataset()` method.  There are two main requirements:

1. Path to a file named `shortnames.txt`, populated with a suitable entries for each dataset. Namely:
	- A *shortname* for the dataset
	- Path to dataset file(s)
	- Path to an associated meta data file for the dataset (more on this below)
2. Informing `onavdata` of the user-specified datasets by using the `onavdata.add_dataset()` function.

Multiple `shortnames.txt` can be used (e.g. using one per project).  Assuming no conflicting shortnames, there is no issue with adding multiple user-specified datasets.

#### Directly Load Dataset
The `examples/simple_data_load_direct.py` file shows how it is possible to directly load a user-specified dataset.  The two requirements are:
1. The path (or list of paths) to the dataset
2. A meta data dictionary

This is advantages for programmatically using `onavdata`.

### Apply Meta to DataFrame
The `examples/apply_meta_to_dataframe.py` file shows how a dataset meta (see description below) can be applied to an existing dataframe.  This is useful for programmatically transforming a loaded dataset using meta parameters.

## Dataset Meta Data

Each dataset must have an associated meta (data) file.  The meta file contains parameters necessary to pre-process and load the dataset in a *clean* state.  Steps like adding a time-index, renaming columns, rotating axes, dropping rows where data is unreliable... all of these and more are made possibly by parameter specifications in the meta file.  Hence, the data loading process handles the steps to clean a raw dataset.  The goal is for experimental user-specified datasets to have similar quality (e.g. remove unreliable transients) and attributes (e.g. columns names) as reference datasets.

Note that more than one dataset can point to the same meta file.  This is commonly done when multiple datasets are collected using the same device or setup.

## Sample Meta Data File Format

Below is an example meta file with all possible parameters demonstrated.  Comment lines begin with the `#` symbol.  In practice, only the parameters needed should be included.

**sample_meta.toml**:
```toml
# Define Sampling Time.
# Checks for a `TimeFromStart (s)` column (after column renaming) or uses the
# specified sampling freq. The latter is only used if the former doesn't exist.
# 'SampleFreq (Hz)' = 200

# Rows to skip before loading dataset (e.g. multi-line header).
'skip-lines'= 0

# Option to drop unnamed columns.
'drop-unnamed' = True

# Specify list of columns to load (or list of columns to drop `columns-drop`).
'columns-use' = ['Time (s)', 'Ax', 'Ay', 'Az', 'GNSSNumSV', 'GNSSFix']
# 'columns-drop' = ['Empty Channel 1']

# Drop rows if column has a matching entry with a list of values.
[drop-rows-where]
'GNSSNumSV' = [0]

# Only keep rows if column has a matching entry with a list of values.
[keep-rows-where]
'GNSSFix' = [1]

# Only keep rows where column has entries GREATER than, LESS than, or BETWEEN.
[keep-rows-gt]
'Time (s)' = 5

[keep-rows-lt]
'Time (s)' = 65

[keep-rows-between]
'Az' = [-1, 1]

# Override default dtypes
# The dtype names must be acceptable to pd.DataFrame.astype() function.
[columns-dtype]
'GNSSNumSV' = 'int32'

# Round columns to decimals specified.
[columns-round-decimals]
'Ax' = 3
'Ay' = 3
'Az' = 3

# Subtract offset for specific columns (e.g. remove sensor bias).
[columns-subtract-offset]
'Ax' = 0.23
'Ay' = 0.01
'Az' = -0.1

# Scale data for specific columns (e.g. change units).
[columns-scale]
'Ax' = 9.81
'Ay' = 9.81
'Az' = 9.81

# Rename columns: 'old name' = 'new name'
[columns-rename]
'Time (s)' = 'TimeFromStart (s)'
'Ax' = 'AccelX (m/s^2)'
'Ay' = 'AccelY (m/s^2)'
'Az' = 'AccelZ (m/s^2)'

# Apply rotations to groups of columns which start with key.
# Notes:
#   Columns found are sorted so as to get order: X->Y->Z
#   Key entries should refer to the renamed column names
[Rsensor2body]
'Accel' = [[ 0, -1,  0],
           [-1,  0,  0],
           [ 0,  0, -1]]
# The columns with the `Accel` prefix will be found and the defined rotation
# matrix applied.

# Add additional columns with constant values, or by copying another column.
[add-columns]
'AnglePitch (rad)' = 0.0
'Temperature (C)' = 28.0
'No. of Satellites' = 'GNSSNumSV'
```
