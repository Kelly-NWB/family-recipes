"""Build Prized cover pair.

#1 (modern): locked 3D render — assets/prized-cover-modern-source.jpg
#2 (original): PXL_20260620_001842979.jpg — untouched photo only

Do NOT regenerate the modern cover from HTML or PIL. Copy the canonical source.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = (
    ROOT
    / "scripts"
    / "Siscookbook-20260620T002650Z-3-001"
    / "Siscookbook"
    / "PXL_20260620_001842979.jpg"
)
ORIG_OUT = ROOT / "assets" / "prized-cover.png"
MODERN_SOURCE = ROOT / "assets" / "prized-cover-modern-source.jpg"
MODERN_OUT = ROOT / "assets" / "prized-cover-modern.png"


def load_source() -> Image.Image:
    img = Image.open(SRC).convert("RGB")
    return ImageOps.exif_transpose(img)


def save_original() -> None:
    img = load_source()
    img.thumbnail((1224, 1591), Image.Resampling.LANCZOS)
    img.save(ORIG_OUT, optimize=True, quality=92)
    print(f"Wrote {ORIG_OUT} ({img.size[0]}x{img.size[1]}) from {SRC.name}")


def install_modern() -> None:
    if not MODERN_SOURCE.exists():
        raise FileNotFoundError(
            f"Missing {MODERN_SOURCE} — restore prized-cover-modern-source.jpg before running."
        )
    img = Image.open(MODERN_SOURCE).convert("RGB")
    img.save(MODERN_OUT, format="PNG", optimize=True)
    print(f"Wrote {MODERN_OUT} ({img.size[0]}x{img.size[1]}) from {MODERN_SOURCE.name}")


def main() -> None:
    save_original()
    install_modern()


if __name__ == "__main__":
    main()