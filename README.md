# z-image-karbon

This repository contains working files for the [Karbon] project.

[Karbon]: https://github.com/keijiro/Karbon

## Overview

This repository is mainly used for asset generation related to Karbon. It includes tools, prompts, and scripts for producing images and videos.

## Contents

### Z-Image Generation Skill

This component provides image generation using the Z-Image Turbo model via the ModelScope API.

To use this feature, the `MODELSCOPE_API_TOKEN` environment variable must be set in advance. Free accounts can typically make up to around 1,000 requests.

### Image Generation Prompts

Several `.md` files are included that define instructions for generating sets of images with specific themes.

### Video Encoding Scripts

Simple shell scripts are provided in subdirectories. These scripts use `ffmpeg` to concatenate generated images into HAP-encoded MP4 files.
