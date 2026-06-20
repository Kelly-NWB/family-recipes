"""Rebuild collections after merges: cabin photos + low-carb docx."""
from __future__ import annotations

import importlib.util
from pathlib import Path


def run_script(name: str) -> None:
    path = Path(__file__).resolve().parent / name
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


if __name__ == "__main__":
    run_script("add-cabin-collection.py")
    run_script("add-prized-collection.py")
    run_script("import-low-carb-docx.py")
    print("Done — cabin, prized, and low-carb refreshed.")