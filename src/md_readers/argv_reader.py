def read_config_path(args):
    if args is None or len(args) < 2: return "mdtoolkit_config.ini"
    else: return args[1]