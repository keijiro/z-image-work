#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i Flower_%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y Flower_hap.mov
