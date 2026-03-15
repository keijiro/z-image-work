#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i bird-%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y Bird.mov
