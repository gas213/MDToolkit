import math

analysis_filetype = ".analysis"

# Sphere that closely but safely envelops the equilibrated droplet
# Used for situations where we need a loose idea of which particles belong to the droplet and which are vapor
# (ex. counting vapor particles or finding droplet's center of mass)
approximation_sphere = {
    "x": 231.0,
    "y": 223.0,
    "z": 304.0,
    "r": 165.0,
}

# Atomic masses lookup table, as given in the atom data file
masses = {
    1: 12.011,    # C
    2: 12.011,    # C
    3: 18.9984,   # F
    4: 35.453,    # Cl
    5: 22.98977,  # Na
    6: 15.9994,   # O
    7: 1.008      # H
}

atom_type_groups = {
    "oxygen": [6],
    "salt": [4, 5],
    "saltwater": [4, 5, 6, 7]
}

# Starting radius to use when building radial count/density profiles as a series of concentric spherical shells
min_radius_for_radial_profiles = 10

# For sphere volume calculation
four_thirds_pi = 4.0 * math.pi / 3.0