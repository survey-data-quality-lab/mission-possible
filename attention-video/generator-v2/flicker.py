import imageio
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ========================
# Configuration (edit here)
# ========================

# Canvas / output
WIDTH, HEIGHT = 1280, 720
FPS = 50
OUTPUT_FILE = "va.mp4"

# Text & layout
TEXT = "3169"              # At most 7 character can fit given the font size 300
STATIC_CHARS_COUNT = 0     # first N chars always visible; remaining will cycle
FONT_SIZE = 300


# -------- FONTS ---------
# FONT_OS = "windows" 
FONT_OS = "linux" 

if FONT_OS == "linux":
    # -----------------
    # --- for LINUX ---
    # -----------------
    FONT_CANDIDATES = [
        "RobotoMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    ]

if FONT_OS == "windows":
    # -------------------
    # --- for WINDOWS ---
    # -------------------
    FONT_CANDIDATES = [
        "C:/Windows/Fonts/consolab.ttf",  # Consolas Bold
        "C:/Windows/Fonts/consola.ttf",   # Consolas Regular
        "C:/Windows/Fonts/cour.ttf",      # Courier New
    ]

# Colors
COLOR_BG = "#f3f4f6"          # light gray
COLOR_TEXT = "#111827"        # dark text

# Timing
INITIAL_DELAY_SECONDS = 1     # wait before any digit activity starts

# ---------------
# --- FLICKER ---
# ---------------
# SHOW_SECONDS = 1 / FPS    # how long the active digit is visible
# GAP_SECONDS = 0           # gap after a digit (no flickering digit visible)
# LOOPS = int(round((20.0 * FPS) / len(TEXT[STATIC_CHARS_COUNT:])))   # how many full passes over the flickering digits

# --------------
# --- BASIC ----
# --------------
SHOW_SECONDS = 1
GAP_SECONDS = 1.5
LOOPS = 4



# Duration control
AUTO_DURATION = True          # if True, compute total duration from timing & loops
DURATION_SECONDS = 20         # used only if AUTO_DURATION = False

# Spacing
CHAR_GAP_RATIO = 0.15         # gap = CHAR_GAP_RATIO * char_width

# ========================
# Script
# ========================

# Load font (mono)
font = None
for path in FONT_CANDIDATES:
    try:
        font = ImageFont.truetype(path, FONT_SIZE)
        break
    except IOError:
        continue
if font is None:
    print("Warning: No preferred font found; falling back to default.")
    font = ImageFont.load_default()

# Measure a single character for layout
try:
    char_bbox = font.getbbox("0")
    char_width = char_bbox[2] - char_bbox[0]
    char_height = char_bbox[3] - char_bbox[1]
except AttributeError:
    # Older Pillow
    char_width, char_height = font.getsize("0")

gap = char_width * CHAR_GAP_RATIO
total_text_width = (len(TEXT) * char_width) + ((len(TEXT) - 1) * gap)
start_x = (WIDTH - total_text_width) / 2
y_pos = (HEIGHT - char_height) / 2

# Timing precompute
delay_in_frames = int(round(FPS * INITIAL_DELAY_SECONDS))
show_frames = int(round(FPS * SHOW_SECONDS))
gap_frames = int(round(FPS * GAP_SECONDS))
segment_frames = show_frames + gap_frames

flickering_part = TEXT[STATIC_CHARS_COUNT:]
flicker_count = len(flickering_part)

# Decide total frames
if AUTO_DURATION:
    if flicker_count > 0:
        total_frames = delay_in_frames + (segment_frames * flicker_count * max(1, LOOPS))
    else:
        # Nothing to flicker: use at least a minimal duration
        total_frames = delay_in_frames + int(round(FPS * max(1, DURATION_SECONDS)))
else:
    total_frames = int(round(FPS * DURATION_SECONDS))

print("Generating frames...")
frames = []

for frame_num in range(total_frames):
    image = Image.new('RGB', (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(image)

    active_digit_index = None   # index within flickering_part
    showing_phase = False       # True only during the SHOW part

    if flicker_count > 0 and frame_num >= delay_in_frames:
        time_past_delay = frame_num - delay_in_frames
        total_cycle_frames = segment_frames * flicker_count

        # If looping is finite, stop showing after LOOPS cycles
        if AUTO_DURATION:
            # We sized total_frames to end exactly after loops, so we can trust indices
            pass
        else:
            # When not auto, we may run past loops; keep looping through digits
            pass

        cycle_pos = time_past_delay % total_cycle_frames
        active_digit_index = cycle_pos // segment_frames
        pos_in_segment = cycle_pos % segment_frames
        showing_phase = pos_in_segment < show_frames

    # Draw each character
    for i, char in enumerate(TEXT):
        is_visible = False

        if i < STATIC_CHARS_COUNT:
            # Always visible static prefix
            is_visible = True
        else:
            # Flickering portion
            if flicker_count > 0 and active_digit_index is not None and showing_phase:
                # index of this char within flickering part
                current_flicker_char_index = i - STATIC_CHARS_COUNT
                if current_flicker_char_index == active_digit_index:
                    is_visible = True
            else:
                # During gap or before delay, flickering digits are hidden
                is_visible = False

        if is_visible:
            current_x = start_x + (i * (char_width + gap))
            draw.text((current_x, y_pos), char, font=font, fill=COLOR_TEXT, anchor="lt")

    frames.append(np.array(image))

print("Writing video file...")
imageio.mimwrite(OUTPUT_FILE, frames, fps=FPS, quality=9)
print(f"Video saved successfully as {OUTPUT_FILE}")
