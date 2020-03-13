import sys
import json
import subprocess
import os
import copy
from subprocess import (PIPE)
from pprint import (pprint)
from utils import (list_all_mp4, check_installed)
from typing import (Tuple, Any, Dict)
from tqdm import tqdm


def probe_duration(fname: str) -> Tuple[str, float]:
    ret1 = subprocess.run('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -sexagesimal {}'.format(fname), \
        text=True, shell=True, stderr=PIPE, stdout=PIPE)
    duration_str = ret1.stdout.strip()
    ret2 = subprocess.run('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}'.format(fname), \
        text=True, shell=True, stderr=PIPE, stdout=PIPE)
    duration_sec = ret2.stdout.strip()
    return duration_str, float(duration_sec)


def probe_samplerate(fname: str) -> str:
    ret = subprocess.run('ffprobe -v error -show_entries stream=sample_rate -of default=noprint_wrappers=1:nokey=1 {}'.format(fname),\
        text=True, shell=True, stderr=PIPE, stdout=PIPE)
    sample_rate = ret.stdout.strip()
    return sample_rate


def new_meta(input_folder: str, template_meta: str) -> Dict[str, Dict]:
    all_files = sorted(list_all_mp4(input_folder))
    with open(template_meta, 'r') as f:
        empty_meta = json.load(f)

    result: Dict[str, Dict] = {}
    for i, fullname in tqdm(enumerate(all_files), ncols=100):
        meta = copy.deepcopy(empty_meta)

        _, basicname = os.path.split(fullname)
        meta['mp4file'] = basicname

        try:
            duration_str, duration_sec = probe_duration(fullname)
            meta['duration'] = duration_str
            meta['durationsec'] = duration_sec
        except ValueError:
            print(fullname)
            raise
        else:
            raise

        # TODO
        result[str(i+1)] = meta

    return result


def test():
    # print(probe_duration('/Users/xy/Documents/cs561_video_2020spring/dynamic_programming_1/dynamic_programming_1.mp4'))
    # print(probe_samplerate('/Users/xy/Documents/cs561_video_2020spring/dynamic_programming_1/dynamic_programming_1.mp4'))

    res = new_meta('/Users/xy/Documents/cs561_video_2020spring/dynamic_programming_1/', '../metadata/template_meta.json')
    pprint(res)


def main():
    assert check_installed('ffmpeg')

    input_folder = '/Data/CNBC_ceo_videos/MP4'
    meta_data = new_meta(input_folder, '../metadata/template_meta.json')
    with open('../metadata/video_ids.json', 'w') as f:
        json.dump(meta_data, indent=4)


if __name__ == "__main__":
    # test()
    main()