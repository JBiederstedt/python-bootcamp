import time
import pyautogui as pag
from PIL import ImageGrab, Image

# Coordinates of the region to monitor for obstacles (x1, y1, x2, y2).
# You may need to adjust these values depending on your screen resolution and browser window position.
DETECT_REGION = (200, 370, 350, 420)
# Pixel intensity threshold: darker than this value is considered an obstacle.
THRESHOLD = 160
# Delay before starting to play (in seconds).
START_DELAY = 3
# Interval between screen checks (in seconds).
CHECK_INTERVAL = 0.01


def jump():
    """Simulate a spacebar press to make the dinosaur jump."""
    pag.keyDown('space')
    time.sleep(0.05)
    pag.keyUp('space')


def detect_obstacle(region, threshold):
    """Capture the screen region and return True if an obstacle is detected."""
    img = ImageGrab.grab(bbox=region).convert('L')  # convert to grayscale
    # Check if any pixel is darker than threshold
    pixels = img.getdata()
    for pixel in pixels:
        if pixel < threshold:
            return True
    return False


def main():
    print(f"Starting T-Rex bot in {START_DELAY} seconds...")
    time.sleep(START_DELAY)
    print("Bot is running. Press Ctrl+C to stop.")

    # Ensure the game window is active
    pag.click(100, 100)  # click once to focus browser
    time.sleep(0.5)
    pag.press('space')  # start the game
    
    try:
        while True:
            if detect_obstacle(DETECT_REGION, THRESHOLD):
                jump()
                # Optional: brief pause after jump to avoid multiple triggers
                time.sleep(0.2)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Bot stopped by user.")


if __name__ == "__main__":
    main()
