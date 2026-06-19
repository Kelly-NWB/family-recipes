"""Copy only the family-facing site into dist/ for thumb drive, GitHub Pages, etc."""
from __future__ import annotations

import shutil
from pathlib import Path

SHIP = [
    "index.html",
    "data/recipes.js",
    "assets/prescott-cover.png",
    "assets/prescott-cover-modern.png",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "dist"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    (out / "data").mkdir()
    (out / "assets").mkdir()

    total = 0
    for rel in SHIP:
        src = root / rel
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        total += src.stat().st_size

    mb = total / (1024 * 1024)
    print(f"Ship bundle -> {out}")
    print(f"{len(SHIP)} files, {mb:.2f} MB")
    print("Zip dist/ and hand to family — thumb drive, email, whatever.")


if __name__ == "__main__":
    main()