#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i shoe_%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y Shoe.mov
