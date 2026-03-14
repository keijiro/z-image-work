#!/bin/sh
set -eu

ffmpeg \
  -framerate 1 \
  -i glass_%02d.png \
  -vf "crop=1024:576:0:224" \
  -c:v hap \
  -pix_fmt rgba \
  -y Glass.mov
