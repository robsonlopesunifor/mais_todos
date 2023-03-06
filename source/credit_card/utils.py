import os


def getenv_or_raise_exception(varname: str) -> str:
    env = os.getenv(varname)
    if env is None:
        raise EnvironmentError(f"Environment variable {varname} is not set!")
    return env
