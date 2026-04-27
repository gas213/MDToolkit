import os.path

from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_operations.write_dump import write_dump
from session_state import SessionState

class WriteDumpCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_exact_arg_count(args, 2)
        self._filter_name = args[0]
        self._write_path_pattern_relative = args[1]
        if self._write_path_pattern_relative.count("*") != 1:
            raise Exception("Exactly one wildcard (*) is expected in write_dump path")

    def execute(self, state: SessionState):
        write_path_full: str = os.path.join(str(state.results_path), self._write_path_pattern_relative.replace("*", str(state.step_current)))
        os.makedirs(os.path.dirname(write_path_full), exist_ok=True)
        state.md_logger.log(f"Writing dump file to {write_path_full}...")
        if state.header is None:
            raise Exception("Cannot perform write_dump without header information; make sure to read in a data file before writing a dump file.")
        atoms = state.get_filtered_atoms(self._filter_name)
        write_dump(write_path_full, state.header.box, state.step_current, atoms)