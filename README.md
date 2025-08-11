# FEATURES

automatically detects the TikTok “reposted” icon in your browser and clicks to unrepost the video, then moves on to the next one.

Detects reposted videos using image matching

Unreposts them automatically

Clicks “Next video” to move on

Works silently in the background


# Download The .PNGS

https://github.com/ErsirMixly1/tiktok-unreposter/blob/main/reposted_icon.png

https://github.com/ErsirMixly1/tiktok-unreposter/blob/main/next_video.png

# 3️⃣ Configuration
If needed, update the script’s constants:
```bash
ICON_DIR = "."  # folder containing your icons
REPOST_ICON = "reposted_icon.png"
NEXT_BUTTON_ICON = "next_video.png"
WINDOW_TITLE = "TikTok -"  # part of the browser tab title
MATCH_THRESHOLD = 0.88     # matching accuracy (0.0–1.0)
# Coordinates fallback clicks
FALLBACK_NEXT = (1335, 599)
TIKTOK_TAB = (125, 19)
```
If the bot doesn’t click correctly, adjust FALLBACK_NEXT and TIKTOK_TAB coordinates.
You can find them using a mouse position tool like MousePos.exe or by printing mouse positions with Python.

# 4️⃣ Running the Bot
Open TikTok in your browser and make sure it’s visible on your screen.

Keep the window active and at the same resolution as when you took your icon screenshots.

In Command Prompt, run:

bash
Copy
Edit
python script.py
The bot will:

Find reposted videos

Click to unrepost

Click “Next video”

Repeat until you stop it

To stop the bot, press:

mathematica
Copy
Edit
Ctrl + C



## Requirements
- Python 3
- OpenCV
- pywin32
- mss

## Install Dependencies
```bash
pip install opencv-python pywin32 mss numpy
