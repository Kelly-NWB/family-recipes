"""Tight demo: short titles, trimmed walkthrough, soft ambient bed."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"
FFMPEG = r"C:\Users\nrthw\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"

RAW = DEMO / "walkthrough-raw.webm"
FINAL = DEMO / "family-recipes-demo.mp4"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
        text=True,
    )
    return float(json.loads(out)["format"]["duration"])


def make_title(out: Path, line1: str, line2: str, sec: float, bg: str) -> None:
    vf = (
        f"color=c={bg}:s=1280x720:d={sec},"
        f"drawtext=fontfile=C\\\\:/Windows/Fonts/georgia.ttf:text='{line1}':"
        f"fontcolor=0xF6F4F0:fontsize=48:x=(w-text_w)/2:y=(h/2)-50,"
        f"drawtext=fontfile=C\\\\:/Windows/Fonts/georgiai.ttf:text='{line2}':"
        f"fontcolor=0x8FA08A:fontsize=24:x=(w-text_w)/2:y=(h/2)+18,"
        f"fade=t=in:st=0:d=0.25,fade=t=out:st={max(0.1, sec - 0.35)}:d=0.35"
    )
    run([FFMPEG, "-y", "-f", "lavfi", "-i", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out)])


def make_ambient(out: Path, duration: float) -> None:
    """Warm major-pad drone — fills silence, stays under UI."""
    d = f"{duration:.2f}"
    fade_out = max(0.1, duration - 1.0)
    filt = (
        f"[0:a][1:a][2:a]amix=inputs=3:normalize=0,volume=0.14[a];"
        f"[a]afade=t=in:st=0:d=0.6,afade=t=out:st={fade_out}:d=1.0[aout]"
    )
    run([
        FFMPEG, "-y",
        "-f", "lavfi", "-i", f"sine=frequency=220:duration={d}",
        "-f", "lavfi", "-i", f"sine=frequency=277:duration={d}",
        "-f", "lavfi", "-i", f"sine=frequency=330:duration={d}",
        "-filter_complex", filt, "-map", "[aout]",
        "-t", d, "-c:a", "aac", "-b:a", "128k", str(out),
    ])


def main() -> None:
    DEMO.mkdir(exist_ok=True)
    if not RAW.exists():
        raise SystemExit(f"Missing {RAW} — run record-demo.py first.")

    intro = DEMO / "intro.mp4"
    outro = DEMO / "outro.mp4"
    walk = DEMO / "walkthrough.mp4"
    ambient = DEMO / "ambient.m4a"
    walk_audio = DEMO / "walkthrough-audio.mp4"
    concat_list = DEMO / "concat.txt"
    merged = DEMO / "merged.mp4"

    make_title(intro, "Family Recipes", "Search · cook · remember", 1.4, "0x2A4035")
    make_title(outro, "family-recipes", "kelly-nwb.github.io/family-recipes", 1.6, "0x1E3028")

    # Trim walkthrough: drop first/last 0.3s dead frames, cap length
    run([
        FFMPEG, "-y", "-ss", "0.25", "-i", str(RAW),
        "-t", "11.5",
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-an",
        str(walk),
    ])

    walk_dur = probe_duration(walk)
    intro_dur = probe_duration(intro)
    outro_dur = probe_duration(outro)
    total = intro_dur + walk_dur + outro_dur

    make_ambient(ambient, total + 0.5)

    concat_list.write_text(
        f"file '{intro.name}'\nfile '{walk.name}'\nfile '{outro.name}'\n",
        encoding="utf-8",
    )
    run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(merged),
    ])

    run([
        FFMPEG, "-y", "-i", str(merged), "-i", str(ambient),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
        str(FINAL),
    ])

    mb = FINAL.stat().st_size / (1024 * 1024)
    print(f"Demo -> {FINAL}")
    print(f"Duration ~{probe_duration(FINAL):.1f}s · {mb:.1f} MB")


if __name__ == "__main__":
    main()