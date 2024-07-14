def pop_lines_from_json_file(file):
    # 1. get lines
    import json
    with open(file) as f:
        lines = json.load(f)

    if len(lines) == 0:
        return None

    # 2. pop line
    line = lines.pop()

    # 3. dump lines
    with open(file, 'w') as f:
        json.dump(lines, f)

    # 4. return line
    return line

def get_audio_duration(file):
    import subprocess
    output = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file])
    return float(output)