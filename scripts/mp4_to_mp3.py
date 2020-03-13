import subprocess
import os
import sys 
import glob
import errno
from tqdm import tqdm
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


def convert(input_folder: str, output_folder: str):

    pass


if __name__ == "__main__":
    assert len(sys.argv) == 3
    assert check_installed('ffmpeg')

    input_folder, output_folder = sys.argv[1:]
    print('input folder: {}'.format(input_folder))
    print('output folder: {}'.format(output_folder))

    mp4_files = list_all_mp4(input_folder)
    print('input folder contains {} .mp4 files'.format(len(mp4_files)))
