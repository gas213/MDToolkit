import os.path

from md_dataclasses.atom import Atom
from md_dataclasses.header import Header
from md_readers.config_reader import ConfigReader
from md_readers import lmp_data_reader as datatxt
from md_readers import dump_txt_reader as dumptxt

def check_path(path: str):
    if path is None:
        raise Exception("Data file path not provided")
    elif not os.path.isfile(path):
        raise Exception(f"No data file was found at the specified path: {path}")

def read_header(config: ConfigReader) -> Header:
    check_path(config.data_path)
    if config.data_type == "LAMMPSData": return datatxt.read_header(config)
    elif config.data_type == "DumpText": return dumptxt.read_header(config)
    else: raise Exception("Unsupported data format specified in config file")

def read_atoms(config: ConfigReader) -> list[Atom]:
    check_path(config.data_path)
    if config.data_type == "LAMMPSData": return datatxt.read_atoms(config)
    elif config.data_type == "DumpText": return dumptxt.read_atoms(config)
    else: raise Exception("Unsupported data format specified in config file")