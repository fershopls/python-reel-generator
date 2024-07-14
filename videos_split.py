import os
import shutil
import datetime
import uuid

def videos_split(dir_from, dir_to):
    # create splits directory
    if not os.path.exists(dir_to):
        os.makedirs(dir_to)

    video_extensions = [
        ".mp4",
        ".mov",
    ]

    for filename in os.listdir(dir_from):
        if any(filename.endswith(ext) for ext in video_extensions):
            print(f"Processing {filename}")
            
            file_path = os.path.join(dir_from, filename)
            file_name, file_extension = os.path.splitext(filename)
            file_video_duration = get_video_duration(file_path)
            
            # split each video in 10 or less seconds
            split_duration = 3.5
            split_count = int(file_video_duration / split_duration)
            
            if split_count == 0:
                continue

            split_duration = round(file_video_duration / split_count, 2)
            
            # split video
            for i in range(split_count):
                split_start = i * split_duration
                split_end = split_start + split_duration
                if split_end > file_video_duration:
                    split_end = file_video_duration

                split_file_name = f"{file_name}_{split_start}-{split_end}.mp4"
                split_file_path = os.path.join(dir_to, split_file_name)

                if not os.path.exists(split_file_path):
                    ffmpeg_command = f'ffmpeg -i "{file_path}" -ss {split_start} -t {split_duration} -c:a libmp3lame -q:a 4 -c:v libx264 -crf 22 -preset veryfast "{split_file_path}"'
                    os.system(ffmpeg_command)
                    print(f"Split {split_file_name}")

def get_video_duration(file_path):
    ffmpeg_command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    result = os.popen(ffmpeg_command).read()
    return float(result)
