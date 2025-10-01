def parse_float(arg: str) -> float:
    try:
        return float(arg)
    except ValueError:
        raise Exception(f"Expected float instead of '{arg}'")

def parse_int(arg: str) -> int:
    try:
        return int(arg)
    except ValueError:
        raise Exception(f"Expected integer instead of '{arg}'")