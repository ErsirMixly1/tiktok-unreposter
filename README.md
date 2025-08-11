Place two image files in the same folder as the script:

reposted_icon.png – cropped screenshot of the solid repost icon

next_video.png – cropped screenshot of the next video button

(I Already Provided These, but you can take a screenshot of them yourself)

This Python script automatically detects the TikTok “reposted” icon in your browser and clicks to unrepost the video, then moves on to the next one.

Features
Detects reposted videos using image matching

Unreposts them automatically

Clicks “Next video” to move on

Handles cases where TikTok tab is inactive

Works silently in the background

## Requirements
- Python 3
- OpenCV
- pywin32
- mss

## Install Dependencies
```bash
pip install opencv-python pywin32 mss numpy
