# Skip intro
Find intro start/end and allow to skip it(in MPV for example).

## How it works
1. Generate file with start and end time of intro.
2. Use generated file to seek in the external media player.

## Usage
```console
# generate intro_time.csv file in the current folder
./gen_intro_time.py <start_frame> <duration of intro(sec)> <files...>

# launch mpv, when intro start, hint appears with skip suggestion
mpv <file> --script=./skip_intro.lua
```
Note: it's possible to omit `--script` option, by "installing"
it ([link](https://github.com/mpv-player/mpv/blob/master/DOCS/man/lua.rst#script-location))

## TODO
- resize image to match video size

## Links
- https://github.com/mpv-player/mpv/blob/master/DOCS/man/lua.rst
- https://mpv.io/manual/master/#properties
- https://tylerneylon.com/a/learn-lua/
