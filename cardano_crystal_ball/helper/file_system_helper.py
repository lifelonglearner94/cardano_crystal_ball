from pathlib import Path
from dotenv import load_dotenv
import os

"""
Help functions relating to the file system
"""

def search_upwards(filename):
    """
    Search upwards for the path where the given file can be found.
    if it's not found returns None

    - argument: filename or foldername
    - return: the path or None
    """

    dir = Path.cwd()
    while dir != Path('/'):
        try_find = dir / filename
        if try_find.exists():
            return (dir.absolute())
        dir = dir.parent
    return None


def get_from_env(name):
    load_dotenv()
    return os.environ.get(name)



if __name__ == '__main__':
    print (search_upwards('raw_data'))
