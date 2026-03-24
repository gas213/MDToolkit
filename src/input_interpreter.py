from md_commands.command_factory import create_command
from session_state import SessionState

class InputInterpreter:
    _lines: list[str]
    _index: int = 0

    def __init__(self, input: list[str]):
        self._lines = []
        for line in input:
            if line.strip() == "": continue
            if line.startswith("#"): continue
            if line.startswith("-"): continue
            if line.startswith("="): continue
            self._lines.append(line)
        
    def run(self, state: SessionState):
        while self._index < len(self._lines):
            self.interpret_next(state)

    def interpret_next(self, state: SessionState):
        terms = self._lines[self._index].split()
        current_command = terms[0].lower()
        args = terms[1:] if len(terms) > 1 else []
        state.logger.debug(f"Interpreting command: {self._lines[self._index]}")
        command = create_command(current_command, args)
        command.execute(state)
        
        if current_command == "next_file" and state.data_files_index < len(state.data_files):
            # Navigate back to the most recent read_atoms command if there are still more files to process
            while self._index >= 0:
                self._index -= 1
                if self._lines[self._index].split()[0].lower() == "read_atoms": break
            if self._index < 0: raise Exception("next_file command did not find a read_atoms command to navigate back to")
        else:
            self._index += 1