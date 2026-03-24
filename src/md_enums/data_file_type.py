from enum import Enum

class DataFileType(Enum):
    DUMP_NETCDF = "dump_netcdf"
    DUMP_TXT = "dump_txt"
    WRITE_DATA = "write_data"