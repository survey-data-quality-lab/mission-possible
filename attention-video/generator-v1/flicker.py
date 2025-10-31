# flicker_vertical_loops_gap.py
import imageio
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ============== Canvas / output ==============
WIDTH, HEIGHT = 1000, 300
FPS = 60
OUTPUT_FILE = "va.mp4"

# ============== Content and loops ==============
INPUT = "3169"            # up to 9 characters work
LOOPS = 4                 # how many full passes over INPUT

# Blank columns to include inside each loop (set to 0 for minimal loop pause)
PAD_COLS_START = 0        # leading spaces inside every loop
PAD_COLS_END   = 0        # trailing spaces inside every loop
PAD_COLS_BETWEEN_LOOPS = 0  # extra blanks inserted between loops

# ============== Font ==============
FONT_SIZE = 125
FONT_CANDIDATES = [
    #"/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    #"RobotoMono-Bold.ttf",
    #"/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "C:/Windows/Fonts/consolab.ttf",
    "C:/Windows/Fonts/consola.ttf",
    "C:/Windows/Fonts/cour.ttf",
]

# ============== Colors ==============
COLOR_BG = "#ffffff"
COLOR_TEXT = "#000000"

# ============== Horizontal layout ==============
LETTER_SPACING = 150.0    # px between columns in the row
AUTO_FIT_TO_WIDTH = True # set True to shrink spacing if the row would exceed WIDTH
MARGIN_X = 0
MIN_LETTER_SPACING = 40.0

# ============== Timing (human readable) ==============
INITIAL_DELAY_SECONDS        = 1.0   # blank before first digit
SHOW_SECONDS                 = 2.0   # time a digit stays visible
GAP_SECONDS                  = 1.5   # blank between digits
GAP_SECONDS_BETWEEN_LOOPS    = 1.5   # blank at the loop seam (make this smaller for a snappier restart)
FINAL_BLANK_SECONDS          = GAP_SECONDS  # blank after the very last digit

# -----------------------------------------------------
# Helpers
# -----------------------------------------------------
def load_font(candidates, size):
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    print("Warning: falling back to default font.")
    return ImageFont.load_default()

def measure_char(font):
    try:
        bb = font.getbbox("0")
        return bb[2] - bb[0], bb[3] - bb[1]
    except Exception:
        return font.getsize("0")

# -----------------------------------------------------
# Build sequence across loops
# -----------------------------------------------------
font = load_font(FONT_CANDIDATES, FONT_SIZE)
char_w, char_h = measure_char(font)

loop_text = (" " * PAD_COLS_START) + INPUT + (" " * PAD_COLS_END)
BASE_COLS = len(loop_text)

seq = []
for k in range(LOOPS):
    if k > 0 and PAD_COLS_BETWEEN_LOOPS > 0:
        seq.extend([" "] * PAD_COLS_BETWEEN_LOOPS)
    seq.extend(list(loop_text))
TOTAL_ITEMS = len(seq)

# Horizontal centering using one loop’s width
if BASE_COLS <= 1:
    letter_spacing_final = 0.0
else:
    available_w = max(0.0, WIDTH - 2 * MARGIN_X - BASE_COLS * char_w)
    fits_spacing = available_w / (BASE_COLS - 1) if BASE_COLS > 1 else 0.0
    letter_spacing_final = LETTER_SPACING
    if AUTO_FIT_TO_WIDTH:
        letter_spacing_final = max(MIN_LETTER_SPACING, min(LETTER_SPACING, fits_spacing))

row_w = BASE_COLS * char_w + (BASE_COLS - 1) * letter_spacing_final
base_x = (WIDTH - row_w) / 2.0
step_x = char_w + letter_spacing_final
x_positions = [base_x + (i % BASE_COLS) * step_x for i in range(TOTAL_ITEMS)]

# -----------------------------------------------------
# Derive vertical motion from timing
# -----------------------------------------------------
# Constant speed so each visible pass lasts SHOW_SECONDS
speed_px_per_sec   = HEIGHT / float(SHOW_SECONDS)
speed_px_per_frame = speed_px_per_sec / float(FPS)

# Vertical strides
stride_items_px = HEIGHT + GAP_SECONDS * speed_px_per_sec
stride_loop_px  = HEIGHT + GAP_SECONDS_BETWEEN_LOOPS * speed_px_per_sec

# Build a stride list where the seam between loops uses stride_loop_px
strides = []
for i in range(TOTAL_ITEMS - 1):
    # Detect if i is the last column of a loop_text block
    is_end_of_loop = ((i + 1) % BASE_COLS == 0)
    if is_end_of_loop:
        strides.append(stride_loop_px)
    else:
        strides.append(stride_items_px)

# Cumulative y positions
y_positions = [0.0]
for s in strides:
    y_positions.append(y_positions[-1] + s)

# Total time: initial delay + time to traverse all strides + last digit’s SHOW + final blank
total_seconds = INITIAL_DELAY_SECONDS + (sum(strides) / speed_px_per_sec) + SHOW_SECONDS + FINAL_BLANK_SECONDS
total_frames = int(round(total_seconds * FPS))

# Start so first digit appears after the initial delay
start_scroll = -(HEIGHT + speed_px_per_sec * INITIAL_DELAY_SECONDS)

# -----------------------------------------------------
# Render
# -----------------------------------------------------
with imageio.get_writer(OUTPUT_FILE, fps=FPS, quality=9, macro_block_size=1) as writer:
    for f in range(total_frames):
        scroll_top = start_scroll + f * speed_px_per_frame

        img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
        draw = ImageDraw.Draw(img)

        # Draw only the item that is currently in the window
        for ch, x, y in zip(seq, x_positions, y_positions):
            y_screen = y - scroll_top
            if 0 <= y_screen < HEIGHT:
                if ch != " ":
                    draw.text((x, y_screen), ch, font=font, fill=COLOR_TEXT)

        writer.append_data(np.array(img))

print(f"Video saved successfully as {OUTPUT_FILE}")
