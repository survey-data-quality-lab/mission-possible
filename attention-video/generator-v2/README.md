# Video Attention Question Generator (ALTERNATIVE) - README

## Overview

This guide shows how to run the two scripts in sequence:

- `flicker.py` renders an MP4 video with sequential characters.
- `mp4ToGif.py` converts that MP4 into a GIF while preserving timing.

## Before You Run

- Put `flicker.py` and `mp4ToGif.py` in the same folder.
- Open `flicker.py` and set `FONT_OS` to `linux` or `windows` to match your system.
- The default output video name is `va.mp4`; the examples below assume that.
- Run the below commands within that folder.

## Note on .mp4 to .gif Conversion

- Conversion from `.mp4` to `.gif` is optional.
- We found it easier to work with `.gif` files rather than `.mp4` when placing them into our survey.
- Conversion into `.gif` makes the video a bit more "choppy", and the `.gif` file is significantly larger in size.

## Note on Alternative Code

- The video generated via this code is **not** the one we used in our survey.
- See `flicker.py` and its corresponding conversion code under the folder called `original`.
- This is an alternative way of generating the video.
- In this version, the animation does not slide vertically but is simply shown for a short period of time.
- This version has the additional option to show static digits at the beginning of the sequence.
- We provided this version in case researchers may prefer flashing digits rather than sliding digits.

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

**Run the generator to produce `va.mp4`:**

```bash
python flicker.py
```

**Convert MP4 to GIF:**

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

**Run the generator to produce `va.mp4`:**

```powershell
python .\flicker.py
```

**Convert MP4 to GIF:**

```powershell
python .\mp4ToGif.py va.mp4 va.gif
```

**Notes for Windows:**

- Ensure `FONT_OS` is set to `windows` in `flicker.py`.
- The script tries Consolas and Courier New from `C:\Windows\Fonts`.
- If you see an error about the text anchor argument, upgrade Pillow using:

```powershell
pip install --upgrade pillow
```

---

## Configuration Tips

- To replicate a specific sequence, set `TEXT` in `flicker.py`.
- To change pacing, edit `SHOW_SECONDS` and `GAP_SECONDS` in `flicker.py`.
- If characters do not fit on one line, reduce `FONT_SIZE` or `CHAR_GAP_RATIO`, or increase `WIDTH`.
- If you want a shorter video, reduce `LOOPS` or use a smaller `SHOW_SECONDS` and `GAP_SECONDS`.

---

## Troubleshooting

- If `va.mp4` is not created, confirm you activated the virtual environment and installed the packages.
- If the MP4 write fails, ensure `imageio-ffmpeg` is installed or that a system `ffmpeg` is on `PATH`.
- If the GIF looks slow or jittery in a browser, it may be the browser timer; the converter uses the input fps to set per-frame duration in milliseconds.
