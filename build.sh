#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg
apt-get update
apt-get install -y ffmpeg