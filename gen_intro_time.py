#!/usr/bin/env python3
import sys
import subprocess

def find_image_ts(video, image):
    """
    Find first image occurrence in video
    from: https://stackoverflow.com/questions/57447740
    """

    #  blackframe only looks at luma, use extractplanes both to speed up blend
    #  and also avoid any unexpected format conversions blend may request.
    extract_planes = "[0]extractplanes=y[v];[1]extractplanes=y[i];[v][i]"
    # Blend two video frames into each other and detect the black frame
    # - https://ffmpeg.org/ffmpeg-filters.html#blackframe
    # settb - MKV has a fixed tb of 1/1000 and so trim duration does not take
    # effect. AVIs contain no timestamps, and ffmpeg will set tb to 1/fps. No
    # harm in always setting it
    match_filters = "blend=difference,settb=1/10000,blackframe=0"
    # metadata filter only passes through frames with blackframe value of 100
    meta_select = "metadata=select:key=lavfi.blackframe.pblack:value=100:function=equal"
    # trim filter stops a 2nd frame from passing through (except if your video's
    # fps is greater than 10000)
    trim_filter = "trim=duration=0.0001"
    #  The 2nd metadata filter prints the selected frame's metadata.
    meta_print = "metadata=print:file=-"
    ffmpeg_cmd = f"ffmpeg -i {video} -i {image} -filter_complex \
                \"{extract_planes}{match_filters},{meta_select},{trim_filter},{meta_print}\"\
                -an -v 0 -vsync 0 -f null -"
    print(ffmpeg_cmd)
    try:
        output = subprocess.check_output(ffmpeg_cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: \n {e.output.decode()}")
        exit(1)
    if output is None:
        return None
    for l in output.splitlines():
        if l.startswith(b"frame:"):
            res = l.split(b"pts_time:")[-1]
            return float(res.decode("utf-8"))

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
            start_time = find_image_ts(video, image)
            end_time = start_time + duration if start_time is not None else None
            f.write(f"{video},{start_time},{end_time}")
