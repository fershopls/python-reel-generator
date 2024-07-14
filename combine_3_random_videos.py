import os
import shutil
import datetime
import uuid
import random

def main():
    directory_videos = r'videos_encoded'
    directory_combines = r'videos_merged'

    # create combines directory
    if not os.path.exists(directory_combines):
        os.makedirs(directory_combines)
    
    videos = os.listdir(directory_videos)
    # random order
    random.shuffle(videos)

    duration_of_each_video = 0.5
    num_files_to_combine = 10
    files_to_combine = []
    for i in range(num_files_to_combine):
        video = videos[i]
        files_to_combine.append(os.path.join(directory_videos, video))
    
    # combine videos
    combine_file_name = f"combine_{uuid.uuid4()}.mp4"
    combine_file_path = os.path.join(directory_combines, combine_file_name)

    if not os.path.exists(combine_file_path):
        #ffmpeg_inputs = " ".join([f'-i "{file}"' for file in files_to_combine])
        # use -ss and -t
        ffmpeg_inputs = " ".join([f'-t {duration_of_each_video} -i "{file}"' for file in files_to_combine])
        ffmpeg_command = f'ffmpeg {ffmpeg_inputs} -filter_complex "concat=n={num_files_to_combine}:v=1:a=1" -c:a libmp3lame -q:a 4 -c:v libx264 -crf 22 -preset veryfast "{combine_file_path}"'
        print(ffmpeg_command)
        os.system(ffmpeg_command)
        print(f"Combine {combine_file_name}")

main()
