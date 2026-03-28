#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i camera-%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y ../../Karbon/Assets/StreamingAssets/Camera.mov
