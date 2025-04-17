import math

# Atomic masses lookup table (should match the masses in the LAMMPS data file)
masses = {
    "C": 12.011,
    "Cl": 35.453,
    "F": 18.9984,
    "H": 1.008,
    "Na": 22.98977,
    "O": 15.9994,
}

# Starting radius to use when building radial count/density profiles as a series of concentric spherical shells
min_radius_for_radial_profiles = 10

# For sphere volume calculation
four_thirds_pi = 4.0 * math.pi / 3.0