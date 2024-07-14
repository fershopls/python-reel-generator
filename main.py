from utils import pop_lines_from_json_file

line = pop_lines_from_json_file('lines.json')

if not line:
    print("no line found")
    exit()

print("creating audio for line:", line)

voice = "en_us_001"

import tiktokvoice
tiktokvoice.tts(line, voice, "voice.mp3", play_sound=False)

# create video audio duration
from utils import get_audio_duration
from video_creator import create_video

duration = get_audio_duration("voice.mp3")
duration = duration + 1.5

create_video(
    output="video.mp4",
    duration=duration,
)

# put audio over video
import os
cmd = f'ffmpeg -i voice.mp3 -i video.mp4 -map 0:0 -map 1:0 -shortest -c:v copy -c:a aac -strict experimental output.mp4'
os.system(cmd)

os.remove("voice.mp3")
os.remove("video.mp4")

# move
import shutil
import uuid
random_id = str(uuid.uuid4())
shutil.move("output.mp4", random_id + ".mp4")