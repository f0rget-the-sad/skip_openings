#!/usr/bin/env python3
import sys
import subprocess

def find_image_ts(video, image, max_duration):
    # ffmpeg search in all video, event with shortest=1,
    # so move with 1 min step
    start = 0
    step = 30
    while start < max_duration:
        if found := find_in_split(video, image, start, step):
            return found

def find_in_split(video, image, start, duration):
    """
    Find first image occurrence in video
    """
    ffmpeg_cmd = f"ffmpeg -ss {start} -t {duration} -i {video} -loop 1 -i {image} -an \
        -filter_complex \"blend=difference:shortest=1,blackframe=98:32\" -f null -"
    print(ffmpeg_cmd)
    # shortest=1 - stop at first match
    # Blend two video frames into each other and detect the black frame
    # - https://ffmpeg.org/ffmpeg-filters.html#blackframe
    try:
        output = subprocess.check_output(ffmpeg_cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: \n {e.output.decode()}")
        exit(1)
    if output is None:
        return None
    for l in output.splitlines():
        if l.startswith(b"[Parsed_blackframe_"):
            res = l.split(b"t:")[1].split()[0]
            return start + float(res.decode("utf-8"))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"usage {sys.argv[0]} <start_frame> <duration(sec)> <files...>")
        exit(1)
    # TODO: use kwargs
    image    = sys.argv[1]         # image of first frame of the intro
    duration = float(sys.argv[2])  # intro duration
    videos   = sys.argv[3:]        # videos to analyze
    # TODO: add maxtime option
    with open("intro_time.csv", "w") as f:
        for video in videos:
            print(f"Searching for intro in '{video}'")
            start_time = find_image_ts(video, image, 5 * 60)
            end_time = start_time + duration if start_time is not None else None
            f.write(f"{video},{start_time},{end_time}")
