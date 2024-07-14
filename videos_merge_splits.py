import os
import shutil
import datetime
import uuid
import random

def videos_merge_splits(directory_videos, output_file, duration):
    videos = os.listdir(directory_videos)
    # random order
    random.shuffle(videos)

    duration_of_each_video = 0.5
    import math
    num_files_to_combine = math.ceil(duration / duration_of_each_video)
    files_to_combine = []
    for i in range(num_files_to_combine):
        video = videos[i]
        files_to_combine.append(os.path.join(directory_videos, video))
    
    if not os.path.exists(output_file):
        #ffmpeg_inputs = " ".join([f'-i "{file}"' for file in files_to_combine])
        # use -ss and -t
        ffmpeg_inputs = " ".join([f'-ss '+get_random_video_seek_time(file, duration_of_each_video)+' -t {duration_of_each_video} -i "{file}"' for file in files_to_combine])
        ffmpeg_command = f'ffmpeg {ffmpeg_inputs} -filter_complex "concat=n={num_files_to_combine}:v=1:a=1" -c:a libmp3lame -q:a 4 -c:v libx264 -crf 22 -preset veryfast "{combine_file_path}"'
        print(ffmpeg_command)
        os.system(ffmpeg_command)
        print(f"Combine {output_file}")

def get_random_video_seek_time(file_path, duration):
    return random.uniform(0, get_video_duration(file_path) - duration)

def get_video_duration(file_path):
    ffmpeg_command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    result = os.popen(ffmpeg_command).read()
    return float(result)
