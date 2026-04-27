# MDToolkit

A command-based toolkit for analyzing molecular dynamics simulation data. Scripts are written as plain text files with one command per line; the toolkit reads them sequentially and executes each command against a shared session state.

## Script Structure

A typical script follows the pattern below.
- Blank lines as well as lines beginning with # or - or = are ignored
- All commands are case-insensitive, but their parameters are processed as-is (the value of data_path is case-sensitive, for example)

```
# Initialization

step_start
step_end
data_path
data_type
[atom_data_column commands]
[atom_mass commands]

# Analysis Loop

read_file
[filter definitions]
[one or more analysis commands]
next_file
```

---

## Command Reference

### `atom_data_column`

Maps an atom property to its column index in the data file. Required for `dump_txt` and `write_data` formats. Must be called once for each of the five required columns: `id`, `type`, `x`, `y`, `z`.

```
atom_data_column <column_type> <column_index>
```

| Argument       | Type    | Values                        | Description                          |
|----------------|---------|-------------------------------|--------------------------------------|
| `column_type`  | string  | `id`, `type`, `x`, `y`, `z`  | The atom property this column holds  |
| `column_index` | integer | ≥ 0                           | Zero-based column index in the file  |

---

### `atom_mass`

Registers the atomic mass for an atom type. Required for any analysis that uses mass-weighted calculations (e.g., center of mass, radial density profile).

```
atom_mass <atom_type> <atom_mass>
```

| Argument    | Type    | Description                           |
|-------------|---------|---------------------------------------|
| `atom_type` | integer | Numeric identifier for the atom type  |
| `atom_mass` | float   | Atomic mass in the simulation units   |

Call this once per atom type present in the simulation.

---

### `cartesian_density_profile`

Calculates the number density of atoms as a function of position along a cartesian axis. Results are written to a file.

```
cartesian_density_profile <filter_name> <aggregation_type> <axis> <bin_start> <bin_stop> <bin_step> <normalization_density> <write_path_relative>
```

| Argument                | Type         | Description                                                          |
|-------------------------|--------------|----------------------------------------------------------------------|
| `filter_name`           | string       | Name of a defined filter selecting the atoms to include              |
| `aggregation_type`      | string       | `none` or `average` — how to combine results across timesteps        |
| `axis`                  | string       | `x`, `y`, or `z` — axis along which to compute the density profile   |
| `bin_start`             | float / none | Start of the position range; `none` uses the simulation box boundary |
| `bin_stop`              | float / none | End of the position range; `none` uses the simulation box boundary   |
| `bin_step`              | float        | Width of each position bin                                           |
| `normalization_density` | float        | Reference bulk density used to normalize the profile                 |
| `write_path_relative`   | string       | Output file path relative to the results directory                   |

Uses atom masses and the cross-sectional area perpendicular to the chosen axis for density calculations.

---

### `center_of_mass`

Calculates the center of mass of all loaded atoms for the current timestep.

```
center_of_mass <aggregation_type>
```

| Argument           | Type   | Values            | Description                                                              |
|--------------------|--------|-------------------|--------------------------------------------------------------------------|
| `aggregation_type` | string | `none`, `average` | `none` replaces any prior result; `average` accumulates across timesteps |

Requires `atom_mass` to be defined for every atom type present. The result is used by `radial_density_profile`.

---

### `data_path`

Sets the directory containing simulation data files and initializes the output results directory. This should be one of the first commands in a script.

```
data_path <path>
```

| Argument | Type   | Description                                     |
|----------|--------|-------------------------------------------------|
| `path`   | string | File system path to the directory of data files |

After this command runs, the toolkit discovers all data files in the directory and filters them to those whose step numbers fall within `[step_start, step_end]`.

---

### `data_type`

Specifies the format of the data files to be processed. Must be called before reading atom data.

```
data_type <data_type>
```

| Argument    | Type   | Values                                  | Description               |
|-------------|--------|-----------------------------------------|---------------------------|
| `data_type` | string | `dump_netcdf`, `dump_txt`, `write_data` | File format of data files |

- `dump_netcdf` — NetCDF binary format; `atom_data_column` commands are not required
- `dump_txt` — LAMMPS text dump format; requires `atom_data_column` commands for each column
- `write_data` — LAMMPS `write_data` format; requires `atom_data_column` commands

---

### `filter`

Creates a named filter that selects a subset of atoms for use in analysis commands. Filters are referenced by name in commands like `radial_density_profile` and `first_neighbor_histogram`.

```
filter <filter_name> <filter_type> [parameters...]
```

| Argument      | Type   | Description                                          |
|---------------|--------|------------------------------------------------------|
| `filter_name` | string | Unique name for this filter (cannot be `all`)        |
| `filter_type` | string | `atom_type`, `cartesian`, `radial`, or `and`         |

The remaining parameters depend on `filter_type`:

#### `atom_type`

Selects atoms whose type matches any of the given type IDs.

```
filter <name> atom_type <type_id> [type_id ...]
```

| Parameter | Type    | Description                        |
|-----------|---------|------------------------------------|
| `type_id` | integer | One or more atom type IDs to match |

Example: `filter water atom_type 6 7`

#### `cartesian`

