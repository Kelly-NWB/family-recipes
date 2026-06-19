from pathlib import Path
import fitz
import json
import re


def slugify(t: str) -> str:
    s = t.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60]


def main() -> None:
    src_pdf = list(Path(__file__).resolve().parents[1].glob("sources/*.pdf"))
    if not src_pdf:
        src_pdf = list(Path(r"D:\GrokBuild\stanley-trip\Recipe").glob("*.pdf"))
    doc = fitz.open(src_pdf[0])

    index_text = "".join(doc[i].get_text() + "\n" for i in range(6))
    lines = [line.strip() for line in index_text.splitlines() if line.strip()]

    recipes_index = []
    current_page = None
    for line in lines:
        if re.match(r"^(Page|Paqe|Paoe)\s*\d+", line, re.I):
            current_page = int(re.search(r"\d+", line).group())
            continue
        if line in {"Index", "lndex"} or line.startswith("Prescott"):
            continue
        recipes_index.append({"title": line, "sourcePage": current_page})

    seen: set[str] = set()
    deduped = []
    for entry in recipes_index:
        sid = slugify(entry["title"])
        if sid in seen:
            continue
        seen.add(sid)
        deduped.append(entry)

    full = [
        {
            "id": "myrtles-sourdough-choc-cake",
            "title": "Myrtle's Sourdough Choc. Cake",
            "collection": "prescott-cousins",
            "sourcePage": 1,
            "author": "Jan Musser",
            "category": "dessert",
            "ingredients": [
                "½ cup sourdough starter with ½ cup non-fat dry milk, 1½ cup flour and 1 cup water",
                "½ cup shortening",
                "1 cup sugar",
                "1 tsp. vanilla",
                "1 tsp. red vegetable coloring",
                "½ tsp. salt",
                "1½ tsp. soda",
                "2 eggs",
                "3 squares melted chocolate",
            ],
            "steps": [
                "Mix starter, dry milk, flour and water. Mix well and let stand a couple hours in a warm place until yeasty.",
                "Cream shortening and sugar. Add vanilla, coloring, salt, soda. Add eggs one at a time and mix well. Add melted chocolate.",
                "Stir creamed mixture into sourdough mix. Gently blend.",
                "Pour into a cake tin about 7×11. Bake at 350° for 30–45 min.",
                "Frost with cream cheese chocolate frosting if you like. Freezes well — often make a double batch.",
            ],
            "notes": ["Like all sourdough products, improves when frozen for a while."],
        },
        {
            "id": "salted-nut-roll-bars",
            "title": "Salted Nut Roll Bars",
            "collection": "prescott-cousins",
            "sourcePage": 1,
            "author": "Naida Snyder",
            "category": "dessert",
            "ingredients": [
                "1 yellow cake mix",
                "1 egg",
                "¼ cup soft oleo",
                "4 cups mini marshmallows",
                "TOPPING: 1 (12 oz) pkg. Reese's peanut butter chips",
                "⅓ cup light Karo syrup",
                "⅓ cup oleo",
                "2 tsp. vanilla",
                "2 cups Rice Krispies",
                "2 cups salted peanuts",
            ],
            "steps": [
                "Mix cake mix, egg and oleo until crumbly. Press into cookie sheet.",
                "Bake 10 min at 350°. Do not over bake.",
                "Sprinkle marshmallows over cake. Return to oven 1–2 min. Cool.",
                "Combine topping ingredients and melt. Add Rice Krispies and peanuts.",
                "Pour over base and refrigerate. Cut in squares.",
            ],
        },
        {
            "id": "nellies-work-dessert",
            "title": "Nellie's Work Dessert",
            "collection": "prescott-cousins",
            "sourcePage": 1,
            "author": "Nellie Baugh",
            "category": "dessert",
            "ingredients": [
                "1 can fruit cocktail",
                "1 can pineapple (crushed or chunky)",
                "1 can mandarin oranges (drained)",
                "2 boxes instant vanilla pudding",
            ],
            "steps": [
                "Combine fruit cocktail, pineapple and drained oranges.",
                "Add pudding mixes. Mix well and refrigerate.",
                "Top with Cool Whip when serving if you like.",
            ],
            "notes": ["Naida: I have tried this with no-sugar items. Works great for diabetics."],
        },
    ]
    full_ids = {recipe["id"] for recipe in full}

    recipes = list(full)
    for entry in deduped:
        sid = slugify(entry["title"])
        if sid in full_ids:
            continue
        recipes.append(
            {
                "id": sid,
                "title": entry["title"],
                "collection": "prescott-cousins",
                "sourcePage": entry["sourcePage"],
                "category": "uncategorized",
                "ingredients": [],
                "steps": [],
                "pending": True,
            }
        )

    data = {
        "collections": [
            {
                "id": "prescott-cousins",
                "title": "Prescott Cousins' Cookbook",
                "subtitle": "Hi, ya'll",
                "cover": "assets/prescott-cover.png",
                "source": src_pdf[0].name,
                "recipeCount": len(recipes),
            }
        ],
        "recipes": recipes,
    }

    root = Path(__file__).resolve().parents[1]
    json_out = root / "data" / "recipes.json"
    js_out = root / "data" / "recipes.js"
    payload = json.dumps(data, indent=2)
    json_out.write_text(payload, encoding="utf-8")
    js_out.write_text(f"window.RECIPE_DATA = {payload};\n", encoding="utf-8")
    print(f"Wrote {len(recipes)} recipes ({len(full)} complete) to {json_out} and {js_out}")


if __name__ == "__main__":
    main()