from os import getenv


def cast_from(name, default=None, getter=getenv):
    """Get a value and cast it to match the default, or a given type."""
    if callable(default):
        cast, default = default, None
    elif default is None:
        cast = str
    else:
        cast = type(default)
    value = getter(name, default)
    if cast is bool and type(value) is str:
        return value is not None and value.lower() in ('1', 't', 'true', 'y', 'yes', 'on')
    return None if value is None else cast(value)


def from_env(name, default=None):
    """Get an environment variable's value and cast it to match the default, or a given type."""
    return cast_from(name, default)
