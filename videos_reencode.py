import os

def videos_reencode(dir_from, dir_to):
    os.makedirs(dir_to, exist_ok=True)

    for file in os.listdir(dir_from):
        file_input = os.path.join(dir_from, file)
        file_output = os.path.join(dir_to, file + ".mp4")
        
        if os.path.exists(file_output):
            print(f"Exists {file_output}")
            continue
        
        cmd = f'ffmpeg -i "{file_input}" -c:v libx264 -preset slow -crf 23 -vf "scale=1080:trunc(ow/a/2)*2" -c:a aac -b:a 128k "{file_output}"'
        print(cmd)
        os.system(cmd)
        print(f"#"*100)