Selects atoms within an axis-aligned bounding box. Use `none` to leave a bound unrestricted.

```
filter <name> cartesian <x_min> <x_max> <y_min> <y_max> <z_min> <z_max>
```

| Parameter | Type         | Description                                         |
|-----------|--------------|-----------------------------------------------------|
| `x_min`   | float / none | Minimum x coordinate (or `none` for no lower bound) |
| `x_max`   | float / none | Maximum x coordinate (or `none` for no upper bound) |
| `y_min`   | float / none | Minimum y coordinate                                |
| `y_max`   | float / none | Maximum y coordinate                                |
| `z_min`   | float / none | Minimum z coordinate                                |
| `z_max`   | float / none | Maximum z coordinate                                |

Example: `filter slab cartesian 0.0 50.0 none none 10.0 40.0`

#### `radial`

Selects atoms within a spherical shell centered at a fixed point.

```
filter <name> radial <cx> <cy> <cz> <r_min> <r_max>
```

| Parameter | Type         | Description                                           |
|-----------|--------------|-------------------------------------------------------|
| `cx`      | float        | X coordinate of the sphere center                     |
| `cy`      | float        | Y coordinate of the sphere center                     |
| `cz`      | float        | Z coordinate of the sphere center                     |
| `r_min`   | float / none | Minimum radial distance (or `none` for no inner bound) |
| `r_max`   | float / none | Maximum radial distance (or `none` for no outer bound) |

Example: `filter core radial 25.0 25.0 25.0 none 10.0`

#### `and`

Combines two or more existing filters, selecting only atoms that pass all of them.

```
filter <name> and <filter_name_1> <filter_name_2> [filter_name ...]
```

| Parameter     | Type   | Description                       |
|---------------|--------|-----------------------------------|
| `filter_name` | string | Name of an already-defined filter |

Example: `filter water_core and water core`

---

### `first_neighbor_histogram`

Builds a histogram of distances from each central atom to its nearest neighbor within a threshold radius. Results are written to a file.

```
first_neighbor_histogram <filter_name_atoms_center> <filter_name_atoms_neighbor> <r_threshold> <aggregation_type> <write_path_relative>
```

| Argument                     | Type   | Description                                                   |
|------------------------------|--------|---------------------------------------------------------------|
| `filter_name_atoms_center`   | string | Filter selecting the central atoms                            |
| `filter_name_atoms_neighbor` | string | Filter selecting candidate neighbor atoms                     |
| `r_threshold`                | float  | Maximum distance to be considered a nearest neighbor          |
| `aggregation_type`           | string | `none` or `average` — how to combine results across timesteps |
| `write_path_relative`        | string | Output file path relative to the results directory            |

---

### `next_file`

Advances the session to the next data file in the sequence. Sets the `is_finished` flag to `true` after the last file, which can be used to terminate a processing loop.

```
next_file
```

No arguments.

---

### `radial_density_profile`

Calculates the number density of atoms as a function of radial distance from the center of mass. Results are written to a file.

```
radial_density_profile <filter_name> <aggregation_type> <bin_start> <bin_stop> <bin_step> <normalization_density> <write_path_relative>
```

| Argument                | Type   | Description                                                   |
|-------------------------|--------|---------------------------------------------------------------|
| `filter_name`           | string | Name of a defined filter selecting the atoms to include       |
| `aggregation_type`      | string | `none` or `average` — how to combine results across timesteps |
| `bin_start`             | float  | Start of the radial distance range                            |
| `bin_stop`              | float  | End of the radial distance range                              |
| `bin_step`              | float  | Width of each distance bin                                    |
| `normalization_density` | float  | Reference bulk density used to normalize the profile          |
| `write_path_relative`   | string | Output file path relative to the results directory            |

Requires `center_of_mass` to have been calculated. Uses atom masses for weighted density calculations.

---

### `read_file`

Reads header information as well as atomic coordinates and properties from the current data file into session state. Must be called each iteration before any analysis commands.

```
read_file
```

No arguments. Requires `data_path`, `data_type`, and (for text formats) `atom_data_column` definitions.

---

### `step_end`

Sets the upper bound (inclusive) on timestep numbers to process. Files with step numbers above this value are excluded.

```
step_end <step>
```

| Argument | Type    | Description                     |
|----------|---------|---------------------------------|
| `step`   | integer | Last timestep number to include |

---

### `step_start`

Sets the lower bound (inclusive) on timestep numbers to process. Files with step numbers below this value are excluded.

```
step_start <step>
```

| Argument | Type    | Description                      |
|----------|---------|----------------------------------|
| `step`   | integer | First timestep number to include |

---

### `write_dump`

Writes a new dump file given a filtered list of atoms, using the time step number of the data file currently read into memory.

```
write_dump <filter_name> <write_path_relative>
```

| Argument                | Type   | Description                                                   |
|-------------------------|--------|---------------------------------------------------------------|
| `filter_name`           | string | Name of a defined filter selecting the atoms to include       |
| `write_path_relative`   | string | Output file path relative to the results directory            |

---

## Aggregation Types

| Value     | Behavior                                                        |
|-----------|-----------------------------------------------------------------|
| `none`    | Replaces any previously computed result for the current file    |
| `average` | Accumulates results across multiple timesteps and averages them |
