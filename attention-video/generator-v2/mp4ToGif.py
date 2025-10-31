import argparse
import imageio
from PIL import Image

def mp4_to_gif_exact(inp, out, width=None, loop=0):
    reader = imageio.get_reader(inp, format="ffmpeg")
    try:
        meta = reader.get_meta_data()
        in_fps = meta.get("fps", 25)
    except Exception:
        in_fps = 25

    # GIF duration is in milliseconds; 50 fps -> 20 ms
    duration_ms = max(10, int(round(1000.0 / float(in_fps))))

    frames = []
    for frame in reader:
        im = Image.fromarray(frame).convert("RGB")
        if width and width > 0 and im.width != width:
            new_h = int(round(im.height * (width / float(im.width))))
            im = im.resize((int(width), new_h), resample=Image.LANCZOS)
        frames.append(im)
    reader.close()

    if not frames:
        raise RuntimeError("no frames read from input")

    # Save via Pillow, no explicit palette to avoid odd color shifts
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        format="GIF",
        loop=loop,
        duration=duration_ms,
        disposal=2  # clear previous frame to prevent ghosting
    )

def main():
    p = argparse.ArgumentParser(description="Convert MP4 to GIF preserving timing")
    p.add_argument("input", help="path to input mp4, for example va.mp4")
    p.add_argument("output", help="path to output gif, for example out.gif")
    p.add_argument("--width", type=int, default=None, help="optional resize width, aspect ratio preserved")
    p.add_argument("--loop", type=int, default=0, help="repeat count, zero means infinite")
    args = p.parse_args()
    mp4_to_gif_exact(args.input, args.output, width=args.width, loop=args.loop)

if __name__ == "__main__":
    main()
