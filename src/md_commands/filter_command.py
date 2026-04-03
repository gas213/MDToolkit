from md_commands.command_interface import Command
from md_commands.command_validation_helper import CommandValidationHelper
from md_enums.filter_type import FilterType
from md_filters.filter_interface import Filter
from md_filters.and_filter import AndFilter
from md_filters.atom_type_filter import AtomTypeFilter
from md_filters.cartesian_filter import CartesianFilter
from md_filters.radial_filter import RadialFilter
from session_state import SessionState

class FilterCommand(Command):
    def __init__(self, command_name: str, args: list[str]):
        helper = CommandValidationHelper(command_name)
        helper.check_for_min_arg_count(args, 2)
        if args[0].lower() == "all":
            raise Exception("Filter name cannot be 'all' because it is a reserved keyword")
        self._filter_name = args[0]
        self._filter_type = helper.check_categorical_arg(args[1].lower(), FilterType)
        self._filter_params = args[2:] if len(args) > 2 else []

        # Do some basic validation of filter parameters now; the rest will be done during execution
        if self._filter_type == FilterType.AND:
            # "And" filter takes two or more filter names as parameters
            if len(self._filter_params) < 2:
                raise Exception("'and' filter requires at least two filter names as parameters")
        elif self._filter_type == FilterType.ATOM_TYPE:
            # Atom type filter takes a list of atom types (integers) as parameters
            if len(self._filter_params) == 0:
                raise Exception("'atom_type' filter requires at least one atom type as a parameter")
            for atom_type in self._filter_params:
                helper.parse_int(atom_type)
        elif self._filter_type == FilterType.CARTESIAN:
            # Cartesian filter takes 6 parameters: x_min, x_max, y_min, y_max, z_min, z_max
            if len(self._filter_params) != 6:
                raise Exception("'cartesian' filter requires exactly six parameters: x_min (float or 'none'), x_max (float or 'none'), y_min (float or 'none'), y_max (float or 'none'), z_min (float or 'none'), z_max (float or 'none')")
            for param in self._filter_params:
                helper.parse_float_or_none(param)
        elif self._filter_type == FilterType.RADIAL:
            # Radial filter takes 5 parameters: x, y, z, r_min, r_max
            if len(self._filter_params) != 5:
                raise Exception("'radial' filter requires exactly five parameters: x, y, z, r_min (float or 'none'), r_max (float or 'none')")
            for param in self._filter_params[:3]:
                helper.parse_float(param)
            for param in self._filter_params[3:]:
                helper.parse_float_or_none(param)
        else:
            raise Exception(f"Unsupported filter_type specified in configuration: '{self._filter_type}' (supported types are {[item.value for item in FilterType]})")

    def execute(self, state: SessionState):
        if self._filter_type == FilterType.AND:
            filters: list[Filter] = []
            for filter_name in self._filter_params:
                if filter_name not in state.filters:
                    raise Exception(f"'and' filter parameter '{filter_name}' is not the name of an existing filter")
                filters.append(state.filters[filter_name])
            state.filters[self._filter_name] = AndFilter(filters)
        elif self._filter_type == FilterType.ATOM_TYPE:
            atom_types: set[int] = set()
            for atom_type in self._filter_params:
                atom_types.add(int(atom_type))
            state.filters[self._filter_name] = AtomTypeFilter(atom_types)
        elif self._filter_type == FilterType.CARTESIAN:
            x_min = None if self._filter_params[0].lower() == "none" else float(self._filter_params[0])
            x_max = None if self._filter_params[1].lower() == "none" else float(self._filter_params[1])
            y_min = None if self._filter_params[2].lower() == "none" else float(self._filter_params[2])
            y_max = None if self._filter_params[3].lower() == "none" else float(self._filter_params[3])
            z_min = None if self._filter_params[4].lower() == "none" else float(self._filter_params[4])
            z_max = None if self._filter_params[5].lower() == "none" else float(self._filter_params[5])
            state.filters[self._filter_name] = CartesianFilter(x_min, x_max, y_min, y_max, z_min, z_max)
        elif self._filter_type == FilterType.RADIAL:
            x = float(self._filter_params[0])
            y = float(self._filter_params[1])
            z = float(self._filter_params[2])
            r_min = None if self._filter_params[3].lower() == "none" else float(self._filter_params[3])
            r_max = None if self._filter_params[4].lower() == "none" else float(self._filter_params[4])
            state.filters[self._filter_name] = RadialFilter(x, y, z, r_min, r_max)