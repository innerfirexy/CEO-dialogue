import subprocess
import errno
import os
import glob
from typing import (List, Any)


def check_installed(prog_name: str) -> bool:
    try:
        subprocess.call([prog_name], stderr=subprocess.DEVNULL)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print('{} is not installed.'.format(prog_name))
        else:
            print('an error occurs while executing {}.'.format(prog_name))
        return False
    else:
        return True


def list_all_mp4(target_dir: str) -> List[str]:
    pattern = os.path.join(target_dir, '*.mp4')
    return glob.glob(pattern)