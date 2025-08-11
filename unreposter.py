import cv2
import numpy as np
import time
import win32gui
import win32con
import win32api
import mss
import os

# Images of the icons/buttons
ICON_DIR = "."  # put your images here
REPOST_ICON = "reposted_icon.png"  # only the solid icon now
NEXT_BUTTON_ICON = "next_video.png"

WINDOW_TITLE = "TikTok -"
MATCH_THRESHOLD = 0.88

# Fallback coordinates for "Next video" button
FALLBACK_NEXT = (1335, 599)
TIKTOK_TAB = (125, 19)  # Coordinates to click TikTok tab

def find_window(title_part):
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd) and title_part.lower() in win32gui.GetWindowText(hwnd).lower():
            result.append(hwnd)
    result = []
    win32gui.EnumWindows(enum_handler, result)
    return result[0] if result else None

def send_click(hwnd, x, y):
    lparam = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lparam)

def get_window_rect(hwnd):
    return win32gui.GetWindowRect(hwnd)

def capture_window(hwnd):
    left, top, right, bottom = get_window_rect(hwnd)
    width, height = right - left, bottom - top
    with mss.mss() as sct:
        img = np.array(sct.grab({"left": left, "top": top, "width": width, "height": height}))
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def match_icon(gray_img, template):
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= MATCH_THRESHOLD:
        return max_loc
    return None

def click_top_left_tab(hwnd):
    send_click(hwnd, 127, 15)
    print("🔙 Clicked top-left tab")

def click_go_back(hwnd):
    send_click(hwnd, 21, 55)
    print("🔙 Clicked go back")

# Load templates
template_repost = cv2.imread(os.path.join(ICON_DIR, REPOST_ICON), cv2.IMREAD_GRAYSCALE)
template_next = cv2.imread(NEXT_BUTTON_ICON, cv2.IMREAD_GRAYSCALE)
tW_r, tH_r = template_repost.shape[::-1]
tW_n, tH_n = template_next.shape[::-1]

hwnd = find_window(WINDOW_TITLE)
if not hwnd:
    print("❌ TikTok window not found.")
    exit()

print(f"✅ Found TikTok window: {win32gui.GetWindowText(hwnd)}")
print("Unreposting videos silently... Press Ctrl+C to stop.")

missing_repost_count = 0
MAX_MISSING = 5

try:
    while True:
        screenshot = capture_window(hwnd)
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        loc_repost = match_icon(gray, template_repost)
        if loc_repost:
            missing_repost_count = 0
            click_x = loc_repost[0] + tW_r // 2
            click_y = loc_repost[1] + tH_r // 2
            send_click(hwnd, click_x, click_y)
            print(f"🖱️ Unreposted at ({click_x}, {click_y})")
            time.sleep(1)

            # Try next video
            screenshot = capture_window(hwnd)
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            loc_next = match_icon(gray, template_next)
            if loc_next:
                click_x_n = loc_next[0] + tW_n // 2
                click_y_n = loc_next[1] + tH_n // 2
                send_click(hwnd, click_x_n, click_y_n)
                print("➡️ Clicked next video")
            else:
                send_click(hwnd, *FALLBACK_NEXT)
                print("⚠️ Next button not found! Clicked fallback position.")

            time.sleep(1)
        else:
            print(f"No repost found ({missing_repost_count+1}/{MAX_MISSING})")
            time.sleep(1)

            # Click TikTok tab to switch back
            print(f"⚠️ Repost missing, clicking TikTok tab at {TIKTOK_TAB}")
            send_click(hwnd, *TIKTOK_TAB)
            time.sleep(0.1)

            # Click next video fallback
            print(f"⚠️ Clicking next video fallback at {FALLBACK_NEXT}")
            send_click(hwnd, *FALLBACK_NEXT)

            missing_repost_count += 1

            if missing_repost_count >= MAX_MISSING:
                click_top_left_tab(hwnd)
                time.sleep(1)
                screenshot = capture_window(hwnd)
                gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                loc_repost_check = match_icon(gray, template_repost)
                if not loc_repost_check:
                    click_go_back(hwnd)
                missing_repost_count = 0

except KeyboardInterrupt:
    print("Stopped by user.")
