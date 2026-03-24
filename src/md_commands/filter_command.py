from md_commands.command_helpers import parse_float, parse_float_or_none, parse_int
from md_commands.command_interface import Command
from md_enums.filter_type import FilterType
from md_filters.filter_interface import Filter
from md_filters.and_filter import AndFilter
from md_filters.atom_type_filter import AtomTypeFilter
from md_filters.cartesian_filter import CartesianFilter
from md_filters.radial_filter import RadialFilter
from session_state import SessionState

class FilterCommand(Command):    
    def __init__(self, filter_name: str, filter_type: FilterType, filter_params: list[str]):
        self._filter_name = filter_name
        self._filter_type = filter_type
        self._filter_params = filter_params
    
    #TODO: Do parameter parsing and validation somewhere else, like in CommandFactory
    def execute(self, state: SessionState):
        if self._filter_type == FilterType.AND:
            # "And" filter takes two or more filter names as parameters
            if len(self._filter_params) < 2:
                raise Exception("'and' filter requires at least two filter names as parameters")
            filters: list[Filter] = []
            for filter_name in self._filter_params:
                if filter_name not in state.filters:
                    raise Exception(f"'and' filter parameter '{filter_name}' does not correspond to a previously defined filter")
                filters.append(state.filters[filter_name])
            state.filters[self._filter_name] = AndFilter(filters)
        elif self._filter_type == FilterType.ATOM_TYPE:
            # Atom type filter takes a list of atom types (integers) as parameters
            if len(self._filter_params) == 0:
                raise Exception("'atom_type' filter requires at least one atom type as a parameter")
            atom_types: set[int] = set()
            for filter_name in self._filter_params:
                atom_types.add(parse_int(filter_name))
            state.filters[self._filter_name] = AtomTypeFilter(atom_types)
        elif self._filter_type == FilterType.CARTESIAN:
            # Cartesian filter takes 6 parameters: x_min, x_max, y_min, y_max, z_min, z_max
            if len(self._filter_params) != 6:
                raise Exception("'cartesian' filter requires exactly six parameters: x_min (float or 'none'), x_max (float or 'none'), y_min (float or 'none'), y_max (float or 'none'), z_min (float or 'none'), z_max (float or 'none')")
            x_min = parse_float_or_none(self._filter_params[0])
            x_max = parse_float_or_none(self._filter_params[1])
            y_min = parse_float_or_none(self._filter_params[2])
            y_max = parse_float_or_none(self._filter_params[3])
            z_min = parse_float_or_none(self._filter_params[4])
            z_max = parse_float_or_none(self._filter_params[5])
            state.filters[self._filter_name] = CartesianFilter(x_min, x_max, y_min, y_max, z_min, z_max)
        elif self._filter_type == FilterType.RADIAL:
            # Radial filter takes 5 parameters: x, y, z, r_min, r_max
            if len(self._filter_params) != 5:
                raise Exception("'radial' filter requires exactly five parameters: x, y, z, r_min (float or 'none'), r_max (float or 'none')")
            x = parse_float(self._filter_params[0])
            y = parse_float(self._filter_params[1])
            z = parse_float(self._filter_params[2])
            r_min = parse_float_or_none(self._filter_params[3])
            r_max = parse_float_or_none(self._filter_params[4])
            state.filters[self._filter_name] = RadialFilter(x, y, z, r_min, r_max)
        else:
            raise Exception(f"Unsupported filter_type specified in configuration: '{self._filter_type}' (supported types are {[item.value for item in FilterType]})")