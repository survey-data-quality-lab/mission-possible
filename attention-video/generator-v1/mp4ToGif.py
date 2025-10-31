import argparse
from PIL import Image
import imageio

def mp4_to_gif_sync_pillow(inp, out, width=None, loop=0, min_ms=10):
    """
    Convert MP4 to GIF while preserving real-time speed.
    - min_ms sets the minimum per-frame delay in milliseconds.
      Use 10 for best 60 fps approximation. If your viewer clamps to 20 ms, set 20.
    """
    reader = imageio.get_reader(inp, format="ffmpeg")

    # Read input fps
    try:
        meta = reader.get_meta_data()
        in_fps = float(meta.get("fps", 25))
        if in_fps <= 0:
            in_fps = 25.0
    except Exception:
        in_fps = 25.0

    # Source frame time in milliseconds
    ms_per_src = 1000.0 / in_fps

    frames = []
    durations = []

    # Error-diffused timing: choose integer ms per frame so cumulative time matches the MP4
    target_total_ms = 0.0
    emitted_total_ms = 0

    for frame in reader:
        target_total_ms += ms_per_src

        # Duration for this frame in integer ms
        dur_ms = int(round(target_total_ms)) - emitted_total_ms
        if dur_ms < min_ms:
            dur_ms = min_ms

        im = Image.fromarray(frame).convert("RGB")
        if width and width > 0 and im.width != width:
            new_h = int(round(im.height * (width / float(im.width))))
            im = im.resize((int(width), new_h), resample=Image.LANCZOS)

        frames.append(im)
        durations.append(dur_ms)
        emitted_total_ms += dur_ms

    reader.close()

    if not frames:
        raise RuntimeError("no frames read from input")

    # Save with Pillow, passing a per-frame duration list
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        format="GIF",
        loop=loop,
        duration=durations,
        disposal=2,   # clear previous frame
        optimize=False
    )

def main():
    p = argparse.ArgumentParser(description="MP4 -> GIF preserving speed using Pillow durations")
    p.add_argument("input", help="input MP4, for example va_vertical.mp4")
    p.add_argument("output", help="output GIF, for example va_vertical.gif")
    p.add_argument("--width", type=int, default=None, help="resize width, aspect ratio preserved")
    p.add_argument("--loop", type=int, default=0, help="repeat count, 0 means infinite")
    p.add_argument("--min-ms", type=int, default=20, help="minimum per-frame delay in ms, 10 or 20 are typical")
    args = p.parse_args()

    mp4_to_gif_sync_pillow(
        args.input,
        args.output,
        width=args.width,
        loop=args.loop,
        min_ms=args.min_ms
    )

if __name__ == "__main__":
    main()
