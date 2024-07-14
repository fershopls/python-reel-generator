import os
from videos_reencode import videos_reencode

DIR_RAW = r"D:\OF\clip-maker\videos_raw"
DIR_REENCODED = r"D:\OF\clip-maker\videos_encoded"
DIR_SPLITS = r"D:\OF\clip-maker\splits"

def create_video(output, duration):
    videos_reencode(DIR_RAW, DIR_REENCODED)

    if not os.path.exists(DIR_SPLITS):
        os.makedirs(DIR_SPLITS)
        from videos_split import videos_split
        videos_split(DIR_REENCODED, DIR_SPLITS)

    from videos_merge_splits import videos_merge_splits
    videos_merge_splits(DIR_SPLITS, output, duration)

if __name__ == "__main__":
    create_video("output.mp4", 10)
