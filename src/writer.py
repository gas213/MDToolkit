import datetime

from constants import analysis_filetype

def write(config, atom_extremes, density_profiles, sanity_checks, vapor_counter):
    with open(config["data path"] + analysis_filetype, "w") as analysis:
        analysis.write("ANALYSIS OF DATA FILE LOCATED AT: " + str(config["data path"]) + "\n")
        analysis.write("Performed: " + str(datetime.datetime.now()) + "\n")
        analysis.write("\nSanity checks: " + str("FAILED" if any(val == False for val in sanity_checks.values()) else "SUCCEEDED") + "\n\n")
        analysis.writelines(str(key) + ": " + str(val) + "\n" for key, val in sanity_checks.items())
        analysis.write("\nHeader aka config values:\n\n")
        analysis.writelines(str(key) + ": " + str(val) + "\n" for key, val in config.items())
        analysis.write("\nMost extreme atom coordinates:\n\n")
        analysis.writelines(str(key) + ": " + str(val) + "\n" for key, val in atom_extremes.items())
        analysis.write("\nNumber of oxygen atoms within vapor measurement box: " + str(vapor_counter) + "\n")
        for axis in ["x", "y", "z"]:
            analysis.write("\nProfile of atom density (count) by truncated " + axis + " coordinate:\n\n")
            analysis.writelines(str(key) + ": " + str(val) + "\n" for key, val in density_profiles[axis].items())