from datetime import datetime
from sys import __stdout__
from typing import Optional, Iterable


def removeprefix(string: str, prefix) -> str:
    """Similar to ``str.removeprefix()`` in python 3.9,
    except it works for lower versions and can take a list of prefixes"""
    if isinstance(prefix, str):
        return string[(string.startswith(prefix) and len(prefix)):]
    elif isinstance(prefix, Iterable):
        for i in prefix:
            string = removeprefix(string, i)
        return string


def removesuffix(string: str, suffix) -> str:
    """Similar to ``str.removesuffix()`` in python 3.9,
    except it works for lower versions and can take a list of suffixes"""
    if isinstance(suffix, str):
        return string[:-len(suffix)] if string.endswith(suffix) else string
    elif isinstance(suffix, Iterable):
        for i in suffix:
            string = removesuffix(string, i)
        return string


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def log(message: str, tag="Main", end="\n", time=True):
    """Logs messages to stdout.
    ``[timestamp] [tag] message (ending)``

    :param str message: message to log
    :param str tag: tag, defaults to "Main"
    :param str end: string to append to the end of the output, defaults to newline (\n)
    :param bool time: whether to output a timestamp"""
    __stdout__.write(f"{('[' + current_time() + '] ') if time else ''}{('[' + tag + ']: ') if tag else ''}{message}{end}")


def to_int(string: str) -> Optional[int]:
    try:
        return int(string)
    except ValueError:
        return None


def to_flt(string: str) -> Optional[float]:
    try:
        return float(string)
    except ValueError:
        return None


def clean_return(string: str) -> str:
    return str(string).replace("\r\n", "\n").replace("\r", "\n").replace(" \n", "\n").strip()


async def load_list(filepath):
    with open(filepath, mode="r", encoding="utf-8") as file:
        return file.read().splitlines()


async def save_list(filepath, array):
    with open(filepath, mode="w", encoding="utf-8") as file:
        for item in array:
            file.write(clean_return(item).replace("\n", " ") + "\n")


def batch(msg: str, d="\n", length=2000):
    splitted = [e + d for e in msg.split(d) if e]
    result = ""
    while splitted:
        if len(result) + len(splitted[0]) <= length:
            result += splitted.pop(0)
        elif result:
            yield result
            result = ""
        else:
            yield splitted.pop(0)
    yield result

# End
