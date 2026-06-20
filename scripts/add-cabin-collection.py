"""Add Cabin photo-recipe collection to recipes.json / recipes.js."""
from __future__ import annotations

import json
from pathlib import Path

CABIN_RECIPES = [
    {
        "id": "cabin-pumpkin-cookies",
        "title": "Pumpkin Cookies with Brown Sugar Icing",
        "collection": "cabin",
        "author": "",
        "category": "dessert",

        "ingredients": [
            "2¾ cup flour",
            "1 tsp baking powder",
            "1 tsp baking soda",
            "¼ tsp salt",
            "½ tsp cinnamon",
            "¼ tsp nutmeg",
            "¾ cup butter (1½ sticks)",
            "2¼ cup brown sugar",
            "2 eggs",
            "½ cup canned pumpkin",
            "¾ cup evaporated milk",
            "1 tsp vanilla",
            "ICING: 4 cups powdered sugar",
            "10 Tbsp butter (1¼ sticks)",
            "¼ cup plus 1 Tbsp evaporated milk (plus more if needed)",
            "2 tsp vanilla",
        ],
        "steps": [
            "Preheat oven to 375°. Mix flour, baking powder, soda, salt, cinnamon and nutmeg. Set aside.",
            "Cream butter and brown sugar until fluffy. Mix in eggs. Add pumpkin, evaporated milk and vanilla.",
            "Add flour mixture. Mix until combined. Drop teaspoonfuls on greased cookie sheet and bake 12 min. Cool completely.",
            "Icing: Melt butter in saucepan until golden brown (~3 min). Add to powdered sugar with evaporated milk and vanilla. Stir smooth. Spread about 1 tsp on each cookie.",
        ],
        "notes": ["Makes approx. 7 dozen."],
        "pending": False,
    },
    {
        "id": "cabin-bokchoy-salad",
        "title": "Bokchoy Salad",
        "collection": "cabin",
        "category": "salad",

        "ingredients": [
            "ROAST MIX: 2 pk ramen noodles (no flavor packets)",
            "½ cup sesame seeds or sunflower seeds (raw)",
            "½ cup sliced almonds",
            "1 cube melted butter",
        ],
        "steps": [
            "Mix roast ingredients together.",
            "Cook at 350° in 9×13 pan for 10–15 minutes, or until browned.",
        ],
        "notes": ["Photo shows roast mix portion — more salad steps may be on another page."],
        "pending": False,
    },
    {
        "id": "cabin-broccoli-slaw",
        "title": "Broccoli Slaw",
        "collection": "cabin",
        "category": "salad",

        "ingredients": [
            "DRESSING: 2 tbsp soy sauce",
            "½ cup red wine vinegar",
            "¼ to 1 cup sugar (to taste)",
            "1 cup oil",
            "3 cups broccoli",
            "3 cups cabbage",
            "½ cup red onion",
        ],
        "steps": [
            "Whisk dressing ingredients together.",
            "Toss with broccoli, cabbage and red onion.",
        ],
        "pending": False,
    },
    {
        "id": "cabin-huckleberry-pie",
        "title": "Huckleberry Pie",
        "collection": "cabin",
        "category": "dessert",

        "ingredients": [
            "1 small pkg cream cheese",
            "½ cup powdered sugar",
            "½ tsp vanilla",
            "1 cup whipping cream",
            "⅓ cup sugar to 1 cup berries",
            "Cornstarch to thicken berries",
        ],
        "steps": [
            "Prepare pie shell.",
            "Beat cream cheese, powdered sugar, vanilla and whipping cream. Spread on shell.",
            "Sweeten huckleberries with sugar and thicken with cornstarch.",
            "Spread berries on top of cream layer.",
        ],
        "pending": False,
    },
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data" / "recipes.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))

    data["recipes"] = [r for r in data["recipes"] if r.get("collection") != "cabin"]
    data["recipes"].extend(CABIN_RECIPES)

    cabin_collection = {
        "id": "cabin",
        "title": "Cabin",
        "subtitle": "Handwritten notebook",
        "cover": "assets/cabin-cover.png",
        "type": "cabin",
        "recipeCount": len(CABIN_RECIPES),
    }

    data["collections"] = [c for c in data["collections"] if c["id"] != "cabin"]
    data["collections"].append(cabin_collection)

    prescott = next(c for c in data["collections"] if c["id"] == "prescott-cousins")
    prescott["recipeCount"] = sum(1 for r in data["recipes"] if r["collection"] == "prescott-cousins")

    payload = json.dumps(data, indent=2, ensure_ascii=False)
    data_path.write_text(payload + "\n", encoding="utf-8")
    (root / "data" / "recipes.js").write_text(
        f"window.RECIPE_DATA = {payload};\n", encoding="utf-8"
    )
    print(f"Added Cabin collection with {len(CABIN_RECIPES)} photo recipes.")


if __name__ == "__main__":
    main()