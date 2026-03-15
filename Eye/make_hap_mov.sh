#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i eye-%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y Eye.mov
