from __future__ import division

import math
import os.path as osp
from pathlib import Path
import shutil
import subprocess
from tempfile import NamedTemporaryFile

import cv2
import skvideo.io


def hhmmss_to_seconds(ts):
    try:
        return float(ts)
    except ValueError:
        return sum(
            float(x) * 60 ** i
            for i, x in enumerate(reversed(ts.split(':'))))


def get_video_duration(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    return float(metadata['video']['@duration'])


def get_video_avg_frame_rate(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    a, b = metadata['video']['@avg_frame_rate'].split('/')
    a = int(a)
    b = int(b)
    return a / b


def get_video_size(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    height = int(metadata['video']['@height'])
    width = int(metadata['video']['@width'])
    return width, height


def get_video_n_frame(video_path):
    video_path = str(video_path)
    if not osp.exists(video_path):
        raise OSError("{} not exists".format(video_path))
    metadata = skvideo.io.ffprobe(video_path)
    if '@nb_frames' not in metadata['video']:
        fps = get_video_avg_frame_rate(video_path)
        return int(fps * get_video_duration(video_path))
    return int(metadata['video']['@nb_frames'])


def split_video(video_file_path, output_path=None,
                start_time=None, end_time=None,
                hflip=False, vflip=False):
    if start_time is None and end_time is None:
        raise ValueError
    start_time = start_time or 0.0
    end_time = end_time or get_video_duration(video_file_path)
    command = ['ffmpeg',
               '-y',
               '-ss', str(start_time),
               '-t', str(end_time - start_time),
               '-i', str(video_file_path)]
    if hflip is True:
        command.extend(['-vf', 'hflip'])
    if vflip is True:
        command.extend(['-vf', 'vflip'])
    if output_path is None:
        suffix = Path(video_file_path).suffix
        with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
            command.append(tmp.name)
            print(f'Running \"{" ".join(command)}\"')
            subprocess.call(command)
            shutil.copy(tmp.name, video_file_path)
    else:
        command.append(str(output_path))
        print(f'Running \"{" ".join(command)}\"')
        subprocess.call(command)


def extract_target_frame_from_timestamp(video_filepath, timestamp):
    """Extract target frame from timestamp.

    Parameters
    ----------
    video_filepath : str
        video filepath
    timestamp : float
        timestamp in seconds.

    Returns
    -------
    image : numppy.ndarray
    """
    duration = get_video_duration(video_filepath)
    timestamp = max(0.0, min(duration, timestamp))
    vidcap = cv2.VideoCapture(str(video_filepath))
    vidcap.set(cv2.CAP_PROP_POS_MSEC, int(timestamp * 1000))
    success, image = vidcap.read()
    return image


def load_frame(video_path, start=0.0, duration=-1,
               target_size=None, sampling_frequency=None):
    """Load frame

    Parameters
    ----------
    video_path : str or pathlib.Path
        input video path.
    start : float
        start time
    duration : int or float
        duration. If this value is `-1`, load all frames.

    Returns
    -------
    frames : list[numpy.ndarray]
        all frames.
    stamps : list[float]
        time stamps.
    """
    video_path = str(video_path)
    vid = cv2.VideoCapture(video_path)
    fps = vid.get(cv2.CAP_PROP_FPS)
    vid.set(cv2.CAP_PROP_POS_MSEC, start)
    vid_avail = True
    if sampling_frequency is not None:
        frame_interval = int(math.ceil(fps * sampling_frequency))
    else:
        frame_interval = 1
    cur_frame = 0
    while True:
        stamp = float(cur_frame) / fps
        vid_avail, frame = vid.read()
        if not vid_avail:
            break
        if duration != -1 and stamp > start + duration:
            break
        if target_size is not None:
            frame = cv2.resize(frame, target_size)
        yield frame, stamp
        cur_frame += frame_interval
        vid.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
    vid.release()


def count_frames(video_path, start=0.0, duration=-1,
                 sampling_frequency=None):
    video_duration = get_video_duration(video_path)
    video_duration -= start
    if duration > 0:
        video_duration = max(video_duration - duration, 0)
    fps = get_video_avg_frame_rate(video_path)
    if sampling_frequency is not None:
        return int(math.ceil(
            video_duration * fps
            / int(math.ceil(fps * sampling_frequency))))
    else:
        return int(math.ceil(video_duration * fps))
