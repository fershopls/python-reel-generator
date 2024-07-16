while True:
    from utils import pop_lines_from_json_file
    line = pop_lines_from_json_file('lines.json')

    if not line:
        print("no line found")
        exit()

    # files to prune
    prune_files = []

    # create audio
    print("creating audio for line:", line)
    voice = "en_us_001"

    import tiktokvoice
    tiktokvoice.tts(line, voice, "voice.mp3", play_sound=False)
    prune_files.append("voice.mp3")

    import os
    if not os.path.exists("voice.mp3"):
        print("no audio file found")
        exit()

    # create video audio duration
    from utils import get_audio_duration
    from video_creator import create_video

    duration = get_audio_duration("voice.mp3")
    duration = duration + 1.5

    create_video(
        output="video.mp4",
        duration=duration,
    )
    prune_files.append("video.mp4")

    # put audio over video
    from utils import cmd
    cmd(f'ffmpeg -y -i voice.mp3 -i video.mp4 -map 0:0 -map 1:0 -shortest -c:v libx264 -c:a aac -strict experimental output.mp4')
    prune_files.append("output.mp4")

    # create text caption
    from utils import get_video_size
    from png_create_text import png_create_text

    video_width, video_height = get_video_size("video.mp4")
    png_create_text(
        width=video_width,
        height=video_height,
        text=line,
        font_size=video_height / 30,
        output_file="caption.png",
    )
    prune_files.append("caption.png")

    # put text caption over video
    cmd(f'ffmpeg -y -i output.mp4 -i caption.png -filter_complex "[0:v][1:v]overlay[out]" -map "[out]" -map 0:a -c:v libx264 -c:a aac -preset slow output2.mp4')

    # remove cache files
    import os
    for file in prune_files:
        os.remove(file)

    # move
    import shutil
    import uuid
    random_id = str(uuid.uuid4())
    shutil.move("output2.mp4", random_id + ".mp4")
