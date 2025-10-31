# Video Attention Question Generator (ORIGINAL) - README

## Overview

This guide shows how to run the two scripts in sequence:

- `flicker.py` renders an MP4 video where characters slide vertically.
- `mp4ToGif.py` converts that MP4 into a GIF while preserving timing.

## Before You Run

- Put `flicker.py` and `mp4ToGif.py` in the same folder.
- Run the below commands within that folder.
- Ensure at least one path in `FONT_CANDIDATES` exists on your system.
- The default output video name is `va.mp4`; the examples below assume that.

## Note on .mp4 to .gif Conversion

- Conversion from `.mp4` to `.gif` is optional.
- We found it easier to work with `.gif` file rather than `.mp4` when placing it into our survey.
- Conversion into `.gif` makes the video a bit more "choppy" and `.gif` file is significantly larger in size.

## Note on Original Code

- This is the code used to generate the video used in our experiments.
- There is an alternative version that instead of animating the numbers by sliding them vertically, it simply shows them for a period of time.
- Conversion code from `.mp4` to `.gif` is different from the one for the alternative version.

---

## Linux Quick Start

**Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Install dependencies:**

```bash
pip install --upgrade pip
pip install pillow imageio imageio-ffmpeg numpy
```

**Render the MP4:**

```bash
python flicker.py
```

**Convert MP4 to GIF with preserved timing:**

```bash
python mp4ToGif.py va.mp4 va.gif
```

---

## Windows Quick Start (PowerShell)

**Create and activate a virtual environment:**

```powershell
py -3 -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

**Install dependencies:**

```powershell
pip install --upgrade pip
pip install pillow imageio imageio-ffmpeg numpy
```

**Render the MP4:**

```powershell
python .\flicker.py
```

**Convert MP4 to GIF with preserved timing:**

```powershell
python .\mp4ToGif.py va.mp4 va.gif
```

**Notes for Windows:**

- Ensure one of the font paths in `FONT_CANDIDATES` exists, for example `C:\Windows\Fonts\consolab.ttf`.
- If text looks tiny, the fallback bitmap font was used; adjust `FONT_CANDIDATES` or install a monospaced TTF.

---

## Configuration Tips for `flicker.py`

### Content and Loops

- `INPUT` controls the sequence of characters (will only work for up to 9 digits/characters with the default settings).
- `LOOPS` sets how many full passes over `INPUT` to render.
- `PAD_COLS_START`, `PAD_COLS_END`, `PAD_COLS_BETWEEN_LOOPS` insert blank columns inside and between loops.

### Timing

- `INITIAL_DELAY_SECONDS` adds blank video before the first character.
- `SHOW_SECONDS` sets how long a character is visible while passing the viewport.
- `GAP_SECONDS` sets blank time between characters.
- `GAP_SECONDS_BETWEEN_LOOPS` sets the blank time at the loop seam.
- `FINAL_BLANK_SECONDS` adds blank after the very last character.

### Canvas, Fonts, Colors

- `WIDTH` and `HEIGHT` set the frame size.
- `FPS` sets the frame rate.
- `FONT_CANDIDATES` lists mono fonts; the first available path is used.
- `COLOR_BG` and `COLOR_TEXT` set background and text colors.

### Horizontal Layout

- `LETTER_SPACING` sets horizontal slot spacing between columns.
- `AUTO_FIT_TO_WIDTH` can reduce spacing so one loop’s row fits within `WIDTH`.
- `MIN_LETTER_SPACING` is the lower bound when auto fit is enabled.

**Notes:**

- The vertical speed is derived from `SHOW_SECONDS` so each character stays visible exactly as configured.
- `GAP_SECONDS` controls the vertical distance between successive rows by time, not pixels.
- The writer uses `macro_block_size=1` to avoid auto-resizing non multiple of 16 frame sizes.

---

## Troubleshooting

- If `va.mp4` is not created, confirm the virtual environment is active and dependencies are installed.
- If the MP4 writer warns about macro blocks, note that `macro_block_size=1` is already set; the warning should not appear.
- If the GIF plays too slow, ensure you used `mp4ToGif_forAlt.py`; if your viewer clamps delays to 20 ms, use `--min-ms 20`.
- If the converter reports no frames read, check the input path and filename.
- If the text looks tiny or jagged, the fallback font was used; point `FONT_CANDIDATES` to a valid monospaced TTF.
