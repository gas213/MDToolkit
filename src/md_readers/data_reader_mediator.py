from md_dataclasses.atom import Atom
from md_dataclasses.header import Header
from md_readers.config_reader import ConfigReader
from md_readers import lmp_data_reader as datatxt
from md_readers import dump_nc_reader as dumpnc
from md_readers import dump_txt_reader as dumptxt

def read_header(config: ConfigReader, data_file: str) -> Header:
    if config.data_type == "LAMMPSData": return datatxt.read_header(data_file)
    elif config.data_type == "DumpText": return dumptxt.read_header(data_file)
    elif config.data_type == "NetCDF": return dumpnc.read_header(data_file)
    else: raise Exception("Unsupported data format specified in config file")

def read_atoms(config: ConfigReader, data_file: str) -> list[Atom]:
    if config.data_type == "LAMMPSData": return datatxt.read_atoms(config, data_file)
    elif config.data_type == "DumpText": return dumptxt.read_atoms(config, data_file)
    elif config.data_type == "NetCDF": return dumpnc.read_atoms(data_file)
    else: raise Exception("Unsupported data format specified in config file")