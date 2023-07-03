import typing as T


def camel_to_snake(str_in: str) -> str:
    # https://stackoverflow.com/a/1176023/10940584
    return "".join(["_" + c.lower() if c.isupper() else c for c in str_in]).lstrip("_")


def snake_to_camel(str_in: str) -> str:
    # https://stackoverflow.com/a/19053800/10940584
    return "".join([t.title() for t in str_in.split("_")])


def dict_keys_camel_to_snake_deep(dict_in) -> T.Any:
    # recursively convert dict keys from camelCase to snake_case
    if isinstance(dict_in, dict):
        dict_in = {camel_to_snake(k): dict_keys_camel_to_snake_deep(v) for k, v in dict_in.items()}
    return dict_in


def dict_keys_snake_to_camel_deep(dict_in) -> T.Any:
    # recursively convert dict keys from snake_case to camelCase
    if isinstance(dict_in, dict):
        dict_in = {snake_to_camel(k): dict_keys_snake_to_camel_deep(v) for k, v in dict_in.items()}
    return dict_in


def get_pretty_seconds(seconds: int, use_days: bool = False) -> str:
    """Given an amount of seconds, return a formatted string with
    hours, minutes and seconds; taken from
    https://stackoverflow.com/a/775075/2972183"""
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if use_days:
        days, hours = divmod(hours, 24)
        string = f"{days:d}d:{hours:d}h:{minutes:02d}m:{seconds:02d}s"
    else:
        string = f"{hours:d}h:{minutes:02d}m:{seconds:02d}s"
    return string
