import netCDF4 as nc

def test(path):
    id = 0
    data = nc.Dataset(path, "r")
    for frame in data.variables["coordinates"]:
        for atom in frame:
            id += 1
            print(str(id) + " ".join(format(coord, "10.3f") for coord in atom))
    return