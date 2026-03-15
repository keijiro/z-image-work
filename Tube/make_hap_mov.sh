#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i tube-%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y Tube.mov
