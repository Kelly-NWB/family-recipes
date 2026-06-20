"""Merge batch transcription JSON files into recipes.json and recipes.js."""
from __future__ import annotations

import json
import re
from pathlib import Path


SKIP_IDS = {"matter", "ll"}


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]


def load_batches(data_dir: Path) -> dict[str, dict]:
    recipes: dict[str, dict] = {}
    for path in sorted(data_dir.glob("batch-*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        items = raw["recipes"] if isinstance(raw, dict) else raw
        for recipe in items:
            recipe = dict(recipe)
            recipe.pop("pending", None)
            recipe["pending"] = False
            recipes[recipe["id"]] = recipe
    return recipes


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    existing = json.loads((data_dir / "recipes.json").read_text(encoding="utf-8"))

    merged = load_batches(data_dir)

    # Keep the three hand-polished early desserts if batches exist; batches should be fine.
    priority_ids = {
        "myrtles-sourdough-choc-cake",
        "salted-nut-roll-bars",
        "nellies-work-dessert",
    }

    final: list[dict] = []
    seen: set[str] = set()

    for old in existing["recipes"]:
        rid = old["id"]
        if rid in SKIP_IDS:
            continue
        if rid in merged:
            final.append(merged[rid])
            seen.add(rid)
        elif not old.get("pending"):
            final.append(old)
            seen.add(rid)

    for rid, recipe in sorted(merged.items(), key=lambda x: x[1].get("title", "").lower()):
        if rid in seen or rid in SKIP_IDS:
            continue
        final.append(recipe)
        seen.add(rid)

    final.sort(key=lambda r: (r.get("sourcePage") or 99, r.get("title", "").lower()))

    collections = existing["collections"]
    collections[0]["recipeCount"] = len(final)

    out = {"collections": collections, "recipes": final}
    payload = json.dumps(out, indent=2, ensure_ascii=False)
    (data_dir / "recipes.json").write_text(payload + "\n", encoding="utf-8")
    (data_dir / "recipes.js").write_text(
        f"window.RECIPE_DATA = {payload};\n", encoding="utf-8"
    )

    complete = sum(1 for r in final if r.get("steps"))
    print(f"Merged {len(final)} recipes ({complete} with content) -> data/recipes.json")

    for script_name in ("add-cabin-collection.py", "add-prized-collection.py"):
        script_path = Path(__file__).resolve().parent / script_name
        if script_path.exists():
            import importlib.util

            spec = importlib.util.spec_from_file_location(script_name, script_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.main()


if __name__ == "__main__":
    main()