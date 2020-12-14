#!/usr/bin/env python3
import json
import sys
import subprocess

FILE = "openings.starts"

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) < 2:
        # For now lets assume all episodes has 1 opening
        print(f"usage {sys.argv[0]} <episode>")
        exit(1)
    with open(FILE, "r") as f:
        dic = json.load(f)
    episode = sys.argv[1]
    try:
        if episode.startswith("./"):
            episode = episode.strip("./")
        ts = dic[episode]
    except KeyError:
        print("Start time for '{episode}' not found!\n Try run `opening_ts.py` first")
        exit(1)
    cmd = f"vlc.exe --start-time={ts} \"{episode}\""
    print(cmd)
    try:
        subprocess.run(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"vlc error: \n {e.output.decode()}")
        exit(1)
