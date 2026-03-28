#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i splash-%03d.png \
  -c:v hap \
  -pix_fmt rgba \
  -y ../../Karbon/Assets/StreamingAssets/Splash.mov
