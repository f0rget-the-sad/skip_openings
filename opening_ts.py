#!/usr/bin/env python3
import sys
import subprocess


def find_image_ts(video, image, duration=60):
    """
    Find first image occurrence in video
    """
    ffmpeg_cmd = f"ffmpeg -t {duration} -i {video} -loop 1 -i {image} -an \
        -filter_complex \"blend=difference:shortest=1,blackframe=99:32\" -f null -"
    print(ffmpeg_cmd)
    output = subprocess.check_output(ffmpeg_cmd, stderr=subprocess.STDOUT, shell=True)
    print("="*100)
    for l in output.splitlines():
        if l.startswith(b"[Parsed_blackframe_"):
            print(l)
            res = l.split(b"t:")[1].split()[0]
            print(res.decode("utf-8"))
            exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"usage {sys.argv[0]} <video> <image>")
    video = sys.argv[1]
    image = sys.argv[2]
    find_image_ts(video, image, 30)

